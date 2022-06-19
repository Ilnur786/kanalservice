import sqlalchemy as db
from sqlalchemy import MetaData, func
import os
from sqlalchemy.dialects.postgresql import insert
from datetime import date
from exchange_api.currency_exchange_api import get_exchange_rate, convert_dollars_in_rubles

db_name = os.getenv('db_name')
user_name = os.getenv('user_name')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')


def change_delete_status(order_ids):
    """
    Receive specified order ids and changed their "deleted" status to True.
    :param order_ids: specified order ids.
    :return: None
    """
    if order_ids is not None:
        engine = db.create_engine(f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}')
        connection = engine.connect()
        metadata = MetaData(engine)
        entries_table = db.Table('entries', metadata, autoload=True, autoload_with=engine)
        sel_query = db.select(entries_table)
        connection.execute(sel_query).fetchall()
        query = db.update(entries_table).values(deleted=True).where(entries_table.c.order_id in order_ids)
        connection.execute(query)
        connection.close()


def change_tg_notice_status():
    """
    Return entries which delivery_date got out from limit and changed "tg_noticed" status to True.
    :return: tuples of entries which consist some columns: order_id, cost_dollars, delivery_date, "deleted" status
    """
    engine = db.create_engine(f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}')
    connection = engine.connect()
    metadata = MetaData(engine)
    entries_table = db.Table('entries', metadata, autoload=True, autoload_with=engine)
    sel_query = db.select(entries_table)
    connection.execute(sel_query).fetchall()
    query = db.update(entries_table).values(tg_noticed=True). \
        filter(func.date(entries_table.c.delivery_date) < date.today()).filter(entries_table.c.tg_noticed == False).\
        returning(entries_table.c.order_id, entries_table.c.cost_dollars, entries_table.c.delivery_date, entries_table.c.deleted)
    result = connection.execute(query).fetchall()
    connection.close()
    return result


def create_or_update_entries(entries):
    """
    Receive entries which could be added or updated.
    :return: None
    """
    # get connection
    engine = db.create_engine(f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}')
    connection = engine.connect()
    metadata = MetaData(engine)
    entries_table = db.Table('entries', metadata, autoload=True, autoload_with=engine)
    # get all entries order_ids
    all_order_ids = [entry[0] for entry in entries]
    # select changed entries query
    select_to_delete_entries_query = db.select(entries_table.c.order_id).filter(entries_table.c.deleted == False).filter(entries_table.c.order_id not in all_order_ids)
    # get changed entries
    to_delete_entries_ids = connection.execute(select_to_delete_entries_query).fetchall()
    # change delete_status of entries
    change_delete_status(to_delete_entries_ids)
    # get exchange rate
    exchange_rate = get_exchange_rate()
    # insert or update entries
    for order_id, cost_dollars, delivery_date in entries:
        insert_entries_query = insert(entries_table).values(
            (order_id, cost_dollars, delivery_date, exchange_rate, convert_dollars_in_rubles(exchange_rate, cost_dollars), False, False))
        update_if_conflict_query = insert_entries_query.on_conflict_do_update(index_elements=['order_id'],
                                                                              set_=dict(order_id=order_id,
                                                                                        cost_dollars=cost_dollars,
                                                                                        delivery_date=delivery_date, deleted=False))
        connection.execute(update_if_conflict_query)



import sqlalchemy as db
from sqlalchemy import MetaData, func
import os
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from datetime import date


db_name = os.getenv('POSTGRES_DB')
user_name = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')


def change_delete_status(order_ids):
    """
    Receive specified order ids and changed their "deleted" status to True.
    :param order_ids: specified order ids.
    :return: None
    """
    if order_ids is not None:
        order_ids = tuple(i[0] for i in order_ids)
        engine = db.create_engine(f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}')
        connection = engine.connect()
        metadata = MetaData(engine)
        entries_table = db.Table('entries', metadata, autoload=True, autoload_with=engine)
        query = db.update(entries_table).values(deleted=True).filter(entries_table.c.order_id.in_(order_ids))
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
    from exchange_api.currency_exchange_api import get_exchange_rate, convert_dollars_in_rubles
    # get connection
    engine = db.create_engine(f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}')
    connection = engine.connect()
    metadata = MetaData(engine)
    entries_table = db.Table('entries', metadata, autoload=True, autoload_with=engine)
    # get all entries order_ids
    all_order_ids = [entry[0] for entry in entries]
    # get entries which not in current Google Sheet state
    select_to_delete_entries_query = db.select(entries_table.c.order_id).filter(entries_table.c.deleted.is_(False)).filter(entries_table.c.order_id.not_in(all_order_ids))
    # execute query above and fetch them
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


def get_data_from_db():
    """
    Return dataframe , which is reflection of current Google Sheet state.
    :return: pandas.dataframe
    """
    engine = db.create_engine(f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}')
    metadata = MetaData(engine)
    entries_table = db.Table('entries', metadata, autoload=True, autoload_with=engine)
    query = entries_table.select().filter(entries_table.c.deleted.is_(False))
    df = pd.read_sql(query, engine, parse_dates={'delivery_date': {'format': '%d-%m-%Y'}})
    return df.sort_values(by=['delivery_date', 'cost_dollars'], ignore_index=True)


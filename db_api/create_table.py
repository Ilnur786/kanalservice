import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, Date, Float, Boolean, MetaData
import os

db_name = os.getenv('POSTGRES_DB')
user_name = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')


def create_table_if_not_exist():
    """
    Create "entries" table if doesn't exist.
    :return: None
    """
    engine = db.create_engine(f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}')
    if not db.inspect(engine).has_table("entries"):
        metadata = MetaData(engine)
        # Create a table with the appropriate Columns
        Table('entries', metadata,
              Column('order_id', Integer, nullable=False, unique=True, primary_key=True),
              Column('cost_dollars', Integer), Column('delivery_date', Date),
              Column('exchange_rate', Float), Column('cost_rubles', Float),
              Column('tg_noticed', Boolean, nullable=False, default=False),
              Column('deleted', Boolean, nullable=False, default=False))
        # Implement the creation
        metadata.create_all()

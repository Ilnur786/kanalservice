from db_api.db_api import create_or_update_entries
from df_api.df_api import get_df
from db_api.create_table import create_table_if_not_exist
import time
from datetime import datetime

if __name__ == '__main__':
    # create table if not exist
    create_table_if_not_exist()
    while True:
        # get google sheet dataframe
        df = get_df()
        # set up correct form
        entries = [(int(order_id), int(cost_dollars), delivery_date)
                   for order_id, cost_dollars, delivery_date in zip(df['заказ №'], df['стоимость,$'], df['срок поставки'])]
        # send df to db_api function
        create_or_update_entries(entries=entries)
        print('all records up to date', datetime.now())
        time.sleep(60)

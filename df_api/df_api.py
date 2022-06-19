from datetime import datetime
import pandas as pd


def get_df():
    sheet_url = "https://docs.google.com/spreadsheets/d/1PsVLEBmCdrp9R8KSIqGC8eD252DIa26IYSOnatMkAUU/edit#gid=0"
    url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url)
    # df.to_csv('df.csv', sep=';', encoding='windows-1251')  # работает
    clean_date_df = change_date_format(df)
    return clean_date_df


def date_parser(date_str):
    try:
        date_object = datetime.strptime(date_str, "%d.%m.%Y")
    except TypeError:
        return None
    return date_object.strftime("%Y-%m-%d")


def change_date_format(dataframe):
    dataframe['срок поставки'] = dataframe['срок поставки'].apply(date_parser)
    return dataframe







from datetime import datetime
import pandas as pd


def get_df(sheet_url):
    """
    Get rows from specified Google Sheet into pandas.dataframe
    :return:
    """
    url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url)
    clean_date_df = change_date_format(df)
    return clean_date_df


def date_parser(date_str):
    """
    Change date format into SQL like.
    :param date_str: date column from df.
    :return: date in SQL like format.
    """
    try:
        date_object = datetime.strptime(date_str, "%d.%m.%Y")
    except TypeError:
        return None
    return date_object.strftime("%Y-%m-%d")


def change_date_format(dataframe):
    """
    Apply date_parser to the whole df
    :param dataframe: pandas dataframe
    :return: changed dataframe
    """
    dataframe['срок поставки'] = dataframe['срок поставки'].apply(date_parser)
    return dataframe







import pandas as pd
from .utils import crypto_asset_json_to_list
from .asset_requests import get_crypto_asset_history


def process_crypto_dataframe(asset_id: str, list_crypto_dicts: list) -> pd.DataFrame:
    """Transforms list of dictionaries into DataFrame and processes the data.

    Args:
        asset_id (str): Name of the crypto asset that will be processed.
        list_crypto_dicts (list): List containing dictionaries with the crypto asset data.

    Returns:
        pd.DataFrame: DataFrame containing crypto asset information. 
    """

    PRICE_COLUMN = "priceUsd"
    DATE_COLUMN = "date"

    df = pd.DataFrame.from_records(list_crypto_dicts)
    df[PRICE_COLUMN] = df[PRICE_COLUMN].astype(float)  # string to float
    df[PRICE_COLUMN] = df[PRICE_COLUMN].round(decimals=2)  # round float
    df[DATE_COLUMN] = pd.to_datetime(
        df[DATE_COLUMN], format="%Y-%m-%d"
    )  # string to datetime
    df[DATE_COLUMN] = df[DATE_COLUMN].dt.date  # maintain only date
    df["crypto_name"] = asset_id
    df = df[["crypto_name", PRICE_COLUMN, DATE_COLUMN]]
    df = df.rename(columns={PRICE_COLUMN: "price_usd"})

    return df


def execute_crypto_asset_etl_routine(
    asset_id: str, start_date: str, end_date: str
) -> pd.DataFrame:

    """Executes all steps necessary for the crypto asset ETL pipeline to work, from extraction to processing and load. 

    Returns:
        pd.DataFrame: DataFrame containing crypto asset information.
    """

    crypto_asset_json = get_crypto_asset_history(asset_id, start_date, end_date)
    list_crypto_dicts = crypto_asset_json_to_list(crypto_asset_json)

    df = process_crypto_dataframe(asset_id, list_crypto_dicts)

    return df

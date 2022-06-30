"""
Extracts and processes specified crypto asset data from CoinCap to later load onto SQL db. 

argument 1: The crypto asset name (e.g. 'bitcoin')
argument 2: The start date to retrieve data (e.g '2022-05-22')
argument 3: The end date to retrieve data (e.g '2022-05-27')
"""

import argparse
import json
import requests
import pandas as pd
from libs.utils import HumanDateToEpoch, crypto_asset_json_to_list

# TODO - Later on, add table for currencies and there value in the main coins (USD, Euro and Sterling)
# TODO - Do same process of cryptos for stocks
# TODO - Create subdirectories to better organize project
# TODO - Create tests for project


def get_crypto_asset_history(asset_id: str, start_date: str, end_date: str) -> dict:

    # put in asset_requests module

    SPECIFIED_INTERVAL = "d1"  # Daily interval (UTC)

    crypto_asset_api_url = f"http://api.coincap.io/v2/assets/{asset_id}/history?interval={SPECIFIED_INTERVAL}&start={start_date}&end={end_date}"

    response = requests.request("GET", crypto_asset_api_url)

    return json.loads(response.text.encode("utf8"))


def process_crypto_dataframe(asset_id: str, list_crypto_dicts: list) -> pd.DataFrame:

    # put in processing module

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
) -> None:

    # Put in processing module

    crypto_asset_json = get_crypto_asset_history(asset_id, start_date, end_date)
    list_crypto_dicts = crypto_asset_json_to_list(crypto_asset_json)

    df = process_crypto_dataframe(asset_id, list_crypto_dicts)

    return df


def main(args):

    asset_id = args.asset_id
    start_date = HumanDateToEpoch.date_to_unix_miliseconds(args.start_date)
    end_date = HumanDateToEpoch.date_to_unix_miliseconds(args.end_date)

    print(execute_crypto_asset_etl_routine(asset_id, start_date, end_date))


def get_parser():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "asset_id",
        help="argument 1: The crypto asset name (e.g. 'bitcoin')",
        metavar="ASSET_ID",
        type=str,
    )
    parser.add_argument(
        "start_date",
        help="argument 2: The start date to retrieve data (e.g '2022-05-22')",
        metavar="START_DATE",
        type=str,
    )
    parser.add_argument(
        "end_date",
        help="argument 3: The end date to retrieve data (e.g '2022-05-27')",
        metavar="END_DATE",
        type=str,
    )

    return parser


if __name__ == "__main__":

    main(get_parser().parse_args())


# TODO - Implement asset id verification

# python3 main.py ASSET_ID="bitcoin" START_DATE="2022-05-15" END_DATE="2022-05-22" ------------------------------------------------

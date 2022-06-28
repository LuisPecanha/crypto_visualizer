"""
Extracts and processes specified crypto asset data from CoinCap to later load onto SQL db. 

argument 1: The crypto asset name (e.g. 'bitcoin')
argument 2: The start date to retrieve data (e.g '2022-05-22')
argument 3: The end date to retrieve data (e.g '2022-05-27')
"""

import argparse
import csv
import json
from datetime import datetime
import time
import requests
import re
import pandas as pd
import sys
import getopt

# TODO - Later on, add table for currencies and there value in the main coins (USD, Euro and Sterling)
# TODO - Do same process of cryptos for stocks
# TODO - Create subdirectories to better organize project
# TODO - Create tests for project


class HumanDateToEpoch:

    # Put in utils module

    @staticmethod
    def __verify_format(human_date_string: str) -> bool:

        date_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}"

        return True if re.match(date_pattern, human_date_string) else False

    @staticmethod
    def __is_future_date(human_date: str) -> bool:

        utc_date = datetime.utcnow().date()

        return False if utc_date < human_date else True

    @staticmethod
    def date_to_unix_miliseconds(human_date_string: str) -> int:

        try:
            dt_date = datetime.strptime(human_date_string, "%Y-%m-%d").date()
        except ValueError:
            print("ERROR: Inserted date is not valid. Must be in format YYYY-mm-dd.\n")
            exit()

        if not HumanDateToEpoch.__is_future_date(dt_date):
            print("ERROR: Input date is in the future. Correct and try again.\n")
            exit()

        result_epoch_string = str(
            int(time.mktime(dt_date.timetuple()) * 1000)  # int to remove float decimal
        )

        return result_epoch_string


def get_crypto_asset_history(asset_id: str, start_date: str, end_date: str) -> dict:

    # put in asset_requests module

    SPECIFIED_INTERVAL = "d1"  # Daily interval (UTC)

    crypto_asset_api_url = f"http://api.coincap.io/v2/assets/{asset_id}/history?interval={SPECIFIED_INTERVAL}&start={start_date}&end={end_date}"

    response = requests.request("GET", crypto_asset_api_url)

    return json.loads(response.text.encode("utf8"))


def crypto_asset_json_to_list(crypto_request_json: dict) -> list:

    # put in utils module

    try:
        crypto_asset_data_dict = crypto_request_json["data"]
    except KeyError:
        print("ERROR-> " + crypto_request_json["error"])
        sys.exit(2)

    list_crypto_dicts = []

    for data in crypto_asset_data_dict:
        list_crypto_dicts.append(data)

    return list_crypto_dicts


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

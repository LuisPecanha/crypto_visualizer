import csv
import json
from datetime import datetime
import time
import requests
import re

# TODO - Later on, add table for currencies and there value in the main coins (USD, Euro and Sterling)
# TODO - Do same process of cryptos for stocks
# TODO - Create subdirectories to better organize project
# TODO - Create tests for project


class HumanDateToEpoch:
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

    SPECIFIED_INTERVAL = "d1"  # Daily interval (UTC)

    crypto_asset_api_url = f"http://api.coincap.io/v2/assets/{asset_id}/history?interval={SPECIFIED_INTERVAL}&start={start_date}&end={end_date}"

    response = requests.request("GET", crypto_asset_api_url)

    return json.loads(response.text.encode("utf8"))


def crypto_asset_json_to_list(crypto_request_json: dict) -> list:

    crypto_asset_data_dict = crypto_request_json["data"]

    list_crypto_data = []

    for data in crypto_asset_data_dict:
        list_crypto_data.append(data)

    return list_crypto_data


# TODO - Transform data into pandas dataframe and apply treatment


# TODO - Pass request keys as args when callin python script

# TODO - Implement asset id verification

asset_id = "ethereum"
specified_interval = "d1"
start_date = HumanDateToEpoch.date_to_unix_miliseconds("2022-05-14")
end_date = HumanDateToEpoch.date_to_unix_miliseconds("2022-05-21")

crypto_asset_json = get_crypto_asset_history(asset_id, start_date, end_date)

print(crypto_asset_json_to_list(crypto_asset_json))

# for data in json_data:
#     print(data)
#     print("\n")

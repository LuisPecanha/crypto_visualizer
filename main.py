import csv
import json
from datetime import datetime
import time
import requests
import re


class HumanDateToEpoch:
    @staticmethod
    def __verify_format(human_date_string):

        date_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}"

        return True if re.match(date_pattern, human_date_string) else False

    @staticmethod
    def __is_future_date(human_date):

        utc_date = datetime.utcnow().date()

        return False if utc_date < human_date else True

    @staticmethod
    def date_to_unix_miliseconds(human_date_string):

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


# TODO - Pass request keys as args when callin python script

# TODO - do verification for crypto id


# url = "http://api.coincap.io/v2/assets/{}/history?interval={}&start={}&end={}"

# payload = {}
# headers = {}

# response = requests.request("GET", url, headers=headers, data = payload)

# json_data = json.loads(response.text.encode('utf8'))


HumanDateToEpoch.date_to_unix_miliseconds("2022-06-26")

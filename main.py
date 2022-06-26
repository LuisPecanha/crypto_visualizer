import csv
import json
from datetime import datetime
import time
import requests


class HumanDateToEpoch:
    @staticmethod
    def date_to_unix_miliseconds(human_date_string):

        # TODO - Add verification if it is a date in the specified format.
        # TODO - Add verification to see if it is not a future date. (do this with a class for date manipulation ?)

        dt_date = datetime.strptime(human_date_string, "%Y-%m-%d").date()

        result_epoch_string = str(
            int(time.mktime(dt_date.timetuple()) * 1000)
        )  # int to remove float decimal

        print(result_epoch_string)


def date_to_unix_miliseconds(human_date_string):

    # TODO - Add verification if it is a date in the specified format.
    # TODO - Add verification to see if it is not a future date. (do this with a class for date manipulation ?)

    dt_date = datetime.strptime(human_date_string, "%Y-%m-%d").date()

    result_epoch_string = str(
        int(time.mktime(dt_date.timetuple()) * 1000)
    )  # int to remove float decimal

    print(result_epoch_string)


# url = "http://api.coincap.io/v2/assets/{}/history?interval={}&start={}&end={}"

# payload = {}
# headers = {}

# response = requests.request("GET", url, headers=headers, data = payload)

# json_data = json.loads(response.text.encode('utf8'))


HumanDateToEpoch.date_to_unix_miliseconds("2011-12-01")

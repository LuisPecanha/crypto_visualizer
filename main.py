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
    def date_to_unix_miliseconds(human_date_string):

        # TODO - Add verification to see if it is not a future date. (do this with a class for date manipulation ?)
        try:
            dt_date = datetime.strptime(human_date_string, "%Y-%m-%d").date()
        except ValueError:
            print("ERROR: Inserted date is not valid. Must be in format YYYY-mm-dd.\n")
            exit()

        result_epoch_string = str(
            int(time.mktime(dt_date.timetuple()) * 1000)  # int to remove float decimal
        )

        return result_epoch_string


# url = "http://api.coincap.io/v2/assets/{}/history?interval={}&start={}&end={}"

# payload = {}
# headers = {}

# response = requests.request("GET", url, headers=headers, data = payload)

# json_data = json.loads(response.text.encode('utf8'))


HumanDateToEpoch.date_to_unix_miliseconds("2011-12")

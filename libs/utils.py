from datetime import datetime
import time, re

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

def crypto_asset_json_to_list(crypto_request_json: dict) -> list:

    # put in utils module

    try:
        crypto_asset_data_dict = crypto_request_json["data"]
    except KeyError:
        print("ERROR-> " + crypto_request_json["error"])
        exit()

    list_crypto_dicts = []

    for data in crypto_asset_data_dict:
        list_crypto_dicts.append(data)

    return list_crypto_dicts
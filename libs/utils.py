from datetime import datetime
import time, re


class HumanDateToEpoch:

    """Class containing methods necessary for transformation of HumanDate to Epoch.
    """

    @staticmethod
    def __verify_format(human_date_string: str) -> bool:
        """Verifies if input string is a valid date.

        Args:
            human_date_string (str): Date in string format.

        Returns:
            bool: True if input is valid. False, otherwise. 
        """

        date_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}"

        return True if re.match(date_pattern, human_date_string) else False

    @staticmethod
    def __is_future_date(human_date: str) -> bool:
        """Checks if date is in the future. 

        Args:
            human_date (str): Date in human date string.

        Returns:
            bool: False if date is in the future. True otherwise
        """

        utc_date = datetime.utcnow().date()

        return False if utc_date < human_date else True

    @staticmethod
    def date_to_unix_miliseconds(human_date_string: str) -> int:
        """Transforms the input string in human date to an epoch in miliseconds.

        Args:
            human_date_string (str): Input date as a string.

        Returns:
            int: Input date as an epoch in miliseconds
        """

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

    """Transforms the JSON containing crypto asset data to list of dicitionaries.

    Returns:
        dict: List of dicitionaries containing crypto asset data.
    """

    try:
        crypto_asset_data_dict = crypto_request_json["data"]
    except KeyError:
        print("ERROR-> " + crypto_request_json["error"])
        exit()

    list_crypto_dicts = []

    for data in crypto_asset_data_dict:
        list_crypto_dicts.append(data)

    return list_crypto_dicts

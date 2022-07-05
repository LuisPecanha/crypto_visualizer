"""
Extracts and processes specified crypto asset data from CoinCap to later load onto SQL db. 

argument 1: The crypto asset name (e.g. 'bitcoin')
argument 2: The start date to retrieve data (e.g '2022-05-22')
argument 3: The end date to retrieve data (e.g '2022-05-27')
"""

import argparse
from ast import arg
from libs.utils import HumanDateToEpoch
from libs.processing import execute_crypto_asset_etl_routine

# TODO - Later on, add table for currencies and there value in the main coins (USD, Euro and Sterling)
# TODO - Do same process of cryptos for stocks
# TODO - Create tests for project


def main(args):

    asset_id = args.asset_id
    start_date = HumanDateToEpoch.date_to_unix_miliseconds(args.start_date)
    end_date = HumanDateToEpoch.date_to_unix_miliseconds(args.end_date)

    print(execute_crypto_asset_etl_routine(asset_id, start_date, end_date))


def get_parser() -> argparse.ArgumentParser:
    """Gets the parser that obtains the arguments passed onto the script call.

    Returns:
        argparse.ArgumentParser: Argument Parser.
    """

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

# python3 main.py "bitcoin" "2022-05-15" "2022-05-22" ------------------------------------------------

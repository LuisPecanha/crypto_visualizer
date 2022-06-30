import requests, json


def get_crypto_asset_history(asset_id: str, start_date: str, end_date: str) -> dict:

    # put in asset_requests module

    SPECIFIED_INTERVAL = "d1"  # Daily interval (UTC)

    crypto_asset_api_url = f"http://api.coincap.io/v2/assets/{asset_id}/history?interval={SPECIFIED_INTERVAL}&start={start_date}&end={end_date}"

    response = requests.request("GET", crypto_asset_api_url)

    return json.loads(response.text.encode("utf8"))

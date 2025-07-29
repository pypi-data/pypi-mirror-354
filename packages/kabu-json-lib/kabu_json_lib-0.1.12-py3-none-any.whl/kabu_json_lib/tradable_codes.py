from functools import cache
import requests


@cache
def fetch_tradable_codes(cache_session=None):
    """
    取引可能な証券コードのリストを取得します。

    Args:
        cache_session: キャッシュ付きのrequests.Sessionオブジェクト（オプション）

    Returns:
        list: 取引可能な証券コードのリスト

    Raises:
        requests.exceptions.RequestException: リクエストに失敗した場合
    """
    session = cache_session or requests.Session()
    # https://github.com/umihico/kabu-json-tradable-codes
    url = 'https://d1rrtoo3h22gy6.cloudfront.net/kabu-json-tradable-codes/v1/tradable_codes.json'
    response = session.get(url)
    response.raise_for_status()
    return response.json()["codes"].split(",")

from functools import cache
import requests

global_cache_dict = {}  # fetch_all_stocks_が引数問わずcacheできるようにグローバル変数からセッションを渡す


def fetch_all_stocks(session=None):
    if session is None:
        session = requests.Session()
    global_cache_dict["session"] = session
    return fetch_all_stocks_()


@cache
def fetch_all_stocks_():
    """
    全銘柄の情報を取得する関数
    結果はlru_cacheでキャッシュされる

    Returns:
        dict: 銘柄コードをキー、銘柄名を値とする辞書
    """
    session = global_cache_dict["session"]
    # https://github.com/umihico/kabu-json-all-stock-list
    response = session.get(
        "https://d1rrtoo3h22gy6.cloudfront.net/kabu-json-all-stock-list/v1/all_stocks.json")
    response.raise_for_status()
    stocks_data = response.json()

    # 銘柄コードと銘柄名のペアを作成
    return {stock["コード"]: stock["銘柄名"] for stock in stocks_data}


def fetch_symbol_name(symbol_code):
    """
    銘柄コードから銘柄名を取得する関数
    全銘柄の情報をキャッシュして使用

    Args:
        symbol_code (str): 銘柄コード

    Returns:
        str: 銘柄名
    """
    all_stocks = fetch_all_stocks()
    return all_stocks.get(symbol_code)

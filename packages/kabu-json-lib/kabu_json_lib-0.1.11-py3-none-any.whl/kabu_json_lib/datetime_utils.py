from datetime import datetime
import pytz
jst = pytz.timezone("Asia/Tokyo")


def fetch_now():
    """
    現在の日本時間をdatetimeオブジェクトで返します。
    タイムゾーンはAsia/Tokyoに設定されています。
    """
    return datetime.now(jst)

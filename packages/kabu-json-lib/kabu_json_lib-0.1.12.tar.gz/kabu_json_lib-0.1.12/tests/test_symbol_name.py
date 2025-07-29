import pytest
from unittest.mock import patch, MagicMock
from kabu_json_lib.symbol_name import fetch_symbol_name, fetch_all_stocks


def test_fetch_all_stocks():
    # モックのレスポンスを作成
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"コード": "1305", "銘柄名": "テスト銘柄1"},
        {"コード": "1306", "銘柄名": "テスト銘柄2"}
    ]
    mock_response.raise_for_status.return_value = None

    # requests.Session().getをモック化
    with patch('requests.Session') as mock_session:
        mock_session.return_value.get.return_value = mock_response

        # 関数を実行
        result = fetch_all_stocks()

        # 結果を検証
        assert result == {
            "1305": "テスト銘柄1",
            "1306": "テスト銘柄2"
        }

        # モックが正しく呼び出されたことを確認
        mock_session.return_value.get.assert_called_once_with(
            "https://d1rrtoo3h22gy6.cloudfront.net/kabu-json-all-stock-list/v1/all_stocks.json"
        )


def test_fetch_symbol_name():
    # fetch_all_stocksの結果をモック
    mock_stocks = {
        "1305": "テスト銘柄1",
        "1306": "テスト銘柄2"
    }

    with patch('kabu_json_lib.symbol_name.fetch_all_stocks', return_value=mock_stocks):
        # 存在する銘柄コード
        assert fetch_symbol_name("1305") == "テスト銘柄1"
        # 存在しない銘柄コード
        assert fetch_symbol_name("9999") is None

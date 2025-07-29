import pytest
from unittest.mock import patch, MagicMock
from kabu_json_lib.tradable_codes import fetch_tradable_codes


def test_fetch_tradable_codes():
    # モックのレスポンスを作成
    mock_response = MagicMock()
    mock_response.json.return_value = {"codes": "1234,5678,9012"}
    mock_response.raise_for_status.return_value = None

    # requests.Session().getをモック化
    with patch('requests.Session') as mock_session:
        mock_session.return_value.get.return_value = mock_response

        # 関数を実行
        result = fetch_tradable_codes()

        # 結果を検証
        assert result == ["1234", "5678", "9012"]

        # モックが正しく呼び出されたことを確認
        mock_session.return_value.get.assert_called_once_with(
            'https://d1rrtoo3h22gy6.cloudfront.net/kabu-json-tradable-codes/v1/tradable_codes.json'
        )

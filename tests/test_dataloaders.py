from unittest.mock import MagicMock, patch
from utils.Dataloaders import getUserFromInfo


def test_get_user_from_info_with_no_user():
    mock_info = MagicMock()
    mock_info.context = {
        "request": MagicMock(headers={"Authorization": "Bearer invalid_token"})
    }

    result = getUserFromInfo(mock_info)

    assert result is None


def test_get_user_from_info_with_valid_token():
    demo_user = {"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "name": "Tester"}

    mock_info = MagicMock()
    mock_info.context = {
        "request": MagicMock(headers={"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"})
    }

    with patch('utils.Dataloaders.demouser', demo_user):
        result = getUserFromInfo(mock_info)

        assert result == demo_user

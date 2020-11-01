from unittest.mock import patch

from app.routers.utils import get_distance


@patch("app.routers.utils.requests.get")
def test_get_distance_mock(mock_get):
    mock_get.json.return_value = {"distance": 1.0}
    assert get_distance("Add 1", "Add 2") == 1.61

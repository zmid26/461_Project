from webapp import client
import pytest
import mock
from mock import call
from mock import patch


# Mock all database interactions in rate_package
mock_rating = {'BusFactor': 0.98, 'Correctness': 0.98, 'RampUp': 1.0, 'ResponsiveMaintainer': 0.97, 'LicenseScore': 1.0, 'GoodPinningPractice': 1.0, 'PullRequest': 0.93, 'NetScore': 0.91}
mock_url = 'https://www.npmjs.com/package/express'

@mock.patch('src.APIs.ratepackage.mark_as_updated')
@mock.patch('src.APIs.ratepackage.update_rating')
@mock.patch('src.APIs.ratepackage.mark_as_rated')
@mock.patch('src.APIs.ratepackage.insert_rating')
@mock.patch('src.APIs.ratepackage.get_package_rating')
@mock.patch('src.APIs.ratepackage.run_cli', return_value = mock_rating)
@mock.patch('src.APIs.ratepackage.get_package_url', return_value = mock_url)
@pytest.mark.parametrize("id, status_code", [
    (100, 200),
    (101, 200),
    (404, 404),
])
def test_mock_ratepackage(mock_get_package_url, mock_run_cli, mock_get_package_rating, mock_insert_rating, mock_mark_as_rated, mock_update_rating, mock_mark_as_updated, client, id, status_code):
    print(id)
    response = client.get(f"/package/{id}/rate")
    html = response.data.decode()
    print(html)
    assert response.status_code == status_code
    # if status_code == 200:
    #     mock_get_package_url.assert_called_once_with(id)
                         


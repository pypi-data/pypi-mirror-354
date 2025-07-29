import pytest
from unittest.mock import AsyncMock, patch
import pandas as pd
from tick_data_downloader.downloader import download_tick_data


@patch("tick_data_downloader.downloader.simulate_user_download", new_callable=AsyncMock)
def test_download_tick_data_success(mock_sim):
    mock_sim.return_value = pd.DataFrame({"price": [1.0, 2.0]})
    df = download_tick_data("EURUSD", "2024-12-12")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    mock_sim.assert_called_once()

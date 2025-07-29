import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from tick_data_downloader.main_downloader import simulate_user_download

class AsyncContextManagerMock:
    def __init__(self, result):
        self.result = result

    async def __aenter__(self):
        return self.result  # Not awaitable

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False


@pytest.mark.asyncio
async def test_simulate_user_download_mocks_everything():
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_frame = AsyncMock()
    mock_download = AsyncMock()
    mock_iframe_element = AsyncMock()
    dummy_df = pd.DataFrame({"a": [1], "b": [2]})

    mock_download.suggested_filename = "dummy.csv"
    mock_download.save_as = AsyncMock()

    with patch("tick_data_downloader.main_downloader.async_playwright") as mock_playwright, \
         patch("tick_data_downloader.main_downloader.symbol_select", new=AsyncMock()), \
         patch("tick_data_downloader.main_downloader.select_date", new=AsyncMock()), \
         patch("tick_data_downloader.main_downloader.set_timezone", new=AsyncMock()), \
         patch("tick_data_downloader.main_downloader.pd.read_csv", return_value=dummy_df), \
         patch("tick_data_downloader.main_downloader.os.remove"):

        # Playwright browser setup
        mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Frame setup
        mock_page.wait_for_selector.return_value = mock_iframe_element
        mock_iframe_element.content_frame.return_value = mock_frame
        mock_frame.wait_for_selector = AsyncMock()

        # GMT button setup
        mock_gmt_button = AsyncMock()
        mock_gmt_button.click = AsyncMock()

        mock_frame_locator = MagicMock()
        mock_frame_locator.locator.return_value = mock_gmt_button
        mock_page.frame_locator = MagicMock(return_value=mock_frame_locator)

        # expect_download as async context manager
        mock_page.expect_download = MagicMock(return_value=AsyncContextManagerMock(mock_download))
        mock_frame.click = AsyncMock()

        # Run function
        result_df = await simulate_user_download("USD/JPY", datetime(2024, 6, 1))

        # Validate result
        pd.testing.assert_frame_equal(result_df, dummy_df)

import pytest
from unittest.mock import AsyncMock, MagicMock
from tick_data_downloader.tz import set_timezone

@pytest.mark.asyncio
async def test_set_timezone():
    frame = MagicMock()

    # 1. First locator for the EET button
    tz_button = AsyncMock()
    frame.locator.return_value = tz_button

    # 2. Second locator (for menu option with .first)
    timezone_option = AsyncMock()
    timezone_option.wait_for = AsyncMock()
    timezone_option.click = AsyncMock()

    # Setup second call to locator() to return an object with `.first`
    frame.locator.side_effect = [
        tz_button,  # for EET click
        MagicMock(first=timezone_option)  # for the UTC menu option
    ]

    # Run the function
    await set_timezone(frame, "UTC")

    # Assert calls
    tz_button.click.assert_awaited()
    timezone_option.wait_for.assert_awaited()
    timezone_option.click.assert_awaited()

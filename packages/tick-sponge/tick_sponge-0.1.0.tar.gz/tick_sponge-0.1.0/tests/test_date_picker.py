import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from tick_data_downloader.date_picker import select_date

@pytest.mark.asyncio
async def test_select_date_navigates_to_correct_date():
    frame = MagicMock()

    # Correct selector keys
    values = {
        "button.d-Ch-fi-btn.d-Ch-fi-ni": ["2023", "2024"],  # year
        "button.d-Ch-fi-btn.d-Ch-fi-mi": ["March", "June"]  # month
    }

    counters = {key: 0 for key in values}

    async def mock_inner_text(selector):
        return values[selector][counters[selector]]

    # Increment counter after each call
    async def mock_inner_text_with_counter(selector):
        result = await mock_inner_text(selector)
        counters[selector] += 1
        return result

    frame.inner_text = AsyncMock(side_effect=mock_inner_text_with_counter)

    # Mock UI elements
    date_display = MagicMock()
    date_display.click = AsyncMock()

    popup = MagicMock()
    popup.wait_for = AsyncMock()

    day_cell = MagicMock()
    day_cell.count = AsyncMock(return_value=1)
    day_cell.first.click = AsyncMock()

    frame.locator.side_effect = lambda selector: {
        "div.a-b-c.a-ab-v.d-wh-vg-Ch-Dh": MagicMock(first=date_display),
        "div.a-popupdatepicker:visible": MagicMock(first=popup),
        "td.d-Ch-fi-Ch:not(.d-Ch-fi-oi-mi):has-text('2')": day_cell
    }.get(selector, MagicMock())

    frame.click = AsyncMock()

    # Run
    await select_date(frame, datetime(2024, 6, 2))

    # Assert
    date_display.click.assert_awaited()
    popup.wait_for.assert_awaited()
    frame.click.assert_awaited()
    day_cell.count.assert_called_once()
    day_cell.first.click.assert_awaited()

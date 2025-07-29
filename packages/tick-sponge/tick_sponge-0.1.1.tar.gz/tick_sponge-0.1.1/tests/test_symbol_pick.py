import pytest
from unittest.mock import AsyncMock

from tick_data_downloader.symbol_picker import symbol_select

@pytest.mark.asyncio
async def test_symbol_select_major(monkeypatch):
    mock_frame = AsyncMock()
    await symbol_select(mock_frame, "EURUSD")
    mock_frame.click.assert_any_call("text=Majors")
    mock_frame.click.assert_any_call("li:has-text('EUR/USD')")

@pytest.mark.asyncio
async def test_symbol_select_cross(monkeypatch):
    mock_frame = AsyncMock()
    await symbol_select(mock_frame, "EURNZD")
    mock_frame.click.assert_any_call("text=Crosses")
    mock_frame.click.assert_any_call("li:has-text('EUR/NZD')")

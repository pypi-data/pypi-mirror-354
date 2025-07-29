# tick_data_downloader/downloader.py

import asyncio
import pandas as pd
from tick_data_downloader.main_downloader import simulate_user_download


def download_tick_data(currency:str, date:str):
    return asyncio.run(simulate_user_download(currency=currency, target_date=pd.to_datetime(date)))

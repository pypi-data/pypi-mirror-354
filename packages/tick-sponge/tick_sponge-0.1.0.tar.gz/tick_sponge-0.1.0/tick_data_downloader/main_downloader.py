import os
import pandas as pd
from playwright.async_api import async_playwright
from tick_data_downloader.tz import set_timezone
from tick_data_downloader.date_picker import select_date
from tick_data_downloader.symbol_picker import symbol_select


async def simulate_user_download(currency, target_date):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        await page.goto("https://www.dukascopy.com/swiss/english/marketwatch/historical/")


        iframe_element = await page.wait_for_selector("iframe[src*='freeserv.dukascopy.com']", timeout=10000)
        widget_frame = await iframe_element.content_frame()

        await widget_frame.wait_for_selector("text=All instruments", timeout=10000)

        # Dismiss cookie banner if present
        try:
            await page.locator(".yummy-cookie-widget-emj").evaluate("e => e.style.display = 'none'")
        except:
            pass

        # select the symbol
        await symbol_select(widget_frame, currency)

        # select the date
        # 🧪 Step – ensure date picker pops up
        frame = page.frame_locator("iframe[src*='freeserv.dukascopy.com']")
        await select_date(widget_frame, target_date)

        # select the UTC option
        await set_timezone(widget_frame, target_zone="UTC")

        # select the GMT option 
        await frame.locator("div[role='button']:has-text('GMT')").click()
        
        # Click Download
        download_button = await widget_frame.wait_for_selector("div[role='button']:has-text('Download')", timeout=10000)
        await download_button.click()

        # Wait for 'Save as .csv' to appear and click it
        await widget_frame.wait_for_selector("div.a-b-c.a-ab-v-y-x:has-text('Save as .csv')", timeout=30000)
        async with page.expect_download() as download:
            await page.click("text=Download")


        # Save file to current directory
        download_path = os.path.join(os.getcwd(), download.suggested_filename)
        await download.save_as(download_path)

        # close browser
        await browser.close()

        # read the csv
        df = pd.read_csv(download_path)

        # Clean up
        os.remove(download_path)

        return df

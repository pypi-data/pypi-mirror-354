import asyncio

async def set_timezone(frame, target_zone="UTC"):

    # Step 1: Click the time zone selector (currently shows 'EET')
    await frame.locator("div.a-b-c.a-u-v-y-x >> text=EET").click()
    await asyncio.sleep(0.3)  # wait for dropdown to render

    # Step 2: Find the dropdown option and click UTC
    timezone_option = frame.locator(f"div[role='menuitemradio']:has-text('{target_zone}')").first
    await timezone_option.wait_for(state="visible", timeout=5000)
    await timezone_option.click()

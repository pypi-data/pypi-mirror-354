
async def symbol_select(frame, currency):
        # Select instrument
    await frame.click("text=All instruments")
    if currency in {'AUDUSD','EURUSD','GBPUSD','NZDUSD','USDCAD','USDCHF','USDJPY'}:
        await frame.click("text=Majors")
        await frame.click(f"li:has-text('{currency[:3]+'/'+currency[3:]}')")
    else:
        await frame.click("text=Crosses")
        await frame.click(f"li:has-text('{currency[:3]+'/'+currency[3:]}')")            
    # Set frequency to Tick
    await frame.click("label:has-text('Candlestick:') >> xpath=..")
    await frame.click("div[role='option']:has-text('Tick')")

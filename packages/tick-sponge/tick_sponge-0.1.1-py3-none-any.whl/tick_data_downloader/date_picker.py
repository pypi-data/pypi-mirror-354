import asyncio


async def select_date(frame, target_date):

    # Find the first visible date picker element
    date_display = frame.locator("div.a-b-c.a-ab-v.d-wh-vg-Ch-Dh").first

    # Click it to open the calendar
    await date_display.click()

    # 4. Wait for the calendar to be visible
    calendar_popup = frame.locator("div.a-popupdatepicker:visible")
    await calendar_popup.first.wait_for(state="visible", timeout=10000)


    # 5. Select year
    while True:
        current_year_str = await frame.inner_text("button.d-Ch-fi-btn.d-Ch-fi-ni")
        current_year = int(current_year_str.strip())
        if current_year == target_date.year:
            break
        elif current_year < target_date.year:
            await frame.click("button.d-Ch-fi-btn.d-Ch-fi-nextYear")
        else:
            await frame.click("button.d-Ch-fi-btn.d-Ch-fi-previousYear")
        await asyncio.sleep(0.3)

    # 6. Select month
    month_names = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    while True:
        current_month_str = await frame.inner_text("button.d-Ch-fi-btn.d-Ch-fi-mi")
        current_month = month_names.index(current_month_str.strip())
        if current_month == target_date.month - 1:
            break
        elif current_month < target_date.month - 1:
            await frame.click("button.d-Ch-fi-btn.d-Ch-fi-nextMonth")
        else:
            await frame.click("button.d-Ch-fi-btn.d-Ch-fi-previousMonth")
        await asyncio.sleep(0.3)

    # 7. Click correct day (exclude adjacent-month cells)
    day_selector = f"td.d-Ch-fi-Ch:not(.d-Ch-fi-oi-mi):has-text('{target_date.day}')"
    days = frame.locator(day_selector)
    count = await days.count()
    if count == 0:
        print(f"❌ No valid cell found for day {target_date.day}. Aborting.")
        return
    await days.first.click()





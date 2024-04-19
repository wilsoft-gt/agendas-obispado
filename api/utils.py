import asyncio
from pyppeteer import launch

async def html_to_pdf(html):
    browser = await launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, headless=True)
    page = await browser.newPage()
    await page.setContent(html)
    pdf = await page.pdf({
        'format':'Letter',
        'margin': {
            'top': '0.5in',
            'right': '0.75in',
            'bottom': '0.5in',
            'left': '0.75in'
        }    
    })
    await browser.close()
    return pdf

def run_asyncio_coroutine(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)

def create_pdf(html):
    return run_asyncio_coroutine(html_to_pdf(html))
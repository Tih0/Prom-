import random
import asyncio
from playwright.async_api import async_playwright, expect

with open('useragent.txt') as f:
    user_agents = []
    user_agents = f.readlines()

with open('proxy.txt') as f:
    proxy = []
    proxy = f.readlines()

with open('adresses.txt') as f:
    adresses = []
    adresses = f.readlines()


async def faucet(proxy, user_agent, address, k):
    if k != 0:
        delay = random.randint(39120, 39600)
        print(f'Delay:{delay}')
        await asyncio.sleep(delay)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True,
                                          proxy={'server': f'http://{proxy.strip()}',
                                                 'username': 'vNuNjA5W',
                                                 'password': 'HmxyeHtB'},
                                          args=['--disable-blink-features=AutomationControlled'])

        context = await browser.new_context(user_agent=user_agent.strip())
        page = await context.new_page()
        await page.goto('https://faucet.prom.io/')
        await page.wait_for_load_state()
        inputs = page.locator('input')
        await expect(inputs).to_be_visible()
        await inputs.type(address.strip())
        button = page.get_by_text("Get Tokens")
        await expect(button).to_be_visible()
        await button.click()
        await asyncio.sleep(30)
        await context.close()
        print(f'https://testnet.promscan.io/address/{address}')

async def main():
    k = 0
    while True:
        tasks = []
        for i in range(len(proxy)):
            tasks.append(faucet(proxy[i], user_agents[i], adresses[i], k))
        await asyncio.gather(*tasks)
        k+=1

asyncio.run(main())

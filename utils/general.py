import datetime
import json
import random
from prisma import Prisma
from selenium_driverless.types.by import By

from scraping_script.utils.paths import PATHS


async def navigate(driver, handle, logger, asyncio):
    try:
        # await adaptive_rate_limit()
        await driver.get(f"https://www.instagram.com/{handle}")
        await asyncio.sleep(random.uniform(2, 3))
        return True
    except Exception as e:
        logger.info(f"Error navigating to {handle}: {e}")
        return False
    

async def scrape_detect(driver, logger, asyncio, XPATHS):
    try:
        scrape = await driver.find_element(By.XPATH, XPATHS['SCRAPE_DETECT'])
        logger.info('Scrape detected, clicking...')
        await scrape.click()
        await asyncio.sleep(random.uniform(4, 6.5))
    except:
        pass

    blocked = False
    try:
        blocked = await driver.find_element(By.XPATH, PATHS['BLOCKED'] )
        if blocked:
            logger.info('Something wrong, 25 min delay')
            # await asyncio.sleep(random.uniform(1400, 1600))  
    except:
        pass

    blockedTwo = False
    try:
        blockedTwo = await driver.find_element(By.XPATH, PATHS["BLOCKED_TWO"])
        if blockedTwo:
            logger.info('Something wrong, 25 min delay')
            # await asyncio.sleep(random.uniform(1400, 1600))  
    except:
        pass

    if blocked or blockedTwo:
        logger.info('Detected')
        return True

    return False



async def scraper_sign_in(driver, prisma:Prisma, user_scraper, logger, asyncio):
    #use insta cookie to login

    if user_scraper.get('cookie', None) is not None:
        logger.info("Loading Cookie from Scraper")
        # TODO check expiration
        cookie_dict = json.loads(user_scraper.get('cookie'))
        await driver.add_cookie(cookie_dict.get('ds_user_id'))
        await driver.add_cookie(cookie_dict.get('sessionid'))
    else:
        logger.info("No cookie saved, manually logging in")
        username_input = await driver.find_element(By.NAME, 'username')
        password_input = await driver.find_element(By.NAME, 'password')
        login_button = await driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')

        await username_input.send_keys(user_scraper.get('email'))
        await asyncio.sleep(2)
        await password_input.send_keys(user_scraper.get('password'))
        await asyncio.sleep(3)
        await login_button.click()
        logger.info('Logged in')
        await driver.sleep(3)

        ds_user_id = await driver.get_cookie('ds_user_id')
        sessionId = await driver.get_cookie('sessionid')

        logger.info(f"Cookies: 'ds': {ds_user_id} 'session':{sessionId} ")

    #save cookie

    if ds_user_id and sessionId:
        logger.info("Saving cookies")
        try:
            scraper = await prisma.scraper.update(
            where={
                'id':user_scraper.get('id')
            }
            ,
            data={
                'cookie':json.dumps({'ds_user_id': ds_user_id, 'sessionid':sessionId})
            }
            )
        except Exception as e:
            logger.info(f"Error updating scraper {e}")




def time_calc(emailsSent, now, iterations, logger):
    time_elapsed = datetime.datetime.now() - now
    total_minutes = time_elapsed.total_seconds() / 60
    total_hours = total_minutes / 60

    days = time_elapsed.days
    hours = time_elapsed.seconds // 3600
    minutes = (time_elapsed.seconds % 3600) // 60

    rate_per_hour = emailsSent / total_hours if total_hours > 0 else 0

    logger.info('\n')
    logger.info(f"Running for: {days} days, {hours} hours, and {minutes} minutes")
    logger.info(f"Rate: {rate_per_hour:.2f} emails per hour\n")
    logger.info(f"Checked: {iterations} accounts")
    logger.info(f"Total: {int(emailsSent)} emails sent")
    logger.info('\n')





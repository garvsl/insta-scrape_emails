


import datetime
import os
import random

from prisma import Prisma
import resend
from scraping_script.utils.general import navigate, scrape_detect
from scraping_script.utils.prisma import create_influencer, create_username, get_influencers
from scraping_script.utils.profile import add_comments, extract_bio, extract_email, extract_first_name, get_element_text, load_comments, parse_followers_count
from scraping_script.utils.timing import exponential_backoff
from selenium_driverless.types.by import By
from dotenv import load_dotenv
load_dotenv()

#marketing email sender
resend.api_key = os.getenv('RESEND_API_KEY')

async def process_profile(driver, prisma, username, user_dict, XPATHS, logger, asyncio):
    attempts = 0
    while attempts < 5:
        try:
            if not await navigate(driver, username, logger, asyncio):
                return

            await asyncio.sleep(random.uniform(0.5, 1.5))
            # await asyncio.sleep(30)
            detected = await scrape_detect(driver, logger, asyncio, XPATHS)

            if(detected):
                return {"status": 'detected'}

            followers = await get_element_text(driver, XPATHS['FOLLOWERS_COUNT'], logger, timeout=2)

            if followers is None:
                await asyncio.sleep(random.uniform(1.5, 2.5))
                return {"status": 'failure'}
            
            if parse_followers_count(followers) <= 1500:
                logger.info(f"{username}: Less than 1500 followers")
                await asyncio.sleep(random.uniform(1.5, 2.5))
                return {"status": 'failure'}

            biography = await extract_bio(driver, XPATHS, logger)
            if biography is None:
                await asyncio.sleep(random.uniform(1.5, 2.5))
                return {"status": 'failure'}
            
            logger.info(f"Username: {username}\nFollower count: {followers}\n")

            email = extract_email(biography)
            if email:
                logger.info(f"Email found in bio: {email}")
                username_text = await get_element_text(driver, XPATHS['NAME'], logger, timeout=3)
                first_name = extract_first_name(username_text).split(" ")[0]
                logger.info(f"First name: {first_name}")
                influencer = await create_influencer(prisma, username, email, first_name, logger)
                await asyncio.sleep(random.uniform(1.5, 2.5))
               
                if influencer is not None:
                    logger.info(f"Sending Email to: {username}")

                    #script in db
                    params: resend.Emails.SendParams = {
                        "from": f"{user_dict.get('name')} <{user_dict.get('email')}>",
                        "to": f"{email.strip()}",
                        "subject": user_dict.get('Script')[-1].get('title'),
                        "html": f"{'<br><br>'.join(user_dict.get('Script')[-1].get('body').replace('{}', first_name).split('\n\n'))}",
                    }

                    try:
                        email = resend.Emails.send(params)
                        logger.info(f"Email sent for {user_dict.get('name')}")
                    except Exception as e:
                        logger.info(f"Failed to send: {e}")
                        return {"status": 'failure'}
                        
                    await asyncio.sleep(random.uniform(1.5, 2.5))
                    return {"status": 'success'}
                
            else:
                logger.info("No email found in bio")
                return {"status": 'failure'}
            
            return {"status": 'failure'}
        except Exception as e:
            logger.warning(f"Encountered error in process_profile: {e}")
            attempts += 1
            await exponential_backoff(attempts, asyncio)
    
    logger.error(f"Failed to process profile for {username} after 5 attempts")
    return False



   

async def process_usernames(driver, prisma, influencer, XPATHS, logger, asyncio) -> int:
    num = 0
    usernames = []

    if not await navigate(driver, influencer, logger, asyncio):
        return num
    
    await asyncio.sleep(2)
    await scrape_detect(driver, logger, asyncio, XPATHS)

    try:
        await driver.find_element(By.XPATH, XPATHS['POSTS'], timeout=3)
    except Exception as e:
        logger.info(f"Error finding element with xpath {XPATHS['POSTS']}: {e}")
        return num
    
    posts = [XPATHS['POSTS'] + "/div[1]", XPATHS['POSTS'] + "/div[2]", XPATHS['POSTS'] + "/div[3]"]

    for post in posts:
        logger.info('Start reading post')
        try:
            await driver.sleep(1)
            single = await driver.find_element(By.XPATH, post, timeout=3)
            await single.click()

            await driver.sleep(2)
            await load_comments(driver, logger, asyncio)
            
      
            people = await add_comments(driver, logger)
            
   

            if people:
                for p in people:
                    username = p.find('a')
                    if username.text not in usernames:
                        usernames.append(username.text)

            logger.info(len(usernames))
            

            await driver.back()
        

        except Exception as e:
            logger.info(f"Post error: {e}")

        logger.info('Finished reading post')
        


    usernames = [{'handle':username} for username in usernames]
    logger.info(usernames)
    logger.info(len(usernames))

    # await asyncio.sleep(500)
    num += len(usernames)
    usernames = await create_username(prisma, usernames, logger)
    

    # update to checked afterward
    await prisma.influencer.update(
        where={
            'handle':influencer
        },
        data={
            'checked': True 
        }
    )

    return num


async def gather_usernames(driver, prisma:Prisma, XPATHS, logger, asyncio):
    usernamesAdded = 0
    iterations = 0
    now = datetime.datetime.now()

    influencers = await get_influencers(prisma)
    
    while iterations < 5:
        if influencers is None or len(influencers) == 0 :
            logger.info("Getting more influencers")
            influencers = await get_influencers(prisma) 
            if influencers is None: 
                logger.info("No influencers to process, exiting")
                iterations = 999
                break 
                
        time_elapsed = datetime.datetime.now() - now
        total_minutes = time_elapsed.total_seconds() / 60
        total_hours = total_minutes / 60

        days = time_elapsed.days
        hours = time_elapsed.seconds // 3600
        minutes = (time_elapsed.seconds % 3600) // 60

        rate_per_hour = usernamesAdded / total_hours if total_hours > 0 else 0

        logger.info('\n')
        logger.info(f"Running for: {days} days, {hours} hours, and {minutes} minutes")
        logger.info(f"Rate: {rate_per_hour:.2f} usernames added per hour\n")
        logger.info(f"Checked: {iterations} accounts")
        logger.info(f"Total: {int(usernamesAdded)} usernames added")
        logger.info('\n')
        
        
        influencere = influencers.pop(0)
        proc = await process_usernames(driver, prisma, influencere.handle, XPATHS, logger, asyncio)

        if proc > 0:
            usernamesAdded += proc

        await asyncio.sleep(2)
        iterations += 1




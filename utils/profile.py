import random
import re
import unicodedata
from bs4 import BeautifulSoup
from selenium_driverless.types.by import By

from scraping_script.utils.paths import PATHS



async def get_element_text(driver, xpath, logger, timeout=3):
    try:
        element = await driver.find_element(By.XPATH, xpath, timeout=timeout)
        return BeautifulSoup(await element.source, 'html.parser').get_text(separator='\n', strip=True)
    except Exception as e:
        logger.info(f"Error finding element with xpath {xpath}: {e}")
        return None
        

def parse_followers_count(followers_str):
    followers_str = followers_str.replace(',', '')
    if followers_str.endswith('K'):
        return float(followers_str[:-1]) * 1000
    elif followers_str.endswith('M'):
        return float(followers_str[:-1]) * 1000000
    else:
        return float(followers_str)
    
async def extract_bio(driver, XPATHS, logger):
    try:
        more = await driver.find_element(By.XPATH, XPATHS['MORE_BIO'], timeout=3)
        await more.click()
    except:
        logger.info('No "More" button found')
    
    return await get_element_text(driver, XPATHS['BIO'], logger, timeout=2)
    
def normalize_stylized_text(text):
    char_map = {
        'ᴀ': 'a', 'ʙ': 'b', 'ᴄ': 'c', 'ᴅ': 'd', 'ᴇ': 'e', 'ꜰ': 'f', 'ɢ': 'g', 'ʜ': 'h', 'ɪ': 'i', 'ᴊ': 'j',
        'ᴋ': 'k', 'ʟ': 'l', 'ᴍ': 'm', 'ɴ': 'n', 'ᴏ': 'o', 'ᴘ': 'p', 'ǫ': 'q', 'ʀ': 'r', 'ꜱ': 's', 'ᴛ': 't',
        'ᴜ': 'u', 'ᴠ': 'v', 'ᴡ': 'w', 'x': 'x', 'ʏ': 'y', 'ᴢ': 'z',
        'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', 'Ｅ': 'E', 'Ｆ': 'F', 'Ｇ': 'G', 'Ｈ': 'H', 'Ｉ': 'I', 'Ｊ': 'J',
        'Ｋ': 'K', 'Ｌ': 'L', 'Ｍ': 'M', 'Ｎ': 'N', 'Ｏ': 'O', 'Ｐ': 'P', 'Ｑ': 'Q', 'Ｒ': 'R', 'Ｓ': 'S', 'Ｔ': 'T',
        'Ｕ': 'U', 'Ｖ': 'V', 'Ｗ': 'W', 'Ｘ': 'X', 'Ｙ': 'Y', 'Ｚ': 'Z',
        'Ⓐ': 'A', 'Ⓑ': 'B', 'Ⓒ': 'C', 'Ⓓ': 'D', 'Ⓔ': 'E', 'Ⓕ': 'F', 'Ⓖ': 'G', 'Ⓗ': 'H', 'Ⓘ': 'I', 'Ⓙ': 'J',
        'Ⓚ': 'K', 'Ⓛ': 'L', 'Ⓜ': 'M', 'Ⓝ': 'N', 'Ⓞ': 'O', 'Ⓟ': 'P', 'Ⓠ': 'Q', 'Ⓡ': 'R', 'Ⓢ': 'S', 'Ⓣ': 'T',
        'Ⓤ': 'U', 'Ⓥ': 'V', 'Ⓦ': 'W', 'Ⓧ': 'X', 'Ⓨ': 'Y', 'Ⓩ': 'Z',
    }
    return ''.join(char_map.get(c, c) for c in text)

def extract_first_name(full_name):
    if not full_name or not isinstance(full_name, str):
        return "Love"

    full_name = full_name.strip()

    full_name = re.sub(r'[^\w\s\-|]', '', full_name)

    parts = re.split(r'[\s|]', full_name)

    parts = [part for part in parts if part and len(part) > 1 and not part.isnumeric()]

    if not parts:
        return "Love"

    first_name = parts[0]

    first_name = first_name.replace('_', ' ').strip()

    if first_name.isupper():
        first_name = first_name.title()

    first_name = ''.join(c for c in unicodedata.normalize('NFD', first_name)
                         if unicodedata.category(c) != 'Mn')
    
    first_name = normalize_stylized_text(first_name)

    if len(first_name) <= 1 and len(parts) > 1:
        first_name = parts[1]

    titles = ['dr', 'mr', 'mrs', 'ms', 'miss', 'prof', 'the', 'its']
    if first_name.lower() in titles and len(parts) > 1:
        first_name = parts[1]

    return first_name.title()

def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None
    


async def load_comments(driver, logger, asyncio):
    while True:
        load_more = None
        load_more_two = None

        try:
            load_more = await driver.find_element(By.XPATH, PATHS['MORE_BUTTON'], timeout=3)
        except:
            load_more = None

        if load_more is not None:
            try:
                await load_more.click(move_to=True)
                logger.info('Loading comments using first button')
                await asyncio.sleep(random.uniform(2.5, 3.5))
            except Exception as e:
                logger.error(f"Error clicking first button: {e}")
                break
        else:
            try:
                load_more_two = await driver.find_element(By.XPATH, PATHS['MORE_BUTTON_TWO'], timeout=3)
                if load_more_two is not None:
                    try:
                        await load_more_two.click(move_to=True)
                        logger.info('Loading comments using second button')
                        await asyncio.sleep(random.uniform(2.5, 3.5))
                    except Exception as e:
                        logger.error(f"Error clicking second button: {e}")
                        break
                else:
                    logger.info("No more comments to load")
                    break
            except:
                logger.info("No more comments to load")
                break


async def add_comments(driver, logger):
    try:
        comments = await driver.find_element(By.XPATH, PATHS['COMMENTS'], timeout=3)
        logger.info("Added comments")
    except:
        try:
            comments = await driver.find_element(By.XPATH, PATHS["COMMENTS_TWO"], timeout=3)
            logger.info("Added comments two")
        except:
            logger.info("No comments to add")
            return
        
    comments_src = await comments.source

    soup = BeautifulSoup(comments_src, 'html.parser')    
    people = soup.find_all('h3')
    return people
    
    
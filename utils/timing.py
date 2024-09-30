import datetime
import random


async def exponential_backoff(attempt, asyncio):
    delay = min(300, (2 ** attempt) + random.uniform(0, 1))
    await asyncio.sleep(delay)

async def adaptive_rate_limit(iterations, asyncio):
    hour = datetime.datetime.now().hour
    if 1 <= hour < 6:  # Early morning hours
        await asyncio.sleep(random.uniform(60, 180))
    elif iterations % 50 == 0:  # Every 50 iterations
        await asyncio.sleep(random.uniform(300, 600))
    else:
        await asyncio.sleep(random.uniform(5, 15))


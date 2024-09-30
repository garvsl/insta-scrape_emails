
import random

from prisma import Prisma


async def get_usernames(prisma:Prisma, logger):

    total_unchecked = await prisma.username.count(
        where={
            'checked': False,
        }
    )

    logger.info(f'Total unchecked Usernames: {total_unchecked}')

    if total_unchecked == 0:
        return None
    
    random_offset = random.randint(0, max(0, total_unchecked - 100))
    
    usernames = await prisma.username.find_many(
        take=100,
        skip=random_offset,
        where={
            'checked': False,
        },
        order={
            'created': 'asc'  
        }
    )

    if len(usernames) < 100:
        additional_usernames = await prisma.username.find_many(
            take=100 - len(usernames),
            where={
                'checked': False,
            },
            order={
                'created': 'desc'
            }
        )
        usernames.extend(additional_usernames)

    random.shuffle(usernames)
    
    
    return usernames if len(usernames) > 0 else None

async def set_checked(prisma:Prisma, username, logger):
    try:
        await prisma.username.update(
        where={
            'handle': username
        },
        data={
            'checked': True
        }
        )
    except:
        logger.info("Failed to set checked")

async def create_influencer(prisma:Prisma, username, email, first_name, logger):
    try:
        influencer = await prisma.influencer.create(
            data={
                'handle': username,
                'email': email,
                'name': first_name
            }
        )
        logger.info("Influencer DB created")
        return influencer
    except Exception as e:
        logger.info(f"Couldn't create influencer: {e}")
        return None
   

async def get_user(id:str, prisma:Prisma, logger):
    try:
        user = await prisma.user.find_unique(
            where={
                'id': id 
            },
            include={
                'Scraper':{
                    'order_by':{
                        'createdAt':'asc'
                    }
                },
                'Script':True
            }
        )
        return user.model_dump(exclude={"hashedPassword"})
    except Exception as e:
        return logger.info(f"User not found {e}")
    

async def get_influencers(prisma):

    total_unchecked = await prisma.influencer.count(
        where={
            'checked': False,
        }
    )

    if total_unchecked == 0:
        return None
    
    random_offset = random.randint(0, max(0, total_unchecked - 100))
    
    influencers = await prisma.influencer.find_many(
        take=100,
        skip=random_offset,
        where={
            'checked': False,
        },
        order={
            'created': 'asc'  
        }
    )

    if len(influencers) < 100:
        additional_influencers = await prisma.influencer.find_many(
            take=100 - len(influencers),
            where={
                'checked': False,
            },
            order={
                'created': 'desc'
            }
        )
        influencers.extend(additional_influencers)

    random.shuffle(influencers)

    
    return influencers if len(influencers) > 0 else None


async def create_username(prisma:Prisma, usernames, logger):
    try:
        usernames = await prisma.username.create_many(
            data=usernames,
            skip_duplicates=True
        )
        logger.info(usernames)
        logger.info("Usernames created")
        return usernames
    except Exception as e:
        logger.info(f"Couldn't create username: {e}")
        return None
    


async def app_auth(cur_user:str, prisma:Prisma, logger):

    
    try:
        user = await prisma.user.find_unique(
            where={
                'id': cur_user 
            },
            include={
                'Scraper':{
                    'order_by':{
                        'createdAt':'desc'
                    }
                },
                'Script':True
            }
        )
    except Exception as e:
        return logger.info(f"User not found {e}...exiting")
        
    user = user.model_dump(exclude={'hashedPassword'})
    
    if user is None:
        logger.info("User not found")
        return

    logger.info(f"Welcome {user.get('name', 'User')}!\n\n")

    if user.get('Scraper', None) is None or len(user.get('Scraper', None)) == 0 :
        logger.info("You need to create a scraper first")
        return
    
    return user


PATHS = {
    #universal paths
    'EXIT_BUTTON': '/html/body/div[7]/div[1]/div/div[2]/div',
    'MORE_BUTTON': '/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button',
    'MORE_BUTTON_TWO': '/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button',               
    'COMMENTS': '/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div',
    'COMMENTS_TWO': '/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div',
    'BLOCKED': '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/span',
    'BLOCKED_TWO': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/span'
}

USER_XPATHS = [
    #change path depending on account
    {
        'id': 'kp',
        'SCRAPE_DETECT': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div[2]/div/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]',
        'FOLLOWERS_COUNT': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a/span/span',
        'NAME': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/div[1]/span',
        'MORE_BIO': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/span/span/div/span',
        'BIO': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/span/div/span',
        'POSTS': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[1]',  
    },
    {
        'id':'harry',
        'SCRAPE_DETECT': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div[2]/div/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]',
        'FOLLOWERS_COUNT': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a/span/span',
        'NAME': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/div[1]/span',
        'MORE_BIO': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/span/span/div/span',
        'BIO': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/span/div/span',
        'POSTS': '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[1]',  
    },
    {
        'id':'ateeq',
        'SCRAPE_DETECT': '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/section/main/div[2]/div/div/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div',
        'FOLLOWERS_COUNT': '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a/span/span',
        'NAME': '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/div[1]/span',
        'MORE_BIO': '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/span/span/div/span',
        'BIO': '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[4]/div/span/div/span',
        'POSTS': '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[1]',  
    }
]


# insta-scraper

Input one account and gather emails endlessly from that one account, branching out. automatically emails if u havent already emailed them.

# setup

- Use seperate backend to create user, scraper, script, and one manual influencer
- Change paths in utils/paths and dedicated scraper as desired in final.py

# run

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
prisma generate
python3 final.py {put user id here, without brackets}

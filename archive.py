import tweepy
import sys
from config import consumer_token, consumer_secret, access_token, access_token_secret

def connect():
    """
    Connects and auths to tweepy API
    """
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def account_lists(account: str, socialbot=False):
    """
    Gets the name of all the associated accounts
    """
    api = connect()

    user = api.get_user(account)
    lists = api.lists_all(user.screen_name)
    for each_list in lists:
        try:
            for each_member in each_list.members():
                name = each_member.screen_name
                if socialbot:
                    print("socialbot: snscrape twitter-user", name)
                else:
                    print("snscrape twitter-user", name)
        except tweepy.error.TweepError as e:
            raise ValueError(account + str(e))

def iterate_accounts(filename: str = "accounts.txt", socialbot: bool = False):
    """
    Iterates through all the accounts in accounts.txt
    """
    with open(filename, "r") as f:
        for each_line in f:
            if each_line and each_line.rstrip() and "#" not in each_line:
                if socialbot:
                    print("socialbot: snscrape twitter-user", each_line.rstrip())
                else:
                    print("snscrape twitter-user", each_line.rstrip())

                account_lists(each_line.rstrip(), socialbot)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        raise ValueError("Not enough args passed")
    elif sys.argv[1] == "socialbot":
        iterate_accounts(socialbot=True)
    else:
        iterate_accounts(socialbot=False)

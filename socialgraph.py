import tweepy
import shutil
from config import consumer_token, consumer_secret, access_token, access_token_secret
from colorama import init, Fore, Back, Style
import re


def connect():
    """
    Connects and auths to tweepy API
    """
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


def main():
    user = input("Please enter the starting user: ")

    walker = Walk(user.rstrip())
    walker.recursive_walk()


class Walk:
    def __init__(self, user: str = "RoyalFamily"):
        init()
        self.api = connect()
        self.user = self.api.get_user(user.rstrip())
        self.recursion_level = 0

        self.user_list = []  # ppl already added
        self.account_list = []  # ppl already added

        with open("accounts.txt") as f:
            for each_line in f:
                self.account_list.append(each_line.rstrip())

        with open("snscrape.txt") as f:
            for each_line in f:
                if "twitter-user" in each_line:
                    self.user_list.append(each_line.split()[2].rstrip())

    def approval(self, msg="") -> bool:
        print()
        if msg:
            print(" " * 4, msg)
        approved = input(
            " " * 5
            + "Y/n? (or c, r={recursion_level}): ".format(
                recursion_level=self.recursion_level
            )
        )
        if approved.rstrip().lower() in ["y", "yes"]:
            print()
            return True
        elif approved.rstrip().lower() in ["c", "cancel"]:
            print()
            raise ValueError()
        else:
            print()
            return False

    def recursive_walk(self, user=None):
        if not user:
            user = self.user

        self.print_user(user)
        if self.approval("Do you want to include this user?"):
            self.add_user(user)

            lists = self.api.lists_all(user.screen_name)

            if len(lists) > 0 and not user.screen_name in self.account_list:
                # print(" " * 4, "{name} has {x} lists".format(name=user.name, x=len(lists)))
                print("{name} has {x} lists".format(name=user.name, x=len(lists)))
                if self.approval("Do you want to see these lists?"):
                    for each_list in lists:
                        # print(" " * 4, each_list.full_name, each_list.member_count)
                        print(each_list.full_name, each_list.member_count)
                    if self.approval("Do you want to add all of these lists?"):
                        self.add_user_lists(user.screen_name)

            if user.friends_count > 0:
                print(
                    "{name} is following {x} ppl".format(
                        name=user.name, x=user.friends_count
                    )
                )
                print()
                self.recursion_level += 1
                for friend in self.api.friends(user.screen_name):
                    if not friend.screen_name in self.user_list:
                        try:
                            self.recursive_walk(friend)
                        except ValueError:
                            break
                self.recursion_level -= 1

    def add_user(self, user: str):
        if isinstance(user, str):
            self.account_list.append(user)
            with open("snscrape.txt", "a") as f:
                f.write("snscrape twitter-user " + user + "\n")
        else:
            self.user_list.append(user.screen_name)
            with open("snscrape.txt", "a") as f:
                f.write("snscrape twitter-user " + user.screen_name + "\n")

    def add_user_lists(self, user: str):
        if isinstance(user, str):
            self.account_list.append(user)
            with open("accounts.txt", "a") as f:
                f.write(user + "\n")
        else:
            self.account_list.append(user.screen_name)
            with open("accounts.txt", "a") as f:
                f.write(user.screen_name + "\n")

    def print_user(self, user: str = "RoyalFamily"):
        print("-" * shutil.get_terminal_size((80, 20)).columns + "\n")
        if user.verified:
            color = Fore.GREEN
        else:
            color = ""

        print(
            " " * 4,
            color + user.name.rstrip(),
            "(" + user.screen_name.rstrip() + ")",
            "({following}, {followed})".format(
                followed=user.followers_count, following=user.friends_count
            ),
            Style.RESET_ALL,
        )
        print(" " * 4, self.highlight(user.description))

    def highlight(self, words: str) -> str:
        terms = [
            "official",
            "gov",
            "government",
            "rep",
            "representative",
            "legal",
            "foundation",
            "president",
            "aid",
            "director",
            "journalist",
            "congress",
            "congressman",
            "congresswoman",
            "senator",
            "ambassador",
            "diplomat",
            "prof",
            "library",
            "union",
            "senate",
            "district",
        ]
        return_string = ""

        tokens = words.split()
        for count, each_token in enumerate(tokens):
            if re.sub("[^a-zA-Z]+", "", each_token.lower()).rstrip() in terms:
                # if each_token.lower().rstrip() in terms:
                return_string += Fore.RED
                return_string += each_token + " "
                return_string += Style.RESET_ALL
            else:
                return_string += each_token + " "

        # return " ".join(tokens).rstrip()
        return return_string


if __name__ == "__main__":
    main()

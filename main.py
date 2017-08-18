import praw
import json
from sys import argv
from sys import exit

secrets = None

# Basic error hand usage handling
try:
    secrets = open(argv[1], "r")
except IndexError:
    print("Usage: python {} <secrets file> [subreddit list]".format(argv[0]))
    exit(1)
except IOError:
    print("Could not open file: {}".format(argv[1]))
    exit(1)

# Generating a JSON string to parse from our secrets file
secret_list = ""
for line in secrets:
    secret_list += line.strip()

secrets.close()
secret_json = json.loads(secret_list)

# Start our reddit instance!
#TODO: Implement error handling here
reddit = praw.Reddit(client_id = secret_json["id"],
                     client_secret = secret_json["key"],
                     username = secret_json["username"],
                     password = secret_json["password"],
                     user_agent = "The coolest Reddit scraper ever, by b4ux1t3")

# Check if the user passed a subreddit list
if len(argv) > 2:
    subreddit_list = []
    try:
        with open(argv[2], "r") as f:
            subreddit_list.append(f.readline().strip())
        f.close()
    except IOError:
        print("Could not open file: {}".format(argv[2]))
else:
    subreddit_list = ["programming", "python"]

subreddit = reddit.subreddit(subreddit_list[0])

hot_subreddit = subreddit.hot(limit = 1)

def get_replies(comment, indent = 0):
    if comment.author != None:
        print((" " * 4) * indent + comment.author.name + ":")
    else:
        print((" " * 4) * indent + "[deleted]:")
    print((" " * 4) * indent + comment.body)
    if len(comment.replies) == 0:
        print("=" * 10)
        return
    else:
        for reply in comment.replies:
            get_replies(reply, indent + 1)

count = 0
for submission in hot_subreddit:
    for comment in submission.comments:
        count += 1
        get_replies(comment)

print("\n\n\n{}".format(count))

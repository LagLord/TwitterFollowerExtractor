import tweepy
from config import *
from csv import DictWriter


id = "43901113"
next_token = ""
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True, return_type="response.Response")

users = client.get_users_followers(id=id, user_fields=["profile_image_url", "id", "verified", "created_at",
                                                       "name", "location", "description", "url", "protected",
                                                       "public_metrics"],
                                   expansions=["pinned_tweet_id"], max_results=1000)
field_names = ['id',
               'username',
               'name', 'created_at', 'verified', 'protected',
               'profile_image_url',
               'url',
               'location',
               'description',
               'followers_count', 'following_count', 'tweet_count', 'listed_count'
               ]
HEADERS_WRITTEN = False

while next_token != "None":
    metadata = users.meta

    next_token = metadata.get("next_token")
    print(next_token)
    for user in users.data:
        user_dict = user.data
        # print(user_dict.items())
        # new_dict = pandas.json_normalize(user_dict)

        for key in user_dict["public_metrics"]:
            user_dict[key] = user_dict["public_metrics"][key]

        with open("followers.csv", mode="a", encoding="utf-8", newline="") as file:
            dict_writer = DictWriter(file, fieldnames=field_names, extrasaction='ignore')
            # if not HEADERS_WRITTEN:
            #     dict_writer.writeheader()
            #     HEADERS_WRITTEN = True
            dict_writer.writerow(user_dict)
    users = client.get_users_followers(id=id, user_fields=["profile_image_url", "id", "verified", "created_at",
                                                           "name", "location", "description", "url", "protected",
                                                           "public_metrics"],
                                       expansions=["pinned_tweet_id"], max_results=1000, pagination_token=next_token)

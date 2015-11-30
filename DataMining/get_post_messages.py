import pandas as pd
import json
import time
from urllib import request
import datetime

with open("app_secrets.ini", "r") as secrets:
    clientid = secrets.readline()  # replace with actual client id
    clientsecret = secrets.readline()  # replace with app secret
    # README: Temporary User access token
    # Needs my authentication since my app doesn't
    # have access to 'Open within UT Austin' only groups.
    # THIS TOKEN WILL NEED TO BE REGENERATED EVERY 2 HOURS TO WORK AGAIN
    access_token = secrets.readline()
# replace with actual client secret

outfile = 'posts_with_text_body.csv'  # change the output filename if you like
# ID of the UT ECE Facebook Group.
group_id = "155621761221818"

# Read the filtered posts list from the .csv format
# and make a dataframe out of it.
posts = pd.read_csv("posts_filtered.csv")

# Prints the first 5 rows, just to make sure it works.
print(posts.head(5))

# Since we want to retrieve the textual content of each post,
# We only want post IDs, not Group ID.
# The csv file I have stores IDs as groupId_postId
post_ids = [post_id.split('_')[1] for post_id in posts["id"]]

# Sanity check to make sure that we are indexing into the
# post IDs correctly.
num_posts = len(post_ids)
print(num_posts)
print(post_ids[0])

# Print type of a column for a pandas dataframe
# Each column of a dataframe is a Series object
print(type(posts['id']))

# Insert a new column (for message body) into the pandas dataframe.
# This will default to the same number of rows as the other columns.
posts['message'] = pd.Series()
# print("New column length:" + str(len(posts['message'])))


"""
Given a Facebook Post ID, and valid access token,
This function will print the textual body of the post.

* This function doesn't need the Group ID, as a post
ID is inherently associated with a group or page.
"""


def testFacebookPostData(access_token, post_id):
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + post_id
    parameters = "?fields=message&access_token={}".format(access_token)
    url = base + node + parameters

    # retrieve data
    # request, urlopen are both from urllib
    req = request.Request(url)

    # response is a http.client.HTTPResponse object
    response = request.urlopen(req)

    # README: I found out that response.read() will consume the field.
    # It moves some sort of iterator or cursor, so the response body
    # needs to be saved when it is read()
    response_body = response.read()
    # response.read() returns a bytes object, so I need to decode that
    # into a string, since json.loads() only takes in a string.
    decoded_response = response_body.decode("utf-8")
    # print(decoded_response)

    # Deserialize the string containing a JSON object into a dict.
    post = json.loads(decoded_response)

    # This particular post will have 2 keys:
    # Message, and ID.
    # We only want to retain the message (textual body).
    for key, value in post.items():
        print("Key:" + key)

    message = post['message']
    print("Message:" + message)
    return message
    # print(json.dumps(post, indent=4, sort_keys=True))


"""
message_num used for debugging purposes
To see exactly when we run up against Facebook API's rate limit
"""


def getPostMessage(post_id, access_token, message_num):
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + post_id
    parameters = "?fields=message&access_token={}".format(access_token)
    url = base + node + parameters

    # retrieve post
    post = json.loads(request_until_succeed(url))
    try:
        message = post['message']
        # Debug print
        # unicode_msg = message.encode('utf-8')
        print("Message number {}: {}".format(str(message_num), message))
        return message
    except Exception as e:
        # Either there is no "message" field (Because a "status" was actually a
        # photo)
        # Or there is some weird encoding error where someone writes something
        # other than english, e.g. - emoticons, as I was able to track down
        # This site is saving me
        # https://stackoverflow.com/questions/3218014/unicodeencodeerror-gbk-codec-cant-encode-character-illegal-multibyte-sequen
        print(e)
        for key, value in post.items():
            print("Key: " + key)
            # print("Value: " + value.encode('utf-8'))
            with open("errors.txt", "a") as error_log:
                if value is None:
                    error_log.write(
                        "Post index {} - No textual message in post"
                            .format(message_num))
                else:
                    error_log.write(
                        "Post index {} - Unicode error".format(message_num))
                error_log.write("\n")
    return 0

"""
When scraping large amounts of data from public APIs, there's a high
probability that you'll hit an HTTP Error 500 (Internal Error) at
some point. There is no way to avoid that on our end. Instead, we'll use
a helper function tocatch the error and try again after a few seconds,
which usually works. This helper function also
consolidates the data retrival code, so it kills two birds with one stone.
"""

# README: My hunch tells me that this function will consume
# twice as many API requests...
# However, it does seem error-prone.
# If time is of the essence, I could probably set a manual loop
# That will only run a batch of 600 requests within a 10-minute time span,
# Which will fit Facebook API v2.4's 600 requests/600 second rate limit.


def request_until_succeed(url):
    req = request.Request(url)
    success = False
    while success is False:
        try:
            response = request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            # This number was originally 5, but I'm skeptical.
            # Facebook API v2.4 supposedly rate limits to
            # 600 requests every 600 seconds (or 10 minutes).
            # I'm putting in a few more seconds just to be safe.
            # Considering that we have ~1800 posts to go through,
            # We have to be safe.
            time.sleep(605)
            print("Error for URL %s: %s" % (url, datetime.datetime.now()))
            # Save partial progress just in case bad things happen
            posts.to_csv('posts_finished.csv')

    # README: I found out that response.read() will consume the field.
    # It moves some sort of iterator or cursor, so the response body
    # needs to be saved when it is read()
    response_body = response.read()
    # response.read() returns a bytes object, so I need to decode that
    # into a string, since json.loads() only takes in a string.
    decoded_response = response_body.decode("utf-8")
    return decoded_response


# Test to see if pandas dataframe gets written to, and
# Test to see if pandas csv export works,
# msg = testFacebookPostData(access_token, post_ids[1])

# Index into column with label 'message' at row i
# Mixed indexing - 0 is an index, while 'message' is a label
# posts.ix[0, 'message'] = msg
# posts.to_csv('posts_finished.csv')

for i in range(1573, num_posts):
    current_post_id = post_ids[i]
    message = getPostMessage(current_post_id, access_token, i)
    # Index into row i at column with label 'message'
    posts.ix[i, 'message'] = message
posts.to_csv('posts_finished.csv')

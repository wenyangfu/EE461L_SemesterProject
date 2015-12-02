import re
import pandas as pd
import json
from urllib import request
import time

course_tags = []
course_aliases = []
access_token = None
group_id = "155621761221818"

with open("ClassListing.txt", 'r') as course_file:
    # Split each course name into a list of words
    for course_name in course_file:
        course_name_parts = course_name.strip('\n').split(" ")
        # Check if line parsed was null
        if course_name_parts[0] == '':
            continue
        filter(None, course_name_parts)
        course_tags.append(course_name_parts)

# Gather a list of aliases for each course

with open("class_aliases.txt", 'r') as course_alias_file:
    # Split each course name into a list of words
    for course_alias in course_alias_file:
        course_name_parts = course_alias.strip('\n').lower().split(',')
        # Check if line parsed was null
        if course_name_parts[0] == '':
            course_aliases.append(None)
            continue
        course_aliases.append(course_name_parts)
# Load Facebook credentials

with open("app_secrets.ini", "r") as secrets:
    clientid = secrets.readline()  # replace with actual client id
    clientsecret = secrets.readline()  # replace with app secret
    # README: Temporary User access token
    # Needs my authentication since my app doesn't
    # have access to 'Open within UT Austin' only groups.
    # THIS TOKEN WILL NEED TO BE REGENERATED EVERY 2 HOURS TO WORK AGAIN
    access_token = secrets.readline()
    # replace with actual client secret
# ID of the UT ECE Facebook Group.
group_id = "155621761221818"

assert(len(course_tags) == len(course_aliases))

posts = pd.read_csv('posts_filtered_final.csv')
# Sanity check to make sure columns are what we expect them to be
print(list(posts.columns.values))
# Check what position the course number is in
print(course_tags[3][1])
print(str(type(course_tags[0])))
# Set up a dict of related courses for each post
related_courses = {}

"""
Input: course_num is a string containing the course number.
msg: lowercase textual contents of a Facebook post.

course_nicknames: a list of nicknames for the course.

department: the 2 or 3-letter initial for the department the course
belongs to.

index: the index of the post.
"""


def tag_relevant_course(index, department, course_num, course_nicknames, msg):
    course_num_lower = course_num.lower()
    msg_split = re.findall(r"[\w]+", msg)
    if course_nicknames is not None:
        if (any(word in msg_split for word in course_nicknames) or
                any(word in msg for word in course_nicknames)):
            if index in related_courses:
                related_courses[index].append(department + course_num)
            else:
                related_courses[index] = [department + course_num]
    if (course_num_lower in msg_split or
            (department + course_num_lower) in msg_split):
        if course_num_lower == "379k":
            return
        if index in related_courses:
            related_courses[index].append(department + course_num)
        else:
            related_courses[index] = [department + course_num]


def tag_all_courses():
    # Tag each course that we have
    for i in range(len(posts.index)):
        message = posts.ix[i, 'message']
        for j in range(len(course_tags)):
            department = course_tags[j][0]
            course_num = course_tags[j][1]
            alias_list = course_aliases[j]
            course_num_lower = course_num.lower()
            # Have to use lowercase course_num, because the original text
            # string was converted to lowercase. Before I added this bugfix,
            # courses with a letter like EE445L were not being caught,
            # becuase 445l != 445L.
            tag_relevant_course(
                i, department, course_num_lower, alias_list, str(message).lower())

tag_all_courses()

"""
This is a helper function to convert a post
into a Python dict.

It will find the entry at index 'key' in
the posts dataframe and convert it into a dict.

value is the list of courses that is associated
with the post at index 'key'
"""


def post_to_dict(key, value):
    post = posts.loc[key]
    # Each post is a pandas Series
    course_as_dict = {}
    fields = ['id', 'message']
    for label in fields:
        course_as_dict[label] = post.loc[label]
    course_as_dict['related_courses'] = value
    return course_as_dict


"""
Get comments for a single Facebook post,
given the post's index within the posts dataframe.
May run into Facebook API errors.
"""


def get_comments(post_index):
    print(access_token)
    post_id = posts.ix[post_index, 'id'].split("_")[1]
    # num_comments is of type: numpy.int64
    num_comments = posts.ix[post_index, 'commentsCount']
     # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + post_id
    parameters = ("/comments?fields=message&limit={}&access_token={}"
                  .format(str(num_comments), access_token))
    url = base + node + parameters

    # Return empty list if there are no comments, of course.
    if num_comments == 0:
        return []
    # retrieve comments
    post = json.loads(request_until_succeed(url))
    comments = post['data']
    print(type(comments))
    try:
        comments_no_metadata = [comment['message'] for comment in comments]
        print("Post number {}".format(str(post_index)))
        return comments_no_metadata
    except Exception as e:
        # Either there is no "message" field
        # Or there is some weird encoding error where someone writes something
        # other than english, e.g. - emoticons, as I was able to track down
        print(e)
        for key, value in post.items():
            print("Key: " + key)
            # print("Value: " + value.encode('utf-8'))
            with open("tag_posts_errors.txt", "w") as error_log:
                error_log.write(
                    "Post index {} - Unicode error".format(message_num))
                error_log.write("\n")
    return []

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
            # Facebook API v2.4 supposedly rate limits to
            # 600 requests every 600 seconds (or 10 minutes).
            # sleep for some time and try again.
            time.sleep(605)
            print("Error for URL %s: %s" % (url, datetime.datetime.now()))
            # Save partial progress just in case bad things happen
            posts.to_csv('posts_finished.csv')

    # README: response.read() will consume the field, so the response body
    # needs to be saved when it is read()
    response_body = response.read()
    # response.read() returns a bytes object, so I need to decode that
    # into a string, since json.loads() only takes in a string.
    decoded_response = response_body.decode("utf-8")
    return decoded_response

"""
 Get comments for all Facebook posts with
 valid tags.
"""


def get_all_comments():
    post_comments = []
    for key, value in related_courses.items():
        post_comments.append(get_comments(key))
    return post_comments


# Output all tagged posts as JSON.

with open("tagged_posts_json.txt", 'w') as outfile:
    # course_dict = {}
    course_json = []
    for key, value in related_courses.items():
        course_json.append(post_to_dict(key, value))
    post_comments = get_all_comments()
    for i in range(len(course_json)):
        course_json[i]['comments'] = post_comments[i]

    json.dump(course_json, outfile)

# Sanity check to make sure posts can be deserialized correctly
with open("tagged_posts_json.txt", 'r') as outfile:
    deserialized = json.load(outfile)
    print(deserialized)


with open("tagged_posts.txt", mode='w') as tagged_posts:
    for key, value in related_courses.items():
        tagged_posts.write("Post index {} ".format(str(key)))
        tagged_posts.write("Related classes - {}\n".format(str(value)))

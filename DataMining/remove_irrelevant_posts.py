import pandas as pd
import re

# This script runs with Python 3, and requires pandas

# Read the filtered posts list from the .csv format
# and make a dataframe out of it.
posts = pd.read_csv("posts_filtered_truncated_pd.csv")
# Remove all posts that contain "buy" or "sell"
num_rows = len(posts.index)
# Create a list of irrelevant post indices

bad_post_words2 = ["$", "http"]
# Import a list of irrelevant words
with open("bad_words.txt", "r") as bad_words:
    bad_post_words = [word.strip('\n') for word in bad_words.readlines()]
print(bad_post_words)

"""
Given the number of rows in the current dataframe,
find the indices of irrelevant posts.
"""


def find_bad_indices(num_rows):
    bad_post_indices = []
    for i in range(num_rows):
        msg = posts.ix[i, 'message']
        # Find all words within a post's message.
        # Check if any of words we deem irrelevant are contained
        # within the post.
        msg_list = re.findall(r"[\w]+", str(msg).lower())
        if (any(word in msg_list for word in bad_post_words) or
                msg == "0" or msg == 0 or
                any(word in str(msg) for word in bad_post_words2)):
            bad_post_indices.append(i)
    return bad_post_indices

bad_post_indices = find_bad_indices(num_rows)
print(bad_post_indices)
posts = posts.drop(bad_post_indices)
# Remove all posts that have no textual body
posts = posts.dropna()
posts.to_csv('posts_filtered_fixed.csv')
labels_to_drop = ['authorName', 'authorId',
                  'sharesCount', 'likesCount', 'url', 'type']
posts = posts.drop(labels_to_drop, axis=1)
posts.to_csv('posts_filtered_final.csv')

select
    id as comment_id,
    author,
    subreddit,
    score,
    created_utc,
    body
from `redditpredict`.reddit_comments_2014.full_2014_comments


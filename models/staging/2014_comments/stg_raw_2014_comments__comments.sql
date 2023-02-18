{%- set relevant_dates = ['HOUR', 'DAY', 'MONTH', 'YEAR'] -%}
with 

comments as (
    
    select * from {{ source('reddit_comments_2014', 'full_2014_comments') }}

),

split_dates as (

    select  
        id as comment_id, 
        author,
        subreddit,
        score,
        body,

        {% for relevant_date in relevant_dates -%}
            cast(extract({{relevant_date|upper}} from timestamp_micros(created_utc*1000000)) as int64) as {{relevant_date|upper}}_int,
        {% endfor %}
    from comments
),

-- {%- set selected_subreddit = ['funny'] -%} -- can add list, filter more for future work
soft_deletes as (
    select *,
        case
            when comment_id is null then true
            when subreddit is null then true
            when score is null then true
            when body is null then true
            when body = '[deleted]' then true
            when body = '[removed]' then true
            when year_int != 2014 then true
            when subreddit != 'funny' then true -- just want funny to replicate old results now
            else false
        end as to_delete
    from split_dates
)


select * from soft_deletes where to_delete = false

select 
    score,
    body,
    HOUR_int,
    DAY_int,
    MONTH_int
from {{ ref('stg_raw_2014_comments__comments') }}



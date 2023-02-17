with comments as (

    select * from {{ ref('stg_raw_2014_comments__comments') }}

)

select * from comments
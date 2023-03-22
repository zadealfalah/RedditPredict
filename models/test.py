def model(dbt, session):
    # Must be either table or incremental (view is not currently supported)
    dbt.config(materialized = "table")

    # DataFrame representing an upstream model
    df = dbt.ref("2014_funny_score_date")
 
    return df
# Reddit Comment Karma Prediction - Python Analysis (WORK IN PROGRESS)
Predicting reddit comment karma (score) using only comment text data within and between subreddits.

## Table of Contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Prospective Roadmap](#prospective-roadmap)
* [Processes and Features](#processes-and-features)
* [Things To Do](#things-to-do)

## General Info
The main goal was to build a regression model to predict the score a comment might get within a subreddit.  This was shifted to a classifcation problem where we look to classify prospective comments as 'good', 'okay', and 'bad' within a subreddit.  Future work will hopefully allow for examinations between subreddits as well.

This project was originally created as a final project for a course in my masters.  I am reinvestigating the material while incorporating new technologies (e.g. dbt).  Many of these new technologies were used during a trial period, so code is being written to accommodate this.  

## Technologies
- python (bertopic, spacy, pandas, pickle, sklearn)
- dbt
- sql
- GCP (BigQuery, buckets)

## Prospective Roadmap
As of right now the ETL has been performed for 2014 reddit comments from the 'funny' subreddit.  The hope is to complete the EDA, analysis, and modeling on this dataset before creating .py file(s) to allow for easy follow-up with new data - whether it be for comparison to the found results or to add on and expand upon them.  For example, the addition of 2015 reddit comments in the 'funny' subreddit or perhaps the 2014 'ask' subreddit.

Other tools may be utilized to gain experience with them and will be added to the readme as they are used.

## Processes and Features
To begin with, ETL was performed with dbt using data from Google BigQuery.  The raw data included many features but of interest to us was only the score (our target), the text body (comment itself) and, possibly, some time information which was added on with SQL commands through dbt.  The transformed data was put into a bucket on GCP and then read in.  It was also stored locally as various technology trials were reaching their ends.  

The data was read in and checked again, it was found that some null values slipped through (208 rows of the 10633856 total) which will necessitate a closer look at the dbt files later.  For now they were cleaned manually in python.   The distribution of the score feature was examined and found to be so concentrated around a value of 1 that the orginal plan of a regressor was scrapped in favor of a classifier with 'bad', 'okay', and 'good' scores of ranges (-inf, 0], [1, 13], and [14, inf) respectively.  

After binning the scores, BERTopic was used along with spacy's en_core_web_sm trained pipeline.  This was chosen as our first model because it was pre-trained on written text including blogs, news, and comments and as such is perfect for our use case.  

As it is right now, the model is having memory issues despite using BERTopic's low_memory and not calculating the probabilities.  This needs to be addressed before any work can continue.

## Things To Do
- Figure out how to address OOM errors if we continue with the same approach for commentModeling
- Update requirements.txt, maybe make specific ones for each task e.g. topicRequirements.txt, commentRequirements.txt, etc?
- Add comparison approaches for commentModeling
- Train init. bert model on either sampled data, or on 'full' training data with class weights
- Maybe try both approaches above, compare metrics?  Costly and time consuming though.
- After best approach is decided for commentModeling, create the .py file(s) for future use
- Refine topicModeling for better topics.  Run for each of our categories to get topic models by category
- Figure out issue with plotting best_model in topicModeling LDAvis
# Sephora Review Dashboard

## Recent Updates
12/28/23: In order to get our json to load I had to shrink our dataset to only include entries from March 2022 to March 2023 (Mar 2023 are the most recent entries in the dataset). The good news is you guys should be able to open up `app.js` and be able to test your code and `console.log` the information using live server on the `index.html` file. For reference: `oneyear_df.json` is the name of the file, but it's already coded into `app.js`.

Some things to be aware of:
- Even shrunk down this file is still pretty big (137mb to be exact) and, as such it takes a few minutes to load - so be patient when loading it and avoid refreshing when you get antsy.
- I'm personally hosting this on AWS, and the way it works I have to pay if the number of requests that are made to it goes over a certain data threshold. Since this file is still pretty sizeable, try to avoid refreshing it constantly so it doesn't constantly make api calls.
  - I'm not policing this and I don't understand it well enough to work around it, but I'm also aware that we have work that needs to be done, so just try your best to not refresh it habitually. If you have to refresh it because it stops loading or you updated something and need to see it in action it's totally fine, I just want everyone to be aware that it's a thing.

12/19/23: I uploaded the resources, starter code, and some files that we'll need to develop later on. Please make sure you all create a branch on the github and always pull from main before beginning to work on anything to avoid issues with staying up to date on commits. Always upload to your own branch so the changes can be checked over first when pull requests are made.

To pull from main before working on files:

`git pull origin main`


To create a new branch use the following, filling in what you want to call it after the -b:

`git checkout -b thenameofyourbranch`

To push your files to your branch, use the following, filling in whatever you named your branch:

`git push -u origin thenameofyourbranch`

**Some notes about the files:**
- In `reviews.ipynb` I already created a merged_df variable if you want to get started experimenting with the dataset, nothing is cleaned up yet though.
- Feel free to unzip the `reviews_all.zip` file if you want to look at the csvs, but don't push any of them to the github - they are too large for it.
- I coded `reviews.ipynb` with some modules that allow us to extract the zipped resources folder and then delete them automatically to avoid having them pushed to the repository later.
  - This is really important. Basically make sure if you use `reviews.ipynb` to play around with the dataset, make sure you always run the first four cells to avoid hanging on to these csv files when you try to save your work later on.


## Project Proposal

## Overview
The goal of this project is to do a study on 5 popular brands (Tatcha, Nars, Dior, Huda Beauty, Laneige) on Sephora and analyze their reviews to learn about their products

Questions:
1. What do the reviews tell the consumer about the products?
  - Wordcloud, ingredients, keywords, etc.
2. How does the price correlate to the rating?
3. How does the number of reviews affect the rating?


## Objectives
1. Analyze the content of the reviews to highlight key words
2. Compare results across the most popular brands
3. Discover a correlation between review frequency and rating/price


## Data Cleanup
- **Translation API**: Some reviews are in French and will need to be translated to English in order to integrate with the Wordcloud
- **Apostrophes and Accent Marks**: Many reviews utilize characters that do not translate well from code to plaintext
- **Merging**: product_info.csv will need the primary_category column merged by product_id

## Data Sources and Collection
Data for this project was sourced from https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews by Nady Inky. The Wordcloud libray implentation was sourced from https://github.com/amueller/word_cloud.

## Key Features
1. Dropdown the select aggregations by product type
2. Hovertext to show product information of the item

## Technology Stack and Implementation
- **Frontend**: JavaScript, CSS, HTML
- **Backend**:
- **Database**: postgresQL
- **Data Processing**: Python, Pandas, Jupyter
- **Hosting**: Github


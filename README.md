# Sephora Review Dashboard
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


CREATE TABLE reviews_db (
	product_id TEXT NOT NULL,
	product_name TEXT NOT NULL,
	brand_name TEXT NOT NULL,
	price_usd REAL NOT NULL,
	rating INT NOT NULL,
	is_recommended REAL,
	helpfulness REAL,
	total_feedback_count INT,
	total_neg_feedback_count INT,
	total_pos_feedback_count INT,
	review_text TEXT,
	review_title TEXT,
	submission_time TIMESTAMP NOT NULL
);
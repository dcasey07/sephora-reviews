import numpy as np
import math
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, request, jsonify
from flask_cors import CORS

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/reviews.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Reviews = Base.classes.reviews

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/catbranddropdown"
        f"/api/v1.0/textwordcloud<br/>"
        f"/api/v1.0/titlewordcloud<br/>"
        f"/api/v1.0/positivenegative<br/>"
        f"/api/v1.0/reviewbydate<br/>"
        f"/api/v1.0/productrating<br/>"
        f"/api/v1.0/valuescore<br/>"
        f"/api/v1.0/valuescorenormalized"
    )

@app.route("/api/v1.0/catbranddropdown")
def catbranddropdown():
    session = Session(engine)

    # Query to get unique categories
    categories = session.query(Reviews.secondary_category).distinct().all()
    categories = [category[0] for category in categories]

    # Query to get unique brands
    brands = session.query(Reviews.brand_name).distinct().all()
    brands = [brand[0] for brand in brands]

    session.close()

    return jsonify({'categories': categories, 'brands': brands})

    
@app.route("/api/v1.0/textwordcloud")
def textwordcloud():
    session = Session(engine)

    # Get query parameters
    secondary_category = request.args.get('secondary_category', type=str)
    brand_name = request.args.get('brand_name', type=str)

    # Print for debugging
    print(f"Debug parameters: secondary_category={secondary_category}, brand_name={brand_name}")

    # Query the text from the body of the reviews
    try:
        query = session.query(Reviews.review_text)

        # Apply dropdown filtering
        if secondary_category:
            query = query.filter(Reviews.secondary_category == secondary_category)
        if brand_name:
            query = query.filter(Reviews.brand_name == brand_name)
        
        # Print for debugging
        print(f"Debug query: {query}")

        results = query.all()
    # Exception for debugging    
    except Exception as e:
        session.close()
        print(f"Error: {e}")
        return jsonify({"error": str(e)})


    # Convert to list of dictionaries
    all_texts = [{"review_text": text} for text in np.ravel(results)]
    return jsonify(all_texts)

@app.route("/api/v1.0/titlewordcloud")
def titlewordcloud():
    session = Session(engine)

    # Get query parameters
    secondary_category = request.args.get('secondary_category', type=str)
    brand_name = request.args.get('brand_name', type=str)

    # Print for debugging
    print(f"Received parameters: secondary_category={secondary_category}, brand_name={brand_name}")

    # Query the text from the review headers
    try:
        query = session.query(Reviews.review_title)

        # Apply dropdown filtering
        if secondary_category:
            query = query.filter(Reviews.secondary_category == secondary_category)
        if brand_name:
            query = query.filter(Reviews.brand_name == brand_name)

        # Print for debugging
        print(f"Debug query: {query}")

        results = query.all()
    # Exception for debugging        
    except Exception as e:
        session.close()
        print(f"Error: {e}")
        return jsonify({"error": str(e)})

    session.close()

    # Convert to list of dictionaries
    all_titles = [{"review_title": title} for title in np.ravel(results)]
    return jsonify(all_titles)



@app.route("/api/v1.0/positivenegative")
def positivenegative():
    session = Session(engine)

    # Get query parameters
    secondary_category = request.args.get('secondary_category', type=str)
    brand_name = request.args.get('brand_name', type=str)

    # Query and group by product_name and sum the positive and negative feedback counts
    try:        
        query = session.query(
            Reviews.product_name,
            Reviews.brand_name, 
            func.sum(Reviews.total_pos_feedback_count).label("total_positive_feedback"),
            func.sum(Reviews.total_neg_feedback_count).label("total_negative_feedback")
        ).group_by(Reviews.product_name)

        # Apply dropdown filtering
        if brand_name:
            query = query.filter(Reviews.brand_name == brand_name)
        if secondary_category:
            query = query.filter(Reviews.secondary_category == secondary_category)

        results = query.all()

    # Exception for debugging
    except Exception as e:
        session.close()
        return jsonify({"error": str(e)})

    session.close()

    # Convert to list of dictionaries
    feedback_data = [{"product_name": name, "brand_name": brand, "total_positive_feedback": pos, "total_negative_feedback": neg} for name, brand, pos, neg in results]
    return jsonify(feedback_data)

@app.route("/api/v1.0/productrating")
def productrating():
    session = Session(engine)

    # Get query parameters
    secondary_category = request.args.get('secondary_category', type=str)
    brand_name = request.args.get('brand_name', type=str)

    # Query and group the avg rating and review count per product
    try:
        query = session.query(
            Reviews.product_name, 
            func.avg(Reviews.rating).label("average_rating"),
            func.count(Reviews.index).label("review_count")
        ).group_by(Reviews.product_name)

        # Apply dropdown filtering
        if brand_name:
            query = query.filter(Reviews.brand_name == brand_name)
        if secondary_category:
            query = query.filter(Reviews.secondary_category == secondary_category)

        # Order by average rating in descending order
        query = query.order_by(func.avg(Reviews.rating).desc())

        # Execute the query
        results = query.all()

    # Exception for debugging    
    except Exception as e:
        session.close()
        return jsonify({"error": str(e)})

    session.close()

    # Convert to list of dictionaries
    rating_data = [{"product_name": name, "average_rating": avg_rating, "review_count": count} for name, avg_rating, count in results]
    return jsonify(rating_data)

@app.route("/api/v1.0/valuescore")
def valuescore():
    session = Session(engine)

    # Get query parameters
    secondary_category = request.args.get('secondary_category', type=str)
    brand_name = request.args.get('brand_name', type=str)

    # Query and group the avg rating and review count along with the price, name, and brand per product
    try:
        query = session.query(
            Reviews.product_name,
            Reviews.brand_name,
            func.avg(Reviews.rating).label("average_rating"),
            func.count(Reviews.index).label("review_count"),
            Reviews.price_usd
        ).group_by(Reviews.product_name, Reviews.brand_name)

        # Apply dropdown filtering
        if brand_name:
            query = query.filter(Reviews.brand_name == brand_name)
        if secondary_category:
            query = query.filter(Reviews.secondary_category == secondary_category)

        results = query.all()

    # Exception for debugging     
    except Exception as e:
        session.close()
        return jsonify({"error": str(e)})

    session.close()

    # List to store and append values
    value_score_data = []
    for name, brand, avg_rating, count, price in results:
        # Account for division by zero
        if price == 0:
            continue

        # Use logarithm to smooth the review count impact
        log_review_count = math.log1p(count)
        # Calculation with all variables
        value_score = (avg_rating * log_review_count) / price

        value_score_data.append({
            "product_name": name,
            "brand_name": brand,
            "average_rating": avg_rating,
            "review_count": count,
            "price_usd": round(price, 2),
            "value_score": value_score
        })

    # Sort the results by value score in descending order
    value_score_data.sort(key=lambda x: x['value_score'], reverse=True)

    return jsonify(value_score_data)

@app.route("/api/v1.0/rating_vs_price")
def rating_vs_price():
    session = Session(engine)

    # Get query parameters
    secondary_category = request.args.get('secondary_category', type=str)
    brand_name = request.args.get('brand_name', type=str)

    # Query of avg price, total review count per product, and item brand/name
    try:
        query = session.query(
            Reviews.product_name,
            Reviews.brand_name,
            func.avg(Reviews.rating).label("average_rating"),
            func.count(Reviews.index).label("review_count"),
            Reviews.price_usd
        ).group_by(Reviews.product_name, Reviews.brand_name, Reviews.price_usd)

        # Apply dropdown filtering
        if brand_name:
            query = query.filter(Reviews.brand_name == brand_name)
        if secondary_category:
            query = query.filter(Reviews.secondary_category == secondary_category)

        results = query.all()

    # Exception for debugging
    except Exception as e:
        session.close()
        return jsonify({"error": str(e)})

    session.close()

    # Convert to list of dictionaries
    rating_price_data = [
        {
            "product_name": name,
            "brand_name": brand,
            "average_rating": avg_rating,
            "review_count": review_count,
            "price_usd": price
        }
        for name, brand, avg_rating, review_count, price in results
    ]

    return jsonify(rating_price_data)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from model import recommend_ads
from flask_sqlalchemy import SQLAlchemy


# Initializing Flask app
app = Flask(__name__)

# static files
app.static_folder = 'static'


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ads.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initializing with sqlite database
db = SQLAlchemy(app)


# SQLAlchemy model
class Ad(db.Model):
    __tablename__ = 'ad_analytics'

    DailyTimeSpentOnSite = db.Column(db.Float, nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    AreaIncome = db.Column(db.Float, nullable=False)
    DailyInternetUsage = db.Column(db.Float, nullable=False)
    AdTopicLine = db.Column(db.String(255), nullable=False, primary_key=True)
    City = db.Column(db.String(120), nullable=False)
    Male = db.Column(db.Boolean, nullable=False)
    Country = db.Column(db.String(120), nullable=False)
    Timestamp = db.Column(db.DateTime, nullable=False)
    ClickedOnAd = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "DailyTimeSpentOnSite": self.DailyTimeSpentOnSite,
            "Age": self.Age,
            "AreaIncome": self.AreaIncome,
            "DailyInternetUsage": self.DailyInternetUsage,
            "AdTopicLine": self.AdTopicLine,
            "City": self.City,
            "Male": self.Male,
            "Country": self.Country,
            "Timestamp": self.Timestamp.isoformat() if self.Timestamp else None,  # Format datetime
            "ClickedOnAd": self.ClickedOnAd
        }


@app.route('/recommend', methods=['POST'])
def recommend():
    body = request.json
    print("body", body)
    recommended_ads = {"ads": recommend_ads(body, 5)}
    print(recommended_ads)
    return jsonify(recommended_ads)


@app.route('/sample-advertisements', methods=['GET'])
def sample_advertisement():
    from db import get_sample_advertisements
    advertisements = get_sample_advertisements()
    recommended_ads = {"ads": advertisements}
    return jsonify(recommended_ads)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ads', methods=['GET'])
def get_all_ads():
    try:
        ads = Ad.query.all()  # Fetch all records
        print(ads)
        ads_list = [ad.to_dict() for ad in ads]  # Convert to dictionary
        return jsonify({"success": True, "data": ads_list}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':

    app.run(debug=True, port=5001)

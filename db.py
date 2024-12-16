from app import Ad, db
import pandas as pd

# Load the dataset
data = pd.read_csv('advertising.csv')


def get_user_ads(user_id):
    return db.session.query(Ad).filter(Ad.user_id == user_id).all()


# def get_sample_advertisements():
#     return db.session.query(Ad).limit(10).all()


def get_sample_advertisements():
    return data.sample(10).to_dict(orient='records')

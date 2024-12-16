import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier

DATA_PATH = 'user_2.csv'

# Load the dataset of the first 300 to 500 rows
data = pd.read_csv(DATA_PATH)

# Data Cleaning / scraping
data.dropna(inplace=True)

# Encoding the categorical variables
label_encoders = {}
for column in ['City', 'Country', 'Ad Topic Line']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

column_list = ['Daily Time Spent on Site', 'Age', 'Area Income',
               'Daily Internet Usage', 'City', 'Country', 'Male', 'Ad Topic Line']

# Split the data into features and labels
X = data[column_list]  # Features
y = data['Clicked on Ad']  # Labels (1 if clicked, 0 otherwise)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Initialize model

# model = DecisionTreeClassifier() Accuracy: 90.5%
model = GradientBoostingClassifier()

# Train model
model.fit(X_train, y_train)
print('Fitting model:', X_train.shape, y_train.shape)

# Make predictions for user data
y_pred = model.predict(X_test)
print('Predictions:', X_test.shape, y_pred.shape)


# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Trained. Accuracy: {accuracy*100:.2f}%')


# function to get user features
def get_user_features(user_data=None):
    try:
        if user_data is None:
            user_data = pd.read_csv(DATA_PATH).sample(10)
        else:
            user_data = {
                'Ad Topic Line': [user_data['Ad Topic Line']],
                'Age': [user_data['Age']],
                'Area Income': [user_data['Area Income']],
                'City': [user_data['City']],
                'Clicked on Ad': [user_data['Clicked on Ad']],
                'Country': [user_data['Country']],
                'Daily Internet Usage': [user_data['Daily Internet Usage']],
                'Daily Time Spent on Site': [user_data['Daily Time Spent on Site']],
                'Male': [user_data['Male']],
                'Timestamp': [user_data['Timestamp']]
            }
        # Create a DataFrame for the user body json
        user_data = pd.DataFrame(user_data)

        # append the user data to the original data
        data = pd.read_csv(DATA_PATH)
        user_data = pd.concat([data, user_data])

        # Data Cleaning / scraping
        user_data.dropna(inplace=True)

        # Encoding the categorical variables
        label_encoders = {}
        for column in ['City', 'Country', 'Ad Topic Line']:
            le = LabelEncoder()
            user_data[column] = le.fit_transform(user_data[column])
            label_encoders[column] = le

        user_data = user_data[column_list]
        # user_data = pd.concat([data, user_data])

        # take 5 random rows
        return user_data
    except Exception as e:
        print('\ERROR while getting user features:', e, "\n")
        return []


# Function to recommend ads based on user features


def recommend_ads(user_data, num_recommendations=5):
    try:
        # Create a DataFrame for the user
        user_features = get_user_features(user_data)
        processed_data = pd.concat([user_features, pd.DataFrame(X)], axis=1)

        # Predict whether the user would click on each ad
        probabilities = model.predict_proba(user_features)
        print('Probabilities:', probabilities)
        probabilities = probabilities[:, 1]

        # Get ads that the model predicts the user would click
        recommended_ads = user_features
        recommended_ads['Probabilities'] = probabilities

        # convert LE to original values
        for column in ['City', 'Country', 'Ad Topic Line']:
            recommended_ads[column] = label_encoders[column].inverse_transform(
                recommended_ads[column])

        # Sort the ads by the probability of the user clicking on them
        recommended_ads = recommended_ads.sort_values(
            by='Probabilities', ascending=False)

        # Get the top 5 recommended ads
        recommended_ads = recommended_ads.head(num_recommendations)
        return recommended_ads.to_dict(orient='records')

    except Exception as e:
        print('\ERROR while recommending ads:', e, "\n")
        return []


# results = recommend_ads(10, 10)

# print("Results:\n", results)

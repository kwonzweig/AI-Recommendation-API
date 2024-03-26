import os

import pandas as pd
from keras.src.saving import load_model

# Load the necessary data
item_encoder = pd.read_pickle(os.path.join('src', 'ml_models', 'item_encoder.pkl'))
model = load_model(os.path.join('src', 'ml_models', 'recommendation_model.keras'))


def make_recommendations(user_id: int, design_idea: pd.Series, n_recommendations=5):

    # user_id to array
    user_id_array = pd.Series(user_id).repeat(len(design_idea))

    # Encode design idea
    design_idea_array = item_encoder.transform(design_idea)

    predictions = model.predict([user_id_array, design_idea_array]).flatten()

    # Get the top-n highest-rated items for this user
    top_items_indices = predictions.argsort()[-n_recommendations:][::-1]
    top_items_encoded = item_encoder.inverse_transform(top_items_indices)

    return top_items_encoded


if __name__ == "__main__":
    test_data = pd.read_csv(os.path.join(os.path.join('src', 'ml_models', 'user_data.csv')))

    # Select a random user ID
    test_user_id = test_data['USER_ID'].sample().values[0]

    # Filter the test data for the selected user
    user_data = test_data[test_data['USER_ID'] == test_user_id]

    recommendations = make_recommendations(test_user_id, user_data['DESIGN_IDEA'], n_recommendations=5)
    print(f"Top design idea recommendations for user {test_user_id}: {recommendations}")

    # Print the test data for comparison
    print(user_data)

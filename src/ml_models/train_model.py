import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras

from src.snowflake_query import query_snowflake


def preprocess_data(df: pd.DataFrame):
    # Encode USER_ID and DESIGN_IDEA as integer indices for embedding layers
    user_encoder = LabelEncoder()
    item_encoder = LabelEncoder()

    df['USER_ID'] = user_encoder.fit_transform(df['USER_ID'])
    df['DESIGN_IDEA'] = item_encoder.fit_transform(df['DESIGN_IDEA'])

    # Assuming ENGAGEMENT_LEVEL is categorical and converting it to numerical
    engagement_mapping = {
        'Very Low Engagement': 0,
        'Low Engagement': 1,
        'Moderate Engagement': 2,
        'High Engagement': 3
    }
    df['ENGAGEMENT_LEVEL'] = df['ENGAGEMENT_LEVEL'].map(engagement_mapping)

    X = df[['USER_ID', 'DESIGN_IDEA']].values
    y = df['ENGAGEMENT_LEVEL'].values

    return X, y, user_encoder, item_encoder


def split_data(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=42)


def build_model(num_users, num_items, embedding_size=50):
    user_input = keras.layers.Input(shape=(1,), name='user_input')
    user_embedding = keras.layers.Embedding(num_users, embedding_size, name='user_embedding')(user_input)
    user_vec = keras.layers.Flatten(name='user_flatten')(user_embedding)

    item_input = keras.layers.Input(shape=(1,), name='item_input')
    item_embedding = keras.layers.Embedding(num_items, embedding_size, name='item_embedding')(item_input)
    item_vec = keras.layers.Flatten(name='item_flatten')(item_embedding)

    concat = keras.layers.Concatenate()([user_vec, item_vec])
    dense = keras.layers.Dense(128, activation='relu')(concat)
    predictions = keras.layers.Dense(1, activation='linear')(dense)

    model = keras.Model(inputs=[user_input, item_input], outputs=predictions)
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def train_and_evaluate(model, X_train, X_test, y_train, y_test):
    model.fit([X_train[:, 0], X_train[:, 1]], y_train, epochs=10, validation_split=0.1)
    model.evaluate([X_test[:, 0], X_test[:, 1]], y_test)


def plot_actual_vs_predicted(X_test, y_test, model):
    # Predict the engagement levels using the model
    predictions = model.predict([X_test[:, 0], X_test[:, 1]]).flatten()

    # Plotting actual vs predicted engagement levels
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, predictions, alpha=0.5)
    plt.title('Actual vs. Predicted Engagement Levels')
    plt.xlabel('Actual Engagement Levels')
    plt.ylabel('Predicted Engagement Levels')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    plt.grid(True)
    plt.show()


def calculate_metrics(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"Mean Absolute Error: {mae}")


def export_encoders(user_encoder, item_encoder):
    with open('user_encoder.pkl', 'wb') as f:
        pickle.dump(user_encoder, f)
    with open('item_encoder.pkl', 'wb') as f:
        pickle.dump(item_encoder, f)


def main():
    # Query Snowflake and get the result as a DataFrame
    query = """
    SELECT
        DATA:UserID::INT AS USER_ID,
        DATA:UserActivity:"Design Idea"::STRING AS DESIGN_IDEA,
        DATA:UserActivity:"Engagement Level"::STRING AS ENGAGEMENT_LEVEL
    FROM
        MY_TABLE LIMIT;
    """

    df = query_snowflake(query)

    # Export the df to a CSV file
    df.to_csv('user_data.csv', index=False)

    # Preprocess data
    X, y, user_encoder, item_encoder = preprocess_data(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Build the model
    num_users = len(np.unique(X[:, 0]))
    num_items = len(np.unique(X[:, 1]))
    model = build_model(num_users, num_items)

    # Train and evaluate the model
    train_and_evaluate(model, X_train, X_test, y_train, y_test)
    model.save('recommendation_model.keras')

    # Export encoders
    export_encoders(user_encoder, item_encoder)

    # Calculate metrics
    predictions = model.predict([X_test[:, 0], X_test[:, 1]]).flatten()
    calculate_metrics(y_test, predictions)

    # Export test data to CSV
    test_data = pd.DataFrame({'USER_ID': X_test[:, 0], 'DESIGN_IDEA': X_test[:, 1], 'ENGAGEMENT_LEVEL': y_test})
    test_data.to_csv('test_data.csv', index=False)


if __name__ == '__main__':
    main()

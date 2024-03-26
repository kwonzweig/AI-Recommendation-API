
# AI Recommendation API Deployment Template

This project is a demo AI recommendation API, template for deploying such a system using FastAPI, Docker, and Kubernetes, integrated with a Snowflake data pipeline. 

### Technology Selection and Rationale

- **FastAPI**: Chosen for its performance, ease of use, and automatic Swagger documentation for building RESTful APIs.
- **Docker**: Facilitates consistent development environments and simplifies deployment.
- **Kubernetes**: Selected for its robust scaling and management capabilities.
- **Snowflake**: Offers a cloud-based data warehouse solution that can handle semi-structured data.
- **TensorFlow & Keras**: Selected to train the recommendation model using deep learning with user and design item history to predict user engagement level for pairs of user&item.
- **Recommendation Algorithm**: Provide personalized recommendations based on user's historical design idea usages and provide top n number of design ideas with high user engagement level predicted.

### Dataset Overview

- **Number of unique "User ID"**: 11,350
- **Number of unique "Design Ideas"**: 3,600
- **Types of "User Engagement"**: High, Medium, Low, Very Low

### Training result: 
```
Mean Squared Error: 1.18
Mean Absolute Error: 0.88
```
- Baseline model can be built to compare the performance of the recommendation model.
- Domain Expertise can be used to evaluate the model performance.
- Hyperparameter tuning can be done to improve the model performance.


## API Usage Example

The API allows clients to request recommendations for users based on design ideas. Here's an example of how to make a request and the expected response:

### Request

POST `/recommend/{user_id}`

```json
{
  "design_idea": ["Design Idea 690", "Design Idea 696", "Design Idea 517", "Design Idea 1187"],
  "num_recommendations": 5
}
```

### Response

```json
{
  "user_id": 86466985,
  "recommendations": ['Design Idea 100' 'Design Idea 1' 'Design Idea 1002' 'Design Idea 1004'
 'Design Idea 1003']
}
```

This example demonstrates how to interact with the API to obtain personalized recommendations based on the user's preferences and history.


## Conclusion

- Pros
  - We can easily deploy this scalable AI recommendation API providing personalized suggestions for existing users and design ideas.

- Cons
  - Requires retraining for new users or new design ideas. (Cold Start Problem)


- Solutions to Cold Start Problem:
  - Fallback Mechanism
    - Use a fallback mechanism to provide recommendations for new users or design ideas.
    - Still requires frequent retraining.
  - Hybrid Approach (Collaborative Filtering with Content-based Filtering)
    - Allows the system to make recommendations based on item characteristics or user demographics in addition to interaction data.
    - Requires feature data for users and items

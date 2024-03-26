Prepared mock data in semi-structured (JSON) format:

```
[
    {
      'UserID': 151603712,
      'UserActivity': {
        'Design Idea': 'Design Idea 1',
        'Engagement Level': 'High Engagement'
      }
    }
    ...
    {
      'UserID': 128470551,
      'UserActivity': {
        'Design Idea': 'Design Idea 302',
        'Engagement Level': 'Very Low Engagement'
      }
    }
]

```

This is stored at SnowFlake (snowflake.sql to set up for the first run)


## Recommendation Method

Neural Network based recommendation to predict the engagement level of a user with a design idea.

- Number of unique users: 11,350
- Number of unique Design Ideas: 3,600
- Types of User Engagement: High, Medium, Low, Very Low
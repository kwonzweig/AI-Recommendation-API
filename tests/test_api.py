import pytest
from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


# Test function using pytest
@pytest.mark.parametrize("user_id, design_idea, num_recommendations", [
    (123456, ['Design Idea 1', 'Design Idea 2'], 5),  # Hardcoded values for testing
])
def test_get_recommendations(user_id, design_idea, num_recommendations):
    response = client.post(f"/recommend/{user_id}",
                           json={"design_idea": design_idea, "num_recommendations": num_recommendations})
    print(response.json())
    assert response.status_code == 200
    assert "recommendations" in response.json()


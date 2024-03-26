import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.ml_models.predict import make_recommendations

app = FastAPI()


class RecommendationRequest(BaseModel):
    design_idea: list
    num_recommendations: int = 5


@app.post("/recommend/{user_id}")
async def get_recommendations(user_id: int, request: RecommendationRequest):
    try:
        recommendations = make_recommendations(user_id, pd.Series(request.design_idea), request.num_recommendations)
        return {"user_id": user_id, "recommendations": list(recommendations)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, )

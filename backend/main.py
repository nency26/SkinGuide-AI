import uvicorn
import sys
import os
import __main__

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.schemas import QuizRequest, RecommendationResponse
from recommendation_models.recommend import generate_recommendations
from recommendation_models.vectorizer import (
    custom_ingredient_tokenizer,
    load_artifacts
)

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

__main__.custom_ingredient_tokenizer = custom_ingredient_tokenizer

app = FastAPI(
    title="SkinGuide AI API",
    description="AI-powered skincare recommendation engine",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_check():
    try:
        load_artifacts()
        print("[SUCCESS] ML artifacts loaded.")
    except Exception as e:
        print(f"[ERROR] ML startup validation failed: {e}")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SkinGuide-AI"
    }


@app.post(
    "/api/v1/recommend",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK
)
async def get_skin_recommendations(payload: QuizRequest):

    if not payload.primary_feeling.strip():
        raise HTTPException(
            status_code=400,
            detail="Primary skin feeling cannot be empty."
        )

    try:
        result = generate_recommendations(
            feeling=payload.primary_feeling,
            concerns=payload.concerns,
            category_filters=payload.preferred_categories,
            country_filters=payload.preferred_countries
        )

        return RecommendationResponse(
            classified_skin_type=result.get(
                "classified_skin_type",
                "Unknown"
            ),
            target_ingredients=result.get(
                "target_ingredients",
                []
            ),
            recommendations=result.get(
                "recommendations",
                []
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation Engine Error: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
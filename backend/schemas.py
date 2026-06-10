from pydantic import BaseModel, Field
from typing import List, Optional

class QuizRequest(BaseModel):
    primary_feeling: str = Field(..., description="User's primary skin feeling.")
    concerns: List[str] = Field(default=[], description="List of target skin concerns.")
    preferred_categories: Optional[List[str]] = Field(default=None, description="Preferred product types.")
    preferred_countries: Optional[List[str]] = Field(default=None, description="Preferred country of origin.")

class ProductRecommendation(BaseModel):
    id: Optional[int] = None      
    product_name: str
    brand: str
    product_type: str
    country: Optional[str] = None
    tags: Optional[str] = None       
    ingredients: str
    match_score: float

class RecommendationResponse(BaseModel):
    classified_skin_type: str
    target_ingredients: List[str]
    recommendations: List[ProductRecommendation]
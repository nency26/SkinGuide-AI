# ✨ SkinGuide AI - Intelligent Skincare Recommendation System

## Overview

**SkinGuide AI** is an AI-powered skincare recommendation platform that analyzes a user's skin profile, concerns, and preferences to provide personalized skincare product recommendations.

The system combines:

* Machine Learning based ingredient matching
* Skin type classification
* Rule-based skincare intelligence
* Product recommendation engine
* FastAPI backend
* Streamlit frontend

The goal is to help users discover skincare products that are better suited to their skin type and concerns using data-driven recommendations.

---

# System Architecture

```text
┌──────────────────────────────────────────────┐
│                 Frontend                     │
│              Streamlit App                   │
│                                              │
│  • Skin Assessment Quiz                      │
│  • Product Preferences                       │
│  • Recommendation Dashboard                  │
│  • Product Explorer                          │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│              FastAPI Backend                 │
│                                              │
│  • API Endpoints                             │
│  • Recommendation Service                    │
│  • Request Validation                        │
│  • Business Logic                            │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│             Machine Learning Layer           │
│                                              │
│  • TF-IDF Vectorizer                         │
│  • Cosine Similarity Engine                  │
│  • Ingredient Matching                       │
│  • Skin Type Classification                  │
│  • Recommendation Ranking                    │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│                 Database                     │
│                                              │
│  • Product Dataset                           │
│  • Ingredients                               │
│  • Product Categories                        │
│  • Countries                                 │
│  • Tags & Benefits                           │
└──────────────────────────────────────────────┘
```

---

# Key Features

## AI Skin Analysis

The system identifies:

* Oily Skin
* Dry Skin
* Combination Skin
* Sensitive Skin
* Acne-Prone Skin

based on user responses and symptom analysis.

---

## Ingredient Intelligence

The recommendation engine focuses on ingredients that are scientifically associated with specific skin concerns.

Examples:

| Concern           | Recommended Ingredients                    |
| ----------------- | ------------------------------------------ |
| Acne              | Salicylic Acid, Benzoyl Peroxide, Tea Tree |
| Oily Skin         | Niacinamide, Zinc PCA                      |
| Hyperpigmentation | Vitamin C, Tranexamic Acid, Alpha Arbutin  |
| Redness           | Centella Asiatica                          |
| Aging             | Retinol, Peptides, Vitamin C               |

---

## Personalized Recommendations

Recommendations are generated using:

### 1. Ingredient Matching

Products containing beneficial ingredients receive higher scores.

### 2. Similarity Search

TF-IDF Vectorization + Cosine Similarity is used to match user needs with product ingredients.

### 3. Skin-Type Filtering

Products unsuitable for the detected skin type are filtered out.

### 4. Product Preferences

Users can filter recommendations by:

* Product Category
* Country of Origin

---

## Interactive Dashboard

The Streamlit application provides:

* Skin Analysis Form
* Product Filters
* Recommendation Dashboard
* Ingredient Insights
* Product Match Scores

---

# Technology Stack

## Frontend

* Streamlit

## Backend

* FastAPI
* Pydantic

## Machine Learning

* Scikit-Learn
* TF-IDF Vectorizer
* Cosine Similarity

## Data Processing

* Pandas
* NumPy

## Database

* SQLite

---

# Project Structure

```text
SkinGuide-AI/
│
├── frontend/
│   └── app.py
│
├── backend/
│   ├── main.py
│   └── schemas.py
│
├── database/
│   ├── connection.py
│   ├── schema.sql
│   └── data_ingest.py
│
├── recommendation_models/
│   ├── recommend.py
│   ├── vectorizer.py
│   ├── skin_types.py
│   └── pickled_models/
│       ├── vectorizer.pkl
│       └── product_matrix.pkl
│
├── data/
│   ├── processed/
│   │    └── skincare.db
│   └── raw/
│       ├── beauty_data.csv
│       ├── data.csv
│       └── datasheet.csv
│
├── requirements.txt
└── README.md
```

---

# Machine Learning Pipeline

## Data Preparation

Product information is extracted from the skincare dataset:

* Product Name
* Brand
* Ingredients
* Tags
* Country
* Product Type

---

## Vectorization

Ingredients are converted into numerical representations using:

```python
TfidfVectorizer()
```

The vectorizer learns ingredient relationships across all products.

---

## Recommendation Generation

User concerns are converted into:

```text
Target Ingredients
        ↓
TF-IDF Vector
        ↓
Cosine Similarity
        ↓
Ingredient Bonus
        ↓
Final Ranking Score
```

Products are ranked according to relevance.

---

# API Endpoints

## Generate Recommendations

```http
POST /api/v1/recommend
```

### Request

```json
{
  "primary_feeling": "Shiny all over, greasy, or prone to breakouts everywhere",
  "concerns": [
    "Active Acne",
    "Large Pores"
  ],
  "preferred_categories": [
    "Serum"
  ],
  "preferred_countries": [
    "South Korea"
  ]
}
```

### Response

```json
{
  "classified_skin_type": "Oily",
  "target_ingredients": [
    "salicylic acid",
    "niacinamide"
  ],
  "recommendations": [
    {
      "product_name": "Spot The Difference Blemish Treatment",
      "brand": "AXIS-Y",
      "match_score": 1.0
    }
  ]
}
```

---

# Example Workflow

### Step 1

Complete the skin assessment questionnaire.

### Step 2

Select:

* Skin concerns
* Product categories
* Country preferences

### Step 3

The system:

* Detects skin type
* Identifies target ingredients
* Generates recommendations

### Step 4

View ranked skincare products with:

* Match Score
* Benefits
* Ingredients
* Product Information

---

# Future Improvements

* Product image support
* Deep learning recommendation models
* User accounts and profiles
* Recommendation history
* Skin routine generator
* Ingredient safety checker
* Dermatologist recommendation mode
* Mobile application
* Cloud deployment

---

# Learning Outcomes

This project demonstrates practical implementation of:

* Recommendation Systems
* Information Retrieval
* TF-IDF Vectorization
* Cosine Similarity
* FastAPI Development
* Streamlit Development
* Machine Learning Pipelines
* Data Processing with Pandas
* Full Stack AI Applications

---

# Author

**Nency Khunt**

B.Tech Information Technology Student

Passionate about:

* Artificial Intelligence
* Machine Learning
* Recommendation Systems
* Full Stack Development

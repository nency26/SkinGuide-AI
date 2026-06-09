import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from recommendation_models.skin_types import (
    SKIN_TYPES,
    determine_skin_profile
)

from recommendation_models.vectorizer import load_artifacts
from database.connection import fetch_all_products


PRODUCT_PREFERENCES = {
    "Acne-Prone": [
        "cleanser",
        "serum",
        "spot treatment"
    ],

    "Dry": [
        "cream",
        "moisturizer",
        "sleeping mask"
    ],

    "Oily": [
        "gel moisturizer",
        "serum",
        "cleanser"
    ]
}


def build_target_ingredients(primary_type, secondary_concerns):

    ingredients = {}

    for ingredient, weight in \
            SKIN_TYPES[primary_type]["target_ingredients"].items():

        ingredients[ingredient] = weight

    for concern in secondary_concerns:

        if concern not in SKIN_TYPES:
            continue

        for ingredient, weight in \
                SKIN_TYPES[concern]["target_ingredients"].items():

            ingredients[ingredient] = max(
                ingredients.get(ingredient, 0),
                weight
            )

    return ingredients


def generate_recommendations(
    feeling,
    concerns,
    category_filters=None,
    country_filters=None,
    top_n=5
):

    profile = determine_skin_profile(
        feeling,
        concerns
    )

    primary_type = profile["primary_skin_type"]
    secondary = profile["secondary_concerns"]

    target_ingredients = build_target_ingredients(
        primary_type,
        secondary
    )

    products = fetch_all_products()

    if not products:
        return {
            "classified_skin_type": primary_type,
            "target_ingredients": list(target_ingredients.keys()),
            "recommendations": []
        }

    df = pd.DataFrame(products)

    vectorizer, product_matrix = load_artifacts()

    target_string = ", ".join(
        target_ingredients.keys()
    )

    user_vector = vectorizer.transform(
        [target_string]
    )

    similarity_scores = cosine_similarity(
        user_vector,
        product_matrix
    ).flatten()

    df["similarity_score"] = similarity_scores

    def ingredient_bonus(ingredients_text):

        score = 0

        text = str(
            ingredients_text
        ).lower()

        for ingredient, weight in \
                target_ingredients.items():

            if ingredient.lower() in text:
                score += weight

        return score

    df["ingredient_bonus"] = (
        df["ingredients"]
        .apply(ingredient_bonus)
    )

    df["final_score"] = (
        df["similarity_score"] * 0.7
        + df["ingredient_bonus"] * 0.3
    )

    avoid_tags = []

    avoid_tags.extend(
        SKIN_TYPES[primary_type]["avoid_tags"]
    )

    for concern in secondary:

        if concern in SKIN_TYPES:
            avoid_tags.extend(
                SKIN_TYPES[concern]["avoid_tags"]
            )

    def contains_bad_tag(tags):

        if pd.isna(tags):
            return False

        tags = str(tags).lower()

        return any(
            bad.lower() in tags
            for bad in avoid_tags
        )

    df = df[
        ~df["tags"].apply(
            contains_bad_tag
        )
    ]

    preferred_types = PRODUCT_PREFERENCES.get(
        primary_type,
        []
    )

    if preferred_types:

        preferred_types = [
            p.lower()
            for p in preferred_types
        ]

        df["product_bonus"] = (
            df["product_type"]
            .astype(str)
            .str.lower()
            .apply(
                lambda x:
                3 if x in preferred_types
                else 0
            )
        )

        df["final_score"] += (
            df["product_bonus"] * 0.1
        )

    if category_filters:

        df = df[
            df["product_type"].isin(
                category_filters
            )
        ]

    if country_filters:

        df = df[
            df["country"].isin(
                country_filters
            )
        ]

    recommendations = (
        df.sort_values(
            by="final_score",
            ascending=False
        )
        .head(top_n)
        .copy()
    )

    if not recommendations.empty:

        max_score = recommendations[
            "final_score"
        ].max()

        if max_score > 0:
            recommendations[
                "match_score"
            ] = (
                recommendations[
                    "final_score"
                ] / max_score
            )
        else:
            recommendations[
                "match_score"
            ] = 0.0

    else:
        recommendations[
            "match_score"
        ] = 0.0

    return {
        "classified_skin_type": primary_type,
        "target_ingredients": list(
            target_ingredients.keys()
        ),
        "recommendations":
            recommendations.to_dict(
                orient="records"
            )
    }


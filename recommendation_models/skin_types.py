from collections import defaultdict

SKIN_TYPES = {
    "Normal": {
        "target_ingredients": {
            "hyaluronic acid": 5,
            "niacinamide": 4,
            "glycerin": 4,
            "vitamin c": 3,
            "panthenol": 3
        },
        "avoid_tags": ["heavy pore-clogging", "highly irritating"]
    },

    "Oily": {
        "target_ingredients": {
            "salicylic acid": 5,
            "niacinamide": 4,
            "zinc pca": 4,
            "tea tree": 3,
            "glycolic acid": 3
        },
        "avoid_tags": ["may worsen oily skin", "heavy"]
    },

    "Acne-Prone": {
        "target_ingredients": {
            "salicylic acid": 5,
            "benzoyl peroxide": 5,
            "niacinamide": 4,
            "tea tree": 3,
            "centella asiatica": 3
        },
        "avoid_tags": ["acne trigger", "comedogenic", "pore-clogging"]
    },

    "Combination": {
        "target_ingredients": {
            "niacinamide": 5,
            "ceramides": 4,
            "squalane": 4,
            "hyaluronic acid": 4,
            "lactic acid": 3
        },
        "avoid_tags": ["heavy pore-clogging"]
    },

    "Dry": {
        "target_ingredients": {
            "hyaluronic acid": 5,
            "ceramides": 5,
            "glycerin": 4,
            "shea butter": 3,
            "squalane": 4
        },
        "avoid_tags": ["drying", "astringent"]
    },

    "Sensitive": {
        "target_ingredients": {
            "centella asiatica": 5,
            "panthenol": 5,
            "allantoin": 4,
            "aloe vera": 4,
            "colloidal oatmeal": 5
        },
        "avoid_tags": ["irritating", "fragrance"]
    },

    "Mature / Aging": {
        "target_ingredients": {
            "retinol": 5,
            "peptides": 5,
            "vitamin c": 4,
            "glycolic acid": 3,
            "ceramides": 4
        },
        "avoid_tags": ["highly irritating"]
    },

    "Hyperpigmentation / Uneven Tone": {
        "target_ingredients": {
            "vitamin c": 5,
            "alpha arbutin": 5,
            "tranexamic acid": 5,
            "licorice root": 4,
            "niacinamide": 4
        },
        "avoid_tags": ["irritating"]
    }
}

SYMPTOMS = {
    "Oily": {
        "shiny": 3,
        "greasy": 3,
        "oily": 3,
        "large pores": 2,
        "blackheads": 2,
        "excess sebum": 4
    },

    "Dry": {
        "tight": 3,
        "flaky": 3,
        "dry": 3,
        "rough": 2,
        "peeling": 3,
        "dehydrated": 3
    },

    "Sensitive": {
        "redness": 3,
        "burning": 4,
        "stinging": 4,
        "irritated": 3,
        "reactive": 4,
        "eczema": 5
    },

    "Acne-Prone": {
        "acne": 4,
        "pimples": 3,
        "breakouts": 4,
        "whiteheads": 3,
        "cystic acne": 5
    },

    "Hyperpigmentation / Uneven Tone": {
        "dark spots": 4,
        "pigmentation": 4,
        "melasma": 5,
        "post acne marks": 4,
        "uneven tone": 3
    },

    "Mature / Aging": {
        "wrinkles": 5,
        "fine lines": 4,
        "sagging": 5,
        "crow feet": 4,
        "loss of elasticity": 5
    }
}

def determine_skin_profile(primary_feeling, concerns):

    text = f"{primary_feeling} {' '.join(concerns)}".lower()

    scores = defaultdict(int)

    for skin_type, keywords in SYMPTOMS.items():
        for keyword, weight in keywords.items():
            if keyword in text:
                scores[skin_type] += weight

    oily_score = scores["Oily"]
    dry_score = scores["Dry"]

    if oily_score >= 4 and dry_score >= 4:
        primary_skin_type = "Combination"
    elif scores:
        primary_skin_type = max(scores, key=scores.get)
    else:
        primary_skin_type = "Sensitive"

    secondary_concerns = []

    for concern, score in scores.items():
        if concern != primary_skin_type and score >= 3:
            secondary_concerns.append(concern)

    return {
        "primary_skin_type": primary_skin_type,
        "secondary_concerns": secondary_concerns,
        "scores": dict(scores)
    }
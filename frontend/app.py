import streamlit as st
import requests

BACKEND_API_URL = "http://127.0.0.1:8000/api/v1/recommend"

PRODUCT_CATEGORIES = [
    "Face Cleanser",
    "Makeup Remover",
    "Toner",
    "Essence",
    "Serum",
    "General Moisturizer",
    "Face Oil",
    "Eye Cream",
    "Sunscreen",
    "Exfoliator",
    "Face Mask"
]

COUNTRIES = [
    "South Korea",
    "Canada",
    "France",
    "United States",
    "United Kingdom",
    "Japan",
    "Germany",
    "Australia",
    "Italy",
    "Spain"
]

st.set_page_config(
    page_title="SkinGuide AI",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

st.title("✨ SkinGuide AI - Your Personalized Skincare Matchmaker")
st.markdown("---")

left_column, right_column = st.columns(2, gap="large")

with left_column:

    with st.form("skin_quiz"):

        st.write("### 🔍 Section 1: Clinical Skin Analysis")

        q1_feeling = st.selectbox(
            "1. How does your skin look or feel by the middle of the day?",
            options=[
                "Select an option...",
                "Balanced, comfortable, neither too oily nor too dry",
                "Shiny all over, greasy, or prone to breakouts everywhere",
                "Shiny in the T-zone (forehead/nose) but normal or dry on cheeks",
                "Tight, flaky, or visibly dry everywhere",
                "Easily irritated, stinging, or experiencing localized redness"
            ]
        )

        q2_concerns = st.multiselect(
            "2. What are your primary skin concerns?",
            options=[
                "Active Acne",
                "Flakiness",
                "Redness",
                "Excessive Sebum",
                "Large Pores",
                "Dark Spots",
                "Fine Lines & Wrinkles"
            ]
        )

        q3_pores = st.radio(
            "3. How visible are your pores?",
            options=[
                "Barely visible (Normal/Dry)",
                "Visible only in the T-zone (Combination)",
                "Large and visible everywhere (Oily)"
            ]
        )

        q4_wash = st.radio(
            "4. How does your face feel 20 minutes after cleansing?",
            options=[
                "Comfortable and balanced",
                "Tight, dry, or desperate for moisture",
                "Already getting shiny or greasy"
            ]
        )

        q5_breakouts = st.selectbox(
            "5. How frequently do you experience breakouts?",
            options=[
                "Rarely or never",
                "Occasionally (hormonal or stress)",
                "Frequent breakouts and active acne"
            ]
        )

        q6_sun = st.selectbox(
            "6. How does your skin react to the sun?",
            options=[
                "Burns easily and turns red (Sensitive)",
                "Tans easily without much burning",
                "Prone to developing dark spots"
            ]
        )

        q7_sensitivity = st.radio(
            "7. How does your skin react to new products?",
            options=[
                "Rarely reacts badly",
                "Sometimes stings or breaks out",
                "Highly reactive, prone to redness"
            ]
        )

        q8_aging = st.radio(
            "8. Have you noticed signs of aging?",
            options=[
                "No visible signs",
                "Some fine lines or uneven texture",
                "Noticeable wrinkles or loss of firmness"
            ]
        )

        st.markdown("---")

        st.write("### 🛍️ Section 2: Product Preferences")

        q9_categories = st.multiselect(
            "Product Categories",
            PRODUCT_CATEGORIES
        )

        q10_countries = st.multiselect(
            "Country Preferences",
            COUNTRIES
        )

        submit_button = st.form_submit_button(
            "Analyze My Skin & Find Products 🚀"
        )

with right_column:

    if submit_button:

        if q1_feeling == "Select an option...":
            st.error("Please answer Question #1.")
            st.stop()

        with st.spinner("Analyzing your skin profile..."):

            ml_concerns = list(q2_concerns)

            # Convert questionnaire answers into ML-friendly keywords

            if "Combination" in q3_pores:
                ml_concerns.append("combination")

            if "Oily" in q3_pores:
                ml_concerns.append("oily")

            if "Tight" in q4_wash:
                ml_concerns.append("dry")

            if "greasy" in q4_wash.lower():
                ml_concerns.append("oily")

            if "active acne" in q5_breakouts.lower():
                ml_concerns.append("active acne")

            if "dark spots" in q6_sun.lower():
                ml_concerns.append("pigmentation")

            if "Sensitive" in q6_sun:
                ml_concerns.append("sensitive")

            if "Highly reactive" in q7_sensitivity:
                ml_concerns.append("sensitive")

            if "fine lines" in q8_aging.lower():
                ml_concerns.append("aging")

            if "wrinkles" in q8_aging.lower():
                ml_concerns.append("wrinkles")

            payload = {
                "primary_feeling": q1_feeling,
                "concerns": ml_concerns,
                "preferred_categories": q9_categories or None,
                "preferred_countries": q10_countries or None
            }

            try:

                response = requests.post(
                    BACKEND_API_URL,
                    json=payload,
                    timeout=15
                )

                if response.status_code != 200:
                    st.error(
                        f"API Error ({response.status_code})\n\n{response.text}"

                    )
                    st.stop()

                data = response.json()

                st.success(
                    f"### 🔬 Classified Skin Type: {data['classified_skin_type']}"
                )

                st.info(
                    "🎯 Recommended Ingredients:\n\n" +
                    ", ".join(data["target_ingredients"]).title()
                )

                st.markdown("---")

                recommendations = data.get(
                    "recommendations",
                    []
                )

                if not recommendations:
                    st.warning(
                        "No products matched your current filters."
                    )
                    st.stop()

                st.write("### 🧴 Recommended Products")

                for rank, item in enumerate(recommendations, start=1):

                    with st.container():

                        st.markdown(
                            f"## #{rank} {item['product_name']}"
                        )

                        st.write(
                            f"**Brand:** {item['brand']}"
                        )

                        st.write(
                            f"**Country:** {item.get('country', 'Unknown')}"
                        )

                        col1, col2 = st.columns(2)

                        with col1:
                            st.caption(
                                f"📦 Category: {item['product_type']}"
                            )

                        with col2:

                            match_percentage = min(
                                99,
                                int(item["match_score"] * 100)
                            )

                            st.caption(
                                f"🎯 Match Score: {match_percentage}%"
                            )

                        if match_percentage >= 80:
                            st.success("⭐ Excellent Match")

                        elif match_percentage >= 60:
                            st.info("✅ Good Match")

                        else:
                            st.warning("⚡ Moderate Match")

                        if item.get("tags"):

                            tags = (
                                item["tags"]
                                .replace(",", " • ")
                                .title()
                            )

                            st.info(
                                f"✨ Benefits: {tags}"
                            )

                        with st.expander(
                            "🔬 View Ingredients"
                        ):
                            st.write(
                                item["ingredients"]
                            )

                        st.markdown("---")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to FastAPI backend. Make sure it is running."
                )

            except Exception as e:
                st.error(str(e))

    else:

        st.write("### 🤖 AI Output Console")

        st.info(
            "Complete the skin assessment form to receive personalized recommendations."
        )

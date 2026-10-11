"""
TASK 1: AI Travel Planner Application
Run with:  streamlit run travel_planner.py
"""
import streamlit as st

# ---------------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------------
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")
st.title("✈️ AI Travel Planner")
st.caption("Tell us about your trip and get a personalised plan.")

# ---------------------------------------------------------------
# DATA (lists used by the app)
# ---------------------------------------------------------------
INTEREST_OPTIONS = ["Beach", "Nature", "Adventure", "History & Culture",
                    "Food", "Shopping", "Nightlife", "Wellness"]

TRAVEL_CHECKLIST = ["Passport / ID", "Flight Tickets", "Hotel Booking Confirmation",
                    "Mobile Charger", "Medicines"]


# ---------------------------------------------------------------
# BUSINESS RULES (each rule lives in its own small function)
# ---------------------------------------------------------------
def classify_budget(budget):
    """Step 3: Budget classification using if-elif-else."""
    if budget < 10000:
        return "Low Budget"
    elif budget <= 30000:
        return "Medium Budget"
    elif budget <= 60000:
        return "Premium Budget"
    else:
        return "Luxury Budget"


def get_recommendation(travel_type):
    """Step 4: Recommendation based on travel type (if-elif-else)."""
    if travel_type == "Solo":
        return "Backpacking & Exploration"
    elif travel_type == "Family":
        return "Family-Friendly Resorts"
    elif travel_type == "Couple":
        return "Romantic Getaway Packages"
    elif travel_type == "Business":
        return "Corporate Hotels & Meeting Facilities"
    else:
        return "Custom Package"


def calculate_readiness_score(budget, travel_type, interests):
    """Step 7: Scoring mechanism, capped at 100."""
    score = 0

    if budget > 30000:                       # Budget > Rs.30,000  -> +25
        score += 25

    if travel_type == "Family" or travel_type == "Couple":   # -> +25
        score += 25

    for interest in interests:               # each interest -> +15
        score += 15

    if score > 100:                          # maximum score = 100
        score = 100
    return score


# ---------------------------------------------------------------
# STEP 1: COLLECT USER INPUTS
# ---------------------------------------------------------------
with st.form("travel_form"):
    destination = st.text_input("Destination", placeholder="e.g. Goa")
    travel_date = st.text_input("Travel Date", placeholder="e.g. 25-Dec-2026")
    budget = st.number_input("Budget (₹)", min_value=0, value=45000, step=1000)
    travel_type = st.selectbox("Travel Type", ["Solo", "Family", "Couple", "Business"])
    interests = st.multiselect("Interests", INTEREST_OPTIONS)
    submitted = st.form_submit_button("Generate Travel Plan")

# ---------------------------------------------------------------
# MAIN FLOW (runs only after the button is pressed)
# ---------------------------------------------------------------
if submitted:

    # STEP 2: INPUT VALIDATION
    errors = []
    if destination.strip() == "":
        errors.append("Destination should not be empty.")
    if travel_date.strip() == "":
        errors.append("Travel Date should not be empty.")
    if len(interests) == 0:
        errors.append("Please select at least one interest.")

    if len(errors) > 0:
        # "Show Error" branch of the process flow
        for message in errors:
            st.warning(message)
    else:
        # "Yes" branch: validation passed
        budget_category = classify_budget(budget)                    # Step 3
        recommendation = get_recommendation(travel_type)             # Step 4
        score = calculate_readiness_score(budget, travel_type, interests)  # Step 7

        st.success("Your travel plan is ready!")
        st.header("Travel Summary")

        st.write(f"**Destination:** {destination.strip()}")
        st.write(f"**Travel Date:** {travel_date.strip()}")
        st.write(f"**Budget Category:** {budget_category}")
        st.write(f"**Recommendation:** {recommendation}")

        # STEP 5: DISPLAY INTERESTS (for loop)
        st.subheader("Selected Interests")
        for interest in interests:
            st.write(f"• {interest}")

        # STEP 6: TRAVEL CHECKLIST (for loop)
        st.subheader("Travel Checklist")
        for item in TRAVEL_CHECKLIST:
            st.write(f"☑ {item}")

        # STEP 7: DISPLAY SCORE
        st.subheader("Travel Readiness Score")
        st.write(f"**Travel Readiness Score: {score}/100**")
        st.progress(score / 100)

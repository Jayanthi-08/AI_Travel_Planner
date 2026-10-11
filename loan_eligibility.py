"""
TASK 2: AI Loan Eligibility System (rule-based)
Run with:  streamlit run loan_eligibility.py
"""
import streamlit as st

# ---------------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------------
st.set_page_config(page_title="AI Loan Eligibility System", page_icon="🏦")
st.title("🏦 AI Loan Eligibility System")
st.caption("Rule-based screening of loan applications.")

DOCUMENT_OPTIONS = ["Aadhaar", "PAN", "Salary Slip", "Passport",
                    "Voter ID", "Bank Statement"]


# ---------------------------------------------------------------
# BUSINESS RULES
# ---------------------------------------------------------------
def evaluate_credit_score(credit_score):
    """Step 3: credit score -> loan status (if-elif-else)."""
    if credit_score < 600:
        return "Reject"
    elif credit_score <= 750:
        return "Review"
    else:
        return "Approve"


def assess_salary_risk(salary):
    """Step 4: salary -> risk level (if-elif-else)."""
    if salary < 30000:
        return "High Risk"
    elif salary <= 70000:
        return "Medium Risk"
    else:
        return "Low Risk"


def generate_final_decision(credit_status, risk_level, existing_loans):
    """
    Step 6: combine credit score, salary and existing loans.
    (The assignment doesn't give exact rules, so these are documented assumptions.)
      - Rejected : credit score < 600, OR more than 3 existing loans
      - Approved : credit score > 750 AND salary risk is not High AND <= 2 existing loans
      - Otherwise: Manual Review Required
    """
    if credit_status == "Reject" or existing_loans > 3:
        return "Rejected"
    elif credit_status == "Approve" and risk_level != "High Risk" and existing_loans <= 2:
        return "Approved"
    else:
        return "Manual Review Required"


# ---------------------------------------------------------------
# STEP 1: COLLECT USER INPUTS
# ---------------------------------------------------------------
with st.form("loan_form"):
    customer_name = st.text_input("Customer Name", placeholder="e.g. Rahul Sharma")
    monthly_salary = st.number_input("Monthly Salary (₹)", min_value=0, value=0, step=1000)
    credit_score = st.number_input("Credit Score", min_value=0, max_value=1000, value=750, step=1)
    existing_loans = st.number_input("Existing Loans", min_value=0, value=0, step=1)
    documents = st.multiselect("Documents Submitted", DOCUMENT_OPTIONS)
    submitted = st.form_submit_button("Check Eligibility")

# ---------------------------------------------------------------
# MAIN FLOW
# ---------------------------------------------------------------
if submitted:

    # STEP 2: INPUT VALIDATION
    errors = []
    if customer_name.strip() == "":
        errors.append("Customer Name should not be empty.")
    if monthly_salary <= 0:
        errors.append("Salary should be greater than zero.")
    if credit_score < 300 or credit_score > 900:
        errors.append("Credit Score should be between 300 and 900.")

    if len(errors) > 0:
        for message in errors:
            st.warning(message)
    else:
        credit_status = evaluate_credit_score(credit_score)           # Step 3
        risk_level = assess_salary_risk(monthly_salary)               # Step 4
        decision = generate_final_decision(credit_status, risk_level, existing_loans)  # Step 6

        # Map the internal credit status to the wording used in the expected output
        status_text = {"Approve": "Approved", "Review": "Under Review", "Reject": "Rejected"}

        st.header("Customer Loan Assessment")
        st.write(f"**Customer Name:** {customer_name.strip()}")
        st.write(f"**Credit Score:** {credit_score}")
        st.write(f"**Loan Status:** {status_text[credit_status]}")
        st.write(f"**Risk Category:** {risk_level}")
        st.write(f"**Existing Loans:** {existing_loans}")

        # STEP 5: DISPLAY DOCUMENTS (for loop)
        st.subheader("Documents Submitted")
        if len(documents) == 0:
            st.write("No documents submitted.")
        else:
            for document in documents:
                st.write(f"• {document}")

        # STEP 6: FINAL DECISION
        st.subheader("Final Decision")
        if decision == "Approved":
            st.success("LOAN APPROVED")
        elif decision == "Rejected":
            st.error("LOAN REJECTED")
        else:
            st.warning("MANUAL REVIEW REQUIRED")

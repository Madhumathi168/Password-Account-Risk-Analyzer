import streamlit as st
import matplotlib.pyplot as plt

from backend import analyze_password, assess_account_risk


# Page configuration
st.set_page_config(
    page_title="Password & Account Risk Analyzer",
    page_icon="🔐",
    layout="wide"
)


# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #101827;
}
h1, h2, h3, p, label {
    color: white;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


# Project heading
st.title("🔐 Password & Account Risk Analyzer")

st.write(
    "Analyze password strength and evaluate your account security."
)

st.info(
    "Educational project: Use sample passwords only. "
    "Never enter your real account password."
)

st.divider()


# Two-column layout
col1, col2 = st.columns(2)


# PASSWORD ANALYSIS
with col1:

    st.header("🔑 Password Analysis")

    password = st.text_input(
        "Enter a sample password",
        type="password",
        placeholder="Enter test password"
    )

    if st.button("Check Password"):

        if password:

            result = analyze_password(password)

            st.subheader("Password Result")

            st.metric(
                "Password Strength",
                result["strength"]
            )

            st.progress(result["score"] / 100)

            st.write(f"**Security Score:** {result['score']} / 100")

            st.subheader("Security Checks")

            for check, passed in result["checks"].items():

                if passed:
                    st.success(f"✓ {check}")
                else:
                    st.error(f"✗ {check}")

            # Password score chart
            fig, ax = plt.subplots()

            ax.bar(
                ["Password Score"],
                [result["score"]]
            )

            ax.set_ylim(0, 100)
            ax.set_ylabel("Score")
            ax.set_title("Password Security Score")

            st.pyplot(fig)
            plt.close(fig)

            if result["recommendations"]:
                st.subheader("Recommendations")

                for recommendation in result["recommendations"]:
                    st.warning(recommendation)

            else:
                st.success("Your sample password passed all checks!")

        else:
            st.warning("Please enter a sample password.")


# ACCOUNT SECURITY ANALYSIS
with col2:

    st.header("🛡️ Account Security Checklist")

    mfa = st.checkbox("Is Multi-Factor Authentication (MFA) enabled?")

    reuse = st.checkbox("Are you reusing the same password?")

    recovery = st.checkbox("Are your recovery options secured?")

    if st.button("Check Account Security"):

        result = assess_account_risk(
            mfa,
            reuse,
            recovery
        )

        st.subheader("Account Risk Result")

        st.metric(
            "Risk Level",
            result["risk_level"]
        )

        st.write(
            f"**Risk Score:** {result['risk_score']} / 3"
        )

        st.progress(result["risk_score"] / 3)

        if result["risk_level"] == "Low":
            st.success("Your account security looks good!")

        elif result["risk_level"] == "Medium":
            st.warning("Your account has some security risks.")

        else:
            st.error("Your account has high security risks!")

        st.subheader("Security Recommendations")

        if result["recommendations"]:

            for recommendation in result["recommendations"]:
                st.warning(recommendation)

        else:
            st.success("All account security checks passed!")


# Footer
st.divider()

st.caption(
    "Password & Account Risk Analyzer | "
    "Python | Streamlit | Educational Project"
)
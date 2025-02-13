from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import LLMChain
from langchain import PromptTemplate

import streamlit as st
import os

# Access API key from Streamlit secrets
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

# Set page configuration
st.set_page_config(page_title="Travel Itinerary Generator", layout="wide")

# Sidebar content
st.sidebar.title("ℹ️ About This Program")
st.sidebar.info(
    "**Travel Itinerary Generator**\n\n"
    "🔹 Uses AI to create customized travel plans.\n\n"
    "🔹 Generates detailed itineraries with activity and food suggestions.\n\n"
    "_Plan your perfect trip effortlessly!_"
)

def generate_itinerary(location, days, month):
    prompt = f"""You are a kind and helpful travel assistant.

    Generate a {days}-day travel itinerary for {location} in {month}.

    Include morning, afternoon, and evening sightseeing activity suggestions with food options.

    Ensure popular and offbeat spots are covered with specific timings.  Be specific about times, e.g., "9:00 AM: Visit the Eiffel Tower..."
    """

    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro")  # Or another suitable Gemini model
        chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt))
        response = chain.run()
        return response
    except Exception as e:
        st.error(f"Error generating itinerary: {e}")  # More informative error message
        return "⚠️ Unable to generate itinerary. Please try again."

def main():
    st.title("🌍 Travel Itinerary Generator ✈️")
    st.subheader("AI Planner for Travel Itinerary!")

    # User inputs
    location = st.text_input("📍 Enter the location:", value="Ho Chi Minh")
    days = st.number_input("📅 Enter the number of days (1-7):", min_value=1, max_value=7, value=2)
    month = st.selectbox(
        "🗓️ Select the month of your trip:",
        ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]
    )

    # Generate itinerary
    if st.button("🚀 Generate Itinerary"):
        if location.strip():
            with st.spinner("Generating itinerary..."):
                itinerary = generate_itinerary(location, days, month)
                st.session_state["itinerary"] = itinerary  # Save to session state
                if "⚠️" not in itinerary:  # Check for error message
                    st.success("✅ Here is your itinerary:")
                    st.markdown(itinerary)  # Display the itinerary
                else:
                    st.error(itinerary)

if __name__ == "__main__":
    main()

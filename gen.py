import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Load the Zocdoc dataset
csv_path = r"C:\Janath\Intern\zocdoc.csv"  # Use raw string
doctors_df = pd.read_csv(csv_path)

# Rename columns for consistency (ensure these columns exist in your dataset)
if "Doctor's Name" in doctors_df.columns and "speciality" in doctors_df.columns:
    doctors_df.rename(columns={"Doctor's Name": "name", "speciality": "specialty"}, inplace=True)

# Configure Google Gemini AI API Key (use environment variable for security)
GOOGLE_API_KEY = "API_KEY"  # Replace with actual key
genai.configure(api_key=GOOGLE_API_KEY)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def ai_recommendation(query):
    """Uses AI to recommend doctors based on user input."""
    prompt = f"Based on global healthcare data, suggest the best doctors or specialists for: {query}. Include details on their expertise and relevant locations."
    response = model.generate_content([prompt])
    return response.text.strip()

# Streamlit UI
st.title("Doctor Recommendation System")
query = st.text_input("Describe your medical concern or specialty you're looking for:")

if st.button("Search"):
    if query:
        results = doctors_df[
            doctors_df.apply(lambda row: query.lower() in row.to_string().lower(), axis=1)
        ].to_dict(orient="records")
        
        if not results:
            ai_suggestion = ai_recommendation(query)
            st.warning("No exact match found. AI Suggests:")
            st.write(ai_suggestion)
        else:
            for doctor in results:
                st.subheader(doctor['name'])
                st.write(f"**Specialty:** {doctor['specialty']}")
    else:
        st.error("Please enter a search query.")

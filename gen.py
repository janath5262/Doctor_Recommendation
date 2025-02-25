import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Load the Zocdoc dataset (Ensure the path is correct)
csv_path = r"C:\Janath\Intern\zocdoc.csv"  # Use raw string for Windows paths
doctors_df = pd.read_csv(csv_path)

# Rename columns for consistency
if "Doctor's Name" in doctors_df.columns and "speciality" in doctors_df.columns:
    doctors_df.rename(columns={"Doctor's Name": "name", "speciality": "specialty"}, inplace=True)

# Configure Google Gemini AI API Key (Use environment variables for security)
GOOGLE_API_KEY = "Your_API"  # Replace with actual key
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini AI Model
model = genai.GenerativeModel("gemini-1.5-pro")

def ai_recommendation(query):
    """Uses AI to recommend doctors worldwide based on user input."""
    prompt = f"""
    I am building a global doctor recommendation system. Based on worldwide healthcare data, suggest well-known specialists for:
{query}.

Provide:
- A few of the most recognized doctors in this field
- Their country or region
- Any notable affiliations (hospitals, research institutions)


"""
    
    
    try:
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        return f"Error fetching AI recommendations: {e}"

# Streamlit UI
st.title("🌍 Doctor Recommendation System")

query = st.text_input("Describe your medical concern or specialty you're looking for:")

if st.button("Search"):
    if query:
        # Filter dataset for relevant doctors
        results = doctors_df[
            doctors_df["specialty"].str.contains(query, case=False, na=False)
        ].to_dict(orient="records")
        
        if results:
            st.subheader("🔍 Doctors Found in Our Database:")
            for doctor in results:
                st.write(f"**👨‍⚕️ {doctor['name']}**")
                st.write(f"📌 Specialty: {doctor['specialty']}")
                st.write("---")
        else:
            st.warning("No exact match found in our database. Searching globally...")
            ai_suggestion = ai_recommendation(query)
            
            if ai_suggestion:
                st.subheader("🌍 AI Recommended Doctors:")
                ai_results = ai_suggestion.split("\n")
                for result in ai_results:
                    st.write(result)
            else:
                st.error("No AI recommendations available.")
    else:
        st.error("Please enter a search query.")

import pandas as pd
import cohere
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
cohere_api_key = os.environ["COHERE_API_KEY"]
co = cohere.Client(cohere_api_key)

# --- Dataset Loading ---
@st.cache_data
def load_exercise_data(csv_file):
    df = pd.read_csv(csv_file)
    # Clean column names for easier access
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('.', '')
    return df

# Replace 'your_data.csv' with your actual filename
exercise_data = load_exercise_data('megaGymDataset.csv')

# --- Helper Functions ---
def user_asks_about_exercise(query):
    # Improved keyword detection for exercise descriptions
    keywords = ["describe", "how to", "what is", "tell me about", "explain"]
    return any(keyword in query.lower() for keyword in keywords)

def extract_exercise_name(query):
    # More robust extraction, considering common phrasing
    query_lower = query.lower()
    for keyword in ["describe ", "how to ", "what is ", "tell me about ", "explain "]:
        if keyword in query_lower:
            return query_lower.split(keyword, 1)[1].strip().replace("?", "")
    return query_lower.replace("?", "") # Fallback

def describe_exercise(exercise_name, data):
    # Case-insensitive search for exercise title
    matching_exercises = data[data['Title'].str.lower() == exercise_name.lower()]
    if not matching_exercises.empty:
        exercise_info = matching_exercises.iloc[0]
        description = exercise_info['Desc']
        exercise_type = exercise_info['Type']
        body_part = exercise_info['BodyPart']
        equipment = exercise_info['Equipment']
        level = exercise_info['Level']
        rating = exercise_info['Rating']

        return {
            "title": exercise_info['Title'],
            "description": description,
            "type": exercise_type,
            "body_part": body_part,
            "equipment": equipment,
            "level": level,
            "rating": rating
        }
    return None

def craft_fitness_prompt(query, data, user_preferences):
    # Incorporate user preferences into the prompt for Cohere
    goal = user_preferences.get("goal", "general fitness")
    experience = user_preferences.get("experience", "any")
    restrictions = "with no specific restrictions"
    if user_preferences.get("restrictions"):
        restrictions = "considering potential injuries or limitations"

    # Add some context about the available data
    sample_exercises = data['Title'].sample(3).tolist()
    data_context = f"I have a dataset of exercises including types, body parts, equipment, and difficulty levels. For example: {', '.join(sample_exercises)}."

    prompt = f"""You are a highly knowledgeable and helpful fitness expert.
The user has the following fitness preferences:
- Goal: {goal}
- Experience Level: {experience}
- Restrictions: {restrictions}
Please provide a detailed, thorough, and step-by-step explanation in response to the user's query.
If the user asks to describe a specific exercise, include:
- The purpose of the exercise
- The muscles targeted
- Equipment needed
- Proper form and technique
- Common mistakes to avoid
- Tips for progression or modifications
If the user asks a general fitness question, provide an in-depth answer tailored to their preferences.
{data_context}
User Query: {query}
"""
    return prompt

# --- Streamlit UI ---
st.set_page_config(page_title="Fitness Knowledge Bot", layout="wide")

st.title("🏋️‍♂️ Fitness Knowledge Bot")
st.markdown("---")

# Sidebar for user preferences
st.sidebar.header("Your Fitness Profile")
with st.sidebar:
    goal = st.selectbox("What's your main fitness goal?",
                        ["Weight Loss", "Build Muscle", "Endurance", "General Fitness"],
                        key="goal_select")
    experience = st.radio("What's your experience level?",
                          ["Beginner", "Intermediate", "Advanced"],
                          key="experience_radio")
    restrictions = st.checkbox("Any injuries or limitations?", key="restrictions_checkbox")

user_preferences = {
    "goal": goal,
    "experience": experience,
    "restrictions": restrictions
}

st.subheader("Ask me anything about workouts or fitness!")

user_input = st.text_input("Type your question here:", key="user_query_input")

if st.button("Get Answer", key="submit_button"):
    if user_input:
        with st.spinner("Thinking..."):
            # Check if the user is asking about a specific exercise
            if user_asks_about_exercise(user_input):
                exercise_name = extract_exercise_name(user_input)
                exercise_details = describe_exercise(exercise_name, exercise_data)

                if exercise_details:
                    st.success(f"Here's what I found about **{exercise_details['title']}**:")
                    st.markdown(f"**Type:** {exercise_details['type']}")
                    st.markdown(f"**Body Part:** {exercise_details['body_part']}")
                    st.markdown(f"**Equipment:** {exercise_details['equipment']}")
                    st.markdown(f"**Level:** {exercise_details['level']}")
                    if exercise_details['rating'] and exercise_details['rating'] != 0.0:
                        st.markdown(f"**Rating:** {exercise_details['rating']} / 10")
                    st.info(f"**Description:** {exercise_details['description']}")
                else:
                    st.warning(f"I couldn't find specific details for '{exercise_name}' in my database. However, I can still provide general fitness advice based on your preferences.")
                    # Fallback to Cohere for general advice if exercise not found
                    prompt = craft_fitness_prompt(user_input, exercise_data, user_preferences)
                    response = co.chat(
                        model='command-nightly',
                        message=prompt,
                        max_tokens=1000,          # Increase max tokens for longer output
                        temperature=0.7,
                        stop_sequences=["--"]
                    )
                    st.markdown("---")
                    st.markdown("### General Advice:")
                    st.write(response.text)
            else:
                # General fitness question, use Cohere
                prompt = craft_fitness_prompt(user_input, exercise_data, user_preferences)
                response = co.chat(
                    model='command-nightly',
                    message=prompt,
                    stop_sequences=["--"]
                )
                st.markdown("---")
                st.markdown("### Chatbot's Response:")
                st.write(response.text)
    else:
        st.warning("Please enter a question to get a response.")

st.markdown("---")
st.caption("Powered by Cohere and Streamlit")

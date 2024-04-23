import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set the Streamlit server port if it's not already set
os.environ["STREAMLIT_SERVER_PORT"] = "8503"

# Configure Google Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def ask_gemini(user_question):
    # Instantiate the Gemini model
    model = genai.GenerativeModel('gemini-pro')

    # Format the prompt to guide the model generation
    prompt = f'Given the user input perform sentiment analysis and give detailed explanation of the intended message, thankyou. {user_question}'

    # Generate content using the Gemini model
    response_gemini = model.generate_content(prompt)

    # Clean up the response text
    response_gemini = response_gemini.text.replace('**', '').replace('*', '•')

    return response_gemini


def format_response(response):
    # Split the response into lines
    lines = response.split('•')
    # Remove empty lines
    lines = [line.strip() for line in lines if line.strip()]
    # Re-organize the lines into a structured format
    formatted_lines = []
    for line in lines:
        if line.isdigit():
            formatted_lines.append(f"**{line}.**")
        else:
            formatted_lines.append(f"- {line}")
    return '\n'.join(formatted_lines)


# Streamlit application layout
def main():
    st.header("Sentiment Analysis Chat Bot")

    # Create a text input for user questions
    user_question = st.text_input("Input your message:", "")

    # Button to submit the question
    if st.button("Submit"):
        with st.spinner("Generating response..."):
            # Generate response from Gemini model
            raw_gemini_response = ask_gemini(user_question)

            # Format the response for better readability
            formatted_gemini_response = format_response(raw_gemini_response)

            # Display the formatted response using markdown
            st.markdown(formatted_gemini_response, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

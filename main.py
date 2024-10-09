from openai import OpenAI
import openai
import pdfplumber
import os
import streamlit as st
from pdfminer.high_level import extract_text

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Set your OpenAI API key

base_url = "https://api.aimlapi.com/v1"
api_key =  os.getenv("API_KEY")

api = OpenAI(api_key=api_key, base_url=base_url)

def extract_text_from_pdf(uploaded_file):
    return extract_text(uploaded_file)

def summarize_text(text):
    response = api.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a summarizer."},
            {"role": "user", "content": f"Summarize the following text:\n{text}"}
        ]
    )
    summary = response.choices[0].message.content  # Change here
    return summary

def generate_flashcards(text):
    response = api.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a teacher preparing flashcards."},
            {"role": "user", "content": f"Create flashcards from the following lecture:\n{text}"}
        ]
    )
    flashcards = response.choices[0].message.content  # Change here
    return flashcards

def take_quiz(topic):
    response = api.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a quiz master."},
            {"role": "user", "content": f"Create a quiz on the following topic:\n{topic}"}
        ]
    )
    quiz = response.choices[0].message.content  # Change here
    return quiz

# Streamlit app
st.write("Upload a PDF or lecture, and choose a task: summarize, generate flashcards, or take a quiz!")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Add a dropdown menu for task selection
task = st.selectbox("Choose a task", ("Summarize", "Generate Flashcards", "Take a Quiz"))

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    
    if task == "Summarize":
        st.write("### Summary")
        summary = summarize_text(text)
        st.write(summary)
    
    elif task == "Generate Flashcards":
        st.write("### Flashcards")
        flashcards = generate_flashcards(text)
        st.write(flashcards)
    
    elif task == "Take a Quiz":
        st.write("### Take a Quiz")
        topic = st.text_input("Enter a topic for the quiz:")
        if topic:
            quiz = take_quiz(topic)
            st.write(quiz)
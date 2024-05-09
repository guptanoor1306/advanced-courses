import streamlit as st
import requests
import json

# API Configuration
API_URL = "https://catalog.prod.learnapp.com/catalog/discover?type=advance-courses"
API_KEY = "ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJjYTMyN2VhMC1mYTY4LTQ5NDItOWE2OC1mYjUxM2RhMTE1OWQiLCJpcCI6IjQ5LjI0OS42OS4yMiwgMTMwLjE3Ni4xODguMjQ2IiwiY291bnRyeSI6IklOIiwiaWF0IjoxNzE1MjUxNTMxLCJleHAiOjE3MTU4NTYzMzEsImF1ZCI6ImxlYXJuYXBwIiwiaXNzIjoiaHlkcmE6MC4wLjEifQ.rDyqyMquTPy4Dr3FVJpD7NxE4DxLh3CkmRERGir-xlU"

def fetch_courses():
    """Fetches courses from the API and handles exceptions."""
    headers = {
        "X-Api-Key": API_KEY,
        "Authorization": AUTH_TOKEN
    }
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch courses: {e}")
        return {}

def main():
    st.title("Advanced Courses Catalog")

    # Fetch courses data
    courses_data = fetch_courses()
    courses = courses_data.get('courses', [])

    if not courses:
        st.write("No courses data found.")
    else:
        # Creating a list of course titles for the dropdown menu
        course_titles = [course['title'] for course in courses if 'title' in course]
        selected_courses = st.multiselect('Select Courses', options=course_titles)

        # Show selected course details in raw JSON format
        if selected_courses:
            selected_course_data = [course for course in courses if course['title'] in selected_courses]
            st.json(selected_course_data)  # This will display the raw JSON data in a nicely formatted way

if __name__ == "__main__":
    main()

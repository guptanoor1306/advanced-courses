import streamlit as st
import requests
import json

# API Configuration
API_URL = "https://catalog.prod.learnapp.com/catalog/discover?type=advance-courses"
API_KEY = "ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJjYTMyN2VhMC1mYTY4LTQ5NDItOWE2OC1mYjUxM2RhMTE1OWQiLCJpcCI6IjQ5LjI0OS42OS4yMiwgMTMwLjE3Ni4xODguMjQ2IiwiY291bnRyeSI6IklOIiwiaWF0IjoxNzE1MjUxNTMxLCJleHAiOjE3MTU4NTYzMzEsImF1ZCI6ImxlYXJuYXBwIiwiaXNzIjoiaHlkcmE6MC4wLjEifQ.rDyqyMquTPy4Dr3FVJpD7NxE4DxLh3CkmRERGir-xlU"

def fetch_courses():
    headers = {
        "X-Api-Key": API_KEY,
        "Authorization": AUTH_TOKEN
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('advCourses', [])  # Adjusted to match the new JSON structure
    else:
        st.error(f"Failed to fetch courses. Status code: {response.status_code}")
        return []

def main():
    st.title("Advanced Courses Catalog")

    # Fetch courses data
    adv_courses_data = fetch_courses()

    if not adv_courses_data:
        st.write("No advanced courses data found.")
    else:
        # Flatten the list of courses across all subjects
        courses = [item for subject in adv_courses_data for item in subject['items']]
        course_titles = [course['title'] for course in courses if 'title' in course]
        selected_courses = st.multiselect('Select Courses', options=course_titles)

        # Show selected course details in raw JSON format
        if selected_courses:
            selected_course_data = [course for course in courses if course['title'] in selected_courses]
            st.json(selected_course_data)  # This will display the raw JSON data in a nicely formatted way

if __name__ == "__main__":
    main()

import streamlit as st
import requests

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
        return response.json().get('advCourses', [])
    else:
        st.error(f"Failed to fetch courses. Status code: {response.status_code}")
        return []

def display_course_details(course):
    st.subheader(course['title'])
    st.write(f"**Canonical Title:** {course['canonicalTitle']}")
    st.write(f"**Summary:** {course.get('summary', 'No summary provided')}")
    st.write(f"**Total Playback Time:** {course['totalPlaybackTime']} minutes")
    st.write(f"**Lesson Count:** {course['lessonCount']}")
    st.write(f"**Language:** {', '.join(course['language'])}")
    st.write(f"**Release Date:** {course['releaseDate']}")

    # Attempt to display the image with error handling
    try:
        image_url = course['assets']['card-238x165-jpg']['url']
        if not image_url.startswith('http'):
            image_url = f"https://example.com/{image_url}"  # Adjust base URL accordingly
        st.image(image_url, caption=course['assets']['card-238x165-jpg']['alt'])
    except Exception as e:
        st.error(f"Failed to load image: {e}")

def main():
    st.title("Advanced Courses Catalog")
    courses_data = fetch_courses()

    if not courses_data:
        st.write("No advanced courses data found.")
        return

    subjects = list(set(subject['subject'] for subject in courses_data if 'subject' in subject))
    selected_subject = st.selectbox('Select Subject', subjects)

    filtered_courses = next((sub['items'] for sub in courses_data if sub['subject'] == selected_subject), [])
    course_titles = [course['title'] for course in filtered_courses]
    selected_course_title = st.selectbox('Select Course', course_titles)

    if selected_course_title:
        selected_course = next((course for course in filtered_courses if course['title'] == selected_course_title), None)
        if selected_course:
            display_course_details(selected_course)

if __name__ == "__main__":
    main()

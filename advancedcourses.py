import streamlit as st
import requests

# API Configuration
API_URL = "https://catalog.prod.learnapp.com/catalog/discover?type=advance-courses"
API_KEY = "ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MTUxNzE5MjcsImV4cCI6MTcxNTc3NjcyNywiYXVkIjoibGVhcm5hcHAiLCJpc3MiOiJoeWRyYTowLjAuMSJ9.Vtbt-nJy3XGDOQW-AManV_Kx6rHjFDOZPmJ3ENyArlM"

def fetch_courses():
    headers = {
        "X-Api-Key": API_KEY,
        "Authorization": AUTH_TOKEN
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch courses from the API. Status code: {}".format(response.status_code))
        return []

def main():
    st.title("Course Catalog")

    # Fetching courses
    courses_data = fetch_courses()
    courses = courses_data.get('courses', [])
    if not courses:
        st.error("No courses found in the API response.")
    else:
        # Extracting course titles
        course_titles = [course['title'] for course in courses if 'title' in course]

        # Multi-select for courses
        selected_courses = st.multiselect('Select Courses', options=course_titles)

        # Display selected courses
        if selected_courses:
            for course in courses:
                if course['title'] in selected_courses:
                    with st.expander(f"{course['title']}"):
                        for key, value in course.items():
                            if key not in ['assets', 'mentors']:
                                if st.checkbox(f'Show {key}', key=f'checkbox_{course["title"]}_{key}', value=True):
                                    st.write(f"{key}: {value}")

if __name__ == "__main__":
    main()

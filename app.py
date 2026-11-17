
import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT,
    email TEXT
)
""")
conn.commit()

st.title("🎓 Student Record Management System")
st.write("Manage Student Records using CRUD Operations")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("Add New Student")

    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    course = st.text_input("Course")
    email = st.text_input("Email")

    if st.button("Add Student"):
        if name and course and email:
            cursor.execute(
                "INSERT INTO students (name, age, course, email) VALUES (?, ?, ?, ?)",
                (name, age, course, email)
            )
            conn.commit()
            st.success("Student Added Successfully!")
        else:
            st.warning("Please fill all fields.")

# READ
elif menu == "View Students":
    st.subheader("All Student Records")

    df = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(df, use_container_width=True)

# UPDATE
elif menu == "Update Student":
    st.subheader("Update Student Details")

    students = cursor.execute(
        "SELECT * FROM students"
    ).fetchall()

    if students:
        student_id = st.selectbox(
            "Select Student ID",
            [s[0] for s in students]
        )

        student = next(s for s in students if s[0] == student_id)

        name = st.text_input("Name", student[1])
        age = st.number_input("Age", min_value=1, max_value=100, value=student[2])
        course = st.text_input("Course", student[3])
        email = st.text_input("Email", student[4])

        if st.button("Update Student"):
            cursor.execute("""
                UPDATE students
                SET name=?, age=?, course=?, email=?
                WHERE id=?
            """, (name, age, course, email, student_id))

            conn.commit()
            st.success("Student Updated Successfully!")
    else:
        st.info("No student records found.")

# DELETE
elif menu == "Delete Student":
    st.subheader("Delete Student Record")

    students = cursor.execute(
        "SELECT id, name FROM students"
    ).fetchall()

    if students:
        student_id = st.selectbox(
            "Select Student",
            students,
            format_func=lambda x: f"ID: {x[0]} - {x[1]}"
        )

        if st.button("Delete Student"):
            cursor.execute(
                "DELETE FROM students WHERE id=?",
                (student_id[0],)
            )
            conn.commit()
            st.success("Student Deleted Successfully!")
    else:
        st.info("No records available.")

conn.close()

"""
================================================================================
Student Feedback Analysis System - Database Seeder
================================================================================
Populates realistic academic dummy data for demonstration during college project
evaluation. Generates realistic feedback distributions, faculty members, courses,
and student qualitative comments.
"""

import random
from datetime import datetime, timedelta
from app import create_app
from database import db
from models import Department, Faculty, Course, Feedback


DEPARTMENTS_DATA = [
    {"code": "CSE", "name": "Computer Science & Engineering"},
    {"code": "IT", "name": "Information Technology"},
    {"code": "ECE", "name": "Electronics & Communication Engineering"}
]

FACULTY_DATA = [
    {"name": "Dr. Rajesh Sharma", "designation": "Professor & HOD", "dept": "CSE", "email": "rajesh.sharma@college.edu", "exp": 16},
    {"name": "Prof. Ananya Roy", "designation": "Associate Professor", "dept": "CSE", "email": "ananya.roy@college.edu", "exp": 10},
    {"name": "Dr. Suresh Kumar", "designation": "Associate Professor", "dept": "CSE", "email": "suresh.kumar@college.edu", "exp": 12},
    {"name": "Prof. Priya Nair", "designation": "Assistant Professor", "dept": "IT", "email": "priya.nair@college.edu", "exp": 6},
    {"name": "Dr. Vikram Mehta", "designation": "Professor", "dept": "IT", "email": "vikram.mehta@college.edu", "exp": 14},
    {"name": "Prof. Sneha Verma", "designation": "Assistant Professor", "dept": "ECE", "email": "sneha.verma@college.edu", "exp": 5}
]

COURSES_DATA = [
    {"code": "CS201", "name": "Data Structures & Algorithms", "dept": "CSE", "sem": 3, "credits": 4, "instructor": "Dr. Rajesh Sharma"},
    {"code": "CS202", "name": "Database Management Systems", "dept": "CSE", "sem": 3, "credits": 4, "instructor": "Prof. Ananya Roy"},
    {"code": "CS301", "name": "Operating Systems", "dept": "CSE", "sem": 5, "credits": 4, "instructor": "Dr. Suresh Kumar"},
    {"code": "CS302", "name": "Computer Networks", "dept": "CSE", "sem": 5, "credits": 3, "instructor": "Dr. Rajesh Sharma"},
    {"code": "IT201", "name": "Web Technologies & Full Stack", "dept": "IT", "sem": 3, "credits": 4, "instructor": "Prof. Priya Nair"},
    {"code": "IT301", "name": "Python Programming & Data Science", "dept": "IT", "sem": 5, "credits": 3, "instructor": "Dr. Vikram Mehta"},
    {"code": "EC201", "name": "Digital Logic & Microprocessors", "dept": "ECE", "sem": 3, "credits": 4, "instructor": "Prof. Sneha Verma"},
    {"code": "CS401", "name": "Machine Learning Fundamentals", "dept": "CSE", "sem": 7, "credits": 4, "instructor": "Prof. Ananya Roy"}
]

POSITIVE_COMMENTS = [
    "Explains complex algorithms with intuitive real-world examples and interactive whiteboard diagrams.",
    "Very punctual and always clarifies doubts after class. One of the best professors this semester!",
    "Lab assignments were challenging and helped us build actual problem-solving skills.",
    "Slides and study notes provided before exams were extremely thorough and well-organized.",
    "Encourages active discussion in lectures rather than just reading off textbook slides.",
    "Great guidance during weekly practicals; evaluation was objective and fair.",
    "Provided useful industry insights and coding competition tips throughout the semester.",
    "Clear pace of teaching, never rushed through difficult topics."
]

IMPROVEMENT_COMMENTS = [
    "Could provide more practice problem sets for recursion and dynamic programming.",
    "Microphone volume in the lecture hall was occasionally faint from the back benches.",
    "Would appreciate if lab submissions were returned with more detailed line-by-line feedback.",
    "Pacing during the first unit felt slightly fast for beginners without prior coding experience.",
    "Include more live coding sessions instead of theoretical PowerPoint presentations.",
    "More reference questions for university semester exams would be very helpful."
]


def seed_database():
    """Seeds departments, faculty, courses, and 120+ feedback records."""
    print("[Seeder] Checking and populating database...")

    # 1. Departments
    dept_map = {}
    for d in DEPARTMENTS_DATA:
        existing = Department.query.filter_by(code=d["code"]).first()
        if not existing:
            dept = Department(code=d["code"], name=d["name"])
            db.session.add(dept)
            db.session.flush()
            dept_map[d["code"]] = dept
        else:
            dept_map[d["code"]] = existing

    # 2. Faculty
    faculty_map = {}
    for f in FACULTY_DATA:
        existing = Faculty.query.filter_by(email=f["email"]).first()
        if not existing:
            dept = dept_map[f["dept"]]
            faculty = Faculty(
                name=f["name"],
                designation=f["designation"],
                department_id=dept.id,
                email=f["email"],
                experience_years=f["exp"]
            )
            db.session.add(faculty)
            db.session.flush()
            faculty_map[f["name"]] = faculty
        else:
            faculty_map[f["name"]] = existing

    # 3. Courses
    course_map = {}
    for c in COURSES_DATA:
        existing = Course.query.filter_by(code=c["code"]).first()
        if not existing:
            dept = dept_map[c["dept"]]
            inst = faculty_map[c["instructor"]]
            course = Course(
                code=c["code"],
                name=c["name"],
                department_id=dept.id,
                semester=c["sem"],
                credits=c["credits"],
                faculty_id=inst.id
            )
            db.session.add(course)
            db.session.flush()
            course_map[c["code"]] = course
        else:
            course_map[c["code"]] = existing

    db.session.commit()

    # 4. Feedback records
    existing_feedback_count = Feedback.query.count()
    if existing_feedback_count >= 50:
        print(f"[Seeder] Database already populated with {existing_feedback_count} feedback records.")
        return

    print("[Seeder] Generating realistic feedback submissions...")
    # Faculty rating profiles to reflect realistic academic variance
    faculty_weights = {
        "Dr. Rajesh Sharma": [0.02, 0.03, 0.15, 0.40, 0.40],   # Avg ~4.1 - 4.5
        "Prof. Ananya Roy": [0.01, 0.02, 0.12, 0.45, 0.40],    # Avg ~4.2 - 4.6
        "Dr. Suresh Kumar": [0.05, 0.10, 0.25, 0.40, 0.20],    # Avg ~3.6 - 3.9
        "Prof. Priya Nair": [0.01, 0.02, 0.10, 0.37, 0.50],    # Avg ~4.3 - 4.7
        "Dr. Vikram Mehta": [0.02, 0.05, 0.20, 0.43, 0.30],    # Avg ~3.9 - 4.2
        "Prof. Sneha Verma": [0.03, 0.07, 0.20, 0.40, 0.30]    # Avg ~3.8 - 4.1
    }

    random.seed(42)  # Deterministic seed for reproducible evaluation data
    records_to_create = []

    courses_list = list(course_map.values())
    semesters = ["Semester 3", "Semester 5"]

    for course in courses_list:
        # Generate 15-20 feedbacks per course
        target_count = random.randint(15, 20)
        faculty = course.instructor or random.choice(list(faculty_map.values()))
        weights = faculty_weights.get(faculty.name, [0.03, 0.07, 0.20, 0.40, 0.30])

        for i in range(target_count):
            t_qual = random.choices([1, 2, 3, 4, 5], weights=weights)[0]
            c_cont = random.choices([1, 2, 3, 4, 5], weights=weights)[0]
            punc = random.choices([1, 2, 3, 4, 5], weights=weights)[0]
            doubt = random.choices([1, 2, 3, 4, 5], weights=weights)[0]
            lab = random.choices([1, 2, 3, 4, 5], weights=weights)[0]

            overall = round((t_qual + c_cont + punc + doubt + lab) / 5.0, 2)

            pos_comment = random.choice(POSITIVE_COMMENTS) if random.random() > 0.25 else ""
            imp_comment = random.choice(IMPROVEMENT_COMMENTS) if random.random() > 0.35 else ""

            # Stagger timestamps across past 60 days
            created_date = datetime.now(timezone.utc) - timedelta(days=random.randint(1, 60), hours=random.randint(0, 23))

            fb = Feedback(
                department_id=course.department_id,
                course_id=course.id,
                faculty_id=faculty.id,
                academic_year="2025-2026",
                semester=f"Semester {course.semester}",
                teaching_quality=t_qual,
                course_content=c_cont,
                punctuality=punc,
                doubt_solving=doubt,
                lab_work_fairness=lab,
                overall_rating=overall,
                comments_positive=pos_comment,
                comments_improvement=imp_comment,
                created_at=created_date
            )
            records_to_create.append(fb)

    db.session.bulk_save_objects(records_to_create)
    db.session.commit()
    print(f"[Seeder] Successfully seeded {len(records_to_create)} feedback submissions!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_database()

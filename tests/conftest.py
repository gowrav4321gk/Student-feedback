import pytest
from app import create_app
from database import db
from models import Department, Faculty, Course, Feedback


@pytest.fixture
def app():
    """Create and configure a clean testing application instance."""
    app_instance = create_app("testing")
    app_instance.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app_instance.app_context():
        db.create_all()
        yield app_instance
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for making HTTP requests."""
    return app.test_client()


@pytest.fixture
def sample_data(app):
    """Seeds consistent sample models for unit tests."""
    with app.app_context():
        dept = Department(code="CSE", name="Computer Science & Engineering")
        db.session.add(dept)
        db.session.flush()

        faculty = Faculty(
            name="Dr. Alan Turing",
            designation="Professor",
            department_id=dept.id,
            email="alan.turing@college.edu",
            experience_years=15
        )
        db.session.add(faculty)
        db.session.flush()

        course = Course(
            code="CS101",
            name="Intro to Computer Systems",
            department_id=dept.id,
            semester=1,
            credits=4,
            faculty_id=faculty.id
        )
        db.session.add(course)
        db.session.flush()

        fb1 = Feedback(
            department_id=dept.id,
            course_id=course.id,
            faculty_id=faculty.id,
            academic_year="2025-2026",
            semester="Semester 1",
            teaching_quality=5,
            course_content=5,
            punctuality=4,
            doubt_solving=5,
            lab_work_fairness=5,
            overall_rating=4.8,
            comments_positive="Brilliant lecture delivery and clarity.",
            comments_improvement="Provide lecture notes slightly earlier."
        )

        fb2 = Feedback(
            department_id=dept.id,
            course_id=course.id,
            faculty_id=faculty.id,
            academic_year="2025-2026",
            semester="Semester 1",
            teaching_quality=4,
            course_content=4,
            punctuality=4,
            doubt_solving=4,
            lab_work_fairness=4,
            overall_rating=4.0,
            comments_positive="Very patient during doubt clearing.",
            comments_improvement="None."
        )

        db.session.add_all([fb1, fb2])
        db.session.commit()

        # Retrieve fully loaded instances using SQLAlchemy 2.0 db.session.get
        feedbacks = Feedback.query.all()
        dept_item = db.session.get(Department, dept.id)
        fac_item = db.session.get(Faculty, faculty.id)
        crs_item = db.session.get(Course, course.id)

        return {
            "department_id": dept.id,
            "faculty_id": faculty.id,
            "course_id": course.id,
            "department": dept_item,
            "faculty": fac_item,
            "course": crs_item,
            "feedbacks": feedbacks
        }

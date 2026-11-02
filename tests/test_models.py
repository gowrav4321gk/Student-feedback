from models import Department, Faculty, Course, Feedback


def test_department_creation(app, sample_data):
    """Test Department model creation and relationships."""
    dept = Department.query.filter_by(code="CSE").first()
    assert dept is not None
    assert dept.name == "Computer Science & Engineering"
    assert len(dept.faculty_members) >= 1
    assert len(dept.courses) >= 1


def test_faculty_average_rating(app, sample_data):
    """Test Faculty model helper methods."""
    faculty = Faculty.query.filter_by(name="Dr. Alan Turing").first()
    assert faculty is not None
    assert faculty.get_feedback_count() == 2
    # (4.8 + 4.0) / 2 = 4.4
    assert faculty.get_average_rating() == 4.4


def test_course_average_rating(app, sample_data):
    """Test Course model methods."""
    course = Course.query.filter_by(code="CS101").first()
    assert course is not None
    assert course.get_feedback_count() == 2
    assert course.get_average_rating() == 4.4


def test_feedback_arithmetic_mean(app):
    """Test Feedback arithmetic mean calculation."""
    fb = Feedback(
        department_id=1,
        course_id=1,
        faculty_id=1,
        academic_year="2025-2026",
        semester="Semester 1",
        teaching_quality=5,
        course_content=4,
        punctuality=4,
        doubt_solving=5,
        lab_work_fairness=4
    )
    # (5 + 4 + 4 + 5 + 4) / 5 = 22 / 5 = 4.4
    assert fb.calculate_overall() == 4.4

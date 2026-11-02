from forms import FeedbackForm


def test_feedback_form_valid(app, sample_data):
    """Test valid FeedbackForm data."""
    with app.test_request_context():
        form = FeedbackForm(
            department_id=sample_data["department_id"],
            course_id=sample_data["course_id"],
            faculty_id=sample_data["faculty_id"],
            academic_year="2025-2026",
            semester="Semester 1",
            teaching_quality=5,
            course_content=4,
            punctuality=5,
            doubt_solving=4,
            lab_work_fairness=5,
            comments_positive="Great explanations and enthusiasm.",
            comments_improvement="Provide code samples earlier."
        )
        form.department_id.choices = [(sample_data["department_id"], "CSE")]
        form.course_id.choices = [(sample_data["course_id"], "CS101")]
        form.faculty_id.choices = [(sample_data["faculty_id"], "Dr. Alan Turing")]

        assert form.validate() is True


def test_feedback_form_invalid_rating_range(app, sample_data):
    """Test FeedbackForm rejects ratings outside 1-5."""
    with app.test_request_context():
        # Score of 7 is invalid (max is 5)
        form = FeedbackForm(
            department_id=sample_data["department_id"],
            course_id=sample_data["course_id"],
            faculty_id=sample_data["faculty_id"],
            academic_year="2025-2026",
            semester="Semester 1",
            teaching_quality=7,
            course_content=4,
            punctuality=5,
            doubt_solving=4,
            lab_work_fairness=5
        )
        form.department_id.choices = [(sample_data["department_id"], "CSE")]
        form.course_id.choices = [(sample_data["course_id"], "CS101")]
        form.faculty_id.choices = [(sample_data["faculty_id"], "Dr. Alan Turing")]

        assert form.validate() is False
        assert "teaching_quality" in form.errors

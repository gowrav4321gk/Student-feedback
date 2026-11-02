from flask import Blueprint, render_template, redirect, url_for, flash, request
from database import db
from models import Department, Course, Faculty, Feedback
from forms import FeedbackForm, FeedbackFilterForm

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")


@feedback_bp.route("/submit", methods=["GET", "POST"])
def submit_feedback():
    """
    Anonymous Student Feedback submission view.
    Validates user input with Flask-WTF and saves ratings anonymously.
    """
    form = FeedbackForm()

    # Dynamically populate dropdown choices from database
    departments = Department.query.order_by(Department.name).all()
    courses = Course.query.order_by(Course.code).all()
    faculty_list = Faculty.query.order_by(Faculty.name).all()

    form.department_id.choices = [(d.id, f"{d.code} - {d.name}") for d in departments]
    form.course_id.choices = [(c.id, f"{c.code} - {c.name}") for c in courses]
    form.faculty_id.choices = [(f.id, f"{f.name} ({f.designation})") for f in faculty_list]

    if form.validate_on_submit():
        # Instantiate feedback model with clean validated form data
        new_feedback = Feedback(
            department_id=form.department_id.data,
            course_id=form.course_id.data,
            faculty_id=form.faculty_id.data,
            academic_year=form.academic_year.data,
            semester=form.semester.data,
            teaching_quality=form.teaching_quality.data,
            course_content=form.course_content.data,
            punctuality=form.punctuality.data,
            doubt_solving=form.doubt_solving.data,
            lab_work_fairness=form.lab_work_fairness.data,
            comments_positive=form.comments_positive.data.strip() if form.comments_positive.data else "",
            comments_improvement=form.comments_improvement.data.strip() if form.comments_improvement.data else ""
        )

        # Compute arithmetic mean across the 5 dimensions
        new_feedback.overall_rating = new_feedback.calculate_overall()

        db.session.add(new_feedback)
        db.session.commit()

        flash("Your anonymous feedback has been recorded successfully. Thank you for your constructive input!", "success")
        return redirect(url_for("feedback.feedback_success"))

    return render_template(
        "submit_feedback.html",
        form=form,
        departments=departments,
        courses=courses,
        faculty_list=faculty_list
    )


@feedback_bp.route("/success")
def feedback_success():
    """Submission confirmation page with anonymity privacy note."""
    return render_template("feedback_success.html")


@feedback_bp.route("/explorer")
def feedback_explorer():
    """
    Search and filter all submitted anonymous feedback responses.
    Allows filtering by department, course, faculty, semester, and minimum rating.
    """
    # Query parameters
    dept_id = request.args.get("department", type=int)
    course_id = request.args.get("course", type=int)
    faculty_id = request.args.get("faculty", type=int)
    min_rating = request.args.get("min_rating", type=float)
    semester = request.args.get("semester", type=str)

    query = Feedback.query

    if dept_id:
        query = query.filter_by(department_id=dept_id)
    if course_id:
        query = query.filter_by(course_id=course_id)
    if faculty_id:
        query = query.filter_by(faculty_id=faculty_id)
    if semester:
        query = query.filter_by(semester=semester)
    if min_rating:
        query = query.filter(Feedback.overall_rating >= min_rating)

    feedbacks = query.order_by(Feedback.created_at.desc()).all()

    # Dropdown options for filter bar
    departments = Department.query.order_by(Department.name).all()
    courses = Course.query.order_by(Course.code).all()
    faculty_list = Faculty.query.order_by(Faculty.name).all()

    return render_template(
        "feedback_explorer.html",
        feedbacks=feedbacks,
        departments=departments,
        courses=courses,
        faculty_list=faculty_list,
        selected_dept=dept_id,
        selected_course=course_id,
        selected_faculty=faculty_id,
        selected_min_rating=min_rating,
        selected_semester=semester
    )

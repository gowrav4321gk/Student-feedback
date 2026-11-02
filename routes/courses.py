from flask import Blueprint, render_template
from database import db
from models import Course, Feedback
from analytics import (
    feedbacks_to_dataframe,
    calculate_kpis,
    generate_rating_distribution_chart,
    generate_category_breakdown_chart
)

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/")
def course_list():
    """
    Displays the directory of academic courses with syllabus credits,
    departments, instructor names, and average student ratings.
    """
    courses = Course.query.order_by(Course.code).all()
    # Sort courses by rating descending
    sorted_courses = sorted(courses, key=lambda c: c.get_average_rating(), reverse=True)
    return render_template("course_list.html", courses=sorted_courses)


@courses_bp.route("/<int:course_id>")
def course_detail(course_id):
    """
    Detailed analytics view for an individual course.
    Evaluates syllabus coverage, teaching effectiveness, and student feedback.
    """
    course = db.get_or_404(Course, course_id)
    feedbacks = Feedback.query.filter_by(course_id=course_id).order_by(Feedback.created_at.desc()).all()

    df = feedbacks_to_dataframe(feedbacks)
    kpis = calculate_kpis(df)

    chart_distribution = generate_rating_distribution_chart(df)
    chart_categories = generate_category_breakdown_chart(df)

    return render_template(
        "course_detail.html",
        course=course,
        feedbacks=feedbacks,
        kpis=kpis,
        chart_distribution=chart_distribution,
        chart_categories=chart_categories
    )

from flask import Blueprint, render_template, abort
from database import db
from models import Faculty, Feedback, Course
from analytics import (
    feedbacks_to_dataframe,
    calculate_kpis,
    generate_rating_distribution_chart,
    generate_category_breakdown_chart
)

faculty_bp = Blueprint("faculty", __name__, url_prefix="/faculty")


@faculty_bp.route("/")
def faculty_list():
    """
    Displays the full directory of faculty members with their designations,
    departments, overall ratings, feedback counts, and performance rankings.
    """
    faculty_members = Faculty.query.all()
    # Sort by average rating descending
    sorted_faculty = sorted(faculty_members, key=lambda f: f.get_average_rating(), reverse=True)

    return render_template("faculty_list.html", faculty_list=sorted_faculty)


@faculty_bp.route("/<int:faculty_id>")
def faculty_detail(faculty_id):
    """
    Detailed analytics page for an individual faculty member.
    Shows multi-dimensional category breakdown, distribution chart,
    and anonymized student comments.
    """
    faculty = db.get_or_404(Faculty, faculty_id)
    feedbacks = Feedback.query.filter_by(faculty_id=faculty_id).order_by(Feedback.created_at.desc()).all()

    # Analytics for this specific instructor using Pandas
    df = feedbacks_to_dataframe(feedbacks)
    kpis = calculate_kpis(df)

    # Individual instructor charts
    chart_distribution = generate_rating_distribution_chart(df)
    chart_categories = generate_category_breakdown_chart(df)

    # Filter positive and improvement comments
    positive_comments = [f.comments_positive for f in feedbacks if f.comments_positive]
    improvement_comments = [f.comments_improvement for f in feedbacks if f.comments_improvement]

    return render_template(
        "faculty_detail.html",
        faculty=faculty,
        feedbacks=feedbacks,
        kpis=kpis,
        chart_distribution=chart_distribution,
        chart_categories=chart_categories,
        positive_comments=positive_comments,
        improvement_comments=improvement_comments
    )

from flask import Blueprint, render_template, redirect, url_for, flash
from models import Department, Faculty, Course, Feedback
from analytics import feedbacks_to_dataframe, calculate_kpis
from database import db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """
    Landing Home Page: Displays high-level platform introduction,
    system highlights, key statistics counter, and action cards.
    """
    total_feedbacks = Feedback.query.count()
    total_faculty = Faculty.query.count()
    total_courses = Course.query.count()
    total_departments = Department.query.count()

    # Calculate overall average rating
    feedbacks = Feedback.query.all()
    df = feedbacks_to_dataframe(feedbacks)
    kpis = calculate_kpis(df)

    return render_template(
        "index.html",
        total_feedbacks=total_feedbacks,
        total_faculty=total_faculty,
        total_courses=total_courses,
        total_departments=total_departments,
        kpis=kpis
    )


@main_bp.route("/about")
def about():
    """
    About Page: Explains technical architecture, project purpose,
    mathematical calculation formulas, and viva presentation talking points.
    """
    return render_template("about.html")


@main_bp.route("/seed-demo")
def seed_demo():
    """
    Convenience route for college presentation: quickly re-seeds or populates
    realistic dummy data if the database is currently empty.
    """
    from seed import seed_database
    try:
        seed_database()
        flash("Sample academic feedback data seeded successfully!", "success")
    except Exception as e:
        flash(f"Error seeding demo data: {str(e)}", "danger")
    return redirect(url_for("dashboard.dashboard_view"))

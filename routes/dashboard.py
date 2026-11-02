from flask import Blueprint, render_template, request
from models import Department, Course, Faculty, Feedback
from analytics import (
    feedbacks_to_dataframe,
    calculate_kpis,
    get_faculty_leaderboard,
    get_course_summary,
    generate_rating_distribution_chart,
    generate_faculty_comparison_chart,
    generate_category_breakdown_chart,
    generate_course_ratings_chart
)

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
def dashboard_view():
    """
    Main Analytics Dashboard:
    Computes statistical summaries with Pandas & NumPy,
    renders Matplotlib charts, and displays faculty/course performance metrics.
    """
    # Optional filters
    dept_id = request.args.get("department", type=int)
    semester = request.args.get("semester", type=str)

    query = Feedback.query
    if dept_id:
        query = query.filter_by(department_id=dept_id)
    if semester:
        query = query.filter_by(semester=semester)

    feedbacks = query.all()

    # Convert to Pandas DataFrame for high-performance vectorized analysis
    df = feedbacks_to_dataframe(feedbacks)

    # 1. Statistical KPIs (Pandas & NumPy)
    kpis = calculate_kpis(df)

    # 2. Aggregated tables
    faculty_leaderboard = get_faculty_leaderboard(df)
    course_summary = get_course_summary(df)

    # 3. Matplotlib visual charts (embedded as clean Base64 images)
    chart_distribution = generate_rating_distribution_chart(df)
    chart_faculty = generate_faculty_comparison_chart(df)
    chart_categories = generate_category_breakdown_chart(df)
    chart_courses = generate_course_ratings_chart(df)

    # Dropdown data for filter controls
    departments = Department.query.order_by(Department.name).all()
    available_semesters = [f"Semester {i}" for i in range(1, 9)]

    return render_template(
        "dashboard.html",
        kpis=kpis,
        faculty_leaderboard=faculty_leaderboard[:5],  # Top 5 for summary card
        course_summary=course_summary[:5],
        chart_distribution=chart_distribution,
        chart_faculty=chart_faculty,
        chart_categories=chart_categories,
        chart_courses=chart_courses,
        departments=departments,
        available_semesters=available_semesters,
        selected_dept=dept_id,
        selected_semester=semester,
        total_records_in_view=len(feedbacks)
    )

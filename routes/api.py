import io
from flask import Blueprint, jsonify, Response, request
import pandas as pd
from models import Department, Course, Faculty, Feedback
from analytics import feedbacks_to_dataframe

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/courses-by-department/<int:department_id>")
def courses_by_department(department_id):
    """
    JSON API endpoint for dynamic dropdown filtering in the feedback form.
    Returns courses belonging to the selected academic department.
    """
    courses = Course.query.filter_by(department_id=department_id).order_by(Course.name).all()
    data = [{"id": c.id, "code": c.code, "name": c.name, "faculty_id": c.faculty_id} for c in courses]
    return jsonify(data)


@api_bp.route("/faculty-by-department/<int:department_id>")
def faculty_by_department(department_id):
    """
    JSON API endpoint returning faculty members for the selected department.
    """
    faculty_list = Faculty.query.filter_by(department_id=department_id).order_by(Faculty.name).all()
    data = [{"id": f.id, "name": f.name, "designation": f.designation} for f in faculty_list]
    return jsonify(data)


@api_bp.route("/export/csv")
def export_feedback_csv():
    """
    Exports all feedback records into a clean, downloadable CSV file
    using the Pandas DataFrame to_csv() functionality.
    """
    dept_id = request.args.get("department", type=int)
    faculty_id = request.args.get("faculty", type=int)
    course_id = request.args.get("course", type=int)

    query = Feedback.query
    if dept_id:
        query = query.filter_by(department_id=dept_id)
    if faculty_id:
        query = query.filter_by(faculty_id=faculty_id)
    if course_id:
        query = query.filter_by(course_id=course_id)

    feedbacks = query.order_by(Feedback.created_at.desc()).all()
    df = feedbacks_to_dataframe(feedbacks)

    # Use in-memory string buffer for CSV stream
    output = io.StringIO()
    df.to_csv(output, index=False)
    csv_data = output.getvalue()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=student_feedback_data.csv"
        }
    )

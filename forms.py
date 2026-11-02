from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    IntegerField,
    TextAreaField,
    SubmitField,
    RadioField,
    StringField
)
from wtforms.validators import DataRequired, NumberRange, Length, Optional


class FeedbackForm(FlaskForm):
    """
    Secure Student Feedback submission form with comprehensive validation.
    Enforces 1-5 rating constraints and validates selections.
    """
    department_id = SelectField(
        "Academic Department",
        coerce=int,
        validators=[DataRequired(message="Please select your department.")]
    )

    course_id = SelectField(
        "Course / Subject",
        coerce=int,
        validators=[DataRequired(message="Please select the course.")]
    )

    faculty_id = SelectField(
        "Faculty Member / Instructor",
        coerce=int,
        validators=[DataRequired(message="Please select the faculty instructor.")]
    )

    academic_year = SelectField(
        "Academic Year",
        choices=[
            ("2025-2026", "2025 - 2026"),
            ("2024-2025", "2024 - 2025"),
            ("2023-2024", "2023 - 2024")
        ],
        default="2025-2026",
        validators=[DataRequired(message="Please select an academic year.")]
    )

    semester = SelectField(
        "Semester",
        choices=[
            ("Semester 1", "Semester 1"),
            ("Semester 2", "Semester 2"),
            ("Semester 3", "Semester 3"),
            ("Semester 4", "Semester 4"),
            ("Semester 5", "Semester 5"),
            ("Semester 6", "Semester 6"),
            ("Semester 7", "Semester 7"),
            ("Semester 8", "Semester 8")
        ],
        default="Semester 3",
        validators=[DataRequired(message="Please select your semester.")]
    )

    # 5 Key Evaluation Dimensions (Scale 1 to 5)
    teaching_quality = IntegerField(
        "Teaching Quality & Concept Clarity",
        validators=[
            DataRequired(message="Please rate teaching quality."),
            NumberRange(min=1, max=5, message="Rating must be between 1 and 5.")
        ],
        default=5
    )

    course_content = IntegerField(
        "Course Syllabus & Content Coverage",
        validators=[
            DataRequired(message="Please rate course content."),
            NumberRange(min=1, max=5, message="Rating must be between 1 and 5.")
        ],
        default=5
    )

    punctuality = IntegerField(
        "Punctuality, Regularity & Communication",
        validators=[
            DataRequired(message="Please rate punctuality."),
            NumberRange(min=1, max=5, message="Rating must be between 1 and 5.")
        ],
        default=5
    )

    doubt_solving = IntegerField(
        "Doubt Solving, Mentorship & Approachability",
        validators=[
            DataRequired(message="Please rate doubt solving."),
            NumberRange(min=1, max=5, message="Rating must be between 1 and 5.")
        ],
        default=5
    )

    lab_work_fairness = IntegerField(
        "Practical Guidance & Evaluation Fairness",
        validators=[
            DataRequired(message="Please rate practical guidance."),
            NumberRange(min=1, max=5, message="Rating must be between 1 and 5.")
        ],
        default=5
    )

    # Qualitative Descriptive Feedback
    comments_positive = TextAreaField(
        "Key Strengths & What You Enjoyed",
        validators=[
            Optional(),
            Length(max=1000, message="Feedback cannot exceed 1000 characters.")
        ]
    )

    comments_improvement = TextAreaField(
        "Suggestions for Improvement / Constructive Advice",
        validators=[
            Optional(),
            Length(max=1000, message="Suggestions cannot exceed 1000 characters.")
        ]
    )

    submit = SubmitField("Submit Anonymous Feedback")


class FeedbackFilterForm(FlaskForm):
    """
    Filter form for Dashboard and Feedback Explorer.
    """
    department = SelectField("Department", coerce=str, default="")
    course = SelectField("Course", coerce=str, default="")
    faculty = SelectField("Faculty", coerce=str, default="")
    semester = SelectField("Semester", coerce=str, default="")
    min_rating = SelectField(
        "Min Rating",
        choices=[
            ("", "All Ratings"),
            ("4.0", "★ 4.0 & above (Excellent)"),
            ("3.0", "★ 3.0 & above (Good)"),
            ("2.0", "★ 2.0 & above (Needs Attention)"),
            ("1.0", "★ 1.0 & above (Critical)")
        ],
        default=""
    )

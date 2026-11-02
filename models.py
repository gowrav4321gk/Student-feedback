from datetime import datetime, timezone
from database import db


def utc_now():
    """Returns current UTC datetime (compatible with Python 3.14+)."""
    return datetime.now(timezone.utc)


class Department(db.Model):
    """
    Represents an Academic Department in the college (e.g., CSE, ECE).
    """
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    faculty_members = db.relationship("Faculty", backref="department", lazy=True, cascade="all, delete-orphan")
    courses = db.relationship("Course", backref="department", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Department {self.code} - {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "faculty_count": len(self.faculty_members),
            "course_count": len(self.courses)
        }


class Faculty(db.Model):
    """
    Represents a Faculty member teaching courses.
    """
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    experience_years = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    courses = db.relationship("Course", backref="instructor", lazy=True)

    def __repr__(self):
        return f"<Faculty {self.name} ({self.designation})>"

    def get_feedback_count(self):
        return len(self.feedbacks)

    def get_average_rating(self):
        if not self.feedbacks:
            return 0.0
        return round(sum(f.overall_rating for f in self.feedbacks) / len(self.feedbacks), 2)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "designation": self.designation,
            "department": self.department.code if self.department else "N/A",
            "department_id": self.department_id,
            "email": self.email,
            "experience_years": self.experience_years,
            "feedback_count": self.get_feedback_count(),
            "average_rating": self.get_average_rating()
        }


class Course(db.Model):
    """
    Represents an Academic Course offered by a department.
    """
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, default=3)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    def __repr__(self):
        return f"<Course {self.code} - {self.name}>"

    def get_feedback_count(self):
        return len(self.feedbacks)

    def get_average_rating(self):
        if not self.feedbacks:
            return 0.0
        return round(sum(f.overall_rating for f in self.feedbacks) / len(self.feedbacks), 2)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "department": self.department.code if self.department else "N/A",
            "department_id": self.department_id,
            "semester": self.semester,
            "credits": self.credits,
            "instructor": self.instructor.name if self.instructor else "Unassigned",
            "feedback_count": self.get_feedback_count(),
            "average_rating": self.get_average_rating()
        }


class Feedback(db.Model):
    """
    Anonymous Student Feedback Record.
    Note: No student ID, roll number, or IP is collected to guarantee 100% anonymity.
    """
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False, default="2025-2026")
    semester = db.Column(db.String(20), nullable=False)

    # 5 Numeric rating categories (scale: 1 to 5)
    teaching_quality = db.Column(db.Integer, nullable=False)
    course_content = db.Column(db.Integer, nullable=False)
    punctuality = db.Column(db.Integer, nullable=False)
    doubt_solving = db.Column(db.Integer, nullable=False)
    lab_work_fairness = db.Column(db.Integer, nullable=False)

    # Computed overall score (mean of the 5 criteria)
    overall_rating = db.Column(db.Float, nullable=False)

    # Qualitative descriptive feedback
    comments_positive = db.Column(db.Text, nullable=True)
    comments_improvement = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=utc_now)

    # Eagerly joined relationships for fast vectorized Pandas extraction
    department = db.relationship("Department", backref=db.backref("feedbacks", lazy=True), lazy="joined")
    course = db.relationship("Course", backref=db.backref("feedbacks", lazy=True), lazy="joined")
    faculty = db.relationship("Faculty", backref=db.backref("feedbacks", lazy=True), lazy="joined")

    def calculate_overall(self):
        """Calculates the arithmetic mean across all 5 evaluation criteria."""
        scores = [
            self.teaching_quality,
            self.course_content,
            self.punctuality,
            self.doubt_solving,
            self.lab_work_fairness
        ]
        return round(sum(scores) / len(scores), 2)

    def to_dict(self):
        """Converts model to dictionary for Pandas DataFrame construction."""
        return {
            "id": self.id,
            "department": self.department.code if self.department else "N/A",
            "department_name": self.department.name if self.department else "N/A",
            "course_code": self.course.code if self.course else "N/A",
            "course_name": self.course.name if self.course else "N/A",
            "faculty_name": self.faculty.name if self.faculty else "N/A",
            "academic_year": self.academic_year,
            "semester": self.semester,
            "teaching_quality": self.teaching_quality,
            "course_content": self.course_content,
            "punctuality": self.punctuality,
            "doubt_solving": self.doubt_solving,
            "lab_work_fairness": self.lab_work_fairness,
            "overall_rating": self.overall_rating,
            "comments_positive": self.comments_positive or "",
            "comments_improvement": self.comments_improvement or "",
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else ""
        }

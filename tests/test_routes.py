def test_index_page(client, sample_data):
    """Test landing home page returns 200 and rendered elements."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Feedback" in response.data
    assert b"Academic Quality Enhancement" in response.data


def test_about_page(client):
    """Test about documentation and viva page returns 200."""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"Technical Architecture" in response.data
    assert b"Viva Voce" in response.data


def test_dashboard_page(client, sample_data):
    """Test dashboard analytics page returns 200."""
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert b"Academic Analytics Dashboard" in response.data
    assert b"Rating Frequency Distribution" in response.data


def test_feedback_submit_get(client, sample_data):
    """Test submit feedback form page renders successfully."""
    response = client.get("/feedback/submit")
    assert response.status_code == 200
    assert b"Submit Anonymous Feedback" in response.data
    assert b"Teaching Quality" in response.data


def test_feedback_submit_post(client, sample_data):
    """Test submitting feedback creates record and redirects."""
    post_data = {
        "department_id": sample_data["department_id"],
        "course_id": sample_data["course_id"],
        "faculty_id": sample_data["faculty_id"],
        "academic_year": "2025-2026",
        "semester": "Semester 1",
        "teaching_quality": 5,
        "course_content": 5,
        "punctuality": 5,
        "doubt_solving": 5,
        "lab_work_fairness": 5,
        "comments_positive": "Outstanding professor!",
        "comments_improvement": "Keep it up."
    }
    response = client.post("/feedback/submit", data=post_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Feedback Has Been Submitted" in response.data


def test_faculty_directory_and_detail(client, sample_data):
    """Test faculty directory and detail view."""
    # List
    response = client.get("/faculty/")
    assert response.status_code == 200
    assert b"Dr. Alan Turing" in response.data

    # Detail
    fac_id = sample_data["faculty_id"]
    response_detail = client.get(f"/faculty/{fac_id}")
    assert response_detail.status_code == 200
    assert b"Dr. Alan Turing" in response_detail.data


def test_courses_directory_and_detail(client, sample_data):
    """Test courses directory and detail view."""
    # List
    response = client.get("/courses/")
    assert response.status_code == 200
    assert b"CS101" in response.data

    # Detail
    course_id = sample_data["course_id"]
    response_detail = client.get(f"/courses/{course_id}")
    assert response_detail.status_code == 200
    assert b"Intro to Computer Systems" in response_detail.data


def test_csv_export_endpoint(client, sample_data):
    """Test CSV export endpoint via Pandas."""
    response = client.get("/api/export/csv")
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "attachment; filename=student_feedback_data.csv" in response.headers.get("Content-Disposition", "")
    assert b"overall_rating" in response.data

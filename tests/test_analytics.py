import pandas as pd
import numpy as np
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


def test_feedbacks_to_dataframe(sample_data):
    """Test Pandas DataFrame conversion and column types."""
    df = feedbacks_to_dataframe(sample_data["feedbacks"])
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "overall_rating" in df.columns
    assert "teaching_quality" in df.columns
    assert df["overall_rating"].dtype in [np.float64, float]


def test_calculate_kpis(sample_data):
    """Test KPI computations using Pandas and NumPy."""
    df = feedbacks_to_dataframe(sample_data["feedbacks"])
    kpis = calculate_kpis(df)

    assert kpis["total_submissions"] == 2
    assert kpis["overall_average"] == 4.4
    assert kpis["median_rating"] == 4.4
    assert kpis["top_faculty"] == "Dr. Alan Turing"
    assert kpis["positive_sentiment_pct"] == 100.0


def test_faculty_leaderboard(sample_data):
    """Test leaderboard ranking aggregation."""
    df = feedbacks_to_dataframe(sample_data["feedbacks"])
    leaderboard = get_faculty_leaderboard(df)

    assert len(leaderboard) == 1
    assert leaderboard[0]["faculty_name"] == "Dr. Alan Turing"
    assert leaderboard[0]["rank"] == 1
    assert leaderboard[0]["avg_rating"] == 4.4


def test_chart_generation(sample_data):
    """Test Matplotlib charts generate non-empty Base64 data URIs."""
    df = feedbacks_to_dataframe(sample_data["feedbacks"])

    chart_dist = generate_rating_distribution_chart(df)
    assert chart_dist.startswith("data:image/png;base64,")

    chart_fac = generate_faculty_comparison_chart(df)
    assert chart_fac.startswith("data:image/png;base64,")

    chart_cat = generate_category_breakdown_chart(df)
    assert chart_cat.startswith("data:image/png;base64,")

    chart_course = generate_course_ratings_chart(df)
    assert chart_course.startswith("data:image/png;base64,")

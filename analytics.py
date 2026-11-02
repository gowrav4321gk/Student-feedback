"""
================================================================================
Student Feedback Analysis System - Data Analytics & Visualization Engine
================================================================================
This module powers the analytical core of the application using:
- Pandas: Data cleaning, DataFrame operations, grouping, aggregating, and pivoting.
- NumPy: Statistical calculations (mean, median, standard deviation, percentile).
- Matplotlib: High-resolution server-side chart generation rendered directly to
  Base64 images for seamless embedding in Jinja2 templates without file lock issues.
"""

import io
import base64
import numpy as np
import pandas as pd
import matplotlib

# Set non-interactive backend for server-side rendering without display server
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Palette matching our modern Navy & Blue academic design system
NAVY_PRIMARY = "#1e3a8a"      # Deep Navy
BLUE_ACCENT = "#2563eb"       # Royal Blue
BLUE_LIGHT = "#60a5fa"        # Light Blue
SUCCESS_GREEN = "#10b981"     # Emerald
WARNING_AMBER = "#f59e0b"     # Amber
DANGER_RED = "#ef4444"        # Crimson
BG_LIGHT = "#f8fafc"          # Clean card background
GRID_COLOR = "#e2e8f0"        # Subtle slate grid lines
TEXT_DARK = "#1e293b"         # Dark slate for text


def feedbacks_to_dataframe(feedbacks):
    """
    Converts a list of Feedback SQLAlchemy model instances into a Pandas DataFrame.
    Returns an empty DataFrame with expected column schema if no data exists.
    """
    if not feedbacks:
        return pd.DataFrame(columns=[
            "id", "department", "department_name", "course_code", "course_name",
            "faculty_name", "academic_year", "semester", "teaching_quality",
            "course_content", "punctuality", "doubt_solving", "lab_work_fairness",
            "overall_rating", "comments_positive", "comments_improvement", "created_at"
        ])
    
    data = [f.to_dict() for f in feedbacks]
    df = pd.DataFrame(data)

    # Ensure numeric columns are properly typed for NumPy and Pandas calculations
    numeric_cols = [
        "teaching_quality", "course_content", "punctuality",
        "doubt_solving", "lab_work_fairness", "overall_rating"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def calculate_kpis(df):
    """
    Calculates key performance indicators (KPIs) using Pandas and NumPy.
    Returns a dictionary of high-level academic metrics.
    """
    if df.empty:
        return {
            "total_submissions": 0,
            "overall_average": 0.0,
            "median_rating": 0.0,
            "std_deviation": 0.0,
            "positive_sentiment_pct": 0.0,
            "top_faculty": "None",
            "top_faculty_rating": 0.0,
            "top_course": "None",
            "top_course_rating": 0.0,
            "category_averages": {
                "teaching_quality": 0.0,
                "course_content": 0.0,
                "punctuality": 0.0,
                "doubt_solving": 0.0,
                "lab_work_fairness": 0.0
            }
        }

    total_submissions = int(len(df))

    # NumPy calculations
    ratings = df["overall_rating"].to_numpy()
    overall_average = float(np.round(np.mean(ratings), 2))
    median_rating = float(np.round(np.median(ratings), 2))
    std_deviation = float(np.round(np.std(ratings), 2))

    # Percentage of ratings >= 4.0 (Student Satisfaction Benchmark)
    satisfied_count = np.sum(ratings >= 4.0)
    positive_sentiment_pct = float(np.round((satisfied_count / total_submissions) * 100, 1))

    # Top faculty calculation using Pandas groupby
    top_faculty = "N/A"
    top_faculty_rating = 0.0
    if "faculty_name" in df.columns:
        faculty_grp = df.groupby("faculty_name")["overall_rating"].agg(["mean", "count"])
        # Consider faculty with at least 1 feedback
        if not faculty_grp.empty:
            best_f = faculty_grp.sort_values(by="mean", ascending=False).iloc[0]
            top_faculty = best_f.name
            top_faculty_rating = float(np.round(best_f["mean"], 2))

    # Top course calculation using Pandas groupby
    top_course = "N/A"
    top_course_rating = 0.0
    if "course_name" in df.columns:
        course_grp = df.groupby("course_name")["overall_rating"].agg(["mean", "count"])
        if not course_grp.empty:
            best_c = course_grp.sort_values(by="mean", ascending=False).iloc[0]
            top_course = best_c.name
            top_course_rating = float(np.round(best_c["mean"], 2))

    # Category averages across the 5 dimensions
    categories = [
        "teaching_quality", "course_content", "punctuality",
        "doubt_solving", "lab_work_fairness"
    ]
    category_averages = {
        cat: float(np.round(df[cat].mean(), 2)) for cat in categories if cat in df.columns
    }

    return {
        "total_submissions": total_submissions,
        "overall_average": overall_average,
        "median_rating": median_rating,
        "std_deviation": std_deviation,
        "positive_sentiment_pct": positive_sentiment_pct,
        "top_faculty": top_faculty,
        "top_faculty_rating": top_faculty_rating,
        "top_course": top_course,
        "top_course_rating": top_course_rating,
        "category_averages": category_averages
    }


def get_faculty_leaderboard(df):
    """
    Aggregates faculty performance using Pandas.
    Returns a list of dictionaries sorted by average score descending.
    """
    if df.empty or "faculty_name" not in df.columns:
        return []

    grouped = df.groupby("faculty_name").agg(
        total_feedback=("overall_rating", "count"),
        avg_rating=("overall_rating", "mean"),
        teaching=("teaching_quality", "mean"),
        content=("course_content", "mean"),
        punctuality=("punctuality", "mean"),
        doubt=("doubt_solving", "mean"),
        lab=("lab_work_fairness", "mean")
    ).reset_index()

    # Round numeric metrics
    for col in ["avg_rating", "teaching", "content", "punctuality", "doubt", "lab"]:
        grouped[col] = grouped[col].round(2)

    # Sort descending by overall rating, then by feedback count
    grouped = grouped.sort_values(by=["avg_rating", "total_feedback"], ascending=[False, False])
    grouped["rank"] = range(1, len(grouped) + 1)

    return grouped.to_dict(orient="records")


def get_course_summary(df):
    """
    Aggregates course ratings using Pandas.
    Returns a list of dictionaries with course metrics.
    """
    if df.empty or "course_name" not in df.columns:
        return []

    grouped = df.groupby(["course_code", "course_name"]).agg(
        total_feedback=("overall_rating", "count"),
        avg_rating=("overall_rating", "mean"),
        teaching=("teaching_quality", "mean"),
        content=("course_content", "mean")
    ).reset_index()

    grouped["avg_rating"] = grouped["avg_rating"].round(2)
    grouped["teaching"] = grouped["teaching"].round(2)
    grouped["content"] = grouped["content"].round(2)

    grouped = grouped.sort_values(by=["avg_rating", "total_feedback"], ascending=[False, False])
    return grouped.to_dict(orient="records")


# ------------------------------------------------------------------------------
# Matplotlib Visualization Helpers (Render directly to base64 images)
# ------------------------------------------------------------------------------

def _fig_to_base64(fig):
    """Encodes a Matplotlib figure into a Base64 string for direct HTML embedding."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=130, facecolor="white")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close(fig)
    return f"data:image/png;base64,{image_base64}"


def generate_rating_distribution_chart(df):
    """
    Generates a Star Rating Distribution bar chart (1 to 5 Stars).
    Shows frequency and percentage of student responses.
    """
    fig, ax = plt.subplots(figsize=(6.5, 4.2))

    # Default bins for 1 to 5 stars
    stars = [1, 2, 3, 4, 5]
    counts = [0, 0, 0, 0, 0]

    if not df.empty and "overall_rating" in df.columns:
        # Round overall rating to nearest integer (1 to 5)
        rounded_ratings = np.clip(np.round(df["overall_rating"]), 1, 5).astype(int)
        val_counts = rounded_ratings.value_counts().to_dict()
        counts = [val_counts.get(s, 0) for s in stars]

    labels = ["1 Star\n(Poor)", "2 Stars\n(Fair)", "3 Stars\n(Good)", "4 Stars\n(Very Good)", "5 Stars\n(Excellent)"]
    bar_colors = [DANGER_RED, WARNING_AMBER, BLUE_LIGHT, BLUE_ACCENT, NAVY_PRIMARY]

    bars = ax.bar(labels, counts, color=bar_colors, width=0.55, edgecolor="#cbd5e1", linewidth=1.2, zorder=3)

    # Add numeric labels on top of bars
    total = sum(counts)
    for bar in bars:
        height = bar.get_height()
        pct = (height / total * 100) if total > 0 else 0
        ax.annotate(f"{height}\n({pct:.0f}%)" if height > 0 else "0",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom",
                    fontsize=9, fontweight="bold", color=TEXT_DARK)

    ax.set_title("Student Rating Distribution (1 - 5 Stars)", fontsize=13, fontweight="bold", color=NAVY_PRIMARY, pad=15)
    ax.set_ylabel("Number of Submissions", fontsize=10, fontweight="bold", color=TEXT_DARK)
    ax.set_ylim(0, max(counts) * 1.25 if max(counts) > 0 else 5)
    ax.grid(axis="y", linestyle="--", alpha=0.6, color=GRID_COLOR, zorder=0)
    ax.set_facecolor(BG_LIGHT)
    fig.patch.set_facecolor("white")

    # Spines
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")

    return _fig_to_base64(fig)


def generate_faculty_comparison_chart(df):
    """
    Generates a horizontal bar chart comparing faculty average scores
    against the college excellence benchmark (4.0/5.0).
    """
    fig, ax = plt.subplots(figsize=(7.2, 4.2))

    if df.empty or "faculty_name" not in df.columns:
        ax.text(0.5, 0.5, "No faculty feedback data available yet.",
                ha="center", va="center", color="#64748b", fontsize=12)
        ax.axis("off")
        return _fig_to_base64(fig)

    grp = df.groupby("faculty_name")["overall_rating"].agg(["mean", "count"]).reset_index()
    grp["mean"] = grp["mean"].round(2)
    grp = grp.sort_values(by="mean", ascending=True)  # ascending so top appears on top in horizontal bar

    names = grp["faculty_name"].tolist()
    scores = grp["mean"].tolist()

    # Dynamic colors: blue for >= 4.0, amber for < 4.0
    colors = [BLUE_ACCENT if s >= 4.0 else WARNING_AMBER for s in scores]

    bars = ax.barh(names, scores, color=colors, height=0.55, edgecolor="#cbd5e1", zorder=3)

    # Value annotations on each bar
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f" {width:.2f} ★",
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha="left", va="center",
                    fontsize=9.5, fontweight="bold", color=TEXT_DARK)

    # Benchmark target line at 4.0
    ax.axvline(4.0, color=SUCCESS_GREEN, linestyle="--", linewidth=1.8, label="Benchmark Target (4.0 ★)", zorder=4)

    ax.set_title("Faculty Performance Comparison", fontsize=13, fontweight="bold", color=NAVY_PRIMARY, pad=15)
    ax.set_xlabel("Average Rating (Out of 5.0)", fontsize=10, fontweight="bold", color=TEXT_DARK)
    ax.set_xlim(0, 5.5)
    ax.legend(loc="lower right", framealpha=0.9, fontsize=9)
    ax.grid(axis="x", linestyle="--", alpha=0.6, color=GRID_COLOR, zorder=0)
    ax.set_facecolor(BG_LIGHT)
    fig.patch.set_facecolor("white")

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")

    return _fig_to_base64(fig)


def generate_category_breakdown_chart(df):
    """
    Generates a grouped bar chart for the 5 core evaluation dimensions:
    Teaching Quality, Course Content, Punctuality, Doubt Solving, Lab Guidance.
    """
    fig, ax = plt.subplots(figsize=(6.8, 4.2))

    categories = [
        ("Teaching\nQuality", "teaching_quality"),
        ("Course\nContent", "course_content"),
        ("Punctuality &\nComms", "punctuality"),
        ("Doubt\nSolving", "doubt_solving"),
        ("Lab Work\nFairness", "lab_work_fairness")
    ]

    names = [c[0] for c in categories]
    values = []

    for _, col in categories:
        if not df.empty and col in df.columns:
            values.append(round(float(df[col].mean()), 2))
        else:
            values.append(0.0)

    colors = ["#1e40af", "#2563eb", "#3b82f6", "#60a5fa", "#0284c7"]
    bars = ax.bar(names, values, color=colors, width=0.52, edgecolor="#cbd5e1", zorder=3)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.2f} / 5",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom",
                    fontsize=9.5, fontweight="bold", color=TEXT_DARK)

    ax.set_title("Average Ratings by Dimension", fontsize=13, fontweight="bold", color=NAVY_PRIMARY, pad=15)
    ax.set_ylabel("Score (Scale 1 to 5)", fontsize=10, fontweight="bold", color=TEXT_DARK)
    ax.set_ylim(0, 5.7)
    ax.grid(axis="y", linestyle="--", alpha=0.6, color=GRID_COLOR, zorder=0)
    ax.set_facecolor(BG_LIGHT)
    fig.patch.set_facecolor("white")

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")

    return _fig_to_base64(fig)


def generate_course_ratings_chart(df):
    """
    Generates a vertical bar chart displaying average student rating per course.
    """
    fig, ax = plt.subplots(figsize=(7.0, 4.2))

    if df.empty or "course_name" not in df.columns:
        ax.text(0.5, 0.5, "No course feedback data available yet.",
                ha="center", va="center", color="#64748b", fontsize=12)
        ax.axis("off")
        return _fig_to_base64(fig)

    grp = df.groupby(["course_code"])["overall_rating"].agg(["mean", "count"]).reset_index()
    grp["mean"] = grp["mean"].round(2)
    grp = grp.sort_values(by="mean", ascending=False)

    codes = grp["course_code"].tolist()
    ratings = grp["mean"].tolist()

    bars = ax.bar(codes, ratings, color=NAVY_PRIMARY, width=0.5, edgecolor="#cbd5e1", zorder=3)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom",
                    fontsize=9.5, fontweight="bold", color=TEXT_DARK)

    ax.set_title("Course Ratings Overview", fontsize=13, fontweight="bold", color=NAVY_PRIMARY, pad=15)
    ax.set_ylabel("Average Rating (Out of 5.0)", fontsize=10, fontweight="bold", color=TEXT_DARK)
    ax.set_ylim(0, 5.5)
    ax.grid(axis="y", linestyle="--", alpha=0.6, color=GRID_COLOR, zorder=0)
    ax.set_facecolor(BG_LIGHT)
    fig.patch.set_facecolor("white")

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")

    return _fig_to_base64(fig)

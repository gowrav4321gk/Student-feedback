# Student Feedback Analysis System
> **An Academic Full-Stack Python & Data Analysis Web Application**  
> *Designed for B.Tech Computer Science & Engineering College Project Demonstration & Evaluation*

---

## 1. Project Overview

The **Student Feedback Analysis System** is an end-to-end web platform designed to collect **100% anonymous** student course and faculty evaluations, process empirical ratings using **Pandas** and **NumPy**, and present actionable insights through an interactive dashboard powered by **Matplotlib** charts.

### The Problem It Solves
- **Eliminates Fear of Bias:** Traditional evaluations often suffer from student hesitation. This system collects zero roll numbers, emails, or IP addresses, ensuring pure anonymity.
- **Multi-Dimensional Metrics:** Evaluates faculty performance across 5 foundational dimensions: *Teaching Quality & Concept Clarity*, *Course Content & Syllabus Coverage*, *Punctuality & Communication*, *Doubt Solving & Mentorship*, and *Practical Guidance & Evaluation Fairness*.
- **Data-Driven Decision Making:** Aggregates feedback instantly with Pandas and NumPy rather than tedious manual paperwork.
- **Accreditation Ready:** Generates statistical indices, standard deviation metrics, and downloadable CSV audit sheets for NBA/NAAC institutional accreditation reviews.

---

## 2. Technology Stack

### Frontend
- **HTML5 & Jinja2:** Semantic document markup with template inheritance (`base.html`).
- **CSS3:** Custom stylesheet (`static/css/style.css`) implementing a light aesthetic with dark navy headers (`#1e3a8a`), royal blue accents (`#2563eb`), cards with subtle box-shadows, and rounded corners.
- **Bootstrap 5 (v5.3.3):** Responsive grid layout, modals, navigation bar, badges, and responsive tables.
- **JavaScript (ES6):** Interactive 5-star rating widget, dynamic cascading dropdowns (`Department` $\rightarrow$ `Course` & `Faculty`) via Fetch API, and real-time textarea character limits.

### Backend
- **Python 3:** Application programming language.
- **Flask:** Lightweight WSGI web framework utilizing the **Application Factory** pattern and modular **Blueprints**.
- **Flask-SQLAlchemy:** Object-Relational Mapping (ORM) for relational models with foreign keys, cascaded relationships, and eager joined loading.
- **Flask-WTF & WTForms:** Server-side CSRF protection, input sanitization, and 1–5 range validators.
- **Pandas:** Vectorized DataFrame transformations, `groupby` aggregations, rankings, and CSV export.
- **NumPy:** Statistical calculations including arithmetic mean ($\mu$), median, sample standard deviation ($\sigma$), and benchmark percentages.
- **Matplotlib (Agg Backend):** Headless, server-side publication-quality chart rendering encoded in-memory as Base64 strings.
- **pytest:** Automated test suite with 18 comprehensive unit and integration tests.

### Database
- **MySQL (Primary):** Relational database with full schema provided in `schema.sql`.
- **PyMySQL:** Pure-Python MySQL client.
- **SQLite (Automatic Fallback):** Automatically activates if MySQL credentials are not yet configured on the local computer, allowing instant zero-friction evaluation.
- **Environment Management:** Powered by `.env` and `python-dotenv` with placeholder template `.env.example`.

---

## 3. Project Directory Architecture

```
student-feedback-system/
├── .env                          # Local environment variables (DO NOT commit credentials)
├── .env.example                  # Template configuration for deployment
├── requirements.txt              # Pinned Python package dependencies
├── schema.sql                    # Pure MySQL relational database schema
├── README.md                     # Comprehensive documentation & evaluation guide
├── app.py                        # Application factory & WSGI server entry point
├── config.py                     # Config classes (Development, Testing, Production, MySQL/SQLite)
├── database.py                   # SQLAlchemy db extension instance
├── models.py                     # Department, Faculty, Course, and Feedback models
├── forms.py                      # Flask-WTF input validation forms
├── analytics.py                  # Pandas & NumPy analysis engine + Matplotlib chart visualizer
├── seed.py                       # Populates 140+ realistic feedback entries for college demo
├── routes/
│   ├── __init__.py
│   ├── main.py                   # Landing page (/), about page (/about), demo seed (/seed-demo)
│   ├── feedback.py               # Form submission (/feedback/submit), explorer (/feedback/explorer)
│   ├── dashboard.py              # Analytics dashboard with KPI cards & 4 Matplotlib charts
│   ├── faculty.py                # Faculty directory & individual analytical profiles
│   ├── courses.py                # Courses directory & syllabus feedback breakdown
│   └── api.py                    # AJAX dynamic cascading dropdowns & Pandas CSV export
├── static/
│   ├── css/
│   │   └── style.css             # Navy & Blue academic design system with card shadows
│   └── js/
│       └── main.js               # Star rating widget, dynamic dropdowns, character counters
├── templates/
│   ├── base.html                 # Master layout template (navbar, flash alerts, footer)
│   ├── index.html                # Hero landing page & system overview
│   ├── submit_feedback.html      # Interactive 5-star student feedback submission form
│   ├── feedback_success.html     # Confirmation receipt with anonymity assurance
│   ├── dashboard.html            # Main analytics dashboard with 4 Matplotlib charts
│   ├── faculty_list.html         # Faculty performance directory & rankings
│   ├── faculty_detail.html       # Individual instructor deep-dive analytics & student comments
│   ├── course_list.html          # Course directory & ratings
│   ├── course_detail.html        # Course detail breakdown
│   ├── feedback_explorer.html    # Filterable database search & audit table
│   ├── about.html                # Technical documentation, formulas, and viva defense FAQ
│   ├── 404.html                  # Custom 404 Not Found error page
│   └── 500.html                  # Custom 500 Internal Server Error page
└── tests/
    ├── __init__.py
    ├── conftest.py               # Pytest test client and in-memory SQLite fixtures
    ├── test_models.py            # Unit tests for models and arithmetic mean calculations
    ├── test_forms.py             # Form validation and range constraint tests
    ├── test_analytics.py         # Pandas DataFrame, NumPy stats, and chart generation tests
    └── test_routes.py            # End-to-end HTTP route integration tests
```

---

## 4. Installation & Local Setup

### Step 1: Clone or Open the Project
```bash
cd /home/hosuri-chandra-hass/.gemini/antigravity/scratch/student-feedback-system
```

### Step 2: Create and Activate Virtual Environment (`venv`)
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and set your credentials:
```ini
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=btech-cse-student-feedback-system-secret-key-2025

# Database Options
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_feedback_db
DB_USER=root
DB_PASSWORD=your_mysql_password
```
> **Smart Fallback Feature:** If MySQL is not currently running or credentials are empty, the application automatically logs an informational notice and falls back to a local SQLite database (`instance/student_feedback.db`). This ensures the app runs smoothly during viva presentations even without a local MySQL server!

### Step 5: (Optional) Initialize MySQL Database
If using MySQL server locally:
```bash
mysql -u root -p < schema.sql
```

### Step 6: Populate Realistic Demo Data
Run the seeder script to instantly populate 3 departments, 6 faculty members, 8 courses, and 140+ realistic feedback responses:
```bash
python seed.py
```

### Step 7: Launch the Application
```bash
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 5. Running Automated Tests

The project includes an automated test suite implemented with `pytest`. It verifies database relations, form validations, Pandas aggregations, NumPy calculations, Matplotlib chart rendering, and Flask HTTP routing.

Run all 18 automated tests with:
```bash
pytest -v
```

Expected output:
```
============================= test session starts ==============================
collected 18 items

tests/test_analytics.py::test_feedbacks_to_dataframe PASSED              [  5%]
tests/test_analytics.py::test_calculate_kpis PASSED                      [ 11%]
tests/test_analytics.py::test_faculty_leaderboard PASSED                 [ 16%]
tests/test_analytics.py::test_chart_generation PASSED                    [ 22%]
tests/test_forms.py::test_feedback_form_valid PASSED                     [ 27%]
tests/test_forms.py::test_feedback_form_invalid_rating_range PASSED      [ 33%]
tests/test_models.py::test_department_creation PASSED                    [ 38%]
tests/test_models.py::test_faculty_average_rating PASSED                 [ 44%]
tests/test_models.py::test_course_average_rating PASSED                  [ 50%]
tests/test_models.py::test_feedback_arithmetic_mean PASSED               [ 55%]
tests/test_routes.py::test_index_page PASSED                             [ 61%]
tests/test_routes.py::test_about_page PASSED                             [ 66%]
tests/test_routes.py::test_dashboard_page PASSED                         [ 72%]
tests/test_routes.py::test_feedback_submit_get PASSED                    [ 77%]
tests/test_routes.py::test_feedback_submit_post PASSED                   [ 83%]
tests/test_routes.py::test_faculty_directory_and_detail PASSED           [ 88%]
tests/test_routes.py::test_courses_directory_and_detail PASSED           [ 94%]
tests/test_routes.py::test_csv_export_endpoint PASSED                    [100%]

============================== 18 passed in 3.29s ==============================
```

---

## 6. Key Features & Walkthrough

1. **Anonymous Student Feedback Form (`/feedback/submit`):**
   - Interactive star rating widgets for all 5 criteria with instant visual descriptions (*Poor*, *Fair*, *Good*, *Very Good*, *Excellent*).
   - Dynamic cascading dropdowns via Fetch API: Selecting a department immediately loads only that department's courses and instructors.
   - Qualitative comment inputs with live character counters.
   - Server-side validation with Flask-WTF preventing forged or out-of-range inputs.

2. **Analytical Executive Dashboard (`/dashboard`):**
   - **4 KPI Metric Cards:** Total Submissions, Campus Mean Score, Satisfaction Index ($\ge 4.0\star$), and Top Ranked Faculty.
   - **4 Matplotlib Analytics Charts:**
     - *Rating Frequency Distribution:* 1 to 5 stars histogram with count and percentage annotations.
     - *Faculty Comparison Bar Chart:* Horizontal ranking compared against the college's $4.0\star$ benchmark line.
     - *Category Multi-Dimensional Breakdown:* Comparative performance across the 5 evaluation dimensions.
     - *Course Overview:* Average rating by course curriculum.
   - Dynamic Department and Semester filtering.

3. **Faculty Performance Directory (`/faculty` & `/faculty/<id>`):**
   - Full instructor directory sorted by overall rating.
   - Detailed individual analytics profile showing specific class distributions and student qualitative feedback (Strengths & Areas of Improvement).

4. **Feedback Explorer & Audit Table (`/feedback/explorer`):**
   - Searchable, multi-parameter filterable table of all student feedback records.
   - **Pandas Data Export (`/api/export/csv`):** One-click download of the complete sanitized dataset in CSV format.

5. **Built-in Viva & Project Guide (`/about`):**
   - Accessible directly in the web app navigation, containing full technical architecture, KaTeX mathematical formulas, and examiner viva Q&A!

---

## 7. Mathematical & Statistical Formulas Explained

### 1. Overall Feedback Rating
For each feedback record, the overall rating is calculated as the arithmetic mean of the five 1-to-5 evaluation criteria:
$$\text{Overall Rating} = \frac{T + C + P + D + L}{5}$$
Where:
- $T$ = Teaching Quality & Concept Clarity
- $C$ = Course Content & Syllabus Coverage
- $P$ = Punctuality & Communication
- $D$ = Doubt Solving & Mentorship
- $L$ = Practical Guidance & Evaluation Fairness

### 2. Sample Standard Deviation ($\sigma$)
To gauge consensus among students, the system computes the standard deviation of ratings using NumPy:
$$s = \sqrt{\frac{1}{N - 1}\sum_{i=1}^N (R_i - \bar{R})^2}$$
- **Low Standard Deviation ($s < 0.5$):** Indicates strong student consensus.
- **High Standard Deviation ($s > 1.0$):** Indicates polarized opinions requiring department attention.

### 3. Student Satisfaction Index (%)
$$\text{Satisfaction Index} = \left(\frac{N_{R \ge 4.0}}{N_{\text{total}}}\right) \times 100$$
Denotes the percentage of evaluations that meet or exceed the college excellence benchmark ($4.0 / 5.0$).

---

## 8. College Project Evaluation & Viva FAQ

#### Q1: How did you implement CSRF protection and input security?
> **Answer:** We used **Flask-WTF** and **WTForms**. Each form renders a hidden CSRF token (`{{ form.hidden_tag() }}`) that is cryptographically validated upon submission. Additionally, ratings are strictly enforced within the $[1, 5]$ integer range using WTForms `NumberRange` validator, and textareas are sanitized to prevent script injection.

#### Q2: Why did you use `matplotlib.use('Agg')`?
> **Answer:** Standard Matplotlib uses GUI backends (like Tkinter or Qt) that require a desktop display window. In a web server environment, calling GUI plotting functions causes crashes because there is no X11 server display. By specifying `matplotlib.use('Agg')`, Matplotlib runs in headless rasterizer mode, rendering PNG graphics directly into an in-memory byte buffer (`io.BytesIO`) which is Base64 encoded and embedded directly into Jinja templates.

#### Q3: How is student privacy and anonymity strictly preserved?
> **Answer:** The database schema has no foreign key or column for student roll number, registration number, student name, email, or client IP address. Once submitted, feedback entries are stored as anonymous records, making it mathematically impossible to trace an opinion back to a specific individual student.

#### Q4: Why use Pandas instead of writing raw SQL aggregation queries?
> **Answer:** While SQL handles basic `AVG()` queries, **Pandas** provides an expressive, vectorized data science API in Python. With Pandas DataFrames, we can effortlessly compute medians, standard deviations, quantile percentiles, multi-column group-bys, and export to CSV with `df.to_csv()` in a single line, making the codebase clean and modular.

---

## 9. Academic Project Submission Checklist
- [x] Full-stack architecture (Frontend + Flask Backend + Database).
- [x] MySQL database support with `.env` credential management and `schema.sql`.
- [x] Zero-configuration SQLite fallback for instant presentation on any evaluator machine.
- [x] Pandas DataFrame grouping and aggregations.
- [x] NumPy numerical calculations (mean, median, standard deviation).
- [x] Matplotlib charts rendered dynamically in-memory.
- [x] Flask-WTF secure form handling with CSRF tokens and 1–5 range validation.
- [x] 18 automated unit and integration tests passing with `pytest`.
- [x] Database seeder with 140+ realistic feedback records.
- [x] Responsive modern dashboard with Navy/Blue academic theme, cards, and subtle shadows.
- [x] In-app About & Viva Documentation page.

---

## Deployment (Render – free)

GitHub Pages only hosts static files, so it cannot run this Flask app (it just shows the README).
Deploy to Render instead:

1. Push this folder's contents to the **root** of your GitHub repo (`render.yaml` must be at the root).
2. Go to https://render.com → **New → Blueprint** → select the repo → **Apply**.
3. Wait for the build; your app is live at `https://student-feedback.onrender.com`.

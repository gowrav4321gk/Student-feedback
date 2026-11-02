/**
 * Student Feedback Analysis System - Frontend Interactivity
 * Provides:
 * 1. Interactive 5-Star Rating click & hover handlers
 * 2. Cascading dropdowns (Department -> Courses & Faculty) via Fetch API
 * 3. Real-time character counters for qualitative comments
 * 4. Alert auto-dismissal
 */

document.addEventListener("DOMContentLoaded", function () {
    // -------------------------------------------------------------------------
    // 1. Star Rating Interactive Widgets
    // -------------------------------------------------------------------------
    const ratingBoxes = document.querySelectorAll(".star-rating-box");

    const ratingDescriptions = {
        1: "1 - Poor (Needs major improvement)",
        2: "2 - Fair (Below expectations)",
        3: "3 - Good (Satisfactory)",
        4: "4 - Very Good (Exceeds expectations)",
        5: "5 - Excellent (Outstanding performance)"
    };

    ratingBoxes.forEach(box => {
        const input = box.querySelector("input[type='number']");
        const stars = box.querySelectorAll(".star-interactive");
        const descSpan = box.querySelector(".rating-desc-text");

        function updateStars(val) {
            const num = parseInt(val, 10) || 0;
            stars.forEach(s => {
                const starVal = parseInt(s.dataset.value, 10);
                if (starVal <= num) {
                    s.classList.add("active");
                    s.textContent = "★";
                } else {
                    s.classList.remove("active");
                    s.textContent = "☆";
                }
            });
            if (descSpan && ratingDescriptions[num]) {
                descSpan.textContent = ratingDescriptions[num];
            }
        }

        // Initialize display from default input value
        if (input) {
            updateStars(input.value || 5);

            stars.forEach(star => {
                // Click sets value
                star.addEventListener("click", () => {
                    const chosenVal = star.dataset.value;
                    input.value = chosenVal;
                    updateStars(chosenVal);
                });

                // Hover preview
                star.addEventListener("mouseenter", () => {
                    const hoverVal = star.dataset.value;
                    updateStars(hoverVal);
                });
            });

            // Revert to saved value on mouse leave
            box.addEventListener("mouseleave", () => {
                updateStars(input.value);
            });
        }
    });

    // -------------------------------------------------------------------------
    // 2. Cascading Dropdown (Department -> Courses & Faculty)
    // -------------------------------------------------------------------------
    const deptSelect = document.getElementById("department_id");
    const courseSelect = document.getElementById("course_id");
    const facultySelect = document.getElementById("faculty_id");

    if (deptSelect && courseSelect) {
        deptSelect.addEventListener("change", function () {
            const deptId = this.value;
            if (!deptId) return;

            // Fetch matching courses
            fetch(`/api/courses-by-department/${deptId}`)
                .then(response => response.json())
                .then(data => {
                    courseSelect.innerHTML = '<option value="">-- Choose Course --</option>';
                    data.forEach(course => {
                        const opt = document.createElement("option");
                        opt.value = course.id;
                        opt.textContent = `${course.code} - ${course.name}`;
                        courseSelect.appendChild(opt);
                    });
                })
                .catch(err => console.error("Error loading courses:", err));

            // Fetch matching faculty
            if (facultySelect) {
                fetch(`/api/faculty-by-department/${deptId}`)
                    .then(response => response.json())
                    .then(data => {
                        facultySelect.innerHTML = '<option value="">-- Choose Instructor --</option>';
                        data.forEach(fac => {
                            const opt = document.createElement("option");
                            opt.value = fac.id;
                            opt.textContent = `${fac.name} (${fac.designation})`;
                            facultySelect.appendChild(opt);
                        });
                    })
                    .catch(err => console.error("Error loading faculty:", err));
            }
        });
    }

    // -------------------------------------------------------------------------
    // 3. Qualitative Comments Character Counters
    // -------------------------------------------------------------------------
    const textareas = document.querySelectorAll("textarea[maxlength]");
    textareas.forEach(ta => {
        const max = ta.getAttribute("maxlength");
        const counter = document.getElementById(`${ta.id}_counter`);
        if (counter) {
            const updateCount = () => {
                const remaining = max - ta.value.length;
                counter.textContent = `${ta.value.length} / ${max} characters`;
            };
            ta.addEventListener("input", updateCount);
            updateCount();
        }
    });

    // -------------------------------------------------------------------------
    // 4. Auto-dismiss Alert Messages after 5 seconds
    // -------------------------------------------------------------------------
    setTimeout(() => {
        const alerts = document.querySelectorAll(".alert.alert-dismissible");
        alerts.forEach(alert => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        });
    }, 5000);
});

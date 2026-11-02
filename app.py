import os
from flask import Flask, render_template
from config import config_by_name
from database import db


def create_app(config_name=None):
    """
    Application Factory pattern:
    Creates and configures an instance of the Flask application.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development").lower()

    app = Flask(__name__)
    config_obj = config_by_name.get(config_name, config_by_name["default"])
    app.config.from_object(config_obj)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from routes.main import main_bp
    from routes.feedback import feedback_bp
    from routes.dashboard import dashboard_bp
    from routes.faculty import faculty_bp
    from routes.courses import courses_bp
    from routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(api_bp)

    # Register custom Jinja template filters
    @app.template_filter("star_rating")
    def star_rating_filter(rating):
        """Converts a numerical rating (0.0 to 5.0) into visual star icons."""
        try:
            r = float(rating)
        except (ValueError, TypeError):
            return "☆☆☆☆☆"
        full_stars = int(round(r))
        empty_stars = 5 - full_stars
        return "★" * full_stars + "☆" * empty_stars

    @app.template_filter("rating_badge")
    def rating_badge_filter(rating):
        """Returns Bootstrap badge class depending on rating score."""
        try:
            r = float(rating)
        except (ValueError, TypeError):
            return "bg-secondary"
        if r >= 4.5:
            return "badge-excel"
        elif r >= 3.8:
            return "badge-good"
        elif r >= 3.0:
            return "badge-avg"
        else:
            return "badge-warn"

    # Global Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("500.html"), 500

    # Initialize database tables on application start
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"[App Init Warning] Could not automatically create tables: {e}")

    return app


# Root application instance for WSGI / CLI execution
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

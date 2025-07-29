import os
import shutil

try:
    from flask import Blueprint
except ImportError:
    Blueprint = None


def setup_theme(app_or_settings):
    """
    Sets up the theme assets for use in Flask or Django apps.

    - In development: serves files directly from the package.
    - In production: copies files to the project's public static directory.
    """
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    theme_name = "taktkit"
    source_dir = os.path.join(static_dir, theme_name)

    if is_flask_app(app_or_settings):
        _setup_flask(app_or_settings, source_dir, theme_name)
    elif is_django_settings(app_or_settings):
        _setup_django(app_or_settings, source_dir, theme_name)
    else:
        raise TypeError(
            "Unsupported object type: expected a Flask app or Django settings module."
        )


def is_flask_app(obj):
    return (
        Blueprint is not None
        and hasattr(obj, "register_blueprint")
        and hasattr(obj, "static_folder")
    )


def is_django_settings(obj):
    return hasattr(obj, "BASE_DIR") and hasattr(obj, "STATICFILES_DIRS")


def _setup_flask(app, source_dir, theme_name):
    target_dir = os.path.join(app.static_folder, theme_name)

    if app.debug or os.environ.get("FLASK_DEBUG") == "1":
        static_url_base = app.static_url_path.rstrip("/")
        blueprint_name = f"{theme_name}_theme"
        blueprint = Blueprint(
            blueprint_name,
            __name__,
            static_folder=source_dir,
            static_url_path=f"{static_url_base}/{theme_name}",
        )
        app.register_blueprint(blueprint)
    else:
        _copy_static_files(source_dir, target_dir)
        _maybe_warn_about_static_url(app)


def _setup_django(settings, source_dir, theme_name):
    is_debug = (
        getattr(settings, "DEBUG", False) or os.environ.get("DJANGO_DEBUG") == "1"
    )

    if is_debug:
        if source_dir not in settings.STATICFILES_DIRS:
            settings.STATICFILES_DIRS.append(source_dir)
    else:
        if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
            base_static_dir = settings.STATICFILES_DIRS[0]
        else:
            base_static_dir = os.path.join(settings.BASE_DIR, "static")

        target_dir = os.path.join(base_static_dir, theme_name)
        _copy_static_files(source_dir, target_dir)


def _copy_static_files(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, rel_path)
        os.makedirs(target_path, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_path, file)
            shutil.copy2(src_file, dst_file)


def _maybe_warn_about_static_url(app):
    static_url_path = app.static_url_path.rstrip("/")
    static_folder = os.path.basename(app.static_folder.rstrip("/\\"))

    if static_url_path != "/static" and not static_url_path.endswith(
        f"/{static_folder}"
    ):
        print(
            f"[STATIC ALERT] ⚠️  Your Flask app is using static_folder='{static_folder}' "
            f"and static_url_path='{static_url_path}'.\n"
            f"Make sure your web server is configured to serve static files at URL path '{static_url_path}'."
        )

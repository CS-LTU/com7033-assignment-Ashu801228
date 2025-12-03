def test_multiple_databases_configured(app):
    """
    Ensure that the application is configured with multiple databases:
    - default auth database
    - 'patients' bind for patient records
    """
    # Default DB URI should exist
    assert "SQLALCHEMY_DATABASE_URI" in app.config
    assert "auth.db" in app.config["SQLALCHEMY_DATABASE_URI"]

    # Second DB (bind) should exist
    binds = app.config.get("SQLALCHEMY_BINDS", {})
    assert "patients" in binds
    assert "patients.db" in binds["patients"]

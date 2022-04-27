def import_tables(app):
    from nuclei.compression_service.models import CompressionService

    # from nuclei.authentication.models import User
    # from nuclei.admin_interface.models import AdminInterface

    app.db.create_all()

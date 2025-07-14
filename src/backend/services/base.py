from src.backend.config.database import Session


class DBSessionContext:
    """
    Base context class for database session management.

    Attributes:
        db (Session): The SQLAlchemy database session.
    """

    def __init__(self, db: Session):
        self.db = db


class AppService(DBSessionContext):
    """
    Base service class that provides access to the database session.

    Inherit from this class to implement application-level services
    that require database access.
    """

    pass


class AppCRUD(DBSessionContext):
    """
    Base CRUD class that provides access to the database session.

    Inherit from this class to implement Create, Read, Update, and Delete
    operations for specific models.
    """

    pass

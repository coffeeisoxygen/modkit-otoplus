"""Modul base.py.

Modul ini merupakan fondasi untuk context session database dan service CRUD di backend.

- DBSessionContext: Kelas dasar untuk manajemen session database SQLAlchemy.
- AppService: Kelas dasar untuk service aplikasi yang membutuhkan akses database.
- AppCRUD: Kelas dasar untuk operasi CRUD model tertentu.

Semua service dan CRUD di backend sebaiknya mewarisi kelas-kelas ini agar konsisten dan mudah di-maintain.

Session yang digunakan harus berasal dari SessionLocal di src.backend.core.app_dbsetting untuk menjaga konsistensi konfigurasi database.

Hasan Maki and Copilot
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


@dataclass
class DBSessionContext:
    """Base context class for database session management.

    Attributes:
        db (Session): The SQLAlchemy database session dari SessionLocal.
    """

    db: "Session"


class AppService(DBSessionContext):
    """Base service class that provides access to the database session.

    Inherit from this class to implement application-level services
    that require database access.
    """

    pass


class AppCRUD(DBSessionContext):
    """Base CRUD class that provides access to the database session.

    Inherit from this class to implement Create, Read, Update, and Delete
    operations for specific models.
    """

    pass

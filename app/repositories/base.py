class BaseRepository:
    """Base repository keeps shared DB object."""

    def __init__(self, db) -> None:
        self.db = db

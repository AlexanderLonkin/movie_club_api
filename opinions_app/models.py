from datetime import UTC, datetime

from . import db


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(UTC)
    )
    added_by = db.Column(db.String(64))

    def to_dict(self):
        """Вернуть словарь со всеми полями мнения и их текущими значениями."""
        return dict(
            id=self.id,
            title=self.title,
            text=self.text,
            source=self.source,
            timestamp=self.timestamp,
            added_by=self.added_by
        )

    def from_dict(self, data):
        """Обновить редактируемые поля мнения из словаря data.

        Использовать только переданные title, text, source и added_by.
        Игнорировать id, timestamp и неизвестные поля.
        """
        for field in ['title', 'text', 'source', 'added_by']:
            if field in data:
                setattr(self, field, data[field])

from collections.abc import Iterable
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, instance: Any) -> Any:
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def list(self, model: Any, *conditions: Any) -> list[Any]:
        stmt = select(model)
        for condition in conditions:
            stmt = stmt.where(condition)
        return list(self.db.scalars(stmt).all())

    def get_one(self, model: Any, *conditions: Any) -> Any | None:
        stmt = select(model)
        for condition in conditions:
            stmt = stmt.where(condition)
        return self.db.scalars(stmt).first()

    def delete(self, instance: Any) -> None:
        self.db.delete(instance)

    def bulk_insert(self, instances: Iterable[Any]) -> None:
        for instance in instances:
            self.db.add(instance)
        self.db.flush()

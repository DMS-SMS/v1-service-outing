import datetime

from typing import List

from sqlalchemy import func, and_

from domain.entity import Outing
from domain.repository.outing_repository import OutingRepository
from infrastructure.mysql import MySQLHandler
from infrastructure.open_tracing import open_tracing
from infrastructure.open_tracing.open_tracing_handler import trace_service


class OutingRepositoryImpl(OutingRepository):
    def __init__(self):
        self.sql = MySQLHandler()

    @trace_service("SQL (save)", open_tracing)
    def save(self, outing: Outing):
        self.sql.db_session.add(outing)
        self.sql.db_session.commit()

    @trace_service("SQL (find)", open_tracing)
    def find_all_by_student_uuid(self, student_id):
        return self.sql.db_session.query(Outing).filter(Outing.student_uuid == func.binary(student_id)).all()

    @trace_service("SQL (find)", open_tracing)
    def find_all_by_student_uuid_and_status(self, student_uuid, status) -> List["Outing"]:
        query = self.sql.db_session.query(Outing).filter(Outing.student_uuid == func.binary(student_uuid))
        if status: query = query.filter(Outing.status == status)
        return query.all()

    @trace_service("SQL (find)", open_tracing)
    def find_by_id(self, id: str) -> Outing:
        return (self.sql.db_session.query(Outing)
                .filter(Outing.outing_uuid == func.binary(id)).first())

    @trace_service("SQL (find)", open_tracing)
    def find_by_student_uuid_and_end_time(self, student_uuid: str, time: float) -> Outing:
        return (self.sql.db_session.query(Outing)
                .filter(and_(Outing.start_time <= datetime.datetime.fromtimestamp(time),
                             Outing.end_time >= datetime.datetime.fromtimestamp(time))).first())
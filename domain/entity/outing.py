from sqlalchemy import Column, Integer, String, DateTime, Enum

from infrastructure.mysql import sql


class Outing(sql.base):
    __tablename__ = "tbl_outing"

    outing_uuid = Column(String(20), primary_key=True)
    student_uuid = Column(String(20), nullable=False)
    status = Column(Enum("-2", "-1", "0", "1", "2", "3", "4", "5"), nullable=False)
    # 0: 외출증 생성 , 1: 학부모 승인, -1: 학부모 거부, 2: 담임 확인, -2: 담임 거부, 3: 외출, 4: 외출 종료, 5: 사후제출
    situation = Column(Enum("NORMAL", "EMERGENCY"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    place = Column(String(50), nullable=False)
    reason = Column(String(150), nullable=False)

    arrival_time = Column(DateTime, nullable=True)
    accepted_teacher = Column(String(20), nullable=True)

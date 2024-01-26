from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.types import Float, DECIMAL, CHAR
from sqlalchemy.orm import relationship
from connect import engine


Base = declarative_base(bind=engine)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    group_sign = Column(CHAR(1))
    students = relationship("Student", back_populates="group")

    # __tablename__ = "groups"
    # id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # group_sign: Mapped[str] = mapped_column(String(1))


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255))
    group_id = Column(Integer, ForeignKey(Group.id, onupdate="CASCADE"))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")
    # id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # full_name: Mapped[str] = mapped_column(String)
    # group_id: Mapped[int] = mapped_column(Integer, ForeignKey("group.id"))
    # group: Mapped["Group"] = relationship(Group)


class Lecturer(Base):
    __tablename__ = "lecturers"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255))
    subjects_taught = relationship("Subject", back_populates="lecturer")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    lecturer_id = Column(Integer, ForeignKey(Lecturer.id, onupdate="CASCADE"))
    lecturer = relationship("Lecturer", back_populates="subjects_taught")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    mark = Column(Float)
    date = Column(DateTime)
    student_id = Column(Integer, ForeignKey(Student.id, onupdate="CASCADE"))
    subject_id = Column(Integer, ForeignKey(Subject.id, onupdate="CASCADE"))
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")


if __name__ == "__main__":
    Base.metadata.drop_all()
    Base.metadata.create_all()

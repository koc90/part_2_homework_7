from connect import session
from model import Student, Group, Lecturer, Subject, Grade
from faker import Faker
from datetime import datetime
from datetime import timedelta
from random import randint, choice


faker = Faker()


GROUP_SIGNS = ("A", "B", "C")
NUMBER_STUDENTS = 50
NUMBER_LECTURERS = 5
MARKS = (2.0, 3.0, 3.5, 4.0, 4.5, 5.0)

SUBJECTS = {
    1: "Mathematics",
    2: "Mechanics",
    3: "Information Technology",
    4: "Chemistry",
    5: "Descriptive Geomery",
    6: "Numerical Methods",
    7: "Physics",
}


students = dict()
lecturers = dict()


def fill_groups_table() -> None:
    counter = 1
    for sign in GROUP_SIGNS:
        group = Group(id=counter, group_sign=sign)
        counter += 1
        session.add(group)
    session.commit()


def fill_students_table() -> dict:
    global students
    counter = 1
    num_groups = len(GROUP_SIGNS)
    for _ in range(NUMBER_STUDENTS):
        person_name = faker.name()
        group_id = counter % num_groups + 1
        students[counter] = person_name
        person = Student(id=counter, full_name=person_name, group_id=group_id)
        counter += 1
        session.add(person)
    session.commit()
    return students


def fill_lecturers_table() -> dict:
    counter = 1
    global lecturers
    for _ in range(NUMBER_LECTURERS):
        person_name = faker.name()
        lecturers[counter] = person_name
        person = Lecturer(id=counter, full_name=person_name)
        counter += 1
        session.add(person)
    session.commit()

    return lecturers


def fill_subjects_table() -> None:
    for key, value in SUBJECTS.items():
        lect_id = (key - 1) % NUMBER_LECTURERS + 1
        subject = Subject(id=key, name=value, lecturer_id=lect_id)
        session.add(subject)
    session.commit()


def create_list_of_dates() -> list[datetime]:
    list_of_dates = []
    classes_start = datetime(year=2023, month=10, day=2).date()

    for i in range(30):
        date = classes_start + timedelta(days=i)

        if date.weekday() not in [5, 6]:
            list_of_dates.append(str(date))

    # print(list_of_dates)
    return list_of_dates


def fill_grades_table() -> list:
    counter = 1
    dates = create_list_of_dates()
    for student_id in students.keys():
        num_grades = randint(16, 20)
        for i in range(num_grades):
            mark = choice(MARKS)
            subject_id = choice(list(SUBJECTS.keys()))
            date = choice(dates)
            grade = Grade(
                id=counter,
                mark=mark,
                date=date,
                subject_id=subject_id,
                student_id=student_id,
            )
            counter += 1
            session.add(grade)
    session.commit()

    return dates


FILL = [
    fill_groups_table,
    fill_students_table,
    fill_lecturers_table,
    fill_subjects_table,
    fill_grades_table,
]


def fill_all_tables():
    data_list = []
    for table_filler in FILL:
        data = table_filler()
        data_list.append(data)

    return data_list


if __name__ == "__main__":
    data_list = fill_all_tables()
    print(students)
    print(lecturers)

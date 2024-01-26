from connect import session
from sqlalchemy import func, desc
from model import Group, Student, Lecturer, Subject, Grade
from seeds import SUBJECTS


def double_print(something, file):
    print(something)
    print(something, file=file)


def print_result_row_by_row(query: str, result: list, num: int, file):
    double_print(f"\n\nQuery number {num}:", file=file)
    double_print(query, file=file)
    double_print("\n Result:", file=file)
    for row in result:
        double_print(row, file=file)


def round_result(result, pos):
    new_result = []
    for row in result:
        temp_row = list(row)
        temp_row[pos] = round(row[pos], 2)
        new_row = tuple(temp_row)
        new_result.append(new_row)

    return new_result

    return result


def select_1() -> list[str, list]:
    # Znajdź 5 studentów z najwyższą średnią ocen ze wszystkich przedmiotów.
    query = (
        session.query(
            Student.full_name,
            func.avg(Grade.mark).label("average"),
            # func.round(func.avg(Grade.mark), 2) działa na zmiennej Decimal, na Float niestety nie
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("average"))
        .limit(5)
    )

    result = query.all()

    result = round_result(result, 1)

    return [query, result]


def select_2() -> list[str, list]:
    # Znajdź studenta z najwyższą średnią ocen z określonego przedmiotu
    query = (
        session.query(
            Subject.name,
            Student.full_name,
            func.avg(Grade.mark).label("average"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .group_by(Subject.id)
        .group_by(Student.id)
        .filter(Subject.name == SUBJECTS[1])
        .order_by(desc("average"))
        .limit(1)
    )

    result = query.all()

    result = round_result(result, 2)
    return [query, result]


def select_3() -> list[str, list]:
    # Znajdź średni wynik w grupach dla określonego przedmiotu.
    query = (
        session.query(
            Subject.name,
            Group.group_sign,
            func.avg(Grade.mark).label("average"),
        )
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .join(Group)
        .group_by(Subject.id)
        .group_by(Group.id)
        .filter(Subject.name == SUBJECTS[4])
    )

    result = query.all()

    result = round_result(result, 2)
    return [query, result]


def select_4() -> list[str, list]:
    # Znajdź średni wynik w grupie (w całej tabeli ocen).
    query = (
        session.query(
            Group.group_sign,
            func.avg(Grade.mark).label("average"),
        )
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .join(Group)
        .group_by(Group.id)
        .order_by(Group.group_sign)
    )

    result = query.all()

    result = round_result(result, 1)

    return [query, result]


# Znajdź przedmioty, których uczy określony wykładowca.


def select_5() -> list[str, list]:
    # Znajdź przedmioty, których uczy określony wykładowca.
    query = (
        session.query(
            Lecturer.full_name,
            Subject.name,
        )
        .select_from(Subject)
        .join(Lecturer)
        .filter(Lecturer.id == 2)
    )

    result = query.all()
    return [query, result]


def select_6() -> list[str, list]:
    # Znajdź listę studentów w określonej grupie.
    query = (
        session.query(
            Group.group_sign,
            Student.full_name,
        )
        .select_from(Group)
        .join(Student)
        .filter(Group.group_sign == "C")
    )

    result = query.all()
    return [query, result]


def select_7() -> list[str, list]:
    # Znajdź oceny studentów w określonej grupie z danego przedmiotu.
    query = (
        session.query(Group.group_sign, Subject.name, Student.full_name, Grade.mark)
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Group.group_sign == "B")
        .filter(Subject.name == SUBJECTS[6])
    )

    result = query.all()
    return [query, result]


def select_8() -> list[str, list]:
    # Znajdź średnią ocenę wystawioną przez określonego wykładowcę z jego przedmiotów.
    query = (
        session.query(Lecturer.full_name, func.avg(Grade.mark).label("average"))
        .select_from(Grade)
        .join(Subject)
        .join(Lecturer)
        .group_by(Lecturer.full_name)
        .filter(Lecturer.id == 5)
    )

    result = query.all()

    result = round_result(result, 1)

    return [query, result]


def select_9() -> list[str, list]:
    # Znajdź listę przedmiotów zaliczonych przez danego studenta.
    query = (
        session.query(
            Student.full_name, Subject.name, func.avg(Grade.mark).label("average")
        )
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .filter(Student.id == 7)
        .group_by(Student.full_name)
        .group_by(Subject.name)
        .order_by(desc("average"))
    )

    # Chciałam dodać jeszcze warunek, że średnia ma być większa lub równa 3.0 ale nic z tego nie wyszło

    result = query.all()

    result = round_result(result, 2)

    print(f"\n\nQuery number {9}:")
    print(query)
    print("\n Result:")
    for row in result:
        print(row)

    # return [query, result]

    new_query = str(query) + f"\n\nWHERE average >= 3.0 - execuded by Python"

    new_result = []
    for row in result:
        if row[2] >= 3:
            new_result.append(row)

    return [new_query, new_result]


def select_10() -> list[str, list]:
    # Znajdź listę kursów prowadzonych przez określonego wykładowcę dla określonego studenta.
    query = (
        session.query(Student.full_name, Lecturer.full_name, Subject.name)
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .join(Lecturer)
        .filter(Student.id == 7)
        .filter(Lecturer.id == 2)
        .group_by(Subject.name)
        .group_by(Student.full_name)
        .group_by(Lecturer.full_name)
    )

    result = query.all()

    print()

    return [query, result]


def select_11() -> list[str, list]:
    # Średnia ocena, jaką określony wykładowca wystawił pewnemu studentowi.
    query = (
        session.query(Student.full_name, Lecturer.full_name, func.avg(Grade.mark))
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .join(Lecturer)
        .filter(Student.id == 7)
        .filter(Lecturer.id == 2)
        .group_by(Student.full_name)
        .group_by(Lecturer.full_name)
    )

    result = query.all()

    result = round_result(result, 2)

    return [query, result]


def select_12() -> list[str, list]:
    # Oceny studentów w określonej grupie z określonego przedmiotu na ostatnich zajęciach.

    support_query = session.query(func.max(Grade.date)).select_from(Grade)
    support_result = support_query.all()
    last_date = support_result[0][0]

    query = (
        session.query(
            Group.group_sign,
            Subject.name,
            Grade.date,
            Student.full_name,
            Grade.mark,
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Group.group_sign == "B")
        .filter(Subject.name == SUBJECTS[6])
        .filter(Grade.date == last_date)
        .order_by(desc(Grade.date))
    )

    result = query.all()

    return [query, result]


SELECTS = [
    select_1,
    select_2,
    select_3,
    select_4,
    select_5,
    select_6,
    select_7,
    select_8,
    select_9,
    select_10,
    select_11,
    select_12,
]



def my_selects():
    query_result_dict = dict()

    for i in SELECTS:
        [query, result] = i()

        query_result_dict[query] = result

    counter = 1
    with open("results.txt", "w") as f:
        for key, value in query_result_dict.items():
            print_result_row_by_row(key, value, counter, f)
            counter += 1



if __name__ == "__main__":
    my_selects()
    

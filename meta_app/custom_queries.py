from django.db import connection


def average_all():
    """
    select s.id ,s.full_name, avg(te.grade), count(te), max(te.grade), min(te.grade) from tests_testexecuted  te join "Student" s on s.id = te.student_id_id
group by s.id, te.student_id_id;
    """
    with connection.cursor() as cursor:
        cursor.execute("""
        select s.id ,s.full_name, avg(te.grade), count(te), max(te.grade), min(te.grade) from tests_testexecuted  te join "Student" s on s.id = te.student_id_id
group by s.id, te.student_id_id;
        """)
        rows = cursor.fetchall()
        ret_list = [{"id": row[0], "Name": row[1], "Average": row[2], "Tests_Done": row[3], "Maximum_grade": row[4], "Minimum_grade": row[5]} for row in rows]
        return ret_list


def average_student(pk):
    """ select s.id ,s.full_name, avg(te.grade), count(te), max(te.grade), min(te.grade) from tests_testexecuted  te join "Student" s on s.id = 5 and te.student_id_id = 5
        group by s.id, te.student_id_id;"""
    with connection.cursor() as cursor:
        cursor.execute("""
        select s.id ,s.full_name, avg(te.grade), count(te), max(te.grade), min(te.grade) from tests_testexecuted  te join "Student" s on s.id = %s and te.student_id_id = %s
        group by s.id, te.student_id_id;""", [pk, pk])
        row = cursor.fetchall()
        ret_list = [{"id": row[0], "Name": row[1], "Average": row[2], "Tests_Done": row[3], "Maximum_grade": row[4], "Minimum_grade": row[5]} for row in row]
        return ret_list



def average_all_sorted():
    """
    select s.id ,s.full_name, avg(te.grade), count(te), max(te.grade), min(te.grade) from tests_testexecuted  te join "Student" s on s.id = te.student_id_id
group by s.id, te.student_id_id;
    """
    with connection.cursor() as cursor:
        cursor.execute("""
        select s.id ,s.full_name, avg(te.grade), count(te), max(te.grade), min(te.grade) from tests_testexecuted  te join "Student" s on s.id = te.student_id_id
group by s.id, te.student_id_id order by avg(te.grade) desc;
        """)
        rows = cursor.fetchall()
        ret_list = [{"id": row[0], "Name": row[1], "Average": row[2], "Tests_Done": row[3], "Maximum_grade": row[4], "Minimum_grade": row[5]} for row in rows]
        return ret_list

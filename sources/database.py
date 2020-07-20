import sqlite3


class DataBase(object):
    @staticmethod
    def connect_database(database):
        connect = sqlite3.connect(database)
        return connect

    @staticmethod
    def insert_into_subject(connect, name):
        cur = connect.cursor()
        cur.execute('''INSERT INTO subject (name_subject) VALUES(?)''', (name,))
        connect.commit()
        cur.close()

    @staticmethod
    def insert_into_lecturer(connect, SNP):
        cur = connect.cursor()
        cur.execute('''INSERT INTO lecturer (SNP) VALUES(?)''', (SNP,))
        connect.commit()
        cur.close()

    @staticmethod
    def insert_into_classroom(connect, classroom_number):
        cur = connect.cursor()
        cur.execute('''INSERT INTO classroom (classroom_number) VALUES(?)''', (classroom_number,))
        connect.commit()
        cur.close()

    @staticmethod
    def insert_into_groups(connect, group_name):
        cur = connect.cursor()
        cur.execute('''INSERT INTO groups (group_name) VALUES(?)''', (group_name,))
        connect.commit()
        cur.close()

    @staticmethod
    def insert_into_timetable(connect, id_group, id_subject, id_lecturer, id_classroom, date_timetable,
                              lesson_number, comment):
        cur = connect.cursor()
        cur.execute(
            '''INSERT INTO timetable 
            (id_group,
            id_subject, 
            id_lecturer, 
            id_classroom, 
            date_timetable, 
            lesson_number,
            comment) 
            VALUES(?, ?, ?, ?, ?, ?, ?)''',
            (id_group, id_subject, id_lecturer, id_classroom, date_timetable, lesson_number, comment))
        connect.commit()
        cur.close()

    @staticmethod
    def delete_from_subject(connect, id):
        cursor = connect.cursor()
        cursor.execute(
            '''DELETE FROM subject
            WHERE name_subject = ?
            ''',
            (id,))
        connect.commit()
        cursor.close()

    @staticmethod
    def delete_from_lecturer(connect, id):
        cursor = connect.cursor()
        cursor.execute(
            '''DELETE FROM lecturer
            WHERE SNP = ?
            ''',
            (id,))
        connect.commit()
        cursor.close()

    @staticmethod
    def delete_from_classroom(connect, id):
        cursor = connect.cursor()
        cursor.execute(
            '''DELETE FROM classroom
            WHERE classroom_number = ?
            ''',
            (id,))
        connect.commit()
        cursor.close()

    @staticmethod
    def delete_from_groups(connect, id):
        cursor = connect.cursor()
        cursor.execute(
            '''DELETE FROM groups
            WHERE group_name = ?
            ''',
            (id,))
        connect.commit()
        cursor.close()

    @staticmethod
    def delete_from_timetable(connect, date):
        cursor = connect.cursor()
        cursor.execute(
            '''DELETE FROM timetable
            WHERE date_timetable = ?
            ''',
            (date,))
        connect.commit()
        cursor.close()

    @staticmethod
    def create_table_subject(connect):
        cur = connect.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS subject "
            "( ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , name_subject TEXT NOT NULL);")
        connect.commit()
        cur.close()

    @staticmethod
    def create_table_lecturer(connect):
        cur = connect.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS lecturer "
            "( ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , SNP TEXT NOT NULL);")
        connect.commit()
        cur.close()

    @staticmethod
    def create_table_classroom(connect):
        cur = connect.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS classroom "
            "( ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , classroom_number INTEGER NOT NULL);")
        connect.commit()
        cur.close()

    @staticmethod
    def create_table_groups(connect):
        cur = connect.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS groups "
            "( ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , group_name TEXT NOT NULL);")
        connect.commit()
        cur.close()

    @staticmethod
    def create_table_timetable(connect):
        cur = connect.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS timetable "
            "( ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , "
            "ID_group INTEGER,"
            "ID_subject INTEGER,"
            "ID_lecturer INTEGER,"
            "ID_classroom INTEGER,"
            "date_timetable DATE,"
            "lesson_number INTEGER,"
            "comment TEXT,"
            "FOREIGN KEY(ID_group) REFERENCES groups(ID),"
            "FOREIGN KEY(ID_subject) REFERENCES subject(ID),"
            "FOREIGN KEY(ID_lecturer) REFERENCES lecturer(ID),"
            "FOREIGN KEY(ID_classroom) REFERENCES classroom(ID));")
        connect.commit()
        cur.close()

    @staticmethod
    def find_ID_classroom(connect, classroom):
        cur = connect.cursor()
        cur.execute(
            '''SELECT ID FROM classroom WHERE classroom_number = ?;''',
            (classroom,))
        data = cur.fetchall()
        connect.commit()
        cur.close()
        if len(data) == 1:
            return data[0][0]
        elif len(data) == 0:
            return 0
        else:
            return data

    @staticmethod
    def find_ID_groups(connect, group):
        cur = connect.cursor()
        cur.execute(
            '''SELECT ID FROM groups WHERE group_name = ?;''',
            (group,))
        data = cur.fetchall()
        connect.commit()
        cur.close()
        if len(data) == 1:
            return data[0][0]
        elif len(data) == 0:
            return 0
        else:
            return data

    @staticmethod
    def find_ID_lecturer(connect, lecturer):
        cur = connect.cursor()
        cur.execute(
            '''SELECT ID FROM lecturer WHERE SNP = ?;''',
            (lecturer,))
        data = cur.fetchall()
        connect.commit()
        cur.close()
        if len(data) == 1:
            return data[0][0]
        elif len(data) == 0:
            return 0
        else:
            return data

    @staticmethod
    def find_ID_subject(connect, subject):
        cur = connect.cursor()
        cur.execute(
            '''SELECT ID FROM subject WHERE name_subject = ?;''',
            (subject,))
        data = cur.fetchall()
        connect.commit()
        cur.close()
        if len(data) == 1:
            return data[0][0]
        elif len(data) == 0:
            return 0
        else:
            return data

    @staticmethod
    def find_timetable(connect, date, group):
        cur = connect.cursor()
        cur.execute(
            '''SELECT lecturer.SNP,
               subject.name_subject,
               lesson_number,
               comment,
               classroom.classroom_number
               FROM timetable
               INNER JOIN groups ON groups.ID = timetable.ID_group
               INNER JOIN lecturer ON lecturer.ID=timetable.ID_lecturer
               INNER JOIN subject ON subject.ID = timetable.ID_subject
               INNER JOIN classroom ON classroom.ID = timetable.ID_classroom
               WHERE date_timetable = ? AND groups.group_name = ?;''',
            (date, group)
        )
        data = cur.fetchall()
        connect.commit()
        cur.close()
        return data

    @staticmethod
    def find_lecturer(connect):
        cur = connect.cursor()
        cur.execute('''SELECT SNP FROM lecturer ORDER BY SNP ASC;''')
        data = cur.fetchall()
        connect.commit()
        cur.close()
        return data

    @staticmethod
    def find_subject(connect):
        cur = connect.cursor()
        cur.execute('''SELECT name_subject FROM subject ORDER BY name_subject ASC;''')
        data = cur.fetchall()
        connect.commit()
        cur.close()
        return data

    @staticmethod
    def find_classroom(connect):
        cur = connect.cursor()
        cur.execute('''SELECT classroom_number FROM classroom ORDER BY classroom_number ASC;''')
        data = cur.fetchall()
        connect.commit()
        cur.close()
        return data

    @staticmethod
    def find_groups(connect):
        cur = connect.cursor()
        cur.execute('''SELECT group_name FROM groups ORDER BY group_name ASC;''')
        data = cur.fetchall()
        connect.commit()
        cur.close()
        return data

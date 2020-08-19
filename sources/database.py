import sqlite3


def connect_database(database):
    connect = sqlite3.connect(database)
    return connect


class DataBase(object):
    def __init__(self, connect):
        self.connect = connect

    def insert_into_subject(self, name):
        cur = self.connect.cursor()
        cur.execute('''INSERT INTO subject (name_subject) VALUES(?)''', (name,))
        self.connect.commit()
        cur.close()

    def insert_into_lecturer(self, SNP):
        cur = self.connect.cursor()
        cur.execute('''INSERT INTO lecturer (SNP) VALUES(?)''', (SNP,))
        self.connect.commit()
        cur.close()

    def insert_into_classroom(self, classroom_number):
        cur = self.connect.cursor()
        cur.execute('''INSERT INTO classroom (classroom_number) VALUES(?)''', (classroom_number,))
        self.connect.commit()
        cur.close()

    def insert_into_groups(self, group_name):
        cur = self.connect.cursor()
        cur.execute('''INSERT INTO groups (group_name) VALUES(?)''', (group_name,))
        self.connect.commit()
        cur.close()

    def insert_into_timetable(self, id_group, id_subject, id_lecturer, id_classroom, date_timetable,
                              lesson_number, comment):
        cur = self.connect.cursor()
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
        self.connect.commit()
        cur.close()

    def delete_from_subject(self, id):
        cursor = self.connect.cursor()
        cursor.execute(
            '''DELETE FROM subject
            WHERE name_subject = ?
            ''',
            (id,))
        self.connect.commit()
        cursor.close()

    def delete_from_lecturer(self, id):
        cursor = self.connect.cursor()
        cursor.execute(
            '''DELETE FROM lecturer
            WHERE SNP = ?
            ''',
            (id,))
        self.connect.commit()
        cursor.close()

    def delete_from_classroom(self, id):
        cursor = self.connect.cursor()
        cursor.execute(
            '''DELETE FROM classroom
            WHERE classroom_number = ?
            ''',
            (id,))
        self.connect.commit()
        cursor.close()

    def delete_from_groups(self, id):
        cursor = self.connect.cursor()
        cursor.execute(
            '''DELETE FROM groups
            WHERE group_name = ?
            ''',
            (id,))
        self.connect.commit()
        cursor.close()

    def delete_from_timetable(self, date):
        cursor = self.connect.cursor()
        cursor.execute(
            '''DELETE FROM timetable
            WHERE date_timetable = ?
            ''',
            (date,))
        self.connect.commit()
        cursor.close()

    def create_table_subject(self):
        cur = self.connect.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS subject "
            "(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , name_subject TEXT NOT NULL, "
            "UNIQUE ('name_subject') ON CONFLICT IGNORE);")
        self.connect.commit()
        cur.close()

    def create_table_lecturer(self):
        cur = self.connect.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS lecturer "
            "(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , SNP TEXT NOT NULL, "
            "UNIQUE ('SNP') ON CONFLICT IGNORE);")
        self.connect.commit()
        cur.close()

    def create_table_classroom(self):
        cur = self.connect.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS classroom "
            "(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , classroom_number INTEGER NOT NULL, "
            "UNIQUE ('classroom_number') ON CONFLICT IGNORE);")
        self.connect.commit()
        cur.close()

    def create_table_groups(self):
        cur = self.connect.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS groups "
            "(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , group_name TEXT NOT NULL, "
            "UNIQUE ('group_name') ON CONFLICT IGNORE);")
        self.connect.commit()
        cur.close()

    def create_table_timetable(self):
        cur = self.connect.cursor()
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
            "FOREIGN KEY(ID_classroom) REFERENCES classroom(ID),"
            "UNIQUE ('date_timetable', 'ID_group') ON CONFLICT REPLACE);")
        self.connect.commit()
        cur.close()

    def find_ID_classroom(self, classroom):
        cur = self.connect.cursor()
        cur.execute(
            '''SELECT ID FROM classroom WHERE classroom_number = ?;''',
            (classroom,))
        data = cur.fetchall()
        self.connect.commit()
        cur.close()
        if len(data) == 1:
            return data[0][0]
        elif len(data) == 0:
            return 0
        else:
            return data

    def find_ID_groups(self, group):
        cur = self.connect.cursor()
        cur.execute(
            '''SELECT ID FROM groups WHERE group_name = ?;''',
            (group,))
        data = cur.fetchall()
        self.connect.commit()
        cur.close()
        if len(data) == 1:
            return data[0][0]
        elif len(data) == 0:
            return 0
        else:
            return data

    def find_ID_lecturer(self, lecturer):
        cur = self.connect.cursor()
        cur.execute(
            '''SELECT ID FROM lecturer WHERE SNP = ?;''',
            (lecturer,))
        data = cur.fetchall()
        self.connect.commit()
        cur.close()
        if len(data) == 1:
            return data[0][0]
        elif len(data) == 0:
            return 0
        else:
            return data

    def find_ID_subject(self, subject):
        cur = self.connect.cursor()
        cur.execute(
            '''SELECT ID FROM subject WHERE name_subject = ?;''',
            (subject,))
        data = cur.fetchall()
        self.connect.commit()
        cur.close()
        if len(data) == 1:
            return data[0][0]
        elif len(data) == 0:
            return 0
        else:
            return data

    def find_timetable(self, date, group):
        cur = self.connect.cursor()
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
        self.connect.commit()
        cur.close()
        return data

    def find_lecturer(self):
        cur = self.connect.cursor()
        cur.execute('''SELECT SNP FROM lecturer ORDER BY SNP ASC;''')
        data = cur.fetchall()
        self.connect.commit()
        cur.close()
        return data

    def find_subject(self):
        cur = self.connect.cursor()
        cur.execute('''SELECT name_subject FROM subject ORDER BY name_subject ASC;''')
        data = cur.fetchall()
        self.connect.commit()
        cur.close()
        return data

    def find_classroom(self):
        cur = self.connect.cursor()
        cur.execute('''SELECT classroom_number FROM classroom ORDER BY classroom_number ASC;''')
        data = cur.fetchall()
        self.connect.commit()
        cur.close()
        return data

    def find_groups(self):
        cur = self.connect.cursor()
        cur.execute('''SELECT group_name FROM groups ORDER BY group_name ASC;''')
        data = cur.fetchall()
        self.connect.commit()
        cur.close()
        return data

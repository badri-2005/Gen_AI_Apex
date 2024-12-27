import sqlite3

connection = sqlite3.connect("Students.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students(
    NAME VARCHAR(20),
    CLASS VARCHAR(20),
    SECTION VARCHAR(20),
    MARK INT
)
""")
cursor.executemany("""
INSERT INTO Students (NAME, CLASS, SECTION, MARK) VALUES
""", [
    ("Rohan", "Data Science", "B", 80),
    ("Dinesh", "Data Science", "A", 90),
    ("Jonathan", "AI", "C", 90),
    ("Tony Stark", "Web Dev", "B", 87)
])
res = cursor.execute(""" select * from Students""")
for i in res:
    print(i)
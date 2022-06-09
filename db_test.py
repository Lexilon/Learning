from mysql.connector import connect, Error

try:
    connection = connect(
        host="localhost",
        user="root",
        password="MySQL!SuperPass01",
        port="3306",
        database="db",
        )


    num = "12345"
    name= "Ноут Lenovo"
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO inv_item (num, name) VALUES ('{num}','{name}')")
        connection.commit()
except Error as e:
    print(e)


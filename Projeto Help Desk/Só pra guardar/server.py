import mysql.connector
from mysql.connector import errorcode




try:
	db_connection = mysql.connector.connect(
    host='localhost',
    database="Hdesk",
    user='admin',
    password='hdpass'
)
	print("A Conexão com banco de dados foi estabelecida!")
except mysql.connector.Error as error:
	if error.errno == errorcode.ER_BAD_DB_ERROR:
		print("O banco de dados não existe")
	elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Usuário ou senha estão errados.")
	else:
		print(error)
else:
	db_connection.close()


# cursor = db_connection.cursor()

# query = ("SELECT * FROM Solicitacao")
# cursor.execute(query)

# for resultado in cursor:
#     print(resultado)

# cursor.close()
# db_connection.close()


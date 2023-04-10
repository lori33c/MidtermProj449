import pymysql

# Connect to the MySql database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password= "",
    db='449_db',
    cursorclass=pymysql.cursors.DictCursor,
    port=3306
)

cur = conn.cursor()

#Define the table schema
create_account_table = """
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(400) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

# Execture the SQL commands to create the tables
cur.execute(create_account_table)

#commit the changes to the database
conn.commit()

# Close the connection to the database
cur.close()
conn.close()
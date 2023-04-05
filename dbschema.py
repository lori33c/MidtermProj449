import pymysql

# Connect to the MySql database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password= "Password123!",
    db='449_db',
    cursorclass=pymysql.cursors.DictCursor
)

cur = conn.cursor()

#Define the table schema
create_account_table = """
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

create_task_table = """
CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) NOT NULL,
  `description` text,
  `due_date` date DEFAULT NULL,
  `priority` enum('low','medium','high') DEFAULT NULL,
  `status` enum('to do','in progress','done') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `userID` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userID_idx` (`userID`),
  CONSTRAINT `userID` FOREIGN KEY (`userID`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

# Execture the SQL commands to create the tables
cur.execute(create_account_table)
cur.execute(create_task_table)

#commit the changes to the database
conn.commit()

# Close the connection to the database
cur.close()
conn.close()
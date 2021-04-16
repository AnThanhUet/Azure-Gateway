import mysql.connector
 
# tạo đối tượng connection
mydb = mysql.connector.connect(
    host = "localhost", 
    user = "root",
    passwd = "admin999999999", 
    database = "azure")
   
# tạo đối tượng cursor
mycursor = mydb.cursor()
   
try:
    
    dbs = mycursor.execute("create table Xuanthuy(Temperature float not null, "
       # + "ID int not null, "
      #  + "Temperature float not null, "
        + "Humidity float not null)")
except:
    mycursor.rollback()
 
mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
mycursor.close()
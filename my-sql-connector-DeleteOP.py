import mysql.connector
def connect(database):
 user="DBM"
 host="localhost"
 password='root'

 conn=mysql.connector.connect(user=user,host=host,password=password,database=database)
 return conn

def delete(table,attrib,value):
 delt="DELETE FROM "+table+" WHERE "+attrib+"="+ value
 return delt
def show(table):
 return "select * from "+table

'''Input from user'''

database=input("Enter name of database\n")
table,attrib,value=tuple(input("Enter Table name,Attribute and its value\nstudent").split())

'''object returned by Connect Function is appended to .cursor() method'''
conn=connect(database)
cursor=conn.cursor()
delquery=delete(table,attrib,value)
cursor.execute(delquery)
#conn.commit() is used to reflect changes in database after CRUD operations
conn.commit()
cursor.execute(show(table))
output=cursor.fetchall()
for x in output:
 print(x)
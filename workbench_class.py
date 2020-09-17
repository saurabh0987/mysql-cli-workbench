import mysql.connector

class Column:
    def __init__(self,name=None,datatype=None,length=0,options=["N","Y","N"]):
        self.name=name.replace(" ","")
        self.datatype=datatype
        self.length=length
        self.primary=options[0]
        self.null=options[1]
        self.inc=options[2]
        self.__tostring()
    def __tostring(self):
        if self.length == 0:
            self.final=self.name +" "+self.datatype
        else:
            self.final=self.name +" "+self.datatype +" ("+self.length +") "

        if(self.primary=="Y"):
            self.final+=" ,primary key("+self.name+")"
        if(self.null=="N"):
            self.final+=" not null"
        if(self.inc=="Y"):
            self.final+=" auto_increment"

class Workbench:
    def __init__(self,dbname,user="DBM",host="localhost",password="root"):
        self.databaseName=dbname
        self.user=user
        self.host=host
        self.password=password
        self.connectToDB()

    def connectToDB(self):
        self.conn=mysql.connector.connect(user=self.user,host=self.host,password=self.password,database=self.databaseName)
    
    def selectFromTable(self,tablename,attribute,limit,conditions,operations):
        self.tablename=tablename;self.attribute=attribute;self.limit=limit;self.conditions=conditions;self.operations=operations
        if len(attribute)==0:
            users="SELECT * FROM "+tablename
        else:
            users="SELECT "
            for i in range(len(attribute)):
                if(i<len(attribute)-1):
                    users+=attribute[i]
                    users+=','
                else:
                    users+=attribute[i]
            users+=" FROM "+tablename
        if len(conditions)!=0:
            users=self.where(users,conditions,operations)
        print(users)
        cursor = self.conn.cursor()
        cursor.execute(users)
        result=cursor.fetchall()
        if len(limit)==0:
            for i in result:
                print(i)
        else:
            temp=1
            for i in result:
              if temp<=limit[0]:
                print(i)
              temp+=1    
    def where(self,query,conditions,operations):
            self.query=query;self.conditions=conditions;self.operations=operations
            query+=" where "
            itr=1
            print(len(conditions))
            print(conditions)
            for lst in conditions:
                if itr<len(conditions):
                    if not lst[1].isnumeric():
                        query=query+lst[0]+"="+'"'+lst[1]+'"'+" "+operations+" "
                    else:
                        query=query+lst[0]+"="+lst[1]+" "+operations+" "
                else:
                    if not lst[1].isnumeric():
                        query+=lst[0]+"="+'"'+lst[1]+'"'
                    else:
                        query+=lst[0]+"="+lst[1]
                itr+=1
            return query

    def creatTable(self,tablename,columns):
        query="create table "
        query+=tablename +" ( "
        #create table tablename (
        temp=0
        for i in columns:
            if(temp!=len(columns)-1):
                query+=i.final+","
            else:
                query+=i.final+")"
            temp+=1
        print(query)
        #create table tablename (name varchar(250),addr varchar(250))
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()  

    def insertvalues(self,tablename,intocolumns,values):
        query="Insert into "+tablename
        if len(intocolumns)!=0:
            query+="("
            for col_index in range(len(intocolumns)):
                if  col_index < ((len(intocolumns)-1)):
                    query+=intocolumns[col_index]+","
                else:
                    query+=intocolumns[col_index]+")"+" values("
        else:
            query+=" values("
        for val in range(len(values)):
            if val < ((len(values)-1)):
                if not values[val].isnumeric():
                    query+='"'+values[val]+'"'+","
                else:
                    query+=values[val]+","
            else:
                if not values[val].isnumeric():
                    query+='"'+values[val]+'"'+")"
                else:
                    query+=values[val]+")"
        print(query)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()        

    def delete(self,tablename,conditions,operations):
        query="DELETE FROM "+tablename
        if len(conditions)!=0:
              query=self.where(query,conditions,operations)
        print(query)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit() 
    def update(self,tablename,ColmValuesToSet,conditions,operations):
        query="UPDATE "+tablename+" SET "
        itr=1
        for colval in ColmValuesToSet:
            if itr < len(ColmValuesToSet):
                if not colval[1].isnumeric():
                    query+=colval[0]+"="+'"'+colval[1]+'"'+","
                else:
                    query+=colval[0]+"="+colval[1]+","
                itr+=1
            else:
                if not colval[1].isnumeric():
                    query+=colval[0]+"="+'"'+colval[1]+'"'
                else:
                    query+=colval[0]+"="+colval[1]
        if len(conditions)!=0:
            query=self.where(query,conditions,operations) 
        print(query)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()


wb=Workbench("employees")
'''while True:
    try:
        wb.insertvalues(tablename="emp_data",intocolumns=["Emp_id","salary","first_name","designation"],values=["19","800","saurabhdddddddddddddddddddddddddddddddddddddddddddddddddddddddd","Sd"])
        break
    except:
        print("Data error Enter the data again\n")'''
#wb.selectFromTable(tablename="emp_data",attribute=[],limit=[],conditions=[["first_name","Archit"]],operations="or")
#wb.update(tablename="emp_data",ColmValuesToSet=[["salary","45000"],["designation","Teamlead"]],conditions=[["Emp_id","3"]],operations="and")
#wb.delete(tablename="emp_data",conditions=[["Emp_id","7"],["Emp_id","8"]],operations="or")
#                                           CREATE TABLE INPUT 
'''
table="test_table_of_connector"
n=int(input('number of attributes\n'))
columns=[]
primary_check=True
for i in range(n):
    name=input('Enter name of col '+str(i)+'\n')
    datatype=input('Enter datatype of col '+str(i)+'\n')
    if(datatype =="varchar" or datatype =="VARCHAR"):
        length=input('Enter size of col '+str(i)+'\n')
    else:
        length=0
    if(primary_check):
        primary=input("primary key?(Y/N)\n")
        if(primary=="Y"):
            primary_check=False
    else:
        primary="N"
    null=input("null(Y/N)\n")
    inc=input("auto increment?(Y/N)\n")

    temp=Column(name,datatype,length,[primary,null,inc])
    columns.append(temp)
    
wb.creatTable(table,columns)
'''
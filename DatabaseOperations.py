import mysql.connector

con= mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mypassword",
  database="companydatabase"
)

def check_employee(ssn):
    cursor=con.cursor(buffered=True)
    cursor.execute("SELECT * FROM employee WHERE Ssn={}".format(ssn))
    r=cursor.rowcount
    if r==1:
        return True
    else:
        return False
    

def view_employee():
    ssn=input("Enter employee SSN: ")
    if(check_employee(ssn)==False):
        print("Employee does not exist \nTry again\n")
        menu()
    else:
        cursor=con.cursor()
        cursor.execute("SELECT E.Fname,E.Minit,E.Lname,E.Ssn,E.Bdate,E.Address,E.Sex,E.Salary,E.Super_ssn,E.Dno,S.Fname,S.Minit,S.Lname,D.Dname,F.Dependent_name FROM employee AS E,employee AS S,department AS D,dependent AS F WHERE E.Super_ssn=S.Ssn AND E.Dno=D.Dnumber AND F.Essn=E.Ssn AND E.Ssn={}".format(ssn))
        result=cursor.fetchall()
        for x in result:
            print(x)
        menu()

def add_employee():
    ssn=input("Enter employee SSN: ")
    if(check_employee(ssn)==True):
        print("Employee already exists \nTry again\n")
        menu()
    else:
        Fname=input("enter employee's first name: ")
        Minit=input("enter employee's middle name: ")
        Lname=input("enter employee's last name: ")
        Bdate=input("enter employee's date of birth: ")
        Address=input("enter employee's address: ")
        Sex=input("enter employee's sex: ")
        Salary=input("enter employee's salary: ")
        Super_ssn=input("enter the supervisor's SSN: ")
        Dno=input("enter employee's department number: ")
        data=(Fname,Minit,Lname,ssn,Bdate,Address,Sex,Salary,Super_ssn,Dno)
        statement="INSERT INTO employee VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor=con.cursor()
        try:
            cursor.execute(statement,data)
            con.commit()
            print("Employee has been added succesfully")
            menu()
        except mysql.connector.Error as err:
            print(err)
            menu()
            


def modify_employee():
    
    ssn=input("Enter employee SSN: ")
    if(check_employee(ssn)==False):
        print("Employee does not exist \nTry again\n")
        menu()
    else:
        cursor=con.cursor()
        firstquery="SELECT * FROM employee WHERE Ssn={} FOR UPDATE".format(ssn)
        cursor.execute(firstquery)
        result=cursor.fetchone()
        print(result)
        updatedcolumn=input("Enter the column (address,sex,salary,super_ssn,dno) you want to update: ")
        newvalue=input("Enter the new value for this column: ")
        combined=updatedcolumn+"="+newvalue
        while True:
            question=input("would you like to update another column: ")
            if(question=='yes'):
                updatedcolumn=input("Enter the column (address,sex,salary,super_ssn,dno) you want to update: ")
                newvalue=input("Enter the new value for this column: ")
                newcombined=","+updatedcolumn+"="+newvalue
                combined+=newcombined
            else:
                break
        nextquery="UPDATE employee SET {} WHERE Ssn={}".format(combined,ssn)
        cursor.execute(nextquery)
        con.commit()
        print("employee has been updated succesfully")
        menu()

def remove_employee():
    ssn=input("Enter employee SSN: ")
    cursor=con.cursor()
    query="SELECT * FROM employee WHERE Ssn={} FOR UPDATE".format(ssn)
    cursor.execute(query)
    result=cursor.fetchone()
    print(result)
    statement="DELETE FROM employee WHERE Ssn={}".format(ssn)
    if(check_employee(ssn)==False):
        print("Employee does not exist \nTry again\n")
        menu()
    else:
        question=input("Are you sure you want to delete this employee: ")
        if(question=='no'):
            print("You have decided not to delete the employee")
            menu()
        else:
            try:
                cursor.execute(statement)
                con.commit()
                print("employee has been removed succesfullly")
                menu()
            except mysql.connector.Error as err:
                print(err)
                print("This error most likely means that the dependencies should be removed first")
                menu()


    

def add_dependent():
    ssn=input("Enter employee SSN: ")
    cursor=con.cursor()
    firstquery="SELECT * FROM dependent WHERE Essn={} FOR UPDATE".format(ssn)
    cursor.execute(firstquery)
    result=cursor.fetchall()
    for x in result:
        print(x)
    dependent_name=input("Enter dependent's name: ")
    sex=input("Enter sex: ")
    bdate=input("Enter date of birth: ")
    relationship=input("Enter relationship with the employee: ")
    data=(ssn,dependent_name,sex,bdate,relationship)
    statement="INSERT INTO dependent VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(statement,data)
    con.commit()
    print("dependent has been added succesfully")
    menu()


def remove_dependent():
    ssn=input("Enter employee SSN: ")
    cursor=con.cursor()
    firstquery="SELECT * FROM dependent WHERE Essn={} FOR UPDATE".format(ssn)
    cursor.execute(firstquery)
    result=cursor.fetchall()
    for x in result:
        print(x)
    dependent_name=input("Enter dependent's name: ")
    statement="DELETE FROM dependent WHERE Essn={} AND dependent_name={}".format(ssn,dependent_name)
    cursor.execute(statement)
    con.commit()
    print("dependent has been removed successfully")
    menu()



def add_department():
    Dname=input("Enter department name: ")
    Dnumber=input("Enter department number: ")
    Mgr_ssn=input("Enter the manager's ssn: ")
    Mgr_start_date=input("Enter the manager's start date: ")
    cursor=con.cursor()
    data=(Dname,Dnumber,Mgr_ssn,Mgr_start_date)
    statement="INSERT INTO department VALUES(%s,%s,%s,%s)"
    try:
        cursor.execute(statement,data)
        con.commit()
        print("department has been added successfully")
        menu()
    except mysql.connector.Error as err:
        print(err)
        menu()

def view_department():
    Dnumber=input("Enter department number: ")
    cursor=con.cursor()
    statement="SELECT E.Fname,E.Minit,E.Lname,D.Dname,F.Dlocation FROM employee AS E,department AS D,dept_locations AS F WHERE D.Dnumber={} AND D.Mgr_ssn=E.Ssn AND F.Dnumber=D.Dnumber".format(Dnumber)
    cursor.execute(statement)
    result=cursor.fetchall()
    for x in result:
        print(x)
    menu()


def remove_department():
    Dnumber=input("Enter department number: ")
    cursor=con.cursor()
    statement="SELECT * FROM department WHERE Dnumber={} FOR UPDATE".format(Dnumber)
    cursor.execute(statement)
    result=cursor.fetchone()
    print(result)
    nextstatement="DELETE FROM department WHERE Dnumber={}".format(Dnumber)
    question=input("Would you really like to remove this department: ")
    if(question=="no"):
        print("you have decided not to remove this department")
        menu()
    else:
        try:
            cursor.execute(nextstatement)
            con.commit()
            print("department removed succesfully")
            menu()
        except mysql.connector.Error as err:
            print(err)
            print("This likely means that the dependencies should be removed first")
            menu()


def add_department_location():
    Dnumber=input("Enter department number: ")
    cursor=con.cursor()
    statement="SELECT Dlocation FROM dept_locations WHERE Dnumber={} FOR UPDATE".format(Dnumber)
    cursor.execute(statement)
    result=cursor.fetchall()
    for x in result:
        print(x)
    location=input("Type in a new location: ")
    data=(Dnumber,location)
    newstatement="INSERT INTO dept_locations VALUES(%s,%s)"
    cursor.execute(newstatement,data)
    con.commit()
    print("new location has been added successfully")
    menu()

def remove_department_location():
    Dnumber=input("Enter department number: ")
    cursor=con.cursor()
    statement="SELECT Dlocation FROM dept_locations WHERE Dnumber={} FOR UPDATE".format(Dnumber)
    cursor.execute(statement)
    result=cursor.fetchall()
    for x in result:
        print(x)
    location=input("choose a location you want removed: ")
    newstatement="DELETE FROM dept_locations WHERE Dnumber={} AND Dlocation={}".format(Dnumber,location)
    cursor.execute(newstatement)
    con.commit()
    print("location has been removed successfully")
    menu()


def menu():
    print("Welcome")
    print("Press")
    print("1 to add an employee")
    print("2 to view an employee")
    print("3 to modify an employee")
    print("4 to remove an employee")
    print("5 to add a dependent")
    print("6 to remove a dependent")
    print("7 to add a department")
    print("8 to view a department")
    print("9 to remove a department")
    print("10 to add a department location")
    print("11 to remove a department location")
    print("12 to exit")
    b=int(input("Enter your choice: "))
    if b==1:
        add_employee()
    elif b==2:
        view_employee()
    elif b==3:
        modify_employee()
    elif b==4:
        remove_employee()
    elif b==5:
        add_dependent()
    elif b==6:
        remove_dependent()
    elif b==7:
        add_department()
    elif b==8:
        view_department()
    elif b==9:
        remove_department()
    elif b==10:
        add_department_location()
    elif b==11:
        remove_department_location()
    elif b==12:
        exit(0)
    else:
        print("not a valid choice")
        menu()

menu()
    
        
    
    
    




            
        
        
        
    
    



    
    
        
                
                
                
        
    
        
        
    





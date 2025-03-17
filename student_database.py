My code
==========================================================================================================

import certifi
import time
import sys
from pymongo import collection
from pymongo.mongo_client import MongoClient
import getpass
from rich.console import Group
from rich.panel import Panel
from rich import print
from rich.console import Console
# 
# 
console = Console()
# 
def splash_screen():
    intro_group = Group(
    Panel("""
    Please select a workspace:
# 
          1.    Connect and enter students information
          2.    Search database
          3.    Exit program
# 
    Please select option: """,style="green"))
    print(Panel(intro_group))
    user_input = int(input("#"))
    if user_input == 1:
        database_connect()
    elif user_input == 2:
        database_search()
    else:
        sys.exit(0)
#    
# 
# 
# 
# 
#Connect to mongodb server
def database_connect():
    password = getpass.getpass()
    uri = "mongodb+srv:/xxxxxx:"+password+"@cluster0.example.mongodb.net/?retryWrites=true&w=majority"
# 
    #Connect to database
# 
    connection = MongoClient(uri, tlsCAFile=certifi.where())
    datab = connection['fakename']
    collection = datab['fakestudent']
# 
#Add data
#=====================================
    #quit_program = "Exit"
# 
    while True:
        fnstudent = input("Enter student's first name: ")
        if fnstudent != "exit":
            lnstudent = input("Enter student's last name: ")
            student_address = input("Enter student's address: ")
            course = input("Enter student's degree or certification program: ")
            education_cost = int(input("Enter student's total education cost: $"))
            payment = int(input("Enter student's payment: $"))
            print("Student's remaining payment: $",int(education_cost-payment))
            remaining_cost = int(education_cost-payment)
            time.sleep(3)
            print("===================================================")
            print("===================================================")
            add_dict = {
                "first name":fnstudent,
                "last name":lnstudent,
                "address":student_address,
                "program":course,
                "program cost":education_cost,
                "payment":payment,
                "remaining_cost":remaining_cost
            }
            collection.insert_one(add_dict)
            #collection.insert_many(add_dict) 
            for items in collection.find():
                console.print("--------------------------------------------")
                console.print(items)
                console.print("--------------------------------------------")
        else:
            console.print("Thank you and please come back!!!")
            # sys.exit(0)
            return splash_screen()
def database_search():
    password = getpass.getpass()
    uri = "mongodb+srv:/xxxx:"+password+"@cluster0.example.mongodb.net/?retryWrites=true&w=majority"
    connection = MongoClient(uri, tlsCAFile=certifi.where())
    datab = connection['chapaman_university']
    collection = datab['students']
    search_student = input("Enter student name to search record: ")
    record_found = collection.find({"first name":search_student})
# 
    for record in record_found:
        console.print("--------------------------------------------")
        console.print(record)
        console.print("--------------------------------------------")
def delete_user_profile():
    name = input("Enter first or last name to delete:")
    result = collection.delete_many({"$or": [{"first_name": name}, {"last_name": name}]})
    if result.deleted_count > 0:
        console.print(f"Deleted {result.deleted_count} user profiles successfully!", style="bold green")
    else:
        console.print("No user profiles found to delete.", style="bold red")
  
# 
# 
splash_screen()
# 


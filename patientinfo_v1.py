import random
import json
import mysql.connector
import getpass


def main():
    db = mysql.connector.connect(host = "localhost",
                                username = "admin@localhost",
                                password = getpass.getpass("Enter password: "),
                                database = "hospital")
    cur = db.cursor()




    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("|Patient Information                                        |")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    medical_record_num = random.randint(10000,99999)
    firstname = input("Patient First Name: ")
    lastname = input("Patient Last Name: ")
    address = input("Address: ")
    dob = input("Enter Date of Birth: ")
    serial_num = input("Enter Social Security: ")
    doctor_name = input("Enter Doctor's Name: ")

    print("**************************************\n")
    print("**************************************\n")

    quy = "insert into patient_info values(%s,%s,%s,%s,%s,%s,%s)"
    data_input = (medical_record_num,firstname,lastname,address,dob,serial_num,doctor_name)
    cur.execute(quy,data_input)
    cur.execute("select * from patient_info")
    results = cur.fetchall()


    db.commit()
    cur.close()
    db.close()


    patient_dict = {
        "medical_record_num": medical_record_num,
        "firstname":firstname,
        "lastname": lastname,
        "address":address,
        "dob":dob,
        "serial_num":serial_num,
        "doctor_name": doctor_name
        }

    converted_json = json.dumps(patient_dict,indent=2)
    print(converted_json)
    
    
    print("**************************************\n")
    print("**************************************\n")

    for r in results:
        print(r[0],' ',r[1],' ',r[2],' ',r[3],' ',r[4],' ',r[5],' ',r[6])





if __name__ == "__main__":
    while True:
        main()
        user_input = input("Enter 'q' to exit: ")
        if user_input.lower() == 'q':
            break

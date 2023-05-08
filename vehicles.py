from prettytable import PrettyTable

class Vehicles:
    def __init__(self,vehicle_id,cost,type,premium_amount):
        self.vehicle_id = vehicle_id
        self.cost = cost
        self.type = type       
        self.premium_amount = premium_amount

    def vehicle_two_wheels(self):
        veh.vehicle_id = input("Enter car id: ")
        veh.cost = int(input("Enter car price: "))
        veh.type = 2
        veh.premium_amount=veh.cost*(6/100)
        table = PrettyTable()
        table.title = "Car Info"
        table.add_column("Vehicle VIN",[veh.vehicle_id])
        table.add_column("Vehicle Cost",[veh.cost])
        table.add_column("Vehicle Type",[veh.type])
        table.add_column("Vehicle Premium",[veh.premium_amount])
        print(table)                               

    def vehicle_four_wheels(self):
        veh.vehicle_id = input("Enter car id: ")
        veh.cost = int(input("Enter car price: "))
        veh.type = 4
        veh.premium_amount=veh.cost*(6/100)
        table = PrettyTable()
        table.title = "Car Info"
        table.add_column("Vehicle VIN",[veh.vehicle_id])
        table.add_column("Vehicle Cost",[veh.cost])
        table.add_column("Vehicle Type",[veh.type])
        table.add_column("Vehicle Premium",[veh.premium_amount])
        print(table)
        # print("Car info:\n","Vehicle ID:\n ",veh.vehicle_id,"\nVehicle Cost:\n ",veh.cost,"\nVehicle Type:\n",veh.type,34543
        # "\nVehicle Premium is:\n",veh.premium_amount)
        
    

veh = Vehicles(7463,20000,2,2)
result = veh.vehicle_four_wheels()



# if wheels == 2
    # Vehicles.premium_amount = Vehicles.cost * 2/100
    # print('Test two')
# elif wheels == 4:
    # Vehicles.premium_amount = Vehicles.cost *6/100
    # print('Test four')
# else:
    # return Vehicles.premium_amount
            # 

# result = v1.v_type()
# 
# print(result)

# Student ID: 011031922

import csv
from datetime import datetime, timedelta


# Hash Table that will be used to store packages
class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
            return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])


# Constructor for package objects
class Package:
    def __init__(self, packageID, address, deadline, city, state, zipCode, weight, status, note):
        self.packageID = packageID
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.weight = weight
        self.status = status
        self.note = note

    def __str__(self):
        return ("Package ID:\t\t   %s\n"
                "Delivery Deadline: %s\n"
                "Weight:\t\t\t   %s kg\n"
                "Current Status:\t   %s\n"
                "Delivery Address:\n"
                "\tStreet:\t\t   %s\n"
                "\tCity:\t\t   %s\n"
                "\tState:\t\t   %s\n"
                "\tZip Code:\t   %s\n"
                "Special Notes:\n\t%s\n"
                % (self.packageID,
                   self.deadline,
                   self.weight,
                   self.status,
                   self.address,
                   self.city,
                   self.state,
                   self.zipCode,
                   self.note))

    def updateStatus(self, updatedStatus):
        self.status = updatedStatus

    def updateAddress(self, updatedAddress):
        self.address = updatedAddress


# Constructor for truck objects
class Truck:
    def __init__(self, truckID, miles, location, packages, speed, departure, arrival):
        self.truckID = truckID
        self.miles = miles
        self.location = location
        self.packages = packages
        self.speed = speed
        self.departure = departure
        self.arrival = arrival

    def __str__(self):
        return ("Truck:\t\t\t%s\n"
                "Total Miles:\t%s Miles\n"
                "Speed:\t\t\t%s MPH\n"
                "Location:\t\t%s\n"
                "Packages:\t\t%s\n"
                "Departure Time: %s\n"
                "Return Time: %s"
                % (self.truckID,
                   self.miles,
                   self.speed,
                   self.location,
                   self.packages,
                   self.departure,
                   self.arrival))


# Constructor for time objects      Note: I used a 24hr Time format instead of a 12hr (AM/PM) Time format
class Time:
    def __init__(self, year, month, day, hour, minute, _dateTime):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self._dateTime = datetime(year, month, day, hour, minute)

    def __str__(self):
        return " %s " % self._dateTime

    def updateTime(self, passedHours, passedMinutes):
        oldTime = self._dateTime
        newTime = timedelta(hours=passedHours, minutes=passedMinutes)
        self._dateTime = oldTime + newTime

    def changeTime(self, year, month, day, hour, minute):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self._dateTime = datetime(year, month, day, hour, minute)

    @property
    def dateTime(self):
        return self._dateTime


# Loads the package data from the csv file
def loadPackageData(fileName):
    with open(fileName) as packageData:
        packageData = csv.reader(packageData)
        next(packageData)
        for package in packageData:
            packageID = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zipCode = package[4]
            deadline = package[5]
            weight = package[6]
            status = "Hub"
            note = package[7].replace(",", "")
            # Creating Package Objects
            package = Package(packageID, address, deadline, city, state, zipCode, weight, status, note)

            # Inserting Package Objects into the hash table
            packageDataHash.insert(packageID, package)


# Loads the distance data from the csv file
def loadDistanceData(fileName):
    with open(fileName) as distanceDataTable:
        distanceDataTable = csv.reader(distanceDataTable, delimiter=',')
        for row in distanceDataTable:
            distanceData.append(row)


# Loads the address data from the csv file
def loadAddressData(fileName):
    with open(fileName) as addressDataTable:
        addressDataTable = csv.reader(addressDataTable)
        for row in addressDataTable:
            addressData.append(row[1])


def deliverPackages(truck, time1):
    # Will update Package 9 if the time is passed 10:20
    if time1 >= datetime(2024, 5, 6, 10, 20):
        packageDataHash.search(9).updateAddress('410 S State St')
    truck.arrival = truck.departure
    priority = []
    routeDistance = float(0)
    # Changes the order of the delivery route and updates the status of each package only if time1 >= departure time
    if time1 >= truck.departure.dateTime:
        n = 0
        # Loops through the list of packages to find the closest distance or packages that have a deadline to create the priority list
        while n < len(truck.packages):
            _results = minDistanceDeliver(truck.packages, truck.location)
            packID = int(_results[0])
            if ((('9:00' in packageDataHash.search(packID).deadline) or ('10:30' in packageDataHash.search(packID).deadline)) or float(minDistanceDeliver(truck.packages, truck.location)[2]) < float(2)) and time1 >= truck.departure.dateTime:
                priority.append(packID)
                packageDataHash.search(packID).updateStatus('Out for delivery')
                truck.packages.remove(packID)
            truck.location = _results[1]
        truck.packages = priority
        truck.location = '4001 South 700 East'
        # Loops through the packages in the truck, changes their status to delivered along with the time, and calculates miles traveled and passed time
        for i in range(len(truck.packages)):
            routeDistance += locationDistance(packageDataHash.search(truck.packages[i]).address, truck.location)
            newAddress = packageDataHash.search(truck.packages[i]).address
            deliveryDuration = float((routeDistance / truck.speed) * 60)
            deliveryTime = truck.departure.dateTime + timedelta(minutes=deliveryDuration)
            truck.location = newAddress
            if newAddress == truck.location and deliveryTime <= time1 >= truck.departure.dateTime:
                packageDataHash.search(truck.packages[i]).updateStatus(f'Delivered: {deliveryTime}')
        routeDistance += locationDistance(truck.location, "4001 South 700 East")
        routeDuration = round(float(((routeDistance / truck.speed) * 60) + .3))
        truck.arrival.updateTime(0, routeDuration)
        truck.location = "4001 South 700 East"
        truck.miles = routeDistance
        return routeDistance, routeDuration


# Uses the csv file for distances to calculate the distance between each address
def locationDistance(address1, address2):
    # The usage of if/elif statements is to eliminate the chance of returning a blank distance
    # if the index value of address 1 >= address 2 index value then return the distance
    if int(addressData.index(address1)) >= int(addressData.index(address2)):
        return float(distanceData[addressData.index(address1)][addressData.index(address2)])
    # if address 1 index value < address 2 index value then switch the order of the addresses and return the distance
    elif int(addressData.index(address1)) < int(addressData.index(address2)):
        return float(distanceData[addressData.index(address2)][addressData.index(address1)])


# Loops through the list of packages in a truck to find the closest delivery address based on the truck's current location
def minDistanceDeliver(truckPackages, predecessorAddress):
    mDistanceAddress = packageDataHash.search(truckPackages[0]).address
    mDistance = float(locationDistance(packageDataHash.search(truckPackages[0]).address, predecessorAddress))
    pID = truckPackages[0]
    # loops through the list of packages in a truck
    for i in range(len(truckPackages)):
        # if the package distance is closer than the previous package then it will update to the closer package
        if locationDistance(packageDataHash.search(truckPackages[i]).address, predecessorAddress) < mDistance:
            mDistance = float(locationDistance(packageDataHash.search(truckPackages[i]).address, predecessorAddress))
            mDistanceAddress = packageDataHash.search(truckPackages[i]).address
            pID = truckPackages[i]
    return [pID, mDistanceAddress, mDistance]


# Creating Objects for the times that the trucks leave
t1Departure = Time(2024, 5, 6, 8, 0, 0)
t2Departure = Time(2024, 5, 6, 9, 5, 0)
t3Departure = Time(2024, 5, 6, 10, 30, 0)
# Creating Objects for the times that the trucks return
t1Return = Time(2024, 5, 6, 0, 0, 0)
t2Return = Time(2024, 5, 6, 0, 0, 0)
t3Return = Time(2024, 5, 6, 0, 0, 0)
# Creating Objects to represent each truck
truck1 = Truck(1, 0, "4001 South 700 East", [1, 2, 4, 7, 13, 14, 15, 16, 19, 20, 21, 29, 33, 34, 39, 40], 18, t1Departure, t1Return)
truck2 = Truck(2, 0, "4001 South 700 East", [3, 5, 6, 8, 17, 18, 25, 26, 27, 30, 31, 32, 35, 36, 37, 38], 18, t2Departure, t2Return)
truck3 = Truck(3, 0, "4001 South 700 East", [9, 10, 11, 12, 22, 23, 24, 28], 18, t3Departure, t3Return)
# Creating time for midnight that will be used to show final outcome of the program
midnight = Time(2024, 5, 6, 23, 59, 0)
# Creating the hash table
packageDataHash = ChainingHashTable()
# Creating Lists where distance and address data will be stored
addressData = []
distanceData = []
# Creating variables to store total distance and duration
combinedDistance = float(0)
totalDuration = float(0)
loadAddressData('WGUPSAddressTable.csv')
loadDistanceData('WGUPSDistanceTable.csv')
loadPackageData('WGUPSPackageFile.csv')


# Creating the interface that will be used to control the program
def menu():
    introduction = 'Welcome to the WGUPS Delivery System'
    menuOptions = 'Menu Options:'
    mainMenu = ('\n********************************************************************************************************************************************************************************************************\n'
                '{:^200}\n'
                '{:^200}\n\n'
                '1. Get Status of a Package.\n\n'
                '2. Get Status of all Packages.\n\n'
                '3. Get Total Mileage of a Truck.\n\n'
                '4. Get Total Mileage of all Trucks.\n\n'
                '5. Exit System.\n'
                '\n********************************************************************************************************************************************************************************************************\n')
    print(mainMenu.format(introduction, menuOptions))
    userInputMenu = input('Enter Number to Select Menu Option: ')
    if '1' in userInputMenu:
        userInputP1 = input('Please Enter the Package ID you would Like to Find the Status for: ')
        userInputP1T = input('Please Enter the Time in the Format (HH:MM): ')
        tp1tInfo = userInputP1T.split(':')
        timeP1T = datetime(2024, 5, 6, int(tp1tInfo[0]), int(tp1tInfo[1]))
        truck = ''
        if int(userInputP1) in truck1.packages:
            t1Departure.changeTime(2024, 5, 6, 8, 0)
            deliverPackages(truck1, timeP1T)
            truck = 'Truck:\t\t\t   1'
        elif int(userInputP1) in truck2.packages:
            t2Departure.changeTime(2024, 5, 6, 9, 5)
            deliverPackages(truck2, timeP1T)
            truck = 'Truck:\t\t\t   2'
        elif int(userInputP1) in truck3.packages:
            t3Departure.changeTime(2024, 5, 6, 10, 30)
            deliverPackages(truck3, timeP1T)
            truck = 'Truck:\t\t\t   3'
        print(f'\n\n{truck}\n{packageDataHash.search(int(userInputP1))}')
        print('\n********************************************************************************************************************************************************************************************************\n\nWould You Like to Return to the Main Menu?\n\n1. Yes\n\n2. No\n\n********************************************************************************************************************************************************************************************************\n')
        userInputReturn1 = input('Enter Number to Select Menu Option: ')
        if '1' in userInputReturn1:
            # reloads package data to reset any updates made to ensure accurate data for next program execution
            loadPackageData('WGUPSPackageFile.csv')
            menu()
        else:
            exit()
    if '2' in userInputMenu:
        userInputPAT = input('Please Enter the Time in the Format (HH:MM): ')
        patInfo = userInputPAT.split(':')
        timePAT = datetime(2024, 5, 6, int(patInfo[0]), int(patInfo[1]))
        t1Departure.changeTime(2024, 5, 6, 8, 0)
        t2Departure.changeTime(2024, 5, 6, 9, 5)
        t3Departure.changeTime(2024, 5, 6, 10, 30)
        deliverPackages(truck1, timePAT)
        deliverPackages(truck2, timePAT)
        deliverPackages(truck3, timePAT)
        for i in range(len(packageDataHash.table)):
            package = packageDataHash.search(i + 1)
            if package.packageID in truck1.packages:
                packageInfo = '{packageID:<20}{truck:<20}{address:<62}{deadline:<24}{status}'.format(packageID=f'Package ID: {package.packageID}', address=f'Delivery Address: {package.address}', deadline=f'Deadline: {package.deadline}', status=f'Package Status: {package.status}', truck='Truck: Truck 1')
                print(packageInfo)
                # print(f'Package ID: {package.packageID}\t\tTruck: Truck 1\t\tDelivery Address: {package.address}\t\t\tPackage Status: {package.status}')
            elif package.packageID in truck2.packages:
                packageInfo = '{packageID:<20}{truck:<20}{address:<62}{deadline:<24}{status}'.format(packageID=f'Package ID: {package.packageID}', address=f'Delivery Address: {package.address}', deadline=f'Deadline: {package.deadline}', status=f'Package Status: {package.status}', truck='Truck: Truck 2')
                print(packageInfo)
                # print(f'Package ID: {package.packageID}\t\tTruck: Truck 2\t\tDelivery Address: {package.address}\t\t\tPackage Status: {package.status}')
            elif package.packageID in truck3.packages:
                packageInfo = '{packageID:<20}{truck:<20}{address:<62}{deadline:<24}{status}'.format(packageID=f'Package ID: {package.packageID}', address=f'Delivery Address: {package.address}', deadline=f'Deadline: {package.deadline}', status=f'Package Status: {package.status}', truck='Truck: Truck 3')
                print(packageInfo)
                # print(f'Package ID: {package.packageID}\t\tTruck: Truck 3\t\tDelivery Address: {package.address}\t\t\tPackage Status: {package.status}')
        print('\n********************************************************************************************************************************************************************************************************\n\nWould You Like to Return to the Main Menu?\n\n1. Yes\n\n2. No\n\n********************************************************************************************************************************************************************************************************\n')
        userInputReturn1 = input('Enter Number to Select Menu Option: ')
        if '1' in userInputReturn1:
            # reloads package data to reset any updates made to ensure accurate data for next program execution
            loadPackageData('WGUPSPackageFile.csv')
            menu()
        else:
            exit()
    if '3' in userInputMenu:
        userInputT1 = input('Please Enter the Truck ID you would Like to Find the Mileage for: ')
        if int(userInputT1) == truck1.truckID:
            t1Departure.changeTime(2024, 5, 6, 8, 0)
            deliverPackages(truck1, midnight.dateTime)
            print(f'\nTotal Mileage for Truck 1: {truck1.miles} miles.')
        elif int(userInputT1) == truck2.truckID:
            t2Departure.changeTime(2024, 5, 6, 9, 5)
            deliverPackages(truck2, midnight.dateTime)
            print(f'\nTotal Mileage for Truck 2: {truck2.miles} miles.')
        elif int(userInputT1) == truck3.truckID:
            t3Departure.changeTime(2024, 5, 6, 10, 30)
            deliverPackages(truck3, midnight.dateTime)
            print(f'\nTotal Mileage for Truck 3: {truck3.miles} miles.')
        print('\n********************************************************************************************************************************************************************************************************\n\nWould You Like to Return to the Main Menu?\n\n1. Yes\n\n2. No\n\n********************************************************************************************************************************************************************************************************\n')
        userInputReturn1 = input('Enter Number to Select Menu Option: ')
        if '1' in userInputReturn1:
            # reloads package data to reset any updates made to ensure accurate data for next program execution
            loadPackageData('WGUPSPackageFile.csv')
            menu()
        else:
            exit()
    if '4' in userInputMenu:
        t1Departure.changeTime(2024, 5, 6, 8, 0)
        t2Departure.changeTime(2024, 5, 6, 9, 5)
        t3Departure.changeTime(2024, 5, 6, 10, 30)
        d1 = deliverPackages(truck1, midnight.dateTime)[0]
        d2 = deliverPackages(truck2, midnight.dateTime)[0]
        d3 = deliverPackages(truck3, midnight.dateTime)[0]
        print(f'Truck 1 Mileage: {d1}\nTruck 2 Mileage: {d2}\nTruck 3 Mileage: {d3}\nTotal Mileage: {d1 + d2 + d3}')
        print('\n********************************************************************************************************************************************************************************************************\n\nWould You Like to Return to the Main Menu?\n\n1. Yes\n\n2. No\n\n********************************************************************************************************************************************************************************************************\n')
        userInputReturn1 = input('Enter Number to Select Menu Option: ')
        if '1' in userInputReturn1:
            # reloads package data to reset any updates made to ensure accurate data for next program execution
            loadPackageData('WGUPSPackageFile.csv')
            menu()
        else:
            exit()
    if '5' in userInputMenu:
        exitMessage1 = 'Thank You for using the WGUPS Delivery System,\n'
        exitMessage2 = 'Have a Nice Day!'
        exitAnnouncement = 'f\n********************************************************************************************************************************************************************************************************\n{:^85}{:^46}'
        print(exitAnnouncement.format(exitMessage1, exitMessage2))
        exit()
    elif ('1' or '2' or '3' or '4' or '5') not in userInputMenu:
        print('\n\n\n\n\n\n********************************************************************************************************************************************************************************************************\n'
              '\nERROR: Please Enter a Valid Option:')
        menu()


menu()

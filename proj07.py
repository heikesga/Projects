''' 
    Computer Project 7

        Have user enter an input, error check the input and then open the file
        Prep the opened file then send it to function to be manipulated
            Groups the data into manufactures
            Function that puts the data into a list within a dictionary within another dictionary
            Returns the dictionary and a year index
        Merges the years in a single list and the dictionaries into a main dictionary
        Sends the data to a function to find the average city and highway MPG per manufacture
        Finds the average MPG per manufacture for the decades entered
        Plots the data
        Displays the data in the correct format
'''

import csv
import pylab
import matplotlib.patches as patches

#Plots the data and displays the graph
def plot_mileage(years,city,highway):

    pylab.figure(1)
    pylab.plot(years, city['Ford'], 'r-', years, city['GM'], 'b-', years,
             city['Honda'], 'g-', years, city['Toyota'], 'y-')
    red_patch = patches.Patch(color='red', label='Ford')
    blue_patch = patches.Patch(color='blue', label='GM')
    green_patch = patches.Patch(color='green', label='Honda')
    yellow_patch = patches.Patch(color='yellow', label='Toyota')
    pylab.legend(handles=[red_patch, blue_patch, green_patch, yellow_patch])
    pylab.xlabel('Years')
    pylab.ylabel('City Fuel Economy (MPG)')
    pylab.show()
    
    # Plot the highway mileage data.
    pylab.figure(2)
    pylab.plot(years, highway['Ford'], 'r-', years, highway['GM'], 'b-', years,
             highway['Honda'], 'g-', years, highway['Toyota'], 'y-')
    pylab.legend(handles=[red_patch, blue_patch, green_patch, yellow_patch])
    pylab.xlabel('Years')
    pylab.ylabel('Highway Fuel Economy (MPG)')
    pylab.show()

#Opens the files, error checks and returns a list of the car data and years entered
def open_file():
    car_list = []
    year_list =[]
    Done = False
    in_file = input('Input multipe decades seperated by commas, eg. 1980, 1990, 2000: ')
    while not Done:
        try:
            data = in_file.split(',')
            for item in data:
                if item in ('1980','1990','2000','2010'):
                    car_list.append((open(item + 's.csv')))
                    year_list.append(int(item))
                    Done = True
                else:
                    in_file = input('Incorrect input, try again: ')
                    for item in car_list:
                        item.close()
        except FileNotFoundError:
            data = input('Error: Enter a correct decade: ')
    return car_list, year_list
    
#Sorts data into makes then creates a make dictionary containing a dictionary of
# years containing a list of city and highway MPGs
def extract_data(data):
    data_dict = {}
    year_lst = []
    for i in data:
        make = (i[46])
        year = int(i[63])
        city_mile = int(i[4])
        hwy_mile = int(i[34])
        if year == 2017:
            continue
        elif make in ('Lexus','Scion','Toyota'):
            make = 'Toyota'
        elif make in ('Chevrolet','Pontiac','Buick','GMC','Cadillac','Oldsmobile','Saturn'):
            make = 'GM'
        elif make in ('Mercury','Lincoln','Ford'):
            make = 'Ford'
        elif make in ('Acura','Honda'):
            make = 'Honda'
        elif make not in ('GM','Honda','Ford','Toyota'):
            continue
        if year not in year_lst:
            year_lst.append(year)

        if  make in data_dict:
            if year in data_dict[make]:
                data_dict[make][year]['city'].append(city_mile)
                data_dict[make][year]['hwy'].append(hwy_mile)
            else:
                data_dict[make][year]={'city':[city_mile],'hwy':[hwy_mile]}

        else:
            data_dict[make]={year:{'city':[city_mile],'hwy':[hwy_mile]}}
    return(data_dict), year_lst
 
#Creates a dictionary of the average city and highway MPGs
def average_mile(data,year_lst):
    city = {}
    hwy = {}
    for key,item in data.items():
        if key not in city:
            city[key]=[]
            hwy[key]=[]
        for year in year_lst:
            city[key].append(sum(data[key][year]['city'])/len(data[key][year]['city']))
            hwy[key].append(sum(data[key][year]['hwy'])/len(data[key][year]['hwy']))      
    return(city,hwy)

#Finds the average MPG for the makes in the provided decade/s
def find_avg_mpg(data):
    avg_D = {}
    for make, avgs in data.items():
        avg = sum(avgs)/len(avgs)
        avg_D[make] = avg
    return avg_D 
    
#Merges the year lists for indexing    
def merge_year(target, source):
    for item in source:
        target.append(item)            
    
#Merges the dictionaries into a main one
def merge_dict(target, source):   
    for key in source:
        if key in target:
            target[key].update(source[key])
        else:
            target[key] = (source[key])

#Returns the input years in a format that can be printed
def print_year(year):
    for item in year:
        return(item)


main_dict = {}
years = []

#Opens the file
opened_file,year_lists = open_file()

#Loop that cycles through the data and merges them into a single dictionary
for file in opened_file:
    csv_file = csv.reader(file)
    next(csv_file)
    car_data, year = extract_data(csv_file)
    merge_year(years,year)
    merge_dict(main_dict, car_data)
    file.close()  

#Sends data to find the averages    
city_miles, highway_miles = average_mile(main_dict,years)
make_avgs_city = find_avg_mpg(city_miles)
make_avgs_hwy = find_avg_mpg(highway_miles)

#Sends data to be plotted
plot_mileage(years,city_miles,highway_miles)

#Prints the data in the correct format
print("Manufactures' average for ", end='')
print(', '.join('%04d'%i for i in year_lists))
print('City')
print('   Company: Mileage')
for make, avg_avg in make_avgs_city.items():
    print('{:>10}{}{:>6}'.format(make,':', '%.2f' %avg_avg))
print('Highway')
print('   Company: Mileage')
for make, avg_avg in make_avgs_hwy.items():
    print('{:>10}{}{:>6}'.format(make,':', '%.2f' %avg_avg))


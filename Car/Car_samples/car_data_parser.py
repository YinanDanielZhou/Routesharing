
# Parse the huge mysql data file downloaded from http://anrg.usc.edu/www/download_files/beijing_trace09.sql
# copy one line from the file and insert into a car_dat_piece.sql file
# filter out records with a speed of 0
from collections import defaultdict


cars = defaultdict(str)


with open('Car/Car_samples/car_data_piece.sql', 'r') as fileIn:
    # Iterate over each line in the file
    for line in fileIn:
        data_list = line.split("),(")
        print(data_list[0])
        print(len(data_list))

        for data_string in data_list:
            data = data_string.split(",")
            if data[5] != '0':
                output_string = "(" + data_string.split(",", 2)[2] + ")\n"
                cars[data[1]]+=(output_string)

for key in cars.keys():
    with open(f"Car/Car_samples/car_{key}_data.txt", 'w') as fileOut:
        fileOut.write(cars[key])
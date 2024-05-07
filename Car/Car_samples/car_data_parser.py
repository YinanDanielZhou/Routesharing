
# Parse the huge mysql data file downloaded from http://anrg.usc.edu/www/download_files/beijing_trace09.sql
# copy one line from the file and insert into a car_dat_piece.sql file
# filter out records with a speed of 0

with open('car_data_piece.sql', 'r') as fileIn, open("car_data_output.txt", 'a') as fileOut:
    # Iterate over each line in the file
    for line in fileIn:
        data_list = line.split("),(")
        print(data_list[0])
        print(len(data_list))

        for data_string in data_list:
            data = data_string.split(",")
            if data[5] != '0':
                output_string = "(" + data_string.split(",", 2)[2] + ")\n"
                fileOut.write(output_string)
                # print("(" + data_string.split(",", 2)[2] + ")")
                # print( "INSERT INTO `location` VALUES (" + data_string + ")" )
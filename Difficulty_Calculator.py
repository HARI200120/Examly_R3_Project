import csv

import xlsxwriter 

# Load a CSV file
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset

# Convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        if(column == 0):
            if(row[column].strip() == "MCQ"):
                row[column] = float(0)
            elif(row[column].strip() == "Fill_up"):
                row[column] = float(1)
            elif(row[column].strip() == "Program"):
                row[column] = float(2)
            elif(row[column].strip() == "Match"):
                row[column] = float(3)
        elif(column == 6):
            if(row[column].strip() == 'C'):
                row[column] = float(0)
            elif(row[column].strip() == 'C++'):
                row[column] = float(1)
            elif(row[column].strip() == 'JAVA'):
                row[column] = float(2)
        else:
            row[column] = float(row[column].strip())

filename = 'Dataset_csv.csv'
dataset = load_csv(filename)
for i in range(len(dataset[0])):
    str_column_to_float(dataset, i)

workbook = xlsxwriter.Workbook('Result.xlsx') 
worksheet = workbook.add_worksheet("My sheet")
for i in range(len(dataset)):
    easy = 0
    medium = 0
    hard = 0
    temp = []
    if(dataset[i][0] == 0 or dataset[i][0] == 1 or dataset[i][0] == 3):
        if(dataset[i][7] != 0 and dataset[i][1]/dataset[i][7] > 0.6):
            easy += 1
        elif(dataset[i][7] == 0 or dataset[i][1]/dataset[i][7] < 0.3):
            hard += 1
        else:
            medium += 1
        if(dataset[i][2] <= 60):
            easy += 1
        elif(dataset[i][2] > 90):
            hard += 1
        else:
            medium += 1
        if(dataset[i][3] == 0):
            easy += 1
        elif(dataset[i][3]>3):
            hard += 1
        else:
            medium += 1
        if(dataset[i][6] == 0):
            easy += 1
        elif(dataset[i][6] == 1):
            medium += 1
        else:
            hard += 1
        if(dataset[i][10] == 2):
            easy += 1
        elif(dataset[i][10] == 4):
            medium += 1
        else:
            hard += 1
    else:
        if(dataset[i][7] != 0 and dataset[i][1]/dataset[i][7] > 0.6):
            easy += 1
        elif(dataset[i][7] == 0 or dataset[i][1]/dataset[i][7] < 0.3):
            hard += 1
        else:
            medium += 1
        if(dataset[i][2] <= 60):
            easy += 1
        elif(dataset[i][2] > 90):
            hard += 1
        else:
            medium += 1
        if(dataset[i][4] <= 1):
            easy += 1
        elif(dataset[i][4]>2):
            hard += 1
        else:
            medium += 1
        if(dataset[i][5] <= 2):
            easy += 1
        elif(dataset[i][4]>6):
            hard += 1
        else:
            medium += 1
        if(dataset[i][6] == 0):
            easy += 1
        elif(dataset[i][6] == 1):
            medium += 1
        else:
            hard += 1
        if(dataset[i][10] == 25):
            easy += 1
        elif(dataset[i][10] == 50):
            medium += 1
        else:
            hard += 1
        
    for j in range(len(dataset[i])):
            if(j == 0):
                    if(dataset[i][j] == 0):
                        worksheet.write(i, j, 'MCQ')
                    elif(dataset[i][j] == 1):
                        worksheet.write(i, j, 'Fill_Up')
                    elif(dataset[i][j] == 2):
                        worksheet.write(i, j, 'Program')
                    else:
                        worksheet.write(i, j, 'Match')
            elif(j == 6):
                    if(dataset[i][j] == 0):
                        worksheet.write(i, j, 'C')
                    elif(dataset[i][j] == 1):
                        worksheet.write(i, j, 'C++')
                    else:
                        worksheet.write(i, j, 'JAVA')
            else:
                    worksheet.write(i, j, dataset[i][j])
    if(easy > medium):
                if(easy > hard):
                    worksheet.write(i, 11, 'Easy')
                else:
                    worksheet.write(i, 11, 'Hard')
    else:
                if(medium > hard):
                    worksheet.write(i, 11,'Medium')
                else:
                    worksheet.write(i, 11, 'Hard')
workbook.close()
            
            
            
        
        
        
        
            














        
        
        

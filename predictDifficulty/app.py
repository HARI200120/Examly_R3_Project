from flask import Flask, request, render_template
import csv
from math import sqrt 
import xlsxwriter 

app = Flask(__name__)

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
            elif(row[column].strip() == "Fill_Up"):
                row[column] = float(1)
            elif(row[column].strip() == "Program"):
                row[column] = float(2)
            elif(row[column].strip() == "Match"):
                row[column] = float(3)
            else:
                row[column] = float(row[column].strip())
         elif(column == 6):
             if(row[column].strip() == "C"):
                row[column] = float(0)
             elif(row[column].strip() == "C++"):
                row[column] = float(1)
             elif(row[column].strip() == "JAVA"):
                row[column] = float(2)
             else:
                 row[column] = float(row[column].strip())
         else:
             row[column] = float(row[column].strip())


# Convert string column to integer
def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = sorted(set(class_values))
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
		#print('[%s] => %d' % (value, i))
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup

# Find the min and max values for each column
def dataset_minmax(dataset):
	minmax = list()
	for i in range(len(dataset[0])):
		col_values = [row[i] for row in dataset]
		value_min = min(col_values)
		value_max = max(col_values)
		minmax.append([value_min, value_max])
	return minmax

# Rescale dataset columns to the range 0-1
def normalize_dataset(dataset, minmax):
	for row in dataset:
		for i in range(len(row)):
			row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])

# Calculate the Euclidean distance between two vectors
def euclidean_distance(row1, row2):
	distance = 0.0
	for i in range(len(row1)-1):
		distance += (row1[i] - row2[i])**2
	return sqrt(distance)

# Locate the most similar neighbors
def get_neighbors(train, test_row, num_neighbors):
	distances = list()
	for train_row in train:
		dist = euclidean_distance(test_row, train_row)
		distances.append((train_row, dist))
	distances.sort(key=lambda tup: tup[1])
	neighbors = list()
	for i in range(num_neighbors):
		neighbors.append(distances[i][0])
	return neighbors

# Make a prediction with neighbors
def predict_classification(train, test_row, num_neighbors):
	neighbors = get_neighbors(train, test_row, num_neighbors)
	output_values = [row[-1] for row in neighbors]
	prediction = max(set(output_values), key=output_values.count)
	return prediction

# Make a prediction with KNN
filename = 'training_set_csv.csv'
dataset = load_csv(filename)
for i in range(len(dataset[0])-1):
	str_column_to_float(dataset, i)
	
# define model parameter
num_neighbors = 10
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
      f = request.files['file']
    row = load_csv(f.filename)
    for i in range(len(row[0])-1):
        str_column_to_float(row, i)
    # convert class column to integers
    str_column_to_int(dataset, len(dataset[0])-1)
    scores = []
    for i in range(len(row)):
        predict = []
        for j in range(len(row[0])-1):
            predict.append(row[i][j])
        label = predict_classification(dataset, predict, num_neighbors)
        if(label == 0):
            predict.append("Easy")
        elif(label == 1):
            predict.append("Hard")
        else:
            predict.append("Medium")
        scores.append(predict)
    workbook = xlsxwriter.Workbook('Result.xlsx') 
    worksheet = workbook.add_worksheet("My sheet") 
    worksheet.write('A1', 'Question type') 
    worksheet.write('B1', 'No of Student Attempted') 
    worksheet.write('C1', 'Time taken') 
    worksheet.write('D1', 'Number of times options changed')
    worksheet.write('E1', 'Number of times compiled') 
    worksheet.write('F1', 'Number of Hints used') 
    worksheet.write('G1', 'Programming language') 
    worksheet.write('H1', 'Correct')
    worksheet.write('I1', 'Wrong') 
    worksheet.write('J1', 'Partially correct') 
    worksheet.write('K1', 'Maximum marks') 
    worksheet.write('L1', 'Difficulty')
    for i in range(len(scores)): 
        for j in range(len(scores[i])):
            if(j == 0):
                    if(scores[i][j] == 0):
                        worksheet.write(i+1, j, 'MCQ')
                    elif(row[i][j] == 1):
                        worksheet.write(i+1, j, 'Fill_Up')
                    elif(row[i][j] == 2):
                        worksheet.write(i+1, j, 'Program')
                    else:
                        worksheet.write(i+1, j, 'Match')
            elif(j == 6):
                    if(row[i][j] == 0):
                        worksheet.write(i+1, j, 'C')
                    elif(row[i][j] == 1):
                        worksheet.write(i+1, j, 'C++')
                    else:
                        worksheet.write(i+1, j, 'JAVA')
            else:
                    worksheet.write(i+1, j, scores[i][j])
    workbook.close()
    return render_template('index.html',Predict = "The results are saved as Excel file")

if __name__ == "__main__":
    app.run(debug=True)

#This code will take all files in .csv format and will return a matrix with the data, as time and OD reads

def transform():
	"""This function will  ask for the name of all files to process and insert them in a list"""
	data=[]
	get_files=0
	while get_files!="no":
		get_files=input('Which files you want to analyze?("no" if no more)')
		data.append(get_files)
	list_names=data[:-1]
	return  list_names


import csv

def readcsv(filename):
	ifile = open(filename, "rU")
	reader = csv.reader(ifile, delimiter=";")
	rownum = 0
	a = []
	for row in reader:
		a.append (row)
		rownum += 1

	ifile.close()
	a_int=[]
	for i in a:
		temp=[]
		for j in i:
			temp.append(float(j))
		a_int.append(temp)
	return a_int



def data_transf(x):
    new=readcsv(x)
    return new

allfiles=transform()

all_data=[]
for i in allfiles:
    alldata.append(data_transf(i))

    
    
    
    
    
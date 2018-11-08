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



alist=readcsv('CAM_simple_script.csv')
print (alist)

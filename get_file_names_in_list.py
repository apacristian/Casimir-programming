#here I will write script to convert OD curve data to matrix that will be analysed

def transform():
	"""This function will  ask for the name of all files to process and insert them in a list"""
	data=[]
	get_files=0
	while get_files!="no":
		get_files=input('Which files you want to analyze?("no" if no more)')
		data.append(get_files)
	data=data[:-1]
	return  data

print (transform())

from filereader import Filereader

if __name__ == '__main__':
	f = Filereader(datapath="./",data="data",params="params")
	results = f.getDatasetNumbers()
	if(results["error"]):
		print(results['message'])
	else: 
		for number in list(results['setnumbers']):
			constraints = f.getConstraints(setnumber=number)
			if(constraints['error']):
				print(constraints['message'])
			else:
				print(constraints)
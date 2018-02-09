from filereader import Filereader

def init_pass(constraints, filereader):
	I = dict()
	num_transactions = 0
	for transaction in f.getTransactions(setnumber=""):
		num_transactions += 1
		for item in transaction:
			if item in I:
				I[item] += 1
			else:
				I[item] = 1
	I = dict(sorted(I.items())) #Lexicographic
	I = [(i,I[i]/num_transactions) for i in sorted(I, key=constraints.get)] #based on MIS with support
	L = []
	found_i = False
	index_i = None
	for j in range(len(I)):
		if not found_i:
			if(I[j][1] >= constraints[I[j][0]]):
				L.append(I[j])
				found_i = True
				index_i = int(j)
		else:
			if(j-1>=0):
				if I[j][1]>=constraints[I[index_i][0]] : 
					L.append(I[j]) 
	return (L,num_transactions)
	
if __name__ == '__main__':
	f = Filereader(datapath="./",data="data",params="params")
	results = f.getDatasetNumbers()
	if(results["error"]):
		print(results['message'])
	else: 
		for number in list(results['setnumbers']):
			constraints = f.getConstraints(setnumber="")
			if(constraints['error']):
				print(constraints['message'])
			try:
				for num_constraints in range(constraints['count']):
					(L, num_transactions) = init_pass(constraints['constraints'][num_constraints],f)
					frequent = [i for i in L if i[1]>=constraints['constraints'][num_constraints][i[0]]]
					print(frequent)
			except Exception as e:
				print(str(e))
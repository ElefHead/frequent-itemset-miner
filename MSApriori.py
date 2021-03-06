from fileoperator import FileOperator
from itertools import combinations
import traceback as tb

def init_pass(constraints, f, number):
	I = dict()
	num_transactions = 0
	for transaction in f.getTransactions(setnumber=number):
		num_transactions += 1
		for item in transaction:
			if item in I:
				I[item] += 1
			else:
				I[item] = 1
	I = dict(sorted(I.items())) #Lexicographic
	I = [(i,I[i]) for i in sorted(I, key=constraints.get)] #based on MIS with support
	L = []
	found_i = False
	index_i = None
	for j in range(len(I)):
		if not found_i:
			if I[j][0] in constraints:
				mis = constraints[I[j][0]]
			else:
				mis = constraints['others']
				constraints[I[j][0]] = mis

			if(I[j][1]/num_transactions >= mis):
				L.append(I[j])
				found_i = True
				index_i = int(j)
		else:
			if(j-1>=0):
				if I[j][1]/num_transactions>=constraints[I[index_i][0]] : 
					L.append(I[j]) 
	return (L,num_transactions)

def msApriori():
	f = FileOperator(datapath="./",data="data2",params="params2",results="results2")
	results = f.getDatasetNumbers()
	if(results["error"]):
		print(results['message'])
	else: 
		for number in list(results['setnumbers']):
			constraints = f.getConstraints(setnumber=number)
			if(constraints['error']):
				print(constraints['message'])
			try:
				for num_constraints in range(len(constraints['count'])):
					k = 1
					(L, num_transactions) = init_pass(constraints['constraints'][num_constraints],f,number)
					for l in L:
						if l[0] not in constraints['constraints'][num_constraints]:
							constraints['constraints'][num_constraints][l[0]] = constraints['constraints'][num_constraints]['others']
					frequent = [(i[0],i[1]) for i in L if i[1]/num_transactions>=constraints['constraints'][num_constraints][i[0]]]
					f.writeFrequentItemset(specificConstraints(frequent,constraints['constraints'][num_constraints]['not_together'],constraints['constraints'][num_constraints]['must_have'],k),None,k,number,constraints['count'][num_constraints])
					while(frequent != []):
						k+=1
						if k==2:
							candidate = level2CandidateGen(L,constraints['constraints'][num_constraints],num_transactions)
							L = dict(L)
						else:
							candidate = msCandidateGen(frequent,L,constraints['constraints'][num_constraints],k-1,num_transactions)
						tailcounts = dict()
						if candidate != []:
							for transaction in f.getTransactions(setnumber=number):
								set_transaction = set(transaction)
								for c in candidate:
									set_c = set(c[0])
									set_tail = set(c[0][1:])
									if set_transaction.union(set_c) == set_transaction :
										c[1]+=1
									if set_tail.issubset(set_transaction):
										if str(c[0]) in tailcounts :
											tailcounts[str(c[0])] += 1
										else:
											tailcounts[str(c[0])] = 1
						frequent = [c for c in candidate if c[1]/num_transactions>=constraints['constraints'][num_constraints][c[0][0]]]
						f.writeFrequentItemset(specificConstraints(frequent,constraints['constraints'][num_constraints]['not_together'],constraints['constraints'][num_constraints]['must_have'],k),tailcounts,k,number,constraints['count'][num_constraints])
			except Exception:
				tb.print_exc()

def level2CandidateGen(L,constraints,num_transactions):
	sdc = constraints['SDC']
	candidate = []
	num = len(L)
	for i in range(num):
		if(L[i][1]/num_transactions>=constraints[L[i][0]]):
			for h in range(i+1,num):
				if L[h][1]/num_transactions>=constraints[L[i][0]] and abs(L[h][1]/num_transactions - L[i][1]/num_transactions) <= sdc:
					candidate.append([[L[i][0], L[h][0]],0])
	return candidate

def msCandidateGen(F,L,constraints,k,num_transactions):
	sdc = constraints['SDC']
	candidate = []
	num = len(F)
	frequentSet = set([str(f[0]) for f in F])
	for l in range(num):
		f1 = F[l][0]
		f1head = f1[0:k-1]
		f1last = f1[k-1]
		for r in range(l+1,num):
			f2 = F[r][0]
			f2head = f2[0:k-1]
			f2last = f2[k-1]
			if f1head == f2head and abs(L[f1last]/num_transactions - L[f2last]/num_transactions) <= sdc:
				c = f1 + [f2last]
				notfrequent = False
				for i in combinations(c, k):
					if {c[1]} in set(i) or constraints[c[0]]==constraints[c[1]]:
						if str(list(i)) not in frequentSet:
							notfrequent = True
				if not notfrequent:
					candidate.append([c,0])
	return candidate

def specificConstraints(frequent,not_together,must_have,k):
	must_have_set = set(must_have) if len(must_have)>1 else {must_have}
	requiredFrequent = []
	for f in frequent:
		good = True
		if k==1:
			fset = {f[0]}
		else:
			fset = set(f[0])
		if len(fset.intersection(must_have_set))>=1 or must_have=="":
			for nt in not_together:
				if len(fset.intersection(set(nt)))>1:
					good = False
		else:
			good = False
		if good:
			requiredFrequent.append(f)
	return requiredFrequent

	
if __name__ == '__main__':
	msApriori()
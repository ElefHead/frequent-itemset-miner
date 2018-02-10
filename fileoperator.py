from os import path, listdir, makedirs
from preprocess import Preprocess
import re

class FileOperator :
	def __init__(self, datapath="", data="data", params="params", results="results"):
		self._path = datapath
		self._data = {
			"data":data,
			"params":params,
			"results":results
		}
		self._patterns = {
			"data":r"(data)([0-9]*)-*(|[0-9]*)(.txt)",
			"params":r"(params)([0-9]*)-*(|[0-9]*)(.txt)"
		}

	def getConstraints(self,setnumber=""):
		try:
			preprocess = Preprocess()
			absolute_path = path.join(self._path, self._data['params'])
			count = 0
			constraints = []
			for filename in listdir(absolute_path):
				match = re.match(self._patterns['params'],filename)
				if match:
					if(match.group(2) == setnumber):
						count+=1
						with open(path.join(absolute_path,filename),"r") as c:
							constraints.append(preprocess.preprocessConstraints(c.read().split("\n")))
			if constraints == []:
				return {
					"error": True,
					"message": "Something's up"
				}
			return {
				"error": False,
				"constraints":constraints,
				"count":count
			}
		except FileNotFoundError:
			return {
				"error": True,
				"message": """Files not found. Please make sure that there is a directory called 'params' 
				in the given path, with the files named as params.txt or params1.txt or params1-1.txt"""
			}

	def getDatasetNumbers(self):
		try:
			absolute_path = path.join(self._path, self._data['data'])
			setnumbers = []
			for filename in listdir(absolute_path):
				match = re.match(self._patterns['data'], filename)
				if match:
					setnumbers.append(match.group(2))
			if (setnumbers == []):
				return {
					"error": True,
					"message": """Files not found, please make sure the naming is of the form data.txt or data1.txt or data1-1.txt"""
				}
			return {
				"error": False,
				"setnumbers":set(setnumbers)
			}
		except FileNotFoundError:
			return {
				"error": True,
				"message": """Files not found. Please make sure that there is some data directory and you specify its name while initializing the class
								and in the path, the filenames are of the form data.txt or data1.txt or data1-1.txt"""
			}

	def getTransactions(self, setnumber=""):
		preprocess = Preprocess()
		try:
			absolute_path = path.join(self._path, self._data['data'])
			for filename in listdir(absolute_path):
				match = re.match(self._patterns['data'],filename)
				if match:
					if(match.group(2)==setnumber):
						with open(path.join(absolute_path,match.group()),"r") as t:
							for transaction in t:
								yield preprocess.preprocessTransaction(transaction.strip())
		except FileNotFoundError:
			raise Exception("Files not found")

	def writeFrequentItemset(self,frequent,tailcounts=None,k=0,datanum="",paramnum=None):
		if(frequent!=[] or k<=1):
			filename = "results"+datanum
			if(paramnum==None):
				filename += ".txt"
			else:
				filename += "-"+str(paramnum+1)+".txt"
			results_directory = path.join(self._path,self._data['results'])
			if not path.exists(results_directory):
				makedirs(results_directory)
			absolute_path = path.join(results_directory, filename)
			if path.exists(absolute_path):
				write_mode = 'a'
			else:
				write_mode = 'w'
			numfreq = len(frequent)
			with open(absolute_path,write_mode) as w:
				w.write("Frequent "+str(k)+"-itemsets: \n")
				if k==1:
					for f in frequent:
						w.write("\t"+str(f[1])+" : "+ "{ " + str(f[0]) +" }\n")
				else:
					for i in range(numfreq):
						w.write("\t"+str(frequent[i][1])+" : { "+ ", ".join([str (x) for x in frequent[i][0]])+" }\n")
						w.write("Tailcount: "+str(tailcounts[str(frequent[i][0][1:])])+"\n")
				w.write("\tTotal number of frequent "+str(k)+"-itemsets = "+str(numfreq)+"\n\n")

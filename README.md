# Frequent Itemset Miner
A python implementation of the Multiple Support Apriori Algorithm

This implementation is based on the algorithm described in the book [Web Data Mining](https://www.cs.uic.edu/~liub/WebMiningBook.html) by [Prof. Bing Liu](https://www.cs.uic.edu/~liub/)  
  
---  

## Brief Description  

  
**preprocess.py** - Handles converting the params and transaction lines into usable formats.  
**fileoperator.py** - Handles all the reading and writing.  
**MSApriori.py** - where main resides. Where the actual algorithm is implemented. 
  
---

## To Run Code  

Please make sure that this is your folder structure (where the code resides)

![Directory Structure](https://github.com/ElefHead/frequent-itemset-miner/blob/master/img/dir_structure.png "Directory Structure")

Inside MSApriori.py, line 39 : You can specify where your data resides. It is relative to the current directory.  
Same way for params and results. If there is no results directory, the code will create one with
the name as specified in this line.  

---

## Feeding Data  

This code can work on data specified in multiple files, multiple sets of parameters and generate relevant results based on the data and params.  
This is done by naming the data appropriately. Any file of the form data1.txt, data1-1.txt, basically data(*N*)(-*M*?).txt will
be considered as one dataset *N*.  
The corresponding params have to be specified as params(*N*)-(*M*).txt.

Please see [data2/](https://github.com/ElefHead/association-rule-miner/tree/master/data2), [params2/](https://github.com/ElefHead/association-rule-miner/tree/master/params2), and [results2/](https://github.com/ElefHead/association-rule-miner/tree/master/results2) for example.  

To run the code on data2/ and params2/ , please change line 39 from  
```python
f = FileOperator(datapath="./",data="data",params="params",results="results")  
```
to  
```python
f = FileOperator(datapath="./",data="data2",params="params2",results="results2")
```  

and delete the results2/ folder(or move it) because the files won't be written over, the outputs will be appended.

**_There were some basic assumptions made as to how the data will be presented to the code. 
To test custom data, please use the given data and params files as example input formats._**  

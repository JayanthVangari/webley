#!/usr/bin/env python

import csv
import sys,getopt
import decimal

isthere=False # boolean that is set to true if a combination of dishes equaling target price is found
Dishes=[] # final list of dishes in the combination


# findDishCombo with parameters dishes list, current target, current index,temporary list of dishes
# recursively finds a combination of dishes that equal to target price
def findDishCombo(dishes_list, target, index, temp):
	global isthere
    	global Dishes
    	if target < 0:
        	return 0
        # if target becomes 0 add temp list values to Dishes which is the final combination of dishes and return.
    	if target == 0:
		isthere=True
		Dishes=temp
        	return 1
	# iterate over dishes_list starting from index i and recursively call 
	# findDishCombo adding the dish to temp list, and backtrack and call recursively when target becomes less than 0. 
    	for i in xrange(index, len(dishes_list)):
		findDishCombo(dishes_list, round(decimal.Decimal(target-float(dishes_list[i][1])),3), i+1, temp+[dishes_list[i]])
		if isthere:
			return 1


# is_number checks if the string given is a number
def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False

    return True


# handler parses the reader object and  
# calls findDishCombo passing dishes list and target price	

def handler(reader):
	dishes_list=[]
	target_price=""
	# target price in the first line of file is read into variable target_price
	try:
        	target_price=next(reader)[1]
	except:
		 print "\n\tERR: target price missing in the first line, exiting..\n"
		 return -1	
	if(target_price.startswith("$")):
  		target_price=float(target_price[1:])
	else:
		target_price=float(target_price)
	# iterate over data values and pushing 'em into dishes list 
	for row in reader:
		 # if price of dish has '$' on it, ignore and just read price
		if row[1].startswith("$"): 
			row[1]=row[1][1:]
		
		# adding values to dishes list only if there are no missing fields and prices are numbers	
		if len(row[0])>0 and len(row[1])>0 and is_number(row[1]): 
			dishes_list.append(row)
		else:
			print "\nWARN : skipping any ill-defined value(s) from computation..\n"
	# sort the dishes list in ascending order with respect to prices 
	dishes_list=sorted(dishes_list,key=lambda i:float(i[1])) 
	if len(dishes_list)>0:	
		return findDishCombo(dishes_list,target_price,0,[])
	else:
		print "\n\t ERR : No proper data given.\n"
		return -1
def main(argv):
	inputfile=''
	try:
		opts,args=getopt.getopt(argv,"hi:")
		if len(opts)<1:
			print '\n\tWRONG COMMAND USE : ./ans.py -i <inputfile>\n'
			sys.exit(2)			
	except getopt.GetoptError:
		print '\n\tWRONG COMMAND  USE : ./ans.py -i <inputfile>\n'
		sys.exit(2)
 	# parse command line arguments and retrieve the file name
	for opt,arg in opts:
		if opt =="-h":
			print '\n\tUSE : ./ans.py -i <inputfile>\n'
			sys.exit(2)
		elif opt=="-i":
         		inputfile = arg
		else:
			print '\n\tWRONG COMMAND USE : ./ans.py -i <inputfile>\n'
			
	try:
		# read csv file into the reader object 		
		with open(inputfile,'rb') as csvfile:
			reader=csv.reader(csvfile)
			k=handler(reader)
			# if a combination of dishes does exist print dishes and price formatted. 
			if k>0:
				print "OUTPUT:"
				print '{:>30} {:>15}'.format("Dishes","Price");
				print '{:>30} {:>15}'.format("--------","------");
				for i in Dishes:
					print '{:>30} {:>15}'.format(i[0],i[1])
			elif k==0:
				print "\nNo combination of dishes found that sum up to target price\n"
	except(IOError):
		print "\n\tfile doesn't exist, please give an existing file name\n"
if __name__ == "__main__":
   main(sys.argv[1:])

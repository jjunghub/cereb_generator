from dateutil import parser
import ast, re
from numpy import NaN
from printUtils import *
def cleansing_publications(paper):
	print(blue("Processing Publication"))
	paper['publication'] = paper.publication.apply(get_repre_pbc)
	print(blue("Done processing Publication"))
	return paper

def get_repre_pbc(pbc):
	src = ['scp', 'wos', 'axv', 'ieee']
	repre = None
	if str(pbc) == 'nan' or str(pbc) == 'None': 
		return None
		
	for s in src:
		pbc_dict = ast.literal_eval(str(pbc))
		if pbc_dict == None: continue
		if pbc_dict.get(s):
			repre = cleansing(pbc_dict.get(s).replace(' & ', ' and ').replace('&', ' and ').strip())
			if repre != None:
				break
	if repre!=None:
		repre = cleansing(repre.strip())
	if repre == None:
		return None
	else:
		return repre

def cleansing(x):
	if str(x).isdigit():
		return None

	if is_date(x):
		return None

	if x.upper() == 'WWW':
		return None
	
	match = re.compile(r'[0-9]{1,3}(th|rd|nd|st)').search(x)
	if match:
		x = re.compile(r'[0-9]{1,3}(th|rd|nd|st)').sub('', x).strip()
		
	match = re.compile(r'\(\w+\)').search(x)
	# abb =''
	if match:
		# abb = match.group(0)[1:-1]
		x = re.compile(r'\(\w+\)').sub('', x).strip()	
	   
	match = re.compile(r'[^\w\s]|\d').search(x)
	if match:
		x = re.compile(r'[^\w\s]|\d').sub('', x).strip()	

	if x == '' or x == None:
		return None
	return x

def is_date(x):
	try:
		dt = parser.parse(x)
		return True
	except:
		return False



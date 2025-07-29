import os,sys,getpass,platform
from project.sparta_8345d6a892.sparta_952c41e91e.qube_ef9e4f9eb1 import sparta_9c89cfd808,sparta_f9f684c510
def sparta_87e146dd92(full_path,b_print=False):
	B=b_print;A=full_path
	try:
		if not os.path.exists(A):
			os.makedirs(A)
			if B:print(f"Folder created successfully at {A}")
		elif B:print(f"Folder already exists at {A}")
	except Exception as C:print(f"An error occurred: {C}")
def sparta_2f207ab8e0():
	if sparta_f9f684c510():A='/app/APPDATA/local_db/db.sqlite3'
	else:C=sparta_9c89cfd808();B=os.path.join(C,'data');sparta_87e146dd92(B);A=os.path.join(B,'db.sqlite3')
	return A
import os,sys,getpass,platform
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_f0d228f17a import sparta_ca71f9cc05,sparta_514b10b7c2
def sparta_4eef2501f8(full_path,b_print=False):
	B=b_print;A=full_path
	try:
		if not os.path.exists(A):
			os.makedirs(A)
			if B:print(f"Folder created successfully at {A}")
		elif B:print(f"Folder already exists at {A}")
	except Exception as C:print(f"An error occurred: {C}")
def sparta_a1d3b46409():
	if sparta_514b10b7c2():A='/app/APPDATA/local_db/db.sqlite3'
	else:C=sparta_ca71f9cc05();B=os.path.join(C,'data');sparta_4eef2501f8(B);A=os.path.join(B,'db.sqlite3')
	return A
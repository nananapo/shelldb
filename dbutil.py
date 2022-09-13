import subprocess
from time import sleep

def execsql(dbpath, sql):
	# injection
	sql = str(sql) + "\n"
	proc = subprocess.run(["sqlite3", str(dbpath)], input=sql, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
	print(proc.stdout)	

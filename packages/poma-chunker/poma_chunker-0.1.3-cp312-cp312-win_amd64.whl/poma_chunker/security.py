D=Exception
import os,sys,platform as B,threading as E,time as C,random as F
A=E.local()
def ensure_secure_environment():
	if not hasattr(A,'checked'):
		if not G():C.sleep(F.random()*2);sys.exit(1)
		A.checked=True
def G():
	H=C.time();E=0
	for I in range(1000):E=hash((E,I))&4294967295
	J=C.time()-H
	if J>.1:return False
	K=['PYTHONDEVMODE','PYTHONINSPECT','PYTHONDEBUG','PYDEVD_LOAD_VALUES_ASYNC']
	for L in K:
		if os.environ.get(L):return False
	for M in list(sys.modules.keys()):
		if any(A in M.lower()for A in['debugger','debug','pydevd','pdb','_pydev_']):return False
	if B.system()=='Windows':
		try:
			import ctypes as A
			if A.windll.kernel32.IsDebuggerPresent()!=0:return False
			N=A.windll.kernel32.GetCurrentProcess();F=A.c_bool();A.windll.kernel32.CheckRemoteDebuggerPresent(N,A.byref(F))
			if F.value:return False
		except D:pass
	elif B.system()=='Darwin':
		try:
			import subprocess as O;G=O.run(['sysctl','kern.proc.trace'],capture_output=True,text=True)
			if G.returncode==0 and'0'not in G.stdout:return False
		except D:pass
	elif B.system()=='Linux':
		try:
			with open('/proc/self/status','r')as P:
				Q=P.read()
				if'TracerPid:\t0'not in Q:return False
		except D:pass
	else:return False
	return True
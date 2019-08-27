#  ================================================================================================
#  ==  BRIEF  : print modules versions to help with reproducibility
#  ==  AUTHOR : stephen.burns.menary@cern.ch
#  ================================================================================================


import sys
from  .setup import version as rt_version


#  Print the versions of whatever modules we depend on
#
def print_versions (*argv) :
	argv = list(argv)
	import sys
	print(f"python version is: {sys.version}")
	print(f"\nreview_tools version is: {rt_version}")
	if "sys" in argv : argv.remove("sys")
	if "ipywidgets" in argv :
		import ipywidgets
		print(f"\nipywidgets version is: {ipywidgets.__version__}")
		argv.remove("ipywidgets")
	if "IPython" in argv :
		import IPython
		print(f"\nIPython version is: {IPython.__version__}")
		argv.remove("IPython")
	for module in argv :
		print(f"\nWARNING\t\tprint_versions()\t\tModule \'{module}\' not recognised")


# Fallback: calls run() when run as a script
#
if sys.__name__ == "__main__" :
	run()
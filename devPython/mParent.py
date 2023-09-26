def mParent(list, firstIsParent=False):
	"""
	mParent
	utility function for maya

	gets MSelection List of DAG nodes, making the end of the list the parent of the rest

	
	:param list:			expects MSelectionList - pipe input through getDAG() before invoking this function
	:param firstIsParent:	expects True/False - if first item should be the Parent instead

	"""
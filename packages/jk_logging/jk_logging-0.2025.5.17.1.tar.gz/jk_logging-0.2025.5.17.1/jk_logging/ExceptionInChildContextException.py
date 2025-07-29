

import jk_exceptionhelper


#
# This class is used to enable a structured way of recovering from nested log contexts.
#
class ExceptionInChildContextException(Exception):

	def __init__(self, originalExeption:Exception, exceptionObj:jk_exceptionhelper.ExceptionObject, exitCode:int = None):
		self.originalExeption = originalExeption
		self.exceptionObj = exceptionObj
	#

#






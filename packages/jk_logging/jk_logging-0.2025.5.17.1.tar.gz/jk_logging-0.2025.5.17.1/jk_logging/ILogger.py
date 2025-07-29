

import typing

import jk_exceptionhelper




#
# This class is an equivalent to interfaces known from other OOP languages.
#
class ILogger(object):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Perform logging with log level ERROR.
	#
	# @param	string text		The text to write to this logger.
	#
	def error(self, textOrException:typing.Union[str,BaseException,jk_exceptionhelper.ExceptionObject]):
		raise NotImplementedError()
	#

	#
	# Perform logging with log level EXCEPTION.
	#
	# @param	Exception exception		The exception to write to this logger.
	#
	def exception(self, exception:typing.Union[BaseException,jk_exceptionhelper.ExceptionObject]):
		raise NotImplementedError()
	#

	#
	# Perform logging with log level SUCCESS.
	#
	# @param	string text		The text to write to this logger.
	#
	def success(self, text:str):
		raise NotImplementedError()
	#

	#
	# Perform logging with log level WARNING. This method is provided for convenience and is identical with <c>warn()</c>.
	#
	# @param	string text		The text to write to this logger.
	#
	def warning(self, text:str):
		raise NotImplementedError()
	#

	#
	# Perform logging with log level WARNING. This method is provided for convenience and is identical with <c>warning()</c>.
	#
	# @param	string text		The text to write to this logger.
	#
	def warn(self, text:str):
		raise NotImplementedError()
	#

	#
	# Perform logging with log level INFO.
	#
	# @param	string text		The text to write to this logger.
	#
	def info(self, text:str):
		raise NotImplementedError()
	#

	#
	# Perform logging with log level NOTICE.
	#
	# @param	string text		The text to write to this logger.
	#
	def notice(self, text:str):
		raise NotImplementedError()
	#

	#
	# Perform logging with log level DEBUG.
	#
	# @param	string text		The text to write to this logger.
	#
	def debug(self, text:str):
		raise NotImplementedError()
	#

	#
	# Perform logging with log level TRACE.
	#
	# @param	string text		The text to write to this logger.
	#
	def trace(self, text:str):
		raise NotImplementedError()
	#

#


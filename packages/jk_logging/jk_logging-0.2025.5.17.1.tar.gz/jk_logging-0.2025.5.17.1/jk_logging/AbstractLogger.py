


from __future__ import annotations

import time
import abc
import typing

import jk_exceptionhelper

from .ILogger import ILogger
from .ExceptionInChildContextException import ExceptionInChildContextException
from .EnumLogLevel import *
from .impl.IDCounter import IDCounter









class AbstractLogger(ILogger):

	__metaclass__ = abc.ABCMeta

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			idCounter:typing.Union[IDCounter,None],
		):

		if idCounter is None:
			idCounter = IDCounter()
		else:
			if not isinstance(idCounter, IDCounter):
				raise Exception("idCounter is invalid: " + repr(idCounter))
		self._idCounter = idCounter
		self._indentationLevel = 0
		self._parentLogEntryID = None
		self._stackTraceProcessor:typing.Union[jk_exceptionhelper.StackTraceProcessor,None] = None
	#

	################################################################################################################################
	## Properties
	################################################################################################################################

	@property
	def logMsgFormatter(self):
		return None
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	#
	# Create a log entry data record.
	#
	# @param		int logEntryID			The ID of this log entry or <c>None</c> if not applicable.
	# @param		int indentation			The current indentation level. Top level entries will have a value of zero here.
	#										This value is always zero if the feature is not supported.
	# @param		int parentLogEntryID	A log entry ID of the parent of this log entry or <c>None</c> if not applicable (or not supported).
	# @param		EnumLogLevel logLevel	A singleton that represents the log level.
	# @param		str text				A text to associate with this log entry.
	# @param		list newList			Typically specify an empty list here that will hold child log entries in the future.
	#
	def _createDescendLogEntryStruct(self, logEntryID, indentation, parentLogEntryID, logLevel, text, newList):
		timeStamp = time.time()

		return ("desc", logEntryID, indentation, parentLogEntryID, timeStamp, logLevel, text, newList)
	#

	#
	# Converts an instance of <c>jk_exceptionhelper.ExceptionObject</c> to a tuple of the following structure:
	#
	# * 1) str: the exception class name
	# * 2) str: the exception text
	# * 3) list with tuples representing stack trace elements:
	#		* 1) str: file path
	#		* 2) int: line number
	#		* 3) str: calling scope
	#		* 4) str: source code line
	# * 4) either None or a tuple representing a nested exception
	#
	# def __exceptionObjToTuples(self, exceptionObject:jk_exceptionhelper.ExceptionObject) -> tuple:
	# 	return (
	# 		exceptionObject.exceptionClassName,
	# 		exceptionObject.exceptionTextHR,
	# 		[ (x.filePath, x.lineNo, x.callingScope, x.sourceCodeLine) for x in exceptionObject.stackTrace ]
	# 			if exceptionObject.stackTrace else [],
	# 		self.__exceptionObjToTuples(exceptionObject.nestedException) if exceptionObject.nestedException else None,
	# 	)
	# #

	#
	# Converts an instance of <c>jk_exceptionhelper.ExceptionObject</c> to a tuple of the following structure:
	#
	# * 1) str: the exception class name.
	# * 2) str: the exception text.
	# * 3) list with tuples representing stack trace elements:
	#		* 1) str: file path
	#		* 2) int: line number
	#		* 3) str: calling scope
	#		* 4) str: source code line
	# * 4) either None or a dictionary of key value pairs. The keys must be strings, the values must be JSON serializable.
	# * 5) either None or a tuple representing a nested exception.
	#
	def __exceptionObjToTuples2(self, exceptionObject:jk_exceptionhelper.ExceptionObject) -> tuple:
		return (
			exceptionObject.exceptionClassName,
			exceptionObject.exceptionTextHR,
			[ (x.filePath, x.lineNo, x.callingScope, x.sourceCodeLine) for x in exceptionObject.stackTrace ]
				if exceptionObject.stackTrace else [],
			exceptionObject.extraValues,
			self.__exceptionObjToTuples2(exceptionObject.nestedException) if exceptionObject.nestedException else None,
		)
	#

	#
	# Creates a log entry data record.
	#
	# @param		int logEntryID			The ID of this log entry or <c>None</c> if not applicable.
	# @param		int indentation			The current indentation level. Top level entries will have a value of zero here.
	#										This value is always zero if the feature is not supported.
	# @param		int parentLogEntryID	A log entry ID of the parent of this log entry or <c>None</c> if not applicable (or not supported).
	# @param		EnumLogLevel logLevel	A singleton that represents the log level.
	# @param		obj textOrException		Either an exception object or a text
	#
	def _createNormalLogEntryStruct(self,
			logEntryID:int,
			indentation:int,
			parentLogEntryID:int,
			logLevel:EnumLogLevel,
			textOrException:typing.Union[BaseException,jk_exceptionhelper.ExceptionObject,str],
		):
		timeStamp = time.time()

		if isinstance(textOrException, BaseException):
			_e = jk_exceptionhelper.ExceptionObject.fromException(
				textOrException,
				ignoreJKTypingCheckFunctionSignatureFrames=True,
				ignoreJKTestingAssertFrames=True,
				ignoreJKLoggingFrames=True,
				stackTraceProcessor=self._stackTraceProcessor,
			)
			_t = self.__exceptionObjToTuples2(_e)
			return (
				"ex2",
				logEntryID,
				indentation,
				parentLogEntryID,
				timeStamp,
				logLevel,
				_t[0],
				_t[1],
				_t[2],
				_t[3],
				_t[4],
			)

		elif isinstance(textOrException, jk_exceptionhelper.ExceptionObject):
			_t = self.__exceptionObjToTuples2(textOrException)
			return (
				"ex2",
				logEntryID,
				indentation,
				parentLogEntryID,
				timeStamp,
				logLevel,
				_t[0],
				_t[1],
				_t[2],
				_t[3],
				_t[4],
			)

		else:
			textOrException = str(textOrException)
			return (
				"txt",
				logEntryID,
				indentation,
				parentLogEntryID,
				timeStamp,
				logLevel,
				textOrException.rstrip("\n")
			)
	#

	#
	# Perform a descending operation. Overwrite this method in subclasses.
	#
	# @param		list logEntryStruct			A log entry structure. See <c>_logi()</c> for a detailed description.
	# @return		AbstractLogger				Return a logger instance representing the logger for a descended level.
	#
	@abc.abstractmethod
	def _descend(self, logEntryStruct):
		raise NotImplementedError('subclasses must override _descend()!')
	#

	#
	# Perform the log operation. This is the heart of each logger. Overwrite this method in subclasses.
	#
	# @param		list logEntryStruct						A log entry structure. Each entry consists of the following elements:
	#														0) <c>str</c> ---- The type of the log entry: "txt", "ex", "ex2", "desc"
	#														1) <c>str</c> ---- The ID of the log entry or <c>None</c> if unused
	#														2) <c>int</c> ---- The indentation level
	#														3) <c>str</c> ---- The ID of the parent log entry or <c>None</c> if unused
	#														4) <c>float</c> ---- The time stamp in seconds since epoch
	#														5) <c>EnumLogLevel</c> ---- The type of the log entry
	#														If the log entry is a text entry:
	#														6) <c>str</c> ---- The text of the log message
	#														If the log entry is a descending entry:
	#														6) <c>str</c> ---- The text of the log message
	#														7) <c>list</c> ---- A list containing nested log items
	#														If the log entry is an exception of type "ex":
	#														6) <c>str</c> ---- The exception class name
	#														7) <c>str</c> ---- The exception text
	#														8) <c>list</c> ---- A list of stack trace elements or <c>None</c>
	#														9) <c>list</c> ---- If there is a nested exception: A four element list with exception class name, exception text, stack trace, and nested exception
	#														If the log entry is an exception of type "ex2":
	#														6) <c>str</c> ---- The exception class name
	#														7) <c>str</c> ---- The exception text
	#														8) <c>list</c> ---- A list of stack trace elements or <c>None</c>
	#														9) <c>dict</c> ---- A JSON serializable dict of key value pairs or <c>None</c>
	#														10) <c>list</c> ---- If there is a nested exception: A four element list with exception class name, exception text, stack trace, and nested exception
	#														Each stack trace element has the following structure:
	#														0) <c>str</c> ---- The source code file path
	#														1) <c>int</c> ---- The source code line number
	#														2) <c>str</c> ---- The source code module name
	#														3) <c>str</c> ---- The source code line in plain text where the error occurred
	# @param		bool bNeedsIndentationLevelAdaption		If <c>True</c> is specified the log entry record still needs adaption at the
	#														indentation level field. This is because it was generated somewhere else and
	#														therefor has been provided by a different logger in a maybe different indentation
	#														context.
	#
	@abc.abstractmethod
	def _logi(self, logEntryStruct, bNeedsIndentationLevelAdaption):
		raise NotImplementedError('subclasses must override _logi()!')
	#

	#
	# This method is invoked in order to log a list of log entries. After adapting the indentation level to the indentation level
	# currently used by this logger either <c>_logi()</c> is called or <c>_descend()</c> in order to perform the logging.
	#
	# The default implementation provided here will perform indentation level adaption as needed. In order to do so a copy of the
	# raw log entry is created.
	#
	# @param		list logEntryStruct						A log entry structure. See <c>_logi()</c> for a detailed description.
	# @param		bool bNeedsIndentationLevelAdaption		If <c>True</c> is specified the log entry records still needs adaption at the
	#														indentation level field. This is because it was generated somewhere else and
	#														therefor has been provided by a different logger in a maybe different indentation
	#														context.
	#
	def _logiAll(self, logEntryStructList, bNeedsIndentationLevelAdaption):
		for logEntryStruct in logEntryStructList:
			#logEntryStruct = list(logEntryStruct)
			#logEntryStruct[2] = self._indentationLevel
			self._logi(logEntryStruct, bNeedsIndentationLevelAdaption)
			if logEntryStruct[0] == "desc":
				logEntryStructClone = (
					logEntryStruct[0],		# str : sType				---- log entry type: "txt", "ex", "ex2", "desc"
					logEntryStruct[1],		# int : logEntryID			---- log entry ID
					logEntryStruct[2],		# int : indentationLevel	---- indentation level
					logEntryStruct[3],		# int : parentLogEntryID	---- ID of the parent log entry
					logEntryStruct[4],		# float : timeStamp			---- time stamp in seconds since epoch
					logEntryStruct[5],		# EnumLogLevel : logLevel	---- type of the log entry
					logEntryStruct[6],		# str : logMsg				---- log message
					[]						# list : nestedList			---- nested log elements
				)
				self._descend(logEntryStructClone)._logiAll(logEntryStruct[7], bNeedsIndentationLevelAdaption)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def log(self, logLevel:EnumLogLevel, logData):
		if logLevel == EnumLogLevel.TRACE:
			self.trace(logData)
		elif logLevel == EnumLogLevel.DEBUG:
			self.debug(logData)
		elif logLevel == EnumLogLevel.NOTICE:
			self.notice(logData)
		elif logLevel == EnumLogLevel.INFO:
			self.info(logData)
		elif logLevel == EnumLogLevel.STDOUT:
			self.stdout(logData)
		elif logLevel == EnumLogLevel.SUCCESS:
			self.success(logData)
		elif logLevel == EnumLogLevel.WARNING:
			self.warn(logData)
		elif logLevel == EnumLogLevel.ERROR:
			self.error(logData)
		elif logLevel == EnumLogLevel.STDERR:
			self.stderr(logData)
		elif logLevel == EnumLogLevel.EXCEPTION:
			self.exception(logData)
		else:
			raise Exception("This log level is not supported: {}".format(logLevel))
	#

	#
	# Perform logging with log level ERROR.
	#
	# @param	string text		The text to write to this logger.
	#
	def error(self, textOrException:typing.Union[str,BaseException,jk_exceptionhelper.ExceptionObject]):
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.ERROR, textOrException), False)
	#

	#
	# Perform logging with log level EXCEPTION.
	#
	# @param	Exception exception		The exception to write to this logger.
	#
	def exception(self, exception:typing.Union[BaseException,jk_exceptionhelper.ExceptionObject]):
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.EXCEPTION, exception), False)
	#

	#
	# Perform logging with log level ERROR.
	# This method is intended to be used in conjunction with STDERR handlers.
	#
	# @param	string text		The text to write to this logger.
	#
	def stderr(self, text:str):
		assert isinstance(text, str)
		text = text.rstrip("\n")
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.STDERR, text), False)
	#

	#
	# Perform logging with log level STDOUT.
	# This method is intended to be used in conjunction with STDOUT handlers.
	#
	# @param	string text		The text to write to this logger.
	#
	def stdout(self, text:str):
		assert isinstance(text, str)
		text = text.rstrip("\n")
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.STDOUT, text), False)
	#

	#
	# Perform logging with log level SUCCESS.
	#
	# @param	string text		The text to write to this logger.
	#
	def success(self, text:str):
		assert isinstance(text, str)
		text = text.rstrip("\n")
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.SUCCESS, text), False)
	#

	#
	# Perform logging with log level WARNING. This method is provided for convenience and is identical with <c>warn()</c>.
	#
	# @param	string text		The text to write to this logger.
	#
	def warning(self, text:str):
		assert isinstance(text, str)
		text = text.rstrip("\n")
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.WARNING, text), False)
	#

	#
	# Perform logging with log level WARNING. This method is provided for convenience and is identical with <c>warning()</c>.
	#
	# @param	string text		The text to write to this logger.
	#
	def warn(self, text:str):
		assert isinstance(text, str)
		text = text.rstrip("\n")
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.WARNING, text), False)
	#

	#
	# Perform logging with log level INFO.
	#
	# @param	string text		The text to write to this logger.
	#
	def info(self, text:str):
		assert isinstance(text, str)
		text = text.rstrip("\n")
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.INFO, text), False)
	#

	#
	# Perform logging with log level NOTICE.
	#
	# @param	string text		The text to write to this logger.
	#
	def notice(self, text:str):
		assert isinstance(text, str)
		text = text.rstrip("\n")
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.NOTICE, text), False)
	#

	#
	# Perform logging with log level DEBUG.
	#
	# @param	string text		The text to write to this logger.
	#
	def debug(self, text:str):
		assert isinstance(text, str)
		text = text.rstrip("\n")
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.DEBUG, text), False)
	#

	#
	# Perform logging with log level TRACE.
	#
	# @param	string text		The text to write to this logger.
	#
	def trace(self, text:str):
		assert isinstance(text, str)
		text = text.rstrip("\n")
		self._logi(self._createNormalLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, EnumLogLevel.TRACE, text), False)
	#

	#
	# Create a nested logger. This new logger can than be used like the current logger, but all log messages will be delivered
	# to an subordinate log structure (if supported by this logger).
	#
	def descend(self, text:str, logLevel:EnumLogLevel = None, bWithhold:bool = False, bWithholdVerbose:bool = False) -> AbstractLogger:
		assert isinstance(text, str)

		if logLevel is None:
			logLevel = EnumLogLevel.INFO

		# NOTE: let's no longer use this restriction.
		# else:
		# 	assert logLevel in ( EnumLogLevel.INFO, EnumLogLevel.NOTICE )

		logEntryStruct = self._createDescendLogEntryStruct(self._idCounter.next(), self._indentationLevel, self._parentLogEntryID, logLevel, text, [])
		self._logi(logEntryStruct, False)

		if bWithhold:
			from . import WithholdingLogger			# NOTE: we avoid cyclic dependencies this way
			return WithholdingLogger.create(self._descend(logEntryStruct), bVerbose=bWithholdVerbose)
		else:
			return self._descend(logEntryStruct)
	#

	#
	# If this logger is buffering log messages, clear all log messages from this buffer.
	# If this logger has references to other loggers, such as a <c>FilterLogger</c>
	# or a <c>MulticastLogger</c>
	#
	#def clear(self):
	#	NOTE: This method has been removed as this can not be a general capability of loggers
	#		See BufferLogger.clear() for details
	#	pass
	#

	#
	# Close this logger. Some logger make use of additional resources (such as files) which will be (permanently) closed by invoking this method.
	# By default this method does nothing. Some loggers may overwrite this method in order to make use of that functionality. After closing
	# a logger you should not invoke any more logging methods of that logger. Loggers that make use of <c>close()</c> should reject any logging
	# request after a <c>close()</c> has been invoked. <c>close()</c> must always be implemented as an indempotent operation: Redundant calls to <c>close()</c>
	# should cause no problems.
	#
	def close(self):
		pass
	#

	def __enter__(self):
		return self
	#

	def __exit__(self, ex_type:type, ex_value:Exception, ex_traceback):
		if ex_type != None:
			exObj = jk_exceptionhelper.ExceptionObject.fromException(ex_value, ignoreJKTypingCheckFunctionSignatureFrames=True, ignoreJKTestingAssertFrames=True, ignoreJKLoggingFrames=True)
			#exObj.dump("##\t")
			#import sys
			#import traceback
			#traceback.print_stack(file=sys.stdout)

			if isinstance(ex_value, ExceptionInChildContextException):
				return False
			if isinstance(ex_value, GeneratorExit):
				return False

			self.exception(exObj)
			raise ExceptionInChildContextException(ex_value, exObj)

		return False
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	"""
	@staticmethod
	def exceptionToJSON(ex):
		exceptionObject = jk_exceptionhelper.analyseException(ex, ignoreJKTypingCheckFunctionSignatureFrames=True, ignoreJKTestingAssertFrames=True, ignoreJKLoggingFrames=True)

		return {
			"exClass": exceptionObject.exceptionClassName,
			"exText": exceptionObject.exceptionTextHR,
			"exStack": [
				[x.filePath, x.lineNo, x.callingScope, x.sourceCodeLine] for x in exceptionObject.stackTrace
			],
		}
	#
	"""

#


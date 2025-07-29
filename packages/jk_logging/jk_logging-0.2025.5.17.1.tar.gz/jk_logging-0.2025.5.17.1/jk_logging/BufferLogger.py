﻿

import os
import typing

import jk_exceptionhelper

from .impl.IDCounter import IDCounter

from .EnumLogLevel import EnumLogLevel
from .impl.LogStats import LogStats
from .AbstractLogger import AbstractLogger
from .impl.Converter import Converter
from .impl.JSONDict import JSONDict






#
# This logger will buffer log messages in an internal array. Later this data can be forwarded to
# other loggers, f.e. in order to store them on disk.
#
# NOTE: This is an enhanced version of BufferLogger that collects statistics while logging.
#
class BufferLogger(AbstractLogger):

	################################################################################################################################
	## Constants
	################################################################################################################################

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self,
			idCounter:typing.Union[IDCounter,None] = None,
			parentID:typing.Union[int,None] = None,
			indentLevel:int = 0,
			logItemList = None,
			logStats:typing.Union[LogStats,None] = None,
			extraProperties:typing.Union[JSONDict,None] = None,
			stackTraceProcessor:typing.Union[jk_exceptionhelper.StackTraceProcessor,None] = None,
		):

		super().__init__(idCounter)

		self._indentationLevel = indentLevel
		if logItemList is None:
			self.__list = []
		else:
			self.__list = logItemList
		if parentID is None:
			parentID = self._idCounter.next()
		self._parentLogEntryID = parentID
		self._logStats = LogStats() if (logStats == None) else logStats
		self._extraProperties = JSONDict() if extraProperties is None else extraProperties
	#

	################################################################################################################################
	## Properties
	################################################################################################################################

	@property
	def stats(self) -> LogStats:
		return self._logStats
	#

	#
	# These extra properties accessed via this property will be part of the serialization of the buffer.
	# While this data has no relevance for logging itself this data will still be part of the JSON serialization results.
	#
	@property
	def extraProperties(self) -> JSONDict:
		return self._extraProperties
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _logi(self, logEntryStruct:list, bNeedsIndentationLevelAdaption:bool) -> list:
		self._logStats.increment(logEntryStruct[5])

		if bNeedsIndentationLevelAdaption:
			logEntryStruct = list(logEntryStruct)
			logEntryStruct[2] = self._indentationLevel
		self.__list.append(logEntryStruct)

		return logEntryStruct
	#

	def _descend(self, logEntryStruct:list) -> AbstractLogger:
		self._logStats.increment(logEntryStruct[5])

		nextID = logEntryStruct[1]
		newList = logEntryStruct[7]

		ret = BufferLogger(
			idCounter=self._idCounter,
			parentID=nextID,
			indentLevel=self._indentationLevel + 1,
			logItemList=newList,
			logStats=self._logStats,
			extraProperties=self._extraProperties,
		)
		ret._stackTraceProcessor = self._stackTraceProcessor
		return ret
	#

	"""
	def __getJSONData(self, items):
		ret = []
		for item in items:
			item2 = list(item)
			item2[5] = int(item2[5])
			if item2[0] == "txt":
				pass
			elif item2[0] == "ex":
				pass
			elif item2[0] == "desc":
				item2[7] = self.__getJSONData(item2[7])
			else:
				raise Exception("Implementation Error!")
			ret.append(item2)
		return ret
	#

	def __stackTraceElementToPrettyJSONData(self, stackTraceItem):
		return {
			"file": stackTraceItem[0],
			"line": stackTraceItem[1],
			"module": stackTraceItem[2],
			"sourcecode": stackTraceItem[3],
		}
	#

	def __getPrettyJSONData(self, items):
		ret = []
		for item in items:
			item2 = list(item)
			t = datetime.datetime.fromtimestamp(item2[4])
			jsonLogEntry = {
				"type": item2[0],
				"id": item2[1],
				"indent": item2[2],
				"timestamp": {
					"t": item2[4],
					"year": t.year,
					"month": t.month,
					"day": t.day,
					"hour": t.hour,
					"minute": t.minute,
					"second": t.second,
					"ms": t.microsecond // 1000,
					"us": t.microsecond % 1000,
				},
				"loglevel": str(item2[5]),
				"logleveln": int(item2[5]),
			}
			if item2[0] == "txt":
				jsonLogEntry["text"] = item2[6]
			elif item2[0] == "ex":
				jsonLogEntry["exception"] = item2[6]
				jsonLogEntry["text"] = item2[7]
				jsonLogEntry["stacktrace"] = [ self.__stackTraceElementToPrettyJSONData(x) for x in item2[8] ] if item2[8] else None
			elif item2[0] == "desc":
				jsonLogEntry["text"] = item2[6]
				jsonLogEntry["children"] = self.__getPrettyJSONData(item2[7])
			else:
				raise Exception("Implementation Error!")
			ret.append(jsonLogEntry)
		return ret
	#
	"""

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def hasData(self):
		return len(self.__list) > 0
	#

	"""
	#
	# Return a list of strings that contains the data stored in this logger.
	#
	# @return		string[]		Returns an array of strings ready to be written to the console or a file.
	#
	def getBufferDataAsStrList(self):
		ret = []
		for logEntryStruct in in self.__list:
			...
		return ret
	"""

	"""
	#
	# Return a single string that contains the data stored in this logger.
	#
	# @return		string		Returns a single string ready to be written to the console or a file.
	#
	def getBufferDataAsStr(self):
		s = ''
		for logEntryStruct in in self.__list:
			...
		return s
	"""

	#
	# Forward the log data stored in this logger to another logger.
	#
	# @param		AbstractLogger logger			Another logger that will receive the log data.
	# @param		bool bClear						Clear buffer after forwarding all log data.
	#
	def forwardTo(self, logger, bClear = False):
		assert isinstance(logger, AbstractLogger)
		logger._logiAll(self.__list, True)
		if bClear:
			self.__list = []
	#

	#
	# Forward the log data stored in this logger to another logger.
	#
	# @param		AbstractLogger logger			Another logger that will receive the log data.
	# @param		str text						The title for the descend section to create.
	# @param		bool bClear						Clear buffer after forwarding all log data.
	#
	def forwardToDescended(self, logger, text:str, bClear = False):
		assert isinstance(logger, AbstractLogger)
		log2 = logger.descend(text)
		log2._logiAll(self.__list, True)
		if bClear:
			self.__list = []
	#

	#def clear(self):
	#	NOTE: This method has been removed as it is not possible to clear only part of a stats object
	#	self.__list = []
	#

	def toJSON(self):
		#return self.__getJSONData(self.__list)
		ret = {
			"magic": {
				"magic": "jk-logging-compact",
				"version": 1,
			},
			"logData": [
				Converter.RAW_TO_COMPACTJSON.logEntry_to_json(x) for x in self.__list
			],
		}

		if self._extraProperties:
			ret["extraProperties"] = self._extraProperties

		return ret
	#

	def toJSONPretty(self):
		#return self.__getPrettyJSONData(self.__list)
		ret = {
			"magic": {
				"magic": "jk-logging-verbose",
				"version": 1,
			},
			"logData": [
				Converter.RAW_TO_PRETTYJSON.logEntry_to_json(x) for x in self.__list
			]
		}

		if self._extraProperties:
			ret["extraProperties"] = self._extraProperties

		return ret
	#

	def __str__(self):
		return "<" + self.__class__.__name__ + "(" + hex(id(self)) + ", indent=" + str(self._indentationLevel) + ",parentID=" + str(self._parentLogEntryID) + ")>"
	#

	def __repr__(self):
		return "<" + self.__class__.__name__ + "(" + hex(id(self)) + ", indent=" + str(self._indentationLevel) + ",parentID=" + str(self._parentLogEntryID) + ")>"
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	"""
	@staticmethod
	def __convertRawLogData(items:list, outLogStats:dict):
		ret = []
		for item in items:
			item = list(item)
			item[5] = EnumLogLevel.parse(item[5])
			iLogLevel = int(item[5])
			outLogStats[iLogLevel] = outLogStats.get(iLogLevel, 0) + 1
			if item[0] == "txt":
				pass
			elif item[0] == "ex":
				pass
			elif item[0] == "desc":
				item[7] = BufferLogger.__convertRawLogData(item[7], outLogStats)
			else:
				raise Exception("Implementation Error!")
			ret.append(item)
		return ret
	#
	"""

	@staticmethod
	def _convertJSONToInternal(jsonData:typing.Union[list,dict,None]) -> typing.Tuple[typing.Union[list,None],typing.Union[JSONDict,None]]:
		if jsonData is None:
			return None, None

		# ----

		appendData = None
		extraProperties = None

		# ----

		jExtraProperties = None

		if isinstance(jsonData, list):
			# seems to be raw data
			appendData = jsonData
		elif isinstance(jsonData, dict):
			if jsonData["magic"]["magic"] == "jk-logging-verbose":
				appendData = [
					Converter.PRETTYJSON_TO_RAW.json_to_logEntry(x) for x in jsonData["logData"]
				]
				jExtraProperties = jsonData.get("extraProperties")
			elif jsonData["magic"]["magic"] == "jk-logging-compact":
				appendData = [
					Converter.COMPACTJSON_TO_RAW.json_to_logEntry(x) for x in jsonData["logData"]
				]
				jExtraProperties = jsonData.get("extraProperties")
			else:
				raise Exception("jsonData is of invalid format!")
		else:
			raise Exception("jsonData is invalid")

		if jExtraProperties is not None:
			extraProperties = JSONDict(**jExtraProperties)

		# ----

		return appendData, extraProperties
	#

	#
	# param		stackTraceProcessor		(optional) 	A stack trace processor that can return a modified version of the stack trace (e.g. a shortened one).
	#									The stack is listed from the bottom: The trace item at position <c>0</c> is the lowest stack trace item,
	#									the item at position <c>length-1</c> is the top most item.
	#
	@staticmethod
	def create(
			jsonData = None,
			stackTraceProcessor:typing.Union[jk_exceptionhelper.StackTraceProcessor,None] = None,
		):

		appendData, extraProperties = BufferLogger._convertJSONToInternal(jsonData)

		logger = BufferLogger(extraProperties=extraProperties)
		logger._stackTraceProcessor = stackTraceProcessor

		if appendData is not None:
			logger._logiAll(appendData, True)

		return logger
	#

#







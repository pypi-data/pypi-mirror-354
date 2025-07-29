


from abc import abstractclassmethod
import os
import datetime
import typing
import json

from ..EnumLogLevel import EnumLogLevel






class Converter_prettyJSON_to_raw(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __json_to_timeStamp(self, jTimeStamp:dict) -> float:
		assert isinstance(jTimeStamp, dict)
		return jTimeStamp["t"]
	#

	def __json_to_stackTraceElement(self, jStackTraceElement:dict) -> tuple:
		assert isinstance(jStackTraceElement, dict)
		return (
			jStackTraceElement["file"],
			jStackTraceElement["line"],
			jStackTraceElement["module"],
			jStackTraceElement["code"],
		)
	#

	def __json_to_nestedException(self, jData:dict) -> tuple:
		assert isinstance(jData, dict)

		stackTraceList = None
		if "stacktrace" in jData:
			stackTraceList = [
				self.__json_to_stackTraceElement(x) for x in jData["stacktrace"]
			]

		nestedException = None
		if "nested" in jData:
			nestedException = [
				self.__json_to_nestedException(jData["nested"])
			]

		return (
			jData["exception"],
			jData["text"],
			stackTraceList,
			nestedException,
		)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def json_to_logEntry(self, jLogEntry:dict) -> list:
		assert isinstance(jLogEntry, dict)

		sType = jLogEntry["type"]
		rawLogEntry = [
			sType,
			0,										# jLogEntry["id"],
			jLogEntry["indent"],
			self.__json_to_timeStamp(jLogEntry["timeStamp"]),
			EnumLogLevel.parse(jLogEntry["logLevel"][0]),
		]

		if sType == "txt":
			rawLogEntry.append(jLogEntry["text"])
			assert len(rawLogEntry) == 7

		elif sType == "ex":
			rawLogEntry.append(jLogEntry["exception"])
			rawLogEntry.append(jLogEntry["text"])
			stackTraceList = None
			if "stacktrace" in jLogEntry:
				stackTraceList = [
					self.__json_to_stackTraceElement(x) for x in jLogEntry["stacktrace"]
				]
			rawLogEntry.append(stackTraceList)
			nestedException = None
			if "nested" in jLogEntry:
				nestedException = [
					self.__json_to_nestedException(jLogEntry["nested"])
				]
			rawLogEntry.append(nestedException)
			assert len(rawLogEntry) == 10

		elif sType == "ex2":
			rawLogEntry.append(jLogEntry["exception"])
			rawLogEntry.append(jLogEntry["text"])
			stackTraceList = None
			if "stacktrace" in jLogEntry:
				stackTraceList = [
					self.__json_to_stackTraceElement(x) for x in jLogEntry["stacktrace"]
				]
			rawLogEntry.append(stackTraceList)
			rawLogEntry.append(jLogEntry["extraValues"])
			nestedException = None
			if "nested" in jLogEntry:
				nestedException = [
					self.__json_to_nestedException(jLogEntry["nested"])
				]
			rawLogEntry.append(nestedException)
			assert len(rawLogEntry) == 11

		elif sType == "desc":
			rawLogEntry.append(jLogEntry["text"])
			children = None
			if "children" in jLogEntry:
				children = [
					self.json_to_logEntry(x) for x in jLogEntry["children"]
				]
			rawLogEntry.append(children)
			assert len(rawLogEntry) == 8

		else:
			raise Exception("Implementation Error!")

		return rawLogEntry
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#











import os
import datetime
import typing
import json






class Converter_raw_to_prettyJSON(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __timeStamp_to_json(self, t:typing.Union[int,float]) -> dict:
		assert isinstance(t, (int,float))
		dt = datetime.datetime.fromtimestamp(t)
		return {
			"t": t,
			"year": dt.year,
			"month": dt.month,
			"day": dt.day,
			"hour": dt.hour,
			"minute": dt.minute,
			"second": dt.second,
			"ms": dt.microsecond // 1000,
			# "us": dt.microsecond % 1000,			# Removed: too fine grained.
		}
	#

	def __stackTraceElement_to_json(self, stackTraceItem:typing.Union[list,tuple]) -> dict:
		assert isinstance(stackTraceItem, (list,tuple))
		assert len(stackTraceItem) == 4
		return {
			"file": stackTraceItem[0],
			"line": stackTraceItem[1],
			"module": stackTraceItem[2],
			"code": stackTraceItem[3],
		}
	#

	def __nestedException_to_json(self, nestedException:typing.Union[list,tuple]) -> dict:
		assert isinstance(nestedException, (list,tuple))
		assert len(nestedException) == 4

		jStacktrace = None
		if nestedException[2] is not None:
			jStacktrace = [
				self.__stackTraceElement_to_json(x) for x in nestedException[3]
			]

		jNested = None
		if nestedException[3] is not None:
			jNested = self.__nestedException_to_json(nestedException[3])

		return {
			"exception": nestedException[0],
			"text": nestedException[1],
			"stacktrace": jStacktrace,
			"nested": jNested,
		}
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def logEntry_to_json(self, rawLogEntry:typing.Union[tuple,list]) -> dict:
		sType = rawLogEntry[0]
		jsonLogEntry = {
			"type": sType,
			#"id": rawLogEntry[1],
			#"indent": rawLogEntry[2],
			"timeStamp": self.__timeStamp_to_json(rawLogEntry[4]),
			"logLevel": [
				int(rawLogEntry[5]),
				str(rawLogEntry[5]),
			],
		}

		if sType == "txt":
			assert len(rawLogEntry) == 7
			jsonLogEntry["text"] = rawLogEntry[6]

		elif sType == "ex":
			assert len(rawLogEntry) == 9
			jsonLogEntry["exception"] = rawLogEntry[6]
			jsonLogEntry["text"] = rawLogEntry[7]
			if rawLogEntry[8] is not None:
				jsonLogEntry["stacktrace"] = [
					self.__stackTraceElement_to_json(x) for x in rawLogEntry[8]
				]
			if rawLogEntry[9] is not None:
				jsonLogEntry["nested"] = self.__nestedException_to_json(rawLogEntry[9])

		elif sType == "ex2":
			assert len(rawLogEntry) == 9
			jsonLogEntry["exception"] = rawLogEntry[6]
			jsonLogEntry["text"] = rawLogEntry[7]
			if rawLogEntry[8] is not None:
				jsonLogEntry["stacktrace"] = [
					self.__stackTraceElement_to_json(x) for x in rawLogEntry[8]
				]
			jsonLogEntry["extraValues"] = rawLogEntry[9]
			if rawLogEntry[10] is not None:
				jsonLogEntry["nested"] = self.__nestedException_to_json(rawLogEntry[10])

		elif sType == "desc":
			assert len(rawLogEntry) == 8
			jsonLogEntry["text"] = rawLogEntry[6]
			if rawLogEntry[7] is not None:
				jsonLogEntry["children"] = [
					self.logEntry_to_json(x) for x in rawLogEntry[7]
				]

		else:
			raise Exception("Implementation Error!")

		return jsonLogEntry
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#











import os
import datetime
import typing
import json






class Converter_raw_to_compactJSON(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __nestedException_to_json(self, nestedException:typing.Union[list,tuple]) -> list:
		assert isinstance(nestedException, (list,tuple))
		assert len(nestedException) == 4

		jNested = None
		if nestedException[3] is not None:
			jNested = self.__nestedException_to_json(nestedException[3])

		return [
			nestedException[0],
			nestedException[1],
			nestedException[2],
			jNested,
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def logEntry_to_json(self, rawLogEntry:typing.Union[tuple,list]) -> list:
		sType = rawLogEntry[0]

		jsonLogEntry = [
			sType,
			# rawLogEntry[1],				# logEntryID
			# rawLogEntry[2],				# indentationLevel
			rawLogEntry[4],					# timeStamp
			int(rawLogEntry[5]),			# logLevel
		]

		if sType == "txt":
			assert len(rawLogEntry) == 7
			# nothing more to convert
			jsonLogEntry.append(rawLogEntry[6])		# logMsg

		elif sType == "ex":
			assert len(rawLogEntry) == 10
			# nothing more to convert
			jsonLogEntry.append(rawLogEntry[6])		# exClass
			jsonLogEntry.append(rawLogEntry[7])		# exMsg
			jsonLogEntry.append(rawLogEntry[8])		# exStackTrace
			jsonLogEntry.append(
				self.__nestedException_to_json(rawLogEntry[9])
				if rawLogEntry[9]
				else None
			)										# exNestedException

		elif sType == "ex2":
			assert len(rawLogEntry) == 11
			# nothing more to convert
			jsonLogEntry.append(rawLogEntry[6])		# exClass
			jsonLogEntry.append(rawLogEntry[7])		# exMsg
			jsonLogEntry.append(rawLogEntry[8])		# exStackTrace
			jsonLogEntry.append(rawLogEntry[9])		# extraValues
			jsonLogEntry.append(
				self.__nestedException_to_json(rawLogEntry[10])
				if rawLogEntry[10]
				else None
			)										# exNestedException

		elif sType == "desc":
			assert len(rawLogEntry) == 8
			# convert list of nested elements
			jsonLogEntry.append(rawLogEntry[6])		# logMsg
			nestedList = None
			if rawLogEntry[7] is not None:
				nestedList = [
					self.logEntry_to_json(x) for x in rawLogEntry[7]
				]
			jsonLogEntry.append(nestedList)

		else:
			raise Exception("Implementation Error!")

		return jsonLogEntry
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#








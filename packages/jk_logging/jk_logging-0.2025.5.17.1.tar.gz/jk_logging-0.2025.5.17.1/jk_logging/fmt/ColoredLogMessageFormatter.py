


import json
import typing

from ..EnumLogLevel import EnumLogLevel
from .AbstractTimeStampFormatter import AbstractTimeStampFormatter
from .AbstractLogMessageFormatter import AbstractLogMessageFormatter
from .DefaultTimeStampFormatter import DefaultTimeStampFormatter
from ..EnumExtensitivity import EnumExtensitivity






#
# This is a default formatter for log messages. It produces human readable output for log messages.
#
class ColoredLogMessageFormatter(AbstractLogMessageFormatter):

	################################################################################################################################
	## Nested Classes
	################################################################################################################################

	################################################################################################################################
	## Constants
	################################################################################################################################

	#
	# Color codes:
	#
	# * dark foregrounds
	#	* 30 = black
	#	* 31 = dark red
	#	* 32 = dark green
	#	* 33 = brown
	# 	* 34 = dark blue
	# 	* 35 = dark pink
	# 	* 36 = dark cyan
	#	* 37 = dark grey
	#
	# * normal foregrounds
	# 	* 90 = dark grey
	# 	* 91 = bright red
	# 	* 92 = green
	# 	* 93 = yellow
	# 	* 94 = blue
	# 	* 95 = pink
	# 	* 96 = cyan
	# 	* 97 = white
	#
	# * backgrounds:
	# 	* 100 = grey
	# 	* 101 = orange
	# 	* 102 = light green
	# 	* 103 = yellow
	# 	* 104 = light blue
	# 	* 105 = light pink
	# 	* 106 = light cyan
	# 	* 107 = white
	# 

	LOG_LEVEL_TO_COLOR_MAP = {
		EnumLogLevel.TRACE: "\033[90m",
		EnumLogLevel.DEBUG: "\033[90m",
		EnumLogLevel.NOTICE: "\033[90m",
		EnumLogLevel.STDOUT: "\033[97m",
		EnumLogLevel.INFO: "\033[37m",
		EnumLogLevel.WARNING: "\033[93m",
		EnumLogLevel.ERROR: "\033[91m",
		EnumLogLevel.STDERR: "\033[91m",
		EnumLogLevel.EXCEPTION: "\033[91m",
		EnumLogLevel.SUCCESS: "\033[92m",
	}
	#STACKTRACE_COLOR = "\033[38;2;204;102;0m"
	#STACKTRACE_COLOR = "\033[93m"
	STACKTRACE_COLOR = "\033[31m"
	RESET_COLOR = "\033[0m"

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			bIncludeIDs:bool = False,
			fillChar:str = "\t",
			extensitivity:EnumExtensitivity = EnumExtensitivity.FULL,
			timeStampFormatter = None,
			bLogLevelRightAligned = True,
		):

		assert isinstance(bIncludeIDs, bool)
		self.__includeIDs = bIncludeIDs

		assert isinstance(fillChar, str)
		self.__fillChar = fillChar
		self.__indentBuffer = fillChar

		assert isinstance(extensitivity, EnumExtensitivity)
		self.__outputMode = extensitivity

		if timeStampFormatter is None:
			timeStampFormatter = DefaultTimeStampFormatter()
		else:
			assert callable(timeStampFormatter)
		self.__timeStampFormatter = timeStampFormatter

		self.__logLevelToStrMap = AbstractLogMessageFormatter.LOG_LEVEL_TO_STR_MAP__RIGHT_ALIGNED if bLogLevelRightAligned \
			else AbstractLogMessageFormatter.LOG_LEVEL_TO_STR_MAP__LEFT_ALIGNED
	#

	################################################################################################################################
	## Properties
	################################################################################################################################

	@property
	def timeStampFormatter(self) -> typing.Union[AbstractTimeStampFormatter,None]:
		return self.__timeStampFormatter
	#

	@property
	def outputMode(self) -> EnumExtensitivity:
		return self.__outputMode
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __formatException(self,
			prefixFirst:str,
			prefixMore:str,
			sExClass:str,
			sLogMsg:typing.Union[str,None],
			listStackTraceEntries:typing.Union[list,tuple],
			extraValues:typing.Union[typing.Dict[str,typing.Any],None],
			nestedException:typing.Union[list,tuple,None],
			ret:typing.List[str],
		):

		if sLogMsg is None:
			sLogMsg = ""

		if sLogMsg:
			ret.append(prefixFirst + sExClass + ": " + sLogMsg + ColoredLogMessageFormatter.RESET_COLOR)
		else:
			ret.append(prefixFirst + sExClass + ColoredLogMessageFormatter.RESET_COLOR)

		if listStackTraceEntries:
			if self.__outputMode == EnumExtensitivity.FULL:
				for (stPath, stLineNo, stModuleName, stLine) in reversed(listStackTraceEntries):
					ret.append(prefixMore + "    | " + stPath + ":" + str(stLineNo) + " " + stModuleName + "    # " + stLine + ColoredLogMessageFormatter.RESET_COLOR)
			elif self.__outputMode == EnumExtensitivity.SHORTED:
				stPath, stLineNo, stModuleName, stLine = listStackTraceEntries[-1]
				ret.append(prefixMore + "    | " + stPath + ":" + str(stLineNo) + " " + stModuleName + "    # " + stLine + ColoredLogMessageFormatter.RESET_COLOR)

		if extraValues:
			i = 0
			_iMax = len(extraValues) - 1
			ret.append(prefixMore + f"    Variables:" + ColoredLogMessageFormatter.RESET_COLOR)
			for k, v in extraValues.items():
				bIsMax = i == _iMax
				i += 1
				lines = json.dumps(v).split("\n")
				part1 = f"    | {k} = "
				part2 = " " * len(part1)
				for i, line in enumerate(lines):
					_part = part1 if i == 0 else part2
					ret.append(f"{prefixMore}{_part}{line}" + ColoredLogMessageFormatter.RESET_COLOR)

		if nestedException:
			if len(nestedException) == 4:
				self.__formatException(
					prefixFirst + "    ",	# prefixFirst
					prefixMore + "    ",	# prefixMore
					nestedException[0],		# sExClass
					nestedException[1],		# sLogMsg
					nestedException[2],		# listStackTraceEntries
					None,					# extraValues
					nestedException[3],		# nestedException
					ret,					# ret
				)
			elif len(nestedException) == 5:
				self.__formatException(
					prefixFirst + "    ",	# prefixFirst
					prefixMore + "    ",	# prefixMore
					nestedException[0],		# sExClass
					nestedException[1],		# sLogMsg
					nestedException[2],		# listStackTraceEntries
					nestedException[3],		# extraValues
					nestedException[4],		# nestedException
					ret,					# ret
				)
			else:
				raise Exception()
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Create and return a string representation of the specified log entry.
	#
	# @param		list logEntryStruct			A log entry structure. See <c>AbstractLogger._logi()</c> for a detailed description.
	# @return		str							Returns the string representation of the log message.
	#
	def format(self, logEntryStruct):
		sStructType = logEntryStruct[0]

		sID = str(logEntryStruct[1]) if (logEntryStruct != None) else "-"

		indentationLevel = logEntryStruct[2]
		while indentationLevel > len(self.__indentBuffer):
			self.__indentBuffer += self.__fillChar
		sIndent = self.__indentBuffer[0:indentationLevel]

		sParentID = str(logEntryStruct[3]) if (logEntryStruct != None) else "-"

		sTimeStamp = self.__timeStampFormatter(logEntryStruct[4])

		sLogType = self.__logLevelToStrMap[logEntryStruct[5]]

		# ----

		if self.__includeIDs:
			s3 = "(" + sParentID + "|" + sID + ") "
		else:
			s3 = ""

		if sTimeStamp:
			s3 += "[" + sTimeStamp + "] "

		s1 = sIndent + ColoredLogMessageFormatter.LOG_LEVEL_TO_COLOR_MAP[logEntryStruct[5]] + s3

		s2 = sIndent + ColoredLogMessageFormatter.STACKTRACE_COLOR + s3

		if sStructType == "txt":
			sLogMsg = logEntryStruct[6]
			if sLogMsg is None:
				sLogMsg = ""
			return s1 + sLogType + ": " + sLogMsg + ColoredLogMessageFormatter.RESET_COLOR

		elif sStructType == "ex":
			sExClass = logEntryStruct[6]
			sLogMsg = logEntryStruct[7]
			if sLogMsg is None:
				sLogMsg = ""
			listStackTraceEntries = logEntryStruct[8]
			nestedException = logEntryStruct[9]

			ret = []
			self.__formatException(s1 + sLogType + ": ", s2 + sLogType + ": ", sExClass, sLogMsg, listStackTraceEntries, None, nestedException, ret)

			return ret

		elif sStructType == "ex2":
			sExClass = logEntryStruct[6]
			sLogMsg = logEntryStruct[7]
			if sLogMsg is None:
				sLogMsg = ""
			listStackTraceEntries = logEntryStruct[8]
			extraValues = logEntryStruct[9]
			nestedException = logEntryStruct[10]

			ret = []
			self.__formatException(s1 + sLogType + ": ", s2 + sLogType + ": ", sExClass, sLogMsg, listStackTraceEntries, extraValues, nestedException, ret)

			return ret

		elif sStructType == "desc":
			sLogMsg = logEntryStruct[6]
			if sLogMsg is None:
				sLogMsg = ""
			return s1 + sLogType + ": " + sLogMsg + ColoredLogMessageFormatter.RESET_COLOR

		else:
			raise Exception()
	#

#



COLOR_LOG_MESSAGE_FORMATTER = ColoredLogMessageFormatter()









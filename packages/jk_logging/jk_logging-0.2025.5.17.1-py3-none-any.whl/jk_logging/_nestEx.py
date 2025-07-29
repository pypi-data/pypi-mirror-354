



from jk_exceptionhelper.ExceptionObject import ExceptionObject





def nestEx(ex:BaseException) -> ExceptionObject:
	return ExceptionObject.fromException(ex)
#





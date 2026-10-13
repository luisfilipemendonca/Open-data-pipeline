INVALID_FILE_EXCEPTION = "Invalid file extension"
INVALID_FILE_HEADERS_EXCEPTION = "Invalid file headers"
INVALID_FILE_DUPLICATED_HEADER_EXCEPTION = "Invalid file duplicated header"
IMPORT_NOT_FOUND_EXCEPTION = "Import not found"


class InvalidFileException(Exception): ...


class InvalidFileHeadersException(Exception): ...


class InvalidFileDuplicatedHeaderException(Exception): ...


class ImportNotFoundException(Exception): ...

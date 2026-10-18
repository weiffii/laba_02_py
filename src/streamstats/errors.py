class StreamStatsError(Exception):
    """Базовая ошибка анализатора файла"""
class InvalidFormatError(StreamStatsError):
    """Ошибка неподдерживаемого формата файла"""
class InvalidEventError(StreamStatsError):
    """Ошибка некорректного события"""
class InvalidTimestampError(InvalidEventError):
    """Ошбка некорректной временной метки"""
class CLIConfigError(StreamStatsError):
    """Ошибка конфигурации командной строки"""

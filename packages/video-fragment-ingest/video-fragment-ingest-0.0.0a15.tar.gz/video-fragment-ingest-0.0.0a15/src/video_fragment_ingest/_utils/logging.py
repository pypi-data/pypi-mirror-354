import logging
import sys
import os


class ColouredFormatter(logging.Formatter):
    RESET = '\x1B[0m'
    RED = '\x1B[31m'
    YELLOW = '\x1B[33m'
    BRGREEN = '\x1B[01;32m'
    BLUE = '\x1b[94m'  # grey in solarized for terminals
    BLACK = '\x1b[90m'

    def _get_color(self, level_no):
        # color = self.BLACK
        # if level_no >= logging.CRITICAL:
        #     color = self.RED
        # elif level_no >= logging.ERROR:
        #     color = self.RED
        # elif level_no >= logging.WARNING:
        #     color = self.YELLOW
        # elif level_no >= logging.INFO:
        #     color = self.BLUE
        # elif level_no >= logging.DEBUG:
        #     color = self.BLACK
        # else:
        #     color = self.RESET
        return self.RESET

    def format(self, record, color=False):
        message = super().format(record)
        if not color:
            return message
        return self._get_color(record.levelno) + message + self.RESET


class ColouredHandler(logging.StreamHandler):
    def __init__(self, stream=sys.stdout):
        super().__init__(stream)

    def format(self, record, color=False):
        if not isinstance(self.formatter, ColouredFormatter):
            self.formatter = ColouredFormatter()

        return self.formatter.format(record, color)

    def emit(self, record):
        stream = self.stream
        try:
            msg = self.format(record, stream.isatty())
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


def get_log_level():
    try:
        try:
            LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "warning")
        except Exception:
            LOGGING_LEVEL = "warning"

        numeric_level = getattr(logging, LOGGING_LEVEL.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % LOGGING_LEVEL.upper())
    except Exception as e:
        numeric_level = 30
    finally:
        return numeric_level


class StringFilter(logging.Filter):
    def __init__(self, substring: str):
        super().__init__()
        self.substring = substring

    def filter(self, record):
        return self.substring in record.getMessage()


logger = logging.getLogger('video_fragment_ingest')
logger.setLevel(get_log_level())

handler = ColouredHandler()
handler.setLevel(get_log_level())
formatter = ColouredFormatter(
    '{asctime}.{msecs:03.0f} {levelname:8} {message}', '%Y-%m-%d %H:%M:%S', '{')
handler.setFormatter(formatter)

logger.addHandler(handler)


logger.debug("Logger set up complete")

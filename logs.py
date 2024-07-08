import logging 
import json


transform_name = {
    'msg': 'customMessage',
    'levelname': 'logLevel',
    'exc_info': 'exceptionStackTrace'
}

def key(k):
    return transform_name[k] if k in transform_name.keys() else k

class BaseJSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        super(BaseJSONFormatter, self).format(record)
        output = {key(k): str(v) for k, v in record.__dict__.items()}
        return json.dumps(output)

cf = BaseJSONFormatter()
sh = logging.StreamHandler()
sh.setFormatter(cf)

logger = logging.getLogger("my.module")
logger.addHandler(sh)

# simple json output
logger.warning("This is a great %s!", "log")
# enrich json output
logger.warning("This is an even greater %s!", "log", extra={'foo': 'bar'})
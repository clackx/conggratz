import logging
import threading
from config import VERBOSE, LOGLEVEL, LOGTOFILE

logger = logging.getLogger('gratzbot')
formatter = logging.Formatter('[%(asctime)s] %(thread)d  '
                              '%(levelname)-7s %(message)s', '%m-%d %H:%M:%S')
handler = logging.FileHandler('gratzbot.log') if LOGTOFILE else logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(LOGLEVEL)
logger.info('=' * 24)
logger.info("╔=== LOGGIN' STARTIN ===")

threads_dict = {}


class Colors:
    Black = "\033[30m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Cyan = "\033[36m"
    LightRed = "\033[91m"
    LightBlue = "\033[94m"
    ENDC = '\033[0m'
    Bold = "\033[1m"
    Blink = "\033[5m"
    Reverse = "\033[7m"


LEVEL0 = 0
LEVELUP = 2
LEVELDOWN = -2


def get_thread():
    thread_id = threading.get_native_id()
    if thread_id not in threads_dict:
        threads_dict[thread_id] = 0
    return thread_id


def get_leading_braces():
    thread_id = get_thread()
    spaces = int(threads_dict[thread_id] / 2)
    braces = ['║', '╎', '┆', '┊']
    lb_str = ''
    for a in range(0, spaces):
        bracetype = braces[a] if a < 4 else braces[3]
        lb_str += bracetype + '  '

    return lb_str


def enter(incoming_str):

    color = Colors.ENDC
    if incoming_str.find('links') != -1:
        color = Colors.Blue
    if incoming_str.find('descr') != -1:
        color = Colors.LightBlue
    if incoming_str.find('tag') != -1:
        color = Colors.Cyan
    if incoming_str.find('label') != -1:
        color = Colors.Cyan

    result_str = color + '├──┮ ' + incoming_str + Colors.ENDC
    cascader(result_str, LEVELUP)

    # if VERBOSE on INFO level, log without cascading
    if logger.getEffectiveLevel() == logging.INFO and VERBOSE:
        logger.info('├╼ ' + incoming_str)


def debug(incoming_str):
    result_str = '├──╼ ' + incoming_str
    cascader(result_str, LEVEL0)

    if logger.getEffectiveLevel() == logging.INFO and VERBOSE:
        logger.info('├╼ ' + incoming_str[:120])


def exiter(incoming_str, result):
    result = str(result).replace('\n', '<CR>')
    result_str = '╰──╼ ' + incoming_str

    if VERBOSE:
        cascader(result_str + ' || RESULT ::', LEVEL0)
        rows = int(len(result) / 100)
        for r in range(0, rows + 1):
            if r > 7:
                cascader(f'    ....   and {rows - 8} rows more   ....', LEVEL0)
                break
            cascader('    ' + result[r * 100:(r + 1) * 100], LEVEL0)
        cascader('', LEVELDOWN)
    else:
        cascader(result_str, LEVELDOWN)


def error(incoming_str):
    res_str = get_leading_braces() + Colors.Blink + Colors.Bold + Colors.LightRed + Colors.Reverse \
              + '!! ' + incoming_str + Colors.ENDC
    logger.error(res_str)


def warn(incoming_str):
    res_str = get_leading_braces() + Colors.Reverse + Colors.Yellow \
              + '! ' + incoming_str + Colors.ENDC
    logger.warning(res_str)


def info(incoming_str):
    result_str = Colors.Bold + incoming_str + Colors.ENDC
    if logger.getEffectiveLevel() == logging.INFO:
        logger.info('├──╼ ' + result_str[:120])
    else:
        cascader('├──┮ ' + result_str, LEVELUP)


def preinfo(incoming_str):
    logger.info('╟─╼ ' + incoming_str)


def cascader(incoming_str, level):
    result_str = get_leading_braces() + incoming_str[:120] + Colors.ENDC
    thread_id = get_thread()

    logger.debug(result_str)

    if logger.getEffectiveLevel() == logging.DEBUG:
        threads_dict[thread_id] += level

    if logger.getEffectiveLevel() == logging.DEBUG and threads_dict[thread_id] == 0:
        logger.debug("╚=== LOGGIN' FINISHED ===")

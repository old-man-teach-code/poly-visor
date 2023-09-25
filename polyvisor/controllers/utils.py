import hashlib
from functools import wraps
import re
from flask import session, abort
from polyvisor.finder import get_username_password, split_config_path
import glob,os
import configparser


#get the date of today
def get_date():
    from datetime import date
    today = date.today()
    return today.strftime("%d-%m-%Y")
    
# check the storage/logs folder and create the folder with the name of the date of today using get_date() function
def check_logs_folder():
    import os
    if not os.path.exists('storage/logs/' + get_date()):
        os.makedirs('storage/logs/' + get_date())
    else:
        pass
    
#test    






def _safe_encode(data):
    """Safely encode @data string to utf-8"""
    try:
        result = data.encode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError, AttributeError):
        result = data
    return result



def constant_time_compare(val1, val2):
    """
    Returns True if the two strings are equal, False otherwise.

    The time taken is independent of the number of characters that match.

    For the sake of simplicity, this function executes in constant time only
    when the two strings have the same length. It short-circuits when they
    have different lengths.

    Taken from Django Source Code
    """
    val1 = hashlib.sha1(_safe_encode(val1)).hexdigest()
    if val2.startswith("{SHA}"):  # password can be specified as SHA-1 hash in config
        val2 = val2.split("{SHA}")[1]
    else:
        val2 = hashlib.sha1(_safe_encode(val2)).hexdigest()
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    return result == 0


def is_login_valid(username, password):
    username = username.strip()
    password = password.strip()
    
    config_path = split_config_path()
    
    for file_path in get_config_files(config_path):
        correct_username, correct_password = get_username_password(file_path)
        
        if constant_time_compare(username, correct_username) and constant_time_compare(password, correct_password):
            return True

    return False

def check_authentication_required():
    config_path = split_config_path()

    for file_path in get_config_files(config_path):
        config_parser = configparser.ConfigParser()
        config_parser.read(file_path)
        
        section_name = 'program:' + os.path.basename(os.path.splitext(file_path)[0])
        
        if section_name in config_parser and 'username' in config_parser[section_name] and 'password' in config_parser[section_name]:
            return True
    
    return False


def get_config_files(config_path):
    file_extension = "*.ini"
    return glob.glob(os.path.join(config_path, file_extension))

def get_username_password(file_path):
    config_parser = configparser.ConfigParser()
    config_parser.read(file_path)
    section_name = 'program:' + os.path.basename(os.path.splitext(file_path)[0])
    username = config_parser[section_name]['username']
    password = config_parser[section_name]['password']
    return username, password



def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            authentication_required = check_authentication_required()
            # Check if the username key 
            if not authentication_required or 'username' in session:
                return f(*args, **kwargs)
            
            abort(401)

        return decorated_function

    return decorator


from functools import wraps
from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

def jwt_login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the JWT payload (user claims)
            user_claims = get_jwt_identity()

            # Check if the JWT contains the required claims for authentication
            if "username" in user_claims and "password" in user_claims:
                return f(*args, **kwargs)
            
            abort(401)  # Return a 401 Unauthorized status if the claims are missing

        return jwt_required()(decorated_function)

    return decorator


_PROTO_RE_STR = "(?P<protocol>\w+)\://"
_HOST_RE_STR = "?P<host>([\w\-_]+\.)*[\w\-_]+|\*"
_PORT_RE_STR = "\:(?P<port>\d{1,5})"


URL_RE = re.compile(
    "({protocol})?({host})?({port})?".format(
        protocol=_PROTO_RE_STR, host=_HOST_RE_STR, port=_PORT_RE_STR
    )
)

def sanitize_url(url, protocol=None, host=None, port=None):
    match = URL_RE.match(url)
    if match is None:
        raise ValueError("Invalid URL: {!r}".format(url))
    pars = match.groupdict()
    _protocol, _host, _port = pars["protocol"], pars["host"], pars["port"]
    protocol = protocol if _protocol is None else _protocol
    host = host if _host is None else _host
    port = port if _port is None else _port
    protocol = "" if protocol is None else (protocol + "://")
    port = "" if port is None else ":" + str(port)
    return dict(
        url="{}{}{}".format(protocol, host, port),
        protocol=protocol,
        host=host,
        port=port,
    )


def parse_dict(obj):
    """Returns a copy of `obj` where bytes from key/values was replaced by str"""
    decoded = {}
    for k, v in obj.items():
        if isinstance(k, bytes):
            k = k.decode("utf-8")
        if isinstance(v, bytes):
            v = v.decode("utf-8")
        decoded[k] = v
    return decoded


def parse_obj(obj):
    """Returns `obj` or a copy replacing recursively bytes by str

    `obj` can be any objects, including list and dictionary"""
    if isinstance(obj, bytes):
        return obj.decode()
    elif isinstance(obj, six.text_type):
        return obj
    elif isinstance(obj, abc.Mapping):
        return {parse_obj(k): parse_obj(v) for k, v in obj.items()}
    elif isinstance(obj, abc.Container):
        return type(obj)(parse_obj(i) for i in obj)
    return obj

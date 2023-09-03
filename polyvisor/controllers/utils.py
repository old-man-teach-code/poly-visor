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



import hashlib
from functools import wraps

from flask import session, abort, jsonify, request

from polyvisor.finder import configPath, get_username_password, split_config_path



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

    config = split_config_path()
    # read all the files from the "config" folder
    
    print(config)
    try:
        import glob,os
        file_extension = "*.ini"
        file_list = glob.glob(os.path.join(config, file_extension))
        print(file_list)
        for file_path in file_list:
            with open(file_path, 'r') as file:
                
                correct_username_password = False
                # get the username and password from the config file and compare it with the username and password entered by the user
                correct_username = get_username_password(file_path, os.path.basename(os.path.splitext(file_path)[0]))[0]
                print(correct_username)
                correct_password = get_username_password(file_path, os.path.basename(os.path.splitext(file_path)[0]))[1]
                print(correct_password)
                if constant_time_compare(username, correct_username) and constant_time_compare(
                    password, correct_password
                ):
                    correct_username_password = True
                    break
                else:
                    pass
    except Exception as e:
        print(e)

    

    return correct_username_password
    # return constant_time_compare(username, correct_username) and constant_time_compare(
    #     password, correct_password
    # )


print(is_login_valid("AlexDemo1", "123Demo1"))

def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if the user is logged in based on your authentication logic
            if 'username' in session:
                return f(*args, **kwargs)
            else:
                # If not logged in, return an unauthorized response (e.g., 401)
                return jsonify({'error': 'Authentication required'}), 401

        return decorated_function

    return decorator

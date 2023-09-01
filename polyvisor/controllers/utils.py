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
import functools

from flask import session, abort

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
                file_contents = file.read()
                # Perform operations on file_contents as needed
                print(f"File {file_path} contents:")
                print(file_contents)
    except Exception as e:
        print(e)

    

    # read from config file of supervisord for username and password

    # correct_username = get_username_password(config, name)[0]
    # correct_password = get_username_password(config, name)[1]
    correct_username = "admin"
    correct_password = "admin"

    print(correct_username)
    print(correct_password)
    
    return constant_time_compare(username, correct_username) and constant_time_compare(
        password, correct_password
    )


is_login_valid("admin", "admin")

# make a decorator to check if the user is logged in or not
def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("logged_in") is not True:
            abort(401)
        return func(*args, **kwargs)

    return wrapper

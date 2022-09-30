import os
import re

#Get config file path of Supervisord
def get_sup_config_path():
    stream = os.popen("""ps ux | grep -P '^(?=.*.conf)(?=.*supervisord)' | head -n -2""")
    output = stream.read()
    s = re.findall(r'(\/.*?\.[\w:]+)', output)
    lis = s[1].split()
    path=""
    for x in lis:
        if(r".conf"in x):
            path+=x
    if path=="" or not path :
        path="Can't find config path of Supervisord"   
        
    return path

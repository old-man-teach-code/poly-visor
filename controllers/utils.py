#get the date of today
def get_date():
    from datetime import date
    today = date.today()
    return today.strftime("%d-%m-%Y")
    
# check the storage/logs folder and create the folder with the date of today if it doesn't exist
def check_logs_folder():
    import os
    if not os.path.exists('storage/logs/'+get_date()):
        os.makedirs('storage/logs/'+get_date())

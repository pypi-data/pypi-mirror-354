import psutil
import subprocess
import winreg
import json
import platform
from requests_html import HTMLSession
import traceback
from datetime import datetime


def StatusLogginfo(DeviceID, Step, Comment,Status):

    url = f"https://api.hakware.com/HakObserver/callLog/{DeviceID}/{Step}/{Comment}/{Status}"

    session = HTMLSession()
        
    response = session.get(url, verify=False)

    if response.status_code == 200:
        print("Device Data inserted successfully via API.")
    else:
        print(url)
        print(f"Failed to insert data via API. Status code: {response.status_code}")

def log(Type, Message):
    error_time = datetime.now().isoformat()
    error_details = traceback.format_exc()
    
    log_entry = {
        "time": error_time,
        "type": Type,
        "details": Message
    }
    
    #Create or append to log.json
    with open("log.json", "a+") as log_file:
        log_file.seek(0)
        if log_file.read(1):
            log_file.write(",\n")
        else:
            log_file.write("[\n")
        json.dump(log_entry, log_file, indent=4)
        log_file.write("\n]")



def collect_firewall_logs():
    #Use PowerShell to collect firewall logs
    powershell_command = """
    $events = Get-WinEvent -LogName 'Security' -MaxEvents 100
    $logs = $events | ForEach-Object { $_.Message }
    $logs
    """
    logs = subprocess.check_output(["powershell", "-Command", powershell_command], shell=True)
    return logs.decode('utf-8')
    
def get_installed_applications(HWDeviceID):
    #Example: Retrieve installed applications and their version numbers from the Windows Registry
    key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    installed_apps = []
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as reg_key:
        for i in range(winreg.QueryInfoKey(reg_key)[0]):
            try:
                app_key = winreg.EnumKey(reg_key, i)
                with winreg.OpenKey(reg_key, app_key) as app_reg_key:
                    app_name = winreg.QueryValueEx(app_reg_key, "DisplayName")[0]
                    app_version = winreg.QueryValueEx(app_reg_key, "DisplayVersion")[0]
                    app_name = str(app_name).replace("-","").replace("/","").replace("(","").replace(")","")

                    #Replace special characters in app_name
                    
                    url = f"https://api.hakware.com/HakObserver/DeviceApps/{HWDeviceID}/{app_name}/{app_version}"

                    #Make a GET request to the URL
                    session = HTMLSession()
                
                    response = session.get(url, verify=False)

                    if response.status_code == 200:
                        print("Device Data inserted successfully via API.")
                    else:
                        print(url)
                        print(app_name)
                        print(f"Failed to insert data via API. Status code: {response.status_code}")

                    installed_apps.append({"name": app_name, "version": app_version})
            except FileNotFoundError:
                pass
    return installed_apps

def get_system_usage(HWDeviceID,ObserverVersion):

    #Example: Retrieve OS version using system-specific commands
    os_version = str(subprocess.check_output("ver", shell=True)).replace('(', '').replace(')', '')

    # CPU, RAM, and disk usage
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    #disk_usage = psutil.disk_usage('C:').percent  Replace 'C:' with appropriate drive letter

    #Retrieve total memory
    total_memory = psutil.virtual_memory().total
    total_memory_gb = total_memory / (1024**3)
    #Retrieve total number of CPUs and cores
    total_cpus = psutil.cpu_count(logical=False)  #Physical CPUs
    total_cores = psutil.cpu_count(logical=True)  #Logical CPUs (cores)

  

    device_name = str(platform.node()).replace('(', '').replace(')', ''),
    processor = str(platform.processor()).replace('(', '').replace(')', ''),
    device_id = str(platform.node()).replace('(', '').replace(')', ''),  #You may replace this with an appropriate identifier for your system
    system_type = str(platform.system()).replace('(', '').replace(')', '')


    
    ObserverVersion = str(ObserverVersion).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    device_id =str(device_id).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    device_name = str(device_name).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    processor = str(processor).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    system_type = str(system_type).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("'","")
    os_version = str(os_version).replace("(","").replace(")","").replace(",","").replace("\\r\\n","").replace("b","").replace("'","")

    print(ObserverVersion)
    print(device_name)
    print(processor)
    print(system_type)
    print(os_version)


    from requests_html import HTMLSession

    url = f"https://api.hakware.com/HakObserver/Device/{HWDeviceID}/{ObserverVersion}/{device_name}/{processor}/{device_id}/{system_type}/{os_version}/{total_memory_gb}/{total_cpus}/{total_cores}"
    
  

    #Make a GET request to the URL
    session = HTMLSession()
   
    response = session.get(url, verify=False, timeout=10)

    print(response)

    if response.status_code == 200:
        print("Device Data inserted successfully via API.")
    else:
        print(f"Failed to insert data via API. Status code: {response.status_code}")
    return {
        "cpu_usage_percent": cpu_usage,
        "ram_usage_percent": ram_usage,
        #"disk_usage_percent": disk_usage,
        "total_memory": total_memory_gb,
        "total_cpus": total_cpus,
        "total_cores": total_cores
    }

#--------
import win32net
import win32netcon
def get_users(DeviceID):
    users = []
    resume = 0
    while True:
        user_info, total, resume = win32net.NetUserEnum(None, 1, win32netcon.FILTER_NORMAL_ACCOUNT, resume)
        
        for user in user_info:

            User = user['name']
            print(user['password'])
            print(user['password_age'])
            Comment = str(user['comment']).replace("/","").replace("'","''")
            age = user['password_age']
            PasswordAge = age // (24 * 3600)

            #InserUsers(DeviceID, User, PasswordAge, Comment)
            url = f"https://api.hakware.com/HakObserver/InsertUsers/{DeviceID}/{User}/{PasswordAge}/{Comment}"
            
            #Make a GET request to the URL
            session = HTMLSession()
        
            response = session.get(url, verify=False, timeout=10)

            print(response)

            if response.status_code == 200:
                print("Device Data inserted successfully via API.")
            else:
                print(f"Failed to insert data via API. Status code: {response.status_code}")
       
        if resume == 0:
            break
    


def monitor_disk_space(DeviceID):
    """
    Monitor disk space usage for all drives and alert if usage exceeds the threshold.
    """
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        Disk = partition.device
        fstype = partition.fstype
        Usage = usage.percent
        Used = usage.used
        Free = usage.free
        Total = usage.total
        

        url = f"https://api.hakware.com/HakObserver/InsertDisks/{DeviceID}/{Disk}/{fstype}/{Usage}/{Used}/{Free}/{Total}"

        #Make a GET request to the URL
        session = HTMLSession()
    
        response = session.get(url, verify=False)

        if response.status_code == 200:
            print("Device Data inserted successfully via API.")
        else:
            print(url)
            print(f"Failed to insert data via API. Status code: {response.status_code}")

       
        # if usage.percent > threshold:
        #     print(f"Alert: Drive {partition.device} is {usage.percent}% full.")
        # else:
        #     print(f"Drive {partition.device} is {usage.percent}% full.")

#1. List of apps and services using resources
def list_Device_Usage(DeviceID):
    print("Process List:")
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            
            pid = proc.info['pid']
            Name = proc.info['name']
            CPUPercentage = proc.info['cpu_percent']
            MemoryMB =proc.info['memory_info'].rss / (1024 * 1024)

            url = f"https://api.hakware.com/HakObserver/DeviceUsage/{DeviceID}/{pid}/{Name}/{CPUPercentage}/{MemoryMB}"
            #Make a GET request to the URL
            session = HTMLSession()
        
            response = session.get(url, verify=False)

            if response.status_code == 200:
                print("Device Data inserted successfully via API.")
            else:
                print(url)
                print(f"Failed to insert data via API. Status code: {response.status_code}")

        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

#2. List of all services currently running
def list_services(DeviceID):
    services = psutil.win_service_iter()
    print("\nServices List:")
    for service in services:
        try:
            svc = service.as_dict()
            print(svc)
            pid = svc['pid']
            if pid==None:
                pid=''
            Name = svc['name']
            display_name = svc['display_name']
            binpath = svc['binpath']
            username = svc['username']
            start_type = svc['start_type']
            description = svc['description']
            Status = svc['status']

            #Services(DeviceID,pid,Name,display_name,binpath,username,start_type,description,Status )
            url = f"https://api.hakware.com/HakObserver/InsertServices/{DeviceID}/{pid}/{Name}/{display_name}/{binpath}/{username}/{start_type}/{description}/{Status}"

            session = HTMLSession()
        
            response = session.get(url, verify=False)

            if response.status_code == 200:
                print("Device Data inserted successfully via API.")
            else:
                print(url)
                print(f"Failed to insert data via API. Status code: {response.status_code}")
            
        except Exception as e:
            print(f"Error: {e}")

#3. CPU, memory, and disk usage
def system_usage(DeviceID):
    print("\nSystem Resource Usage:")
    #CPU usage
    print(psutil.cpu_percent())
    print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")

    #Memory usage
    memory = psutil.virtual_memory()
    print(f"Memory Usage: {memory.percent}%")

    #Disk usage
    disk_usage = psutil.disk_usage('/')
    print(f"Disk Usage: {disk_usage.percent}%")

    #Insert_System_Usage(DeviceID,, )
    cpu_percentage = psutil.cpu_percent(interval=1)
    memory_mb = memory.percent
    disk = disk_usage.percent
    url = f"https://api.hakware.com/HakObserver/InsertSystemUsage/{DeviceID}/{cpu_percentage}/{memory_mb}/{disk}"
    session = HTMLSession()
        
    response = session.get(url, verify=False)

    if response.status_code == 200:
        print("Device Data inserted successfully via API.")
    else:
        print(url)
        print(f"Failed to insert data via API. Status code: {response.status_code}")

########################################################################################
####################System Logs#######################################################3#

import win32evtlog
import datetime
import win32api
#import win32evtlogutil

# Map event type values to human-readable descriptions
EVENT_TYPE_MAP = {
    1: "Error",
    2: "Warning",
    4: "Information",
    8: "Success Audit",
    16: "Failure Audit"
}

def get_event_type_description(event_type):
    """
    Returns the human-readable description of an event type.

    Args:
        event_type (int): The event type (e.g., 1, 2, 4).

    Returns:
        str: The description of the event type.
    """
    return EVENT_TYPE_MAP.get(event_type, f"Unknown Type ({event_type})")

EVENT_DESCRIPTIONS = {
    # Logon/Logoff Events
    4624: "An account was successfully logged on.",
    4625: "An account failed to log on.",
    4634: "An account was logged off.",
    4647: "A user initiated logoff.",
    4648: "A logon was attempted using explicit credentials.",
    4672: "Special privileges assigned to new logon.",
    4675: "SIDs were filtered.",
    4778: "A session was reconnected to a Window Station.",
    4779: "A session was disconnected from a Window Station.",

    # Object Access Events
    4656: "A handle to an object was requested.",
    4660: "An object was deleted.",
    4661: "A handle to an object was requested for auditing.",
    4663: "An attempt was made to access an object.",
    4670: "Permissions on an object were changed.",

    # Account Management Events
    4720: "A user account was created.",
    4722: "A user account was enabled.",
    4724: "An attempt was made to reset an account's password.",
    4725: "A user account was disabled.",
    4726: "A user account was deleted.",
    4732: "A member was added to a security-enabled local group.",
    4733: "A member was removed from a security-enabled local group.",
    4735: "A security-enabled local group was changed.",
    4738: "A user account was changed.",
    4739: "Domain policy was changed.",
    4740: "A user account was locked out.",
    4756: "A member was added to a security-enabled universal group.",
    4757: "A member was removed from a security-enabled universal group.",
    4765: "SID History was added to an account.",
    4766: "SID History was removed from an account.",
    4767: "A user account was unlocked.",
    4776: "The domain controller attempted to validate credentials.",
    4781: "The name of an account was changed.",
    4794: "An attempt was made to set the Directory Services Restore Mode administrator password.",
    4798: "A user's local group membership was enumerated.",
    4799: "A user's local group membership was enumerated.",

    # Policy Change Events
    4674: "An operation was attempted on a privileged object.",
    4717: "System security access was granted to an account.",
    4719: "System audit policy was changed.",
    4902: "The Per-user audit policy table was created.",
    4904: "A logon attempt was made with explicit credentials.",

    # Sensitive Operations Events
    5061: "A cryptographic operation was performed.",
    5136: "A directory service object was modified.",
    5140: "A network share object was accessed.",
    5141: "A directory service object was deleted.",
    5142: "A network share object was modified.",
    5145: "A network share object was checked to ensure access.",
    5156: "The Windows Filtering Platform has allowed a connection.",
    5379: "Credential Manager credentials were read.",

    6005: "The Event Log service was started.",
    6006: "The Event Log service was stopped.",
    6008: "The previous system shutdown was unexpected.",
    7001: "A service dependency failed to start.",
    7009: "A service timeout occurred while starting.",
    7011: "A service timeout occurred while responding.",
    7022: "The service hung on starting.",
    7031: "The service terminated unexpectedly.",
    7034: "The service terminated unexpectedly without recovery.",
    7035: "The service was sent a control request.",
    7036: "The service entered the stopped state.",
    7040: "The startup type of the service was changed.",
    7045: "A new service was installed in the system.",
    1100: "The Event Log service encountered an error.",
    1102: "The audit log was cleared.",
}

def resolve_event_category(event):
    """
    Resolves the human-readable name of an event's category.

    Args:
        event: The event log record.

    Returns:
        str: Human-readable category name, or the numeric category ID if resolution fails.
    """
    try:
        # Load the message file for the event source
        hkey = win32api.RegOpenKey(win32api.HKEY_LOCAL_MACHINE,
                                   f"SYSTEM\\CurrentControlSet\\Services\\EventLog\\{event.LogName}\\{event.SourceName}")
        message_file, _ = win32api.RegQueryValueEx(hkey, "CategoryMessageFile")
        win32api.RegCloseKey(hkey)

        # Load the message file into the system
        handle = win32api.LoadLibraryEx(message_file, 0, win32api.LOAD_LIBRARY_AS_IMAGE_RESOURCE)

        # Format the category ID
        category_text = win32api.FormatMessage(win32api.FORMAT_MESSAGE_FROM_HMODULE,
                                               handle, event.EventCategory)
        return category_text.strip()

    except Exception as e:
        # If resolution fails, return the numeric category ID as a fallback
        return f"Category {event.EventCategory} (unresolved)"





#---------------------
def get_Security_events(DeviceID, server='localhost', log_type='Security'):
    """
    Retrieve events from the past week from the specified Windows Event Log.

    Args:
        server (str): The server name to fetch logs from. Default is localhost.
        log_type (str): The log type (e.g., 'System', 'Application', 'Security').

    Returns:
        list: List of events from the past week.
    """
    try:
        # Open the event log
        handle = win32evtlog.OpenEventLog(server, log_type)
        
        # Get the date for one week ago
        #one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        
        # Define flags for reading logs
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        
        # Read and filter logs
        events = win32evtlog.ReadEventLog(handle, flags, 0)
        recent_events = []
        

        for event in events:
            # Convert the event's TimeGenerated to a datetime object
            log_type
            RecordNumber = event.RecordNumber
            # print(event.StringInserts)
            # print(event.TimeGenerated)
            strEventTypeID= str(event.EventType)
            EventTypeDescription = get_event_type_description(event.EventType)

            EventID=event.EventID
            description = EVENT_DESCRIPTIONS.get(EventID)
            if description:
                EventDescription = description
            else:
                EventDescription = "Description not available for this Event ID."

            
            Source=event.SourceName
            
            EventTime =str(event.TimeGenerated)
            EventCategoryID=event.EventCategory
            category_text = resolve_event_category(event)
            #print(category_text)
          
            EventData=  str(event.StringInserts[00])
            if not event.StringInserts:
                EventData= "Unknown"

            # Handle specific EventIDs
            if event.EventID == 4624 or event.EventID == 4625:  # Logon events
                EventData=  event.StringInserts[5]  # Username
            elif event.EventID == 4720:  # User account creation
                EventData=  event.StringInserts[0]  # Created username
            elif event.EventID == 4726:  # User account deletion
                EventData=  event.StringInserts[0]  # Deleted username
            else:
                EventData=  event.StringInserts[0]

            #InsertEvents(DeviceID,RecordNumber, log_type,EventID ,EventDescription,Source,EventTime,strEventTypeID, EventTypeDescription,EventCategoryID ,category_text,EventData)
            url = f"https://api.hakware.com/HakObserver/InsertEvents/{DeviceID}/{RecordNumber}/{log_type}/{EventID}/{EventDescription}/{Source}/{EventTime}/{strEventTypeID}/{EventTypeDescription}/{EventCategoryID}/{category_text}/{EventData}"  

            session = HTMLSession()
        
            response = session.get(url, verify=False)

            if response.status_code == 200:
                print("Device Data inserted successfully via API.")
            else:
                print(url)
                print(f"Failed to insert data via API. Status code: {response.status_code}")

        # Close the event log
        win32evtlog.CloseEventLog(handle)

        return recent_events

    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

def get_System_events(DeviceID,server='localhost', log_type='System'):
    """
    Retrieve events from the past week from the specified Windows Event Log.

    Args:
        server (str): The server name to fetch logs from. Default is localhost.
        log_type (str): The log type (e.g., 'System', 'Application', 'Security').

    Returns:
        list: List of events from the past week.
    """
    try:
        # Open the event log
        handle = win32evtlog.OpenEventLog(server, log_type)
        
        # Get the date for one week ago
        #one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        
        # Define flags for reading logs
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        
        # Read and filter logs
        events = win32evtlog.ReadEventLog(handle, flags, 0)
        

        for event in events:
            # Convert the event's TimeGenerated to a datetime object
            log_type
            RecordNumber = event.RecordNumber
            # print(event.StringInserts)
            # print(event.TimeGenerated)
            strEventTypeID= str(event.EventType)
            EventTypeDescription = get_event_type_description(event.EventType)

            EventID=event.EventID
            description = EVENT_DESCRIPTIONS.get(EventID)
            if description:
                EventDescription = description
            else:
                EventDescription = "Description not available for this Event ID."

            
            Source=event.SourceName
            
            EventTime =str(event.TimeGenerated)
            EventCategoryID=event.EventCategory
            category_text = resolve_event_category(event)
            #print(category_text)
          
            EventData=  str(event.StringInserts[00])
            if not event.StringInserts:
                EventData= "Unknown"

            # Handle specific EventIDs
            if event.EventID == 4624 or event.EventID == 4625:  # Logon events
                EventData=  "User : " +event.StringInserts[5]  # Username
            elif event.EventID == 4720:  # User account creation
                EventData=  "User : " +event.StringInserts[0]  # Created username
            elif event.EventID == 4726:  # User account deletion
                EventData= "User : " + event.StringInserts[0]  # Deleted username
            else:
                EventData=  "User : " + event.StringInserts[0]

            #InsertEvents(DeviceID,RecordNumber, log_type,EventID ,EventDescription,Source,EventTime,strEventTypeID, EventTypeDescription,EventCategoryID ,category_text,EventData)
            url = f"https://api.hakware.com/HakObserver/InsertEvents/{DeviceID}/{RecordNumber}/{log_type}/{EventID}/{EventDescription}/{Source}/{EventTime}/{strEventTypeID}/{EventTypeDescription}/{EventCategoryID}/{category_text}/{EventData}"  

            session = HTMLSession()
        
            response = session.get(url, verify=False)

            if response.status_code == 200:
                print("Device Data inserted successfully via API.")
            else:
                print(url)
                print(f"Failed to insert data via API. Status code: {response.status_code}")

        # Close the event log
        win32evtlog.CloseEventLog(handle)

        

    except Exception as e:
        print(f"Error fetching logs: {e}")
        

###############################################################################################################################################################################
def InitiateCollecection(HWDeviceID, ObserverVersion): 

    StatusLogginfo(HWDeviceID, 'Starting HakObserver Scan', 'Starting','Completed')
    try:
        get_system_usage(HWDeviceID,ObserverVersion)
        StatusLogginfo(HWDeviceID, 'System Details', 'Gsathering System Resource Information','Completed')

    except Exception as e:
        StatusLogginfo(HWDeviceID, 'System Details', str(e),'Error') 
        pass
#---------------------------------------
    try:
        get_installed_applications(HWDeviceID)
        StatusLogginfo(HWDeviceID, 'Installed Applications', 'get_installed_applications','Completed')

    except Exception as e:
        StatusLogginfo(HWDeviceID, 'System Details', str(e),'Error') 
        pass


#---------------------------------------
    try:
        get_users(HWDeviceID)
        StatusLogginfo(HWDeviceID, 'System Users', 'Get active Users','Completed')

    except Exception as e:
        StatusLogginfo(HWDeviceID, 'System Users', str(e),'Error') 
        pass


#---------------------------------------
    try:
        monitor_disk_space(HWDeviceID)
        StatusLogginfo(HWDeviceID, 'Disks', 'Get allocated disks','Completed')

    except Exception as e:
        StatusLogginfo(HWDeviceID, 'Disks', str(e),'Error') 
        pass
    
#---------------------------------------
    try:
        list_Device_Usage(HWDeviceID)
        StatusLogginfo(HWDeviceID, 'Resource Usage', 'List of apps and services using resources','Completed')

    except Exception as e:
        StatusLogginfo(HWDeviceID, 'Resource Usage', str(e),'Error') 
        pass


#---------------------------------------
    try:
        list_services(HWDeviceID)
        StatusLogginfo(HWDeviceID, 'Services', 'List of all services currently running','Completed')

    except Exception as e:
        StatusLogginfo(HWDeviceID, 'Services', str(e),'Error') 
        pass

#---------------------------------------
    try:
        system_usage(HWDeviceID)
        StatusLogginfo(HWDeviceID, 'Resources', 'CPU, memory, and disk usage','Completed')

    except Exception as e:
        StatusLogginfo(HWDeviceID, 'Resources', str(e),'Error') 
        pass

    
#---------------------------------------
    try:
        get_Security_events(HWDeviceID)
        StatusLogginfo(HWDeviceID, 'Security Events', 'Security Event Logs','Completed')

    except Exception as e:
        StatusLogginfo(HWDeviceID, 'Security Events', str(e),'Error') 
        pass
  
#---------------------------------------
    try:
        get_System_events(HWDeviceID)
        StatusLogginfo(HWDeviceID, 'Security Events', 'Security Event Logs','Completed')

    except Exception as e:
        StatusLogginfo(HWDeviceID, 'Security Events', str(e),'Error') 
        pass 
    
    
   

    collect_firewall_logs()
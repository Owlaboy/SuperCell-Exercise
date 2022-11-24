import json
import threading

class UserData:
    usertimestamps = {}
    # usertimestamps = {"user1": {"statusKey": (timestamp, statusValue), "StatusKey": (timestamp, StatusValue)}}
    userstatus = {}
    # userstatus = {"user1": {"statusKey": statusValue, "StatusKey": StatusValue}}


def read_json_file(file_path, file_name):
    events = []
    with open(f"{file_path}{file_name}.txt", "r") as f:
        for row in f:
            jobject = json.loads(row)
            events.append(jobject)
    
    return events

def update_event(event, userstatus, latest_timestamps):
    if event["user"] not in userstatus.keys():
        threadLock.acquire()
        if event["user"] not in userstatus.keys():
            userstatus[event["user"]] = {}  
            latest_timestamps[event["user"]] = {}      
            threadLock.release()
        else:
            threadLock.release()

    update_userstatus(event, userstatus, latest_timestamps)

def update_userstatus(event, userstatus, latest_timestamps):
    values = list(event["values"].keys())
    for value in values:
        if value not in latest_timestamps[event["user"]].keys(): 
            threadLock.acquire()
            if value not in latest_timestamps[event["user"]].keys():          
                userstatus[event["user"]][value] = event["values"][value]
                latest_timestamps[event["user"]][value] = (event["timestamp"], event["values"][value])
                threadLock.release()
        elif latest_timestamps[event["user"]][value][0] < event["timestamp"]:
            threadLock.acquire()
            if latest_timestamps[event["user"]][value][0] < event["timestamp"]:
                userstatus[event["user"]][value] = event["values"][value]
                latest_timestamps[event["user"]][value] = (event["timestamp"], event["values"][value])
            threadLock.release()

def threadtarget(UserData, event):
    update_event(event, UserData.userstatus, UserData.usertimestamps)


path = "/home/pran/Desktop/supercell/SuperCell-Exercise/tests/ex2/"
events = read_json_file(path,"input1")
threadLock = threading.Lock()

thread_list = []
for event in events:
    x = threading.Thread(target=threadtarget, args = (UserData, event,))
    x.start()
    thread_list.append(x)

for thread in thread_list:
    thread.join()

print(UserData.userstatus)


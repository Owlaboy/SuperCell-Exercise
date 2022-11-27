#! /usr/bin/python3

import sys
import os
import json
import threading

class UserData:
    usertimestamps = {}
    # usertimestamps = {"user1": {"statusKey": (timestamp, statusValue), "StatusKey": (timestamp, StatusValue)}}
    userstatus = {}
    # userstatus = {"user1": {"statusKey": statusValue, "StatusKey": StatusValue}}


def read_json_file(file_path):
    events = []
    with open(f"{file_path}", "r") as f:
        for row in f:
            jobject = json.loads(row)
            events.append(jobject)
    
    return events

def update_event(event, userstatus, latest_timestamps):
    threadLock.acquire()
    if event["user"] not in userstatus.keys():
        userstatus[event["user"]] = {}  
        latest_timestamps[event["user"]] = {}      
    threadLock.release()

    update_userstatus(event, userstatus, latest_timestamps)

def update_userstatus(event, userstatus, latest_timestamps):
    values = list(event["values"].keys())
    for value in values:
        threadLock.acquire()
        if value not in latest_timestamps[event["user"]].keys():          
            userstatus[event["user"]][value] = event["values"][value]
            latest_timestamps[event["user"]][value] = (event["timestamp"], event["values"][value])
        if latest_timestamps[event["user"]][value][0] < event["timestamp"]:
            userstatus[event["user"]][value] = event["values"][value]
            latest_timestamps[event["user"]][value] = (event["timestamp"], event["values"][value])
        threadLock.release()

def threadtarget(UserData, event):
    update_event(event, UserData.userstatus, UserData.usertimestamps)


if sys.argv[0] != "./ex2.py":
    print("The command must be the form of './ex2.py -i <input_file>'")

if sys.argv[1] != "-i":
    print("The command must be the form of './ex2.py -i <input_file>'")
else:
    file_name = sys.argv[2]


events = read_json_file(sys.argv[2])
threadLock = threading.Lock()

thread_list = []
for event in events:
    x = threading.Thread(target=threadtarget, args = (UserData, event,))
    x.start()
    thread_list.append(x)

for thread in thread_list:
    thread.join()

outputFileName = "ex2 output #.txt"
outputVersion = 1
while os.path.isfile(outputFileName.replace("#", str(outputVersion))):
    outputVersion += 1
outputFileName = outputFileName.replace("#", str(outputVersion))


with open(outputFileName, "w") as output:
    output.write(json.dumps(UserData.userstatus, indent=2))

import json

# Get the json values for the ex1
def read_json_file(file_path, file_name):
    events = []
    with open(f"{file_path}{file_name}.txt", "r") as f:
        for row in f:
            jobject = json.loads(row)
            events.append(jobject)
    
    return events

def make_friends_event(event,target_dict):
    if event["user1"] not in target_dict:
        target_dict[event["user1"]] = []
    if event["user2"] not in target_dict:
        target_dict[event["user2"]] = []
    target_dict[event["user1"]].append(event["user2"])
    target_dict[event["user2"]].append(event["user1"])
    return target_dict

def del_friends_event(event,target_dict):
    if event["user1"] in target_dict.keys():
        target_dict[event["user1"]].remove(event["user2"])
        target_dict[event["user2"]].remove(event["user1"])

def new_broadcast(event,targets,latest_timestamps):
    if targets == []:
        return None
    new = {"broadcast": targets, "user": event["user"], "timestamp": event["timestamp"], "values": {}}
    values = list(event["values"].keys())
    for value in values:
        if event["user"] not in latest_timestamps.keys():
            latest_timestamps[event["user"]] = {}
        if value not in latest_timestamps[event["user"]].keys():          
            new["values"][value] = event["values"][value]
            latest_timestamps[event["user"]][value] = (event["timestamp"], event["values"][value])
        elif latest_timestamps[event["user"]][value][0] < event["timestamp"]:
            new["values"][value] = event["values"][value]
            latest_timestamps[event["user"]][value] = (event["timestamp"], event["values"][value])
    if new["values"] == {}:
        return None 
    return new

def update_event(event, target_dict, latest_timestamps):
    if event["user"] not in target_dict.keys():
        target_dict[event["user"]] = []        
    targets = target_dict[event["user"]].copy()
    broadcast = new_broadcast(event, targets, latest_timestamps)

    return broadcast


def generate_broadcasts(events, target_dict):
    latest_timestamps = {}
    broadcast_list = []
    for event in events:
        if event["type"] == "make_friends":
            make_friends_event(event,target_dict)
        
        elif event["type"] == "del_friends":
            del_friends_event(event,target_dict)
        
        # timestampValues = dict["username"] = dict[valueskey] = (timestamp, valuesvalue)

        elif event["type"] == "update":
            broadcast = update_event(event,target_dict, latest_timestamps)
            if broadcast:
                #if broadcast["user"] not in userlist or latest_timestamps[broadcast["user"]] < broadcast["timestamp"]:
                broadcast_list.append(broadcast)
    return broadcast_list

# timestampValues = dict["username"] = dict[valueskey] = (timestamp, valuesvalue)

def main(file_name):
    file_path = "/home/pran/Desktop/supercell/SuperCell-Exercise/tests/ex1/"
    events = read_json_file(file_path, file_name)

    # target_dict is a dictionary with the broadcast targets for each user
    target_dict = {}
    
    all = generate_broadcasts(events, target_dict)
    for i in all:
        print(i)
    

if __name__ == "__main__":
    main("input1")
    print("_"*20)
    main("input2")
    print("_"*20)
    main("input3")

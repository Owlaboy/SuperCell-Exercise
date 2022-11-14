import os, json, enum

# Get the json values for the ex1
def read_json_file(file_name):
    events = []
    with open(f"/home/pran/Desktop/supercell/SuperCell-Exercise/tests/ex1/{file_name}.txt", "r") as f:
        for row in f:
            #print(row)
            jobject = json.loads(row)
            #print(type(jobject))
            events.append(jobject)
    
    return events

def new_broadcast(event,targets):
    #print(event)
    new = {"broadcast": targets, "user": event["user"], "timestamp": event["timestamp"], "values": event["values"]}
    return new

def make_friends(event,users):
    if event["user1"] not in users:
        users[event["user1"]] = []
    if event["user2"] not in users:
        users[event["user2"]] = []
    users[event["user1"]].append(event["user2"])
    users[event["user2"]].append(event["user1"])
    return users

def del_friends_event(event,users):
    if event["user1"] in users.keys():
        users[event["user1"]].remove(event["user2"])
        users[event["user2"]].remove(event["user1"])

def update_event(event,users):
    if event["user"] not in users.keys():
        users[event["user"]] = []        
    broadcast = new_broadcast(event, users[event["user"]])
    return broadcast


def generate_broadcasts(events, users):
    latest_timestamps = {}
    broadcast_list = []
    for event in events:
        
        if event["type"] == "make_friends":
            make_friends(event,users)
        
        elif event["type"] == "update":
            broadcast = update_event(event,users)
            userlist = list(latest_timestamps.keys())
            if broadcast:
                if broadcast["user"] not in userlist or latest_timestamps[broadcast["user"]] < broadcast["timestamp"]:
                    latest_timestamps[broadcast["user"]] = broadcast["timestamp"]
                    if broadcast["broadcast"] != []:
                        broadcast_list.append(broadcast)
            
        elif event["type"] == "del_friends":
            del_friends_event(event,users)
    return broadcast_list

def main(file_name):
    events = read_json_file(file_name)
    users = {}
    
    all = generate_broadcasts(events, users)
    for i in all:
        print(i)
        
    #print(users)
    #print(broadcasts)

if __name__ == "__main__":
    main("input1")
    print("_"*20)
    main("input2")
    print("_"*20)
    main("input3")

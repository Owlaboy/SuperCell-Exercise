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
    new = {"broadcast": targets, "user": event["user"], "timestamp": event["timestamp"], "values": event["values"]},
    return new

def make_friends(event,users):
    if event["user1"] not in users:
        users[event["user1"]] = []
    if event["user2"] not in users:
        users[event["user2"]] = []
    users[event["user1"]].append(event["user2"])
    users[event["user2"]].append(event["user1"])
    return users

def update_event(event,users):
    if event["user"] in users.keys():
        if users[event["user"]] == []:
            return
        #if event["values"] == : #Check how to handle this
            return
        broadcast = new_broadcast(event, users[event["user"]])
        return broadcast

def del_friends_event(event,users):
    if event["user1"] in users.keys():
        users[event["user1"]].remove(event["user2"])
        users[event["user2"]].remove(event["user1"])

def main(file_name):
    events = read_json_file(file_name)
    users = {}
    broadcasts = []
    for event in events:
        
        if event["type"] == "make_friends":
            make_friends(event,users)
        
        elif event["type"] == "update":
            broadcast = update_event(event,users)
            if broadcast:
                broadcasts.append(broadcast)
            print(broadcast)    
        elif event["type"] == "del_friends":
            del_friends_event(event,users)
        
        
    #print(users)
    #print(broadcasts)

if __name__ == "__main__":
    main("input1")
    print("_"*20)
    main("input2")
    print("_"*20)
    main("input3")

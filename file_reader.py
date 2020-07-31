import websocket
import json

def on_message(ws, message):
    
    a = '''
mutation {
    saveChatMessage(input: {
        type: "normal"'''
    
    b = '''
    }) {
        success
    }
}'''
    
    msg = json.loads(message)
    
    if "data" in msg and "chat" in msg["data"]:
        msgtype = msg["data"]["chat"]["type"]
        msgtext = msg["data"]["chat"]["text"]
        msgrole = msg["data"]["chat"]["role"]
        
        if not msgtext == None:
            print("Bot Message: " +  msgtext)
        
        
        if msgtype == "normal" and msgrole == "rep":
            
            global count
            count = count + 1
            
            if count == 1:
                
                f2.write(msgtext + "\n")
            
            if count == 2:
                
                if len(temp) == 0:
                    print("Done reading file")
                    ws.close()
                    
                line = temp.pop(0)
                
                payload = a + "\npid: " + '"' + _pid + '"' + "\ntext: " + '"' + line + '"' + b
                ws.send(payload)
                
                count = 0 
        
def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    
def on_open(ws): 
    
    print("OPENED")
    
    a = '''subscription {
    chat(input: {
        participationId: '''
            
    b = '''
    }) {
        type
        role
        text
    }
}'''
    
    subscribe = a + '"' + _pid + '"' + b
    ws.send(subscribe)
        
    print("SUBSCRIBED")
    
def connect(wsurl, pid):
    
    global f
    global f2
    global count
    
    count = 0
    
    filename = input("Enter input file's name': ")
    
    with open(filename, encoding="utf-8") as f:
        
        global temp
        temp = f.read().splitlines()
        
    filename2 = input("Enter output file's name': ")

    f2 = open(filename2, "a", encoding="utf-8")
    
    global _pid
    
    _pid = pid
    
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(wsurl,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    
    ws.on_open = on_open
    ws.run_forever()

    
    



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
    
    print("GOT MESSAGE")
    print(message)
        
    msg = json.loads(message)
    
    if "chat" in msg["data"]:
        
        msgtype = msg["data"]["chat"]["type"]
        msgtext = msg["data"]["chat"]["text"]
        msgrole = msg["data"]["chat"]["role"]
        
        if msgtype == "normal" and not msgtext[0:5] == "Hello" and msgrole == "rep":
            
            message = input("Send Message: ")
            
            if message == "exit":
                ws.close()
                
            payload = a + "\npid: " + '"' + _pid + '"' + "\ntext: " + '"' + message + '"' + b
            print(payload)
            
            
            ws.send(payload)

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
    
    global _pid 
    _pid = pid
    
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(wsurl,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    
    ws.on_open = on_open
    ws.run_forever()

    
    

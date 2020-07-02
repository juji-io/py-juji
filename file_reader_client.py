import requests 
import websocket
import time
import json

with open('query.txt', encoding="utf-8") as f:
    temp = f.read().splitlines()

f2 = open("output.txt", "a", encoding="utf-8")
    

name = input("Enter your name: ")
data2 = {'firstName': name}

#link: https://juji.ai/pre-chat/5ed6e8ba-218d-43ee-80e9-94ce0550978a?mode=test

link = input("Enter the link of the chatbot you are connecting to: ")
r = requests.post(link, data = data2) 
  
response = eval(r.text)

wsurl = response["websocketUrl"]
pid = response["participationId"]

count = 0

def on_message(ws, message):
    
    global count
    
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
    
    if "data" in msg:
        msgtype = msg["data"]["chat"]["type"]
        msgtext = msg["data"]["chat"]["text"]
        msgrole = msg["data"]["chat"]["role"]
        
        if msgtype == "normal" and msgrole == "rep":
            
            count = count + 1
            
            if count == 1:
                
                f2.write(msgtext + "\n")
            
            if count == 2:
                
                line = temp.pop(0)
                
                payload = a + "\npid: " + '"' + pid + '"' + "\ntext: " + '"' + line + '"' + b
                print(payload)
                ws.send(payload)
                
                count = 0 
        
def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    f2.close()
    f.close()
    
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
    
    subscribe = a + '"' + pid + '"' + b
    ws.send(subscribe)
        
    print("SUBSCRIBED")
    

if __name__ == "__main__":
    
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(wsurl,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    
    ws.on_open = on_open
    ws.run_forever()

    
    



import requests 
import websocket
import json

name = input("Enter your name: ")
data2 = {'firstName': name}

#link: https://juji.ai/pre-chat/5ed6e8ba-218d-43ee-80e9-94ce0550978a?mode=test

link = input("Enter the link of the chatbot you are connecting to: ")
r = requests.post(link, data = data2) 
  
response = eval(r.text)

wsurl = response["websocketUrl"]
pid = response["participationId"]

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
                
            payload = a + "\npid: " + '"' + pid + '"' + "\ntext: " + '"' + message + '"' + b
            print(payload)
            
            
            ws.send(payload)
            
    else:
        
        token = msg["data"]["authenticate"]["token"]
        
        print("UPLOADING")
        print(token)
        
        with open('nlidb.csv', 'rb') as f:
            #headers = {}
            headers = {"Authorization": "Bearer " + token}
            r = requests.post('https://juji.ai/api/analyze', files={'nlidb.csv': f}, headers = headers)
            print(r.text)
            print("UPLOADED")


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
        
    
    subscribe = a + '"' + pid + '"' + b
    ws.send(subscribe)
        
    print("SUBSCRIBED")
    
    
    upload_request = '''mutation
      authenticate($input: AuthenticateInput!) {
        authenticate(input: {email: "jonathandou100@gmail.com", password: "incorrect"}) {
          token
        }
      }'''
      
    ws.send(upload_request)
    
    print("REQUESTED")
    

if __name__ == "__main__":
    
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(wsurl,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    
    ws.on_open = on_open
    ws.run_forever()

    
    

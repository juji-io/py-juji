import requests 
import websocket
import json

def on_message(ws, message):
    
    print("Message from chatbot: " + message)
    
    msg = json.loads(message)
    
    if "data" in msg:
        if "authenticate" in msg["data"]:
            
            token = msg["data"]["authenticate"]["token"]
            
            print("UPLOADING")
            print("Token: " + token)
            
            headers = {"Authorization": "Bearer " + token}
            r = requests.post('https://juji.ai/api/analyze', headers = headers, files={'file': open(filename, 'rb')})
            print("TEXT: " + r.text)
            print("UPLOADED")
        


def on_error(ws, error):
    print("ERROR: " + error)

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
    
    email = input("Enter your email: ")
    password = input("Enter your password: ")
      
    upload_request = '''mutation
    authenticate($input: AuthenticateInput!) {
      authenticate(input: {email: ''' + '"' + email + '"' + ", password: " + '"' + password + '"' + '''}) {
        token
      }
    }'''
    
    ws.send(upload_request)
    
    print("REQUESTED")
    
    global filename
    
    filename = input("Enter the filename: ")
    

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

    
    

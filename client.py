import requests 
import chat
import file_upload
import file_reader


if __name__ == "__main__":
    
    name = input("Enter your name: ")
    data2 = {'firstName': name}
    
    #link: https://juji.ai/pre-chat/5ed6e8ba-218d-43ee-80e9-94ce0550978a?mode=test
    
    link = input("Enter the link of the chatbot you are connecting to: ")
    r = requests.post(link, data = data2) 
      
    response = eval(r.text)
    
    wsurl = response["websocketUrl"]
    pid = response["participationId"]
    
    while True: 
        text = input("type chat to text with chatbot\ntype upload to for uploading files\ntype query to send queries to the chatbot from a file\ntype exit to quit\n>>")
        
        if text == "chat":
            chat.connect(wsurl, pid)
            
        if text == "upload":
            file_upload.connect(wsurl, pid)
            
        if text == "query":
            file_reader.connect(wsurl, pid)
            
        if text == "exit":
            break
        
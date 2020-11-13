import socket
import time
import _thread
from utils import *

# Server Configuration

MAX_USERS = 1000
server_ip = "127.0.0.1" # Server ip
server_port   = 12345 # Server Port

# Loading the Database and the users list
DATABASE = load_data("database.pkl")
user_list = list(DATABASE.keys())

# Declaring Functions
def home_screen(username, socket_client):
    while(True):
        socket_client.send(
"""
Welcome to Mini-Face
Options: (Reply with)
1: Friends
2: Messages
3: Pending Friend Requests
4: Feed
5: Upload post
6: Delete post
7: See your Timeline
0: Exit Mini-Face
""".encode())
        option = socket_client.recv(1024).decode()
        if(option == "1"):
            friend_options(username, socket_client)
        
        elif(option == "2"):
            messages = 0 # Message options
        
        elif(option == "3"):
            get_pending_requests(DATABASE,username,socket_client)
            
        elif(option == "4"):
            get_feed(DATABASE,username,socket_client)

        elif(option == "5"):
            upload_post(DATABASE,username,socket_client)
            
        elif(option == "6"):
            delete_post(DATABASE,username,socket_client)
        
        elif(option == "7"):
            get_timeline(DATABASE,username,socket_client)
            
        elif(option == "0"):
            return
        
        else:
            socket_client.send("Invalid Option!".encode())

def find_friend(username, socket_client):
    while True:    
        socket_client.send(
"""     
Find Friends        
1: Search for Friends
2: See Friends of Friends
0: Go to Friend Options
""".encode())
        option = socket_client.recv(1024).decode()
        if(option == "0"):
            return
        
        if(option == "1"):
            search_user(DATABASE,username,socket_client,user_list)

        if(option == "2"):
            if(len(DATABASE[username]['friends']) < 2):
                response = "Make more friends!"
                socket_client.send(response.encode())
            else:
                get_friends_of_friends(DATABASE,username,socket_client)
    
def friend_options(username, socket_client):
    while True:    
        socket_client.send(
"""      
Friend Options        
1: See your Friends
2: Find new Friends
3: Remove Friends
0: Go to Home Screen
""".encode())
        option = socket_client.recv(1024).decode()
        if(option == "0"):
            return
        
        if(option == "1"):
            see_friends(DATABASE,username,socket_client)
        
        if(option == "2"):
            find_friend(username, socket_client)


def client_thread(socket_client, address):

    user = login(DATABASE,user_list,socket_client)
    DATABASE[user]["is_online"] = True
    home_screen(user, socket_client)
    DATABASE[user]["is_online"] = False
    print("closing thread: ", address)
    socket_client.send("Thank you for using Mini-Face".encode())
    time.sleep(0.5)
    write_database("database.pkl",DATABASE)
    socket_client.close()
     

if(__name__ == "__main__"): 

    socket_tcp = socket.socket(family = socket.AF_INET,type =socket.SOCK_STREAM)

    # Creating Socket for TCP
    socket_tcp.bind((server_ip, server_port)) # Binding is necessary in TCP
    socket_tcp.listen(MAX_USERS) # Listents to the clients sending connection request

    print("Server is up and running")

    # creating thread for each new client
    while(True):
        socket_client, address = socket_tcp.accept()
        print("Client Connected:", address)

        _thread.start_new_thread(client_thread, (socket_client, address))
        


import threading
import socket
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT


HOST = '0.0.0.0'
# [TODO] 166XX, XX is your tool box number
PORT = 16666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
tSocket=[]

# [HINT] currentRing stores the ring state
currentRing = None
# [HINT] Lock maintain the indentity of resource
Lock = threading.Lock()
# [HINT] variable for socket
conn, addr = None,None


def mqttcallback(client, userdata, message):
    global currentRing,conn,addr,Lock
    try:
        # [TODO] write callback to deal with MQTT message from Lambda
    except Exception as e:
        print(e)



# [TODO] Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT
ENDPOINT = "a3ez73z2hom29i-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "HSCC"
PATH_TO_CERT = "./6974c2d6a6-certificate.pem.crt"
PATH_TO_KEY = "./6974c2d6a6-private.pem.key"
PATH_TO_ROOT = "./CA1.txt"

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

myAWSIoTMQTTClient.connect()
# [TODO] subscribe AWS topic(s)
myAWSIoTMQTTClient.subscribe(XXXXX)

def on_new_client(clientsocket,addr):
    global currentRing
    while True:
        # [TODO] decode message from Arduino and send to AWS
        pass
    clientsocket.close()

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

def main():
    global conn, addr
    try:
        conn, addr = s.accept()
        print('connected by ' + str(addr))
        t = threading.Thread(target=on_new_client,args=(conn,addr))
        tSocket.append(t)
        tSocket[-1].start()
    except Exception as e:
        print(e)
        s.close()
        print("socket close")

if __name__ == '__main__':
    main()
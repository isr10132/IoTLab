import threading
import socket
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT


HOST = '0.0.0.0'
# [DONE] 166XX, XX is your tool box number
PORT = 16631

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
        payload = json.loads(str(message.payload.decode('utf-8')))
        print('payload:')
        print(payload)
        if 'desired' in payload['state']:
            Lock.acquire()
            currentRing = payload['state']['desired']['ring']
            Lock.release()
            print('currentRing:')
            print(currentRing)
            conn.send(str(currentRing).encode())
        
    except Exception as e:
        print(e)



# [DONE] Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT
ENDPOINT = "ah7v6710o79ui-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "Lab3"
PATH_TO_CERT = "./8e540da958-certificate.pem.crt"
PATH_TO_KEY = "./8e540da958-private.pem.key"
PATH_TO_ROOT = "./CA1key.txt"

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

myAWSIoTMQTTClient.connect()
# [DONE] subscribe AWS topic(s)
myAWSIoTMQTTClient.subscribe("$aws/things/Lab3/shadow/update", 0, mqttcallback)

def on_new_client(clientsocket,addr):
    global currentRing
    while True:
        # [TODO] decode message from Arduino and send to AWS
        data = clientsocket.recv(200).decode()
        humidity, currentRing = data.split(',')
        print('humidity:'+humidity)
        print('currentRing:'+currentRing)
        
        messageDice = {
            "state": {
                "reported": {
                    "humidity": float(humidity),
                    "ring": int(currentRing)
                }
            }
        }
        myAWSIoTMQTTClient.publish("$aws/things/Lab3/shadow/update", json.dumps(messageDice), 0)
        
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

import socket
#import serial # for arduino serial communication

# # FLAG ENABLED FOR DEVELOPMENT PURPOSES
# flag = True

# get the hostname
#host = socket.gethostname()
#host = '192.168.43.66'
#port = 3350  # initiate port no above 1024


server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 1234))

#s.listen(5)
print('Server On\n')
#print('Host: '+host)
#print('Port: '+str(port))
#server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
#server_socket.bind(('', port))  # bind host address and port together

# for communicating with Arduino
# sPort = "/dev/ttyACM0" # sPort is the serial port that the Arduino is connected to
# arduino = serial.Serial(sPort,9600)
# # initial flush
# arduino.flushInput()

while True:
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, (conn_host, conn_port) = server_socket.accept()  # accept new connection
    print("Connection from: " + str(conn_host) + str(conn_port))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()



        if not data:
            # if data is not received break
            break

        print("from connected user: " + str(data))
        #data = input(' -> ')
        #conn.send(data.encode())  # send data to the client
        
#         # push data to arduino via serial
#         to_arduino = str(data)
#         to_arduino = to_arduino.encode("utf-8")
#         arduino.write(to_arduino)
            
        

conn.close()  # close the connection


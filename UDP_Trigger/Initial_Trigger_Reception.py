import socket, time

#Arm's IP address and Port - SBC
UDP_IP = "192.168.1.3"
UDP_PORT = 5005

#Walker's IP address and Port - SBC
Walker_IP = "192.168.1.6"
Walker_PORT = 5010

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

try:
        while True:
                data, addr = sock.recvfrom(1024) # buffer size = 1024 bytes
                print "received message:", data
                if data=='TriggerRobotArm007':
                        good_ack = 'data OK, starting ARM in T minus 5 seconds'
                        print good_ack
                        sock.sendto(good_ack, (Walker_IP,Walker_PORT))
                        time.sleep(5)
                        execfile("InvKin_Control.py")
                else:
                        bad_ack = 'bad data received, pls resend'
                        print bad_ack
                        sock.sendto(bad_ack, (Walker_IP,Walker_PORT))
except KeyboardInterrupt:
        print 'User has cancelled the program'


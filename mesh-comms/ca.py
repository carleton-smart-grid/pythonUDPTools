# Nathaniel Charlebois
# 20/1/2018

# importing tcp communication library
import tcpcomms

# TODO Keep a local copy of the stack in a DB
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
        #TODO add code to handle DB push

    def pop(self):
        #TODO add code to handle DB pop 
        return self.items.pop()

    def isEmpty(self):
        return (self.items == [])

    

if __name__ == '__main__':
    def upload(payload):
        timeouts = 0
        while(timeouts < MAX_TIMEOUTS):
            #TODO Add delay
            
            try:
                print('Attempting to send payload to TA at ' + TA_IP)
                tcpcomms.send(TA_IP, payload)

                # Runs conditionally on tcpcomms.send() success
                # Set exit condition
                timeouts = MAX_TIMEOUTS
                transmitStack()
            except Exception as e:
                #Catches all generic exceptions

                #TODO hook in error logging system
                print(e)
                if(timeouts < MAX_TIMEOUTS):
                    timeouts += 1
                    print('Incrementing the timeout counter to ' + str(timeouts))
                    if(timeouts == MAX_TIMEOUTS):
                        print('Pushing the current payload into the message Stack')
                        msgStack.push(payload)

    def transmitStack():
        for item in msgStack.items:
            tcpcomms.send(list.pop())

    # declaring constant
    MAX_TIMEOUTS = 5
    TA_IP = 'dead:beef::1'

    # declaring local __main__ variables
    msgStack = Stack()
    upload('Hello World')



    
        
        

    

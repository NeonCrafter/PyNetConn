import sockets
import sys
from itertools import batched
class Host():
    def __init__(ip = socket.gethostbyname(socket.gethostname()) , port = 8990 , sendSize = False ,etc = "" , splitData = True , splitDataSize = 1024):
        #Ip is to initiate the server and port is required too.
        #etc is a string which will be sent to every client. It is customizable. It is nothing by default
        #Sendsize is a boolean which if true,will send a datapacket to the client which startswith a "VARSIZE:" string.
        #if SplitData is true,the program will automatically slice the data into 'SplitDataSize' and send it one packet after the other. Before the actual data is recieved,the server will send a packet with info in the following format:
        """
        [SPLITDATA]
        [PACKETSIZE](splitDataSize)
        [NUMPACKETS](Number of packets that should be sent to send the large piece of data)
        """
        if type(splitDataSize) != int:
            raise ValueError(f"Argument splitDataSize must be of type 'int',not {type(splitDataSize)}") 
        if type(ip) != str:
            raise ValueError(f"Argument ip must be of type 'str',not {type(splitDataSize)}") 
        if type(sendSize) != bool:
            raise ValueError(f"Argument sendSize must be of type 'bool',not {type(splitDataSize)}") 
        if type(port) != int:
            raise ValueError(f"Argument port must be of type 'int',not {type(splitDataSize)}") 
        if type(splitData) != bool:
            raise ValueError(f"Argument splitData must be of type 'bool',not {type(splitDataSize)}") 
        if type(etc) != str:
            raise ValueError(f"Argument etc must be of type 'str',not {type(splitDataSize)}")
        self.etc = etc
        self.splitData = splitData
        self.SplitDataSize = SplitDataSize
        self.ip = ip
        self.port = port
        self.sendSize = sendSize
        self.socket = socket.scoket(socket.AF_INET , socket.SOCK_STREAM)
    def bind(self):
        self.socket.bind((self.ip , self.port))
    def listen(self , numClients = 1):
        self.socket.listen()
        self.socket.accept(numClients)
    def setupSessionDefault(self):
        self.bind()
        self.listen()
    def send(self , data):
        try:
            if self.SplitData == True and sys.getsizeof(data) > self.SplitDataSize:
                self.socket.send(f"""
                    [SPLITDATA]
                    [PACKETSIZE]{self.splitDataSize}
                    [NUMPACKETS]{sys.getsizeof(data) // self.SplitDataSize}
        """.encode())
                for i in batched(data , sys.getsizeof(data) // self.SplitDataSize):
                    self.socket.send(i.encode())
            if self.sendSize == True:
                self.socket.send(f"VARSIZE:{sys.getsizeof(data)}") 
            self.socket.send(str(data).encode())

        except Exception as e:
            return e

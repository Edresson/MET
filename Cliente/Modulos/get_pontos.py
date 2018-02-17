import socket
HOST = '192.168.2.3'     # Endereco IP do Servidor
PORT = 12001           # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
tcp.send (B'getpontos:48')
#tcp.close()


#frequencia      x = [1070,465,408,918,979,726,84,50,40,120,160,210,260,360,630,590,690,830,1130,850]

# deslocamento cm Y = [17.4,8.5,7.6,15.2,16.2,12.3,1.5,1,0.7,2.2,2.7,3.9,4.6,6.5,10.8,10.2,11.8,14,18.33,14.3]


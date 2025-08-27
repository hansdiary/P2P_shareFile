import socket
import threading

def startServer(host="127.0.0.1", port=5000, filename="noms.txt"):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[SERVER] En écoute sur {host}:{port}")
    
    while True:
        conn, addr = server_socket.accept()
        print("[SERVER] Nouveau client : {addr}")
        
        with open(filename, "rb") as f:
            data = f.read()
            conn.sendall(data)
        print("Fichier envoyé avec suucès !!!")
        conn.close()    
        
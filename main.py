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
def startClient(server_host="127.0.0.1", server_port=5000, output_file="downloaded.txt"):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    print(f"[CLIENT] Connecté à {server_host}:{server_port}")
    
    with open(output_file, "wb") as f:
        while True:
            data = client_socket(1024)
            if not data:
                break
            f.write(data)
    print(f"[CLIENT] Fichier téléchargé et sauvegardé en `{output_file}`")
    client_socket.close()        
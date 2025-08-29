import socket
import threading
import os
import hashlib
import tkinter as tk
from tkinter import filedialog

# --- DHT simulée ---
DHT = {}  # clé = hash, valeur = {"name": nom, "path": chemin}

# --- Choisir des fichiers à partager ---
def choisir_fichiers():
    root = tk.Tk()
    root.withdraw()
    fichiers = filedialog.askopenfilenames(
        title="Choisir des fichiers à partager",
        filetypes=[("Tous les fichiers", "*.*")]
    )
    return list(fichiers)

# --- Ajouter fichiers dans la DHT ---
def ajouter_dans_dht(fichiers):
    for f in fichiers:
        try:
            with open(f, "rb") as file:
                contenu = file.read()
                h = hashlib.sha256(contenu).hexdigest()
                if h not in DHT:
                    DHT[h] = {"name": os.path.basename(f), "path": f}
                    print(f"[AJOUTÉ] {f}")
        except Exception as e:
            print(f"Erreur en indexant {f} : {e}")

# --- Gérer une connexion client ---
def handle_client(conn, addr):
    print(f"[NOUVELLE CONNEXION] {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data == "LIST":
                response = "\n".join(
                    [f"{i+1}. {info['name']} (hash={h[:8]}...)" 
                     for i, (h, info) in enumerate(DHT.items())]
                )
                conn.send(response.encode())

            elif data.startswith("GET"):
                 _, choix = data.split()
                 choix = int(choix) - 1
                 if 0 <= choix < len(DHT):
                     h = list(DHT.keys())[choix]
                     file_info = DHT[h]
                     path = file_info["path"]
             
                     # envoyer la taille
                     size = os.path.getsize(path)
                     conn.send(str(size).encode().ljust(16))
             
                     # envoyer le nom du fichier
                     conn.send(file_info['name'].encode().ljust(256))
             
                     # envoyer le fichier en chunks
                     with open(path, "rb") as f:
                         while chunk := f.read(4096):
                             conn.sendall(chunk)
                     print(f"[ENVOYÉ] {file_info['name']} à {addr}")
                 else:
                     conn.send("0".encode().ljust(16))  # fichier non trouvé
             
    except Exception as e:
        print(f"[ERREUR] {e}")
    finally:
        conn.close()

# --- Boucle d'acceptation des clients ---
def boucle_accept(server):
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# --- Menu pour ajouter des fichiers pendant le serveur ---
def menu_ajout():
    while True:
        cmd = input("\nTapez 'ajout' pour ajouter des fichiers ou 'quit' pour quitter le menu : ").strip().lower()
        if cmd == "ajout":
            fichiers = choisir_fichiers()
            if fichiers:
                ajouter_dans_dht(fichiers)
        elif cmd == "quit":
            print("Menu d’ajout arrêté (le serveur continue).")
            break

# --- Lancer le serveur ---
def start_server(host="127.0.0.1", port=5000):
    print("Sélectionnez les fichiers à partager au démarrage...")
    fichiers = choisir_fichiers()
    if fichiers:
        ajouter_dans_dht(fichiers)

    print(f"Fichiers dans la DHT : {[f['name'] for f in DHT.values()]}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[SERVEUR LANCÉ] en écoute sur {host}:{port}")

    threading.Thread(target=lambda: boucle_accept(server), daemon=True).start()
    menu_ajout()  # menu console pour ajout après lancement

if __name__ == "__main__":
    start_server()

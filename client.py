import socket
import os

def start_client(host="127.0.0.1", port=5000):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    while True:
        action = input("\n1. Voir la liste des fichiers\n2. Télécharger un fichier\n3. Quitter\n> ")

        if action == "1":
            client.send("LIST".encode())
            response = client.recv(4096).decode()
            print("\nFichiers disponibles :")
            print(response)

        elif action == "2":
            num = input("Numéro du fichier à télécharger : ")
            client.send(f"GET {num}".encode())

            # recevoir la taille du fichier (16 octets)
            size_data = client.recv(16).decode().strip()
            if not size_data.isdigit() or int(size_data) == 0:
                print("Erreur : fichier introuvable")
                continue
            size = int(size_data)

            # recevoir le nom du fichier (256 octets)
            name_data = client.recv(256).decode().strip()
            if not name_data:
                print("Erreur : nom de fichier vide")
                continue

            # préparer le chemin complet
            os.makedirs("downloads", exist_ok=True)
            filename = os.path.join("downloads", name_data)

            # recevoir et écrire le fichier par chunks
            received = 0
            with open(filename, "wb") as f:
                while received < size:
                    chunk = client.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            print(f"✅ Téléchargement terminé ({received} octets) → {filename}")

        elif action == "3":
            print("Déconnexion...")
            client.close()
            break

if __name__ == "__main__":
    start_client()

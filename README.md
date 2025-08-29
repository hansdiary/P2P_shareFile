📂 P2P File Sharing System (Python)

Un système P2P (peer-to-peer) de partage de fichiers développé en Python, sans serveur central. Chaque pair peut partager plusieurs fichiers via une DHT simulée et permettre aux autres pairs de les télécharger directement.

✨ Fonctionnalités

🔗 Architecture P2P : pas de serveur central, chaque nœud agit comme client et serveur.

📑 Indexation par hash (SHA-256) : chaque fichier est identifié de manière unique.

🗂️ Sélection multiple via explorateur : choisissez plusieurs fichiers à partager à la fois.

➕ Ajout dynamique : ajouter de nouveaux fichiers sans arrêter le serveur.

📥 Téléchargement rapide : les fichiers sont téléchargés en chunks pour gérer tous les types et tailles.

📂 Dossier downloads/ : les fichiers téléchargés conservent leur nom original.

🚀 Installation et utilisation
Prérequis

Python 3.8 ou supérieur

Tkinter (sudo apt install python3-tk sur Linux si nécessaire)

Lancer le serveur

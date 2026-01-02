import requests
import os
import time

# --- CONFIGURAZIONE ---
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")
FILE_MEMORIA = "giochi_visti.txt"

def ottieni_giochi_gratis():
    """Recupera la lista dei giochi gratis dalle API"""
    url = "https://www.gamerpower.com/api/giveaways?type=game&platform=all"
    try:
        risposta = requests.get(url)
        if risposta.status_code == 200:
            return risposta.json()
        return []
    except Exception as e:
        print(f"Errore API: {e}")
        return []

def invia_gioco_con_foto(testo, url_foto):
    """Invia una foto con il testo come didascalia su Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendPhoto"
    dati = {
        "chat_id": CHAT_ID,
        "photo": url_foto,
        "caption": testo,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, data=dati)
        if r.status_code != 200:
            print(f"Errore Telegram: {r.text}")
    except Exception as e:
        print(f"Errore invio: {e}")

def carica_cronologia():
    """Carica l'elenco dei giochi già inviati"""
    if not os.path.exists(FILE_MEMORIA):
        return []
    with open(FILE_MEMORIA, "r") as f:
        return f.read().splitlines()

def salva_in_cronologia(id_gioco):
    """Salva l'ID del gioco nel file locale"""
    with open(FILE_MEMORIA, "a") as f:
        f.write(f"{id_gioco}\n")

if __name__ == "__main__":
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("ERRORE: Configura TOKEN_TELEGRAM e CHAT_ID nei Secrets!")
    else:

import requests
import os
import time

# --- CONFIGURAZIONE ---
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")
FILE_MEMORIA = "giochi_visti.txt"

def ottieni_giochi_gratis():
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
    """Invia una foto con il testo come didascalia"""
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendPhoto"
    dati = {
        "chat_id": CHAT_ID,
        "photo": url_foto,
        "caption": testo,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=dati)
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

def carica_cronologia():
    if not os.path.exists(FILE_MEMORIA):
        return []
    with open(FILE_MEMORIA, "r") as f:
        return f.read().splitlines()

def salva_in_cronologia(id_gioco):
    with open(FILE_MEMORIA, "a") as f:
        f.write(f"{id_gioco}\n")

if __name__ == "__main__":
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("ERRORE: Secrets non configurati!")
    else:
        print("Scansione giochi in corso...")
        giochi = ottieni_giochi_gratis()
        visti = carica_cronologia()
        nuovi_trovati = 0

        for gioco in giochi:
            id_gioco = str(gioco['id'])
            
            if id_gioco not in visti:
                # Creiamo il messaggio formattato
                messaggio = (
                    f"🎁 *NUOVO GIOCO GRATIS!*\n\n"
                    f"🕹 *{gioco['title']}*\n"
                    f"💻 Piattaforma: {gioco['platforms']}\n"
                    f"💰 Valore: {gioco['worth']}\n\n"
                    f"🔗 [Riscatta qui]({gioco['open_giveaway_url']})"
                )
                
                # Usiamo l'immagine fornita dall'API (thumbnail o image)
                url_immagine = gioco['image']
                
                invia_gioco_con_foto(messaggio, url_immagine)
                salva_in_cronologia(id_gioco)
                nuovi_trovati += 1
                time.sleep(2)

        print(f"Fatto! Inviati {nuovi_trovati} nuovi giochi.")

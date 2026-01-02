import requests
import os
import time

TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")
FILE_MEMORIA = "giochi_visti.txt"

def ottieni_giochi_gratis():
    url = "https://www.gamerpower.com/api/giveaways?type=game&platform=all"
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else []
    except:
        return []

def invia_gioco_con_foto(testo, url_foto):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendPhoto"
    dati = {"chat_id": CHAT_ID, "photo": url_foto, "caption": testo, "parse_mode": "Markdown"}
    requests.post(url, data=dati)

def carica_cronologia():
    if not os.path.exists(FILE_MEMORIA): return []
    with open(FILE_MEMORIA, "r") as f: return f.read().splitlines()

def salva_in_cronologia(id_gioco):
    with open(FILE_MEMORIA, "a") as f: f.write(f"{id_gioco}\n")

if __name__ == "__main__":
    if TOKEN_TELEGRAM and CHAT_ID:
        giochi = ottieni_giochi_gratis()
        visti = carica_cronologia()
        for gioco in giochi:
            id_gioco = str(gioco['id'])
            if True: # Forza l'invio per il test
                msg = f"🎁 *GIOCO GRATIS!*\n\n🕹 *{gioco['title']}*\n💻 {gioco['platforms']}\n\n🔗 [Riscatta qui]({gioco['open_giveaway_url']})"
                invia_gioco_con_foto(msg, gioco.get('image', ''))
                salva_in_cronologia(id_gioco)
                time.sleep(2)

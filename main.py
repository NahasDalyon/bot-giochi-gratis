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

def invia_gioco_completo(testo, url_foto):
    # Proviamo a inviare con foto, se fallisce inviamo solo testo
    url_foto_api = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendPhoto"
    dati = {"chat_id": CHAT_ID, "photo": url_foto, "caption": testo, "parse_mode": "Markdown"}
    
    r = requests.post(url_foto_api, data=dati)
    if r.status_code != 200:
        # Fallback: invia solo testo se l'immagine ha problemi
        url_testo = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
        requests.post(url_testo, data={"chat_id": CHAT_ID, "text": testo, "parse_mode": "Markdown"})

def carica_cronologia():
    if not os.path.exists(FILE_MEMORIA): return []
    with open(FILE_MEMORIA, "r") as f: return f.read().splitlines()

def salva_in_cronologia(id_gioco):
    with open(FILE_MEMORIA, "a") as f: f.write(f"{id_gioco}\n")

if __name__ == "__main__":
    if TOKEN_TELEGRAM and CHAT_ID:
        giochi = ottieni_giochi_gratis()
        visti = carica_cronologia()
        nuovi_count = 0

        for gioco in giochi:
            id_gioco = str(gioco['id'])
            
            # Da ora in poi invia solo i NUOVI
            if id_gioco not in visti:
                msg = (
                    f"🎁 *NUOVO GIOCO GRATIS!*\n\n"
                    f"🕹 *{gioco['title']}*\n"
                    f"💻 Piattaforma: {gioco['platforms']}\n\n"
                    f"🔗 [Riscatta qui]({gioco['open_giveaway_url']})"
                )
                
                invia_gioco_completo(msg, gioco.get('image'))
                salva_in_cronologia(id_gioco)
                nuovi_count += 1
                time.sleep(2)
        
        print(f"Lavoro terminato. Nuovi messaggi: {nuovi_count}")

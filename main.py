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
    r = requests.post(url, data=dati)
    print(f"DEBUG Invio Foto: {r.status_code} - {r.text}")

if __name__ == "__main__":
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("ERRORE: Secrets mancanti!")
    else:
        # --- TEST DI CONNESSIONE DIRETTO ---
        print(f"DEBUG: Provo invio a CHAT_ID: {CHAT_ID}")
        url_test = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
        r_test = requests.post(url_test, data={"chat_id": CHAT_ID, "text": "🤖 Test connessione: il bot sta provando a scrivere!"})
        print(f"DEBUG Risposta Test Testo: {r_test.status_code} - {r_test.text}")
        
        # --- PROCESSO GIOCHI ---
        giochi = ottieni_giochi_gratis()
        if giochi:
            # Ne prendiamo solo 2 per il test per non intasare
            for gioco in giochi[:2]:
                msg = f"🎁 *TEST FOTO*\n🕹 *{gioco['title']}*\n🔗 [Link]({gioco['open_giveaway_url']})"
                invia_gioco_con_foto(msg, gioco.get('image', ''))
                time.sleep(2)
        else:
            print("DEBUG: Nessun gioco trovato dalle API.")

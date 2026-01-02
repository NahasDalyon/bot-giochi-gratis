import requests
import os
import time

# --- CONFIGURAZIONE SICURA ---
# Il bot proverà a leggere i dati dai Secrets di GitHub. 
# Se non li trova (ad esempio se lo lanci sul PC), darà un errore invece di fallire silenziosamente.
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

def invia_messaggio(testo):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    dati = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=dati)

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
        print("ERRORE: Token o Chat ID mancanti nei Secrets di GitHub!")
    else:
        giochi = ottieni_giochi_gratis()
        visti = carica_cronologia()
        nuovi_trovati = 0

        for gioco in giochi:
            id_gioco = str(gioco['id'])
            if id_gioco not in visti:
                messaggio = (
                    f"🎁 *NUOVO GIOCO GRATIS!*\n\n"
                    f"🕹 *{gioco['title']}*\n"
                    f"💻 Piattaforma: {gioco['platforms']}\n\n"
                    f"🔗 [Riscatta qui]({gioco['open_giveaway_url']})"
                )
                invia_messaggio(messaggio)
                salva_in_cronologia(id_gioco)
                nuovi_trovati += 1
                time.sleep(1) 
                if nuovi_trovati >= 5: break # Limite per evitare spam


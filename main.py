import requests
import os
import time

# --- CONFIGURAZIONE ---
# Il bot legge queste informazioni dai "Secrets" che hai impostato su GitHub
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")
FILE_MEMORIA = "giochi_visti.txt"

def ottieni_giochi_gratis():
    """Recupera la lista dei giochi gratis dalle API di GamerPower"""
    url = "https://www.gamerpower.com/api/giveaways?type=game&platform=all"
    try:
        risposta = requests.get(url)
        if risposta.status_code == 200:
            return risposta.json()
        return []
    except Exception as e:
        print(f"Errore durante la chiamata API: {e}")
        return []

def invia_messaggio(testo):
    """Invia un messaggio formattato al canale Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    dati = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, data=dati)
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

def carica_cronologia():
    """Legge il file dei giochi già inviati per non ripetersi"""
    if not os.path.exists(FILE_MEMORIA):
        return []
    with open(FILE_MEMORIA, "r") as f:
        return f.read().splitlines()

def salva_in_cronologia(id_gioco):
    """Aggiunge l'ID di un nuovo gioco inviato al file di memoria"""
    with open(FILE_MEMORIA, "a") as f:
        f.write(f"{id_gioco}\n")

if __name__ == "__main__":
    # Verifica che le configurazioni siano presenti
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("ERRORE: TOKEN_TELEGRAM o CHAT_ID non configurati nei Secrets!")
    else:
        print("Avvio scansione giochi...")
        giochi = ottieni_giochi_gratis()
        visti = carica_cronologia()
        nuovi_trovati = 0

        for gioco in giochi:
            id_gioco = str(gioco['id'])
            
            # Se il gioco non è mai stato inviato prima...
            if id_gioco not in visti:
                messaggio = (
                    f"🎁 *NUOVO GIOCO GRATIS!*\n\n"
                    f"🕹 *{gioco['title']}*\n"
                    f"💻 Piattaforma: {gioco['platforms']}\n"
                    f"📝 {gioco['description'][:100]}...\n\n"
                    f"🔗 [Riscatta qui]({gioco['open_giveaway_url']})"
                )
                
                invia_messaggio(messaggio)
                salva_in_cronologia(id_

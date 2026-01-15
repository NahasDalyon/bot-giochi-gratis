import requests
import os

# --- CONFIGURAZIONE TRAMITE GITHUB SECRETS ---
# os.getenv legge i valori che hai inserito nei Secrets di GitHub
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_URL = "https://www.gamerpower.com/api/giveaways"
DB_FILE = "sent_games.txt"

def get_sent_games():
    """Legge i giochi già inviati dal file di testo per evitare duplicati."""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        # Legge riga per riga e rimuove eventuali spazi bianchi o invii
        return [line.strip() for line in f.readlines() if line.strip()]

def save_sent_game(game_id):
    """Aggiunge l'ID del gioco appena inviato al file di testo."""
    with open(DB_FILE, "a") as f:
        f.write(f"{game_id}\n")

def send_telegram_message(message):
    """Invia il messaggio formattato in HTML al canale Telegram."""
    if not TOKEN or not CHAT_ID:
        print("ERRORE: TOKEN o CHAT_ID non trovati nei Secrets!")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False # Mostra l'anteprima del link
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # Genera un errore se la chiamata fallisce
        print("Messaggio inviato con successo!")
    except Exception as e:
        print(f"Errore durante l'invio a Telegram: {e}")

def check_for_games():
    """Controlla l'API dei giochi e invia notifiche per quelli nuovi."""
    print("Controllo nuovi giochi in corso...")
    sent_games = get_sent_games()
    
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        games = response.json()
    except Exception as e:
        print(f"Errore nel recupero dati dall'API: {e}")
        return

    # Controlliamo gli ultimi 15 giochi caricati dall'API
    # Invertiamo la lista per inviare prima i più "vecchi" tra i nuovi
    new_found = 0
    for game in reversed(games[:15]):
        game_id = str(game['id'])
        
        if game_id not in sent_games:
            # Creazione messaggio con formattazione HTML
            msg = (
                f"🎮 <b>NUOVO GIOCO GRATIS!</b>\n\n"
                f"<b>Titolo:</b> {game['title']}\n"
                f"<b>Piattaforma:</b> {game['platforms']}\n"
                f"<b>Valore:</b> <s>{game['worth']}</s> ⮕ <b>GRATIS</b>\n"
                f"<b>Tipo:</b> {game['type']}\n\n"
                f"🔗 <a href='{game['open_giveaway_url']}'>RISCATTA ORA</a>"
            )
            
            send_telegram_message(msg)
            save_sent_game(game_id)
            new_found += 1
        
    if new_found == 0:
        print("Nessun nuovo gioco trovato.")
    else:
        print(f"Operazione completata: inviati {new_found} nuovi giochi.")

if __name__ == "__main__":
    check_for_games()

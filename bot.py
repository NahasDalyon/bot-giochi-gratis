import requests
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_URL = "https://www.gamerpower.com/api/giveaways"
DB_FILE = "sent_games.txt"

def get_sent_games():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_sent_game(game_id):
    with open(DB_FILE, "a") as f:
        f.write(f"{game_id}\n")

def send_telegram_message(message, silent=False):
    """Invia il messaggio. Se silent=True, non fa suonare il telefono."""
    if not TOKEN or not CHAT_ID:
        print("ERRORE: Secrets mancanti!")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_notification": silent  # <-- Questa è la chiave per il silenzio
    }
    
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Errore invio: {e}")

def check_for_games():
    print("Controllo nuovi giochi in corso...")
    sent_games = get_sent_games()
    
    try:
        response = requests.get(API_URL)
        games = response.json()
    except Exception as e:
        print(f"Errore API: {e}")
        return

    new_found = 0
    for game in reversed(games[:15]):
        game_id = str(game['id'])
        
        if game_id not in sent_games:
            msg = (
                f"🎮 <b>NUOVO GIOCO GRATIS!</b>\n\n"
                f"<b>Titolo:</b> {game['title']}\n"
                f"<b>Piattaforma:</b> {game['platforms']}\n"
                f"🔗 <a href='{game['open_giveaway_url']}'>RISCATTA ORA</a>"
            )
            send_telegram_message(msg, silent=False) # Notifica sonora per i giochi
            save_sent_game(game_id)
            new_found += 1
        
    if new_found == 0:
        # Messaggio di stato SILENZIOSO (non disturba gli utenti)
        status_msg = "🤖 <b>Status:</b> Controllo completato. Nessun nuovo gioco oggi, ma io sono attivo!"
        send_telegram_message(status_msg, silent=True) 
        print("Nessun nuovo gioco. Notifica di stato inviata.")
    else:
        print(f"Inviati {new_found} nuovi giochi.")

if __name__ == "__main__":
    check_for_games()

import requests
import os

# Secrets da GitHub
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")           # Il tuo canale
PERSONAL_ID = os.getenv("MY_PERSONAL_ID") # Il tuo ID privato
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

def send_telegram_message(message, target, silent=False):
    """Invia un messaggio a un target specifico (canale o utente)."""
    if not TOKEN or not target:
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": target,
        "text": message,
        "parse_mode": "HTML",
        "disable_notification": silent
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
        send_telegram_message(f"❌ Errore API: {e}", PERSONAL_ID)
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
            # Invia al CANALE con suono
            send_telegram_message(msg, CHAT_ID, silent=False)
            save_sent_game(game_id)
            new_found += 1
    
    # INVIA LO STATUS SOLO A TE (Privato e Silenzioso)
    status_text = f"🤖 <b>Bot Status:</b> Eseguito con successo.\nNuovi giochi inviati: {new_found}"
    send_telegram_message(status_text, PERSONAL_ID, silent=True)
    print("Log inviato privatamente.")

if __name__ == "__main__":
    check_for_games()

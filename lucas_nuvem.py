
import requests
from datetime import date

# 🔐 SEUS TOKENS AQUI
API_FUTEBOL = "live_a94fe83f73acf0b20c9d6803d38154"
TELEGRAM_TOKEN = "7319244858:AAFO4r2JfYs3GLtAdjySK7FRkWBDl9Hj50o"
TELEGRAM_CHAT_ID = "1600739046"  # Seu ID do Telegram

# 🔧 Cabeçalho da API
HEADERS = {
    "Authorization": f"Bearer {API_FUTEBOL}"
}

def pegar_data_hoje():
    return date.today().isoformat()

def pegar_jogos_hoje():
    data = pegar_data_hoje()
    url = f"https://api.api-futebol.com.br/v1/partidas/{data}"
    resp = requests.get(url, headers=HEADERS)

    if resp.status_code != 200:
        print("Erro ao buscar jogos:", resp.text)
        return []

    jogos = resp.json()
    return jogos if isinstance(jogos, list) else []

def gerar_palpite():
    jogos = pegar_jogos_hoje()
    palpites = []

    for jogo in jogos:
        try:
            time_casa = jogo["time_mandante"]["nome_popular"]
            time_fora = jogo["time_visitante"]["nome_popular"]
            palpite = f"{time_casa} {2} x {1} {time_fora}"
            palpites.append(palpite)
        except:
            continue

    if not palpites:
        return "Nenhum jogo encontrado para hoje."

    return "🎯 Palpites de hoje:\n\n" + "\n".join(palpites)

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem
    }
    requests.post(url, data=payload)

def main():
    msg = gerar_palpite()
    print("🔁 Enviando mensagem para o Telegram...")
    enviar_telegram(msg)
    print("✅ Enviado com sucesso!")

if __name__ == "__main__":
    main()

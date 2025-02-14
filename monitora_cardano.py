
import requests
from time import sleep

# Configuração
WA_NUMBER = "5516993379492"  # Número de WhatsApp (55 + DDD + número)
API_KEY = "1271569"  # Substitua pela sua chave real do CallMeBot
ALTA = float(input('Digite rompimento da alta')) # Preço para definir alta
BAIXA = float(input('Digite rompimento da alta'))  # Preço para definir baixa

def notifica_alta():
    """Envia uma notificação via WhatsApp quando o preço do ADA sobe."""
    mensagem = "O Cardano subiu 🚀"
    url = f"https://api.callmebot.com/whatsapp.php?phone={WA_NUMBER}&text={mensagem}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("📢 Notificação de alta enviada com sucesso!")
        else:
            print(f"⚠️ Erro ao enviar notificação: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar à API do CallMeBot: {e}")

def notifica_baixa():
    """Envia uma notificação via WhatsApp quando o preço do ADA cai."""
    mensagem = "O Cardano abaixou 📉"
    url = f"https://api.callmebot.com/whatsapp.php?phone={WA_NUMBER}&text={mensagem}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("📢 Notificação de baixa enviada com sucesso!")
        else:
            print(f"⚠️ Erro ao enviar notificação: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar à API do CallMeBot: {e}")

def get_ada_price():
    """Obtém o preço do ADA em reais (BRL) a partir da API do CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=cardano&vs_currencies=brl"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["cardano"]["brl"]
        else:
            print(f"⚠️ Erro {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return None

# Loop de atualização
qtde_atualizacao = 0
qtde_erros = 0

while True:
    ada_price = get_ada_price()
    
    if ada_price is not None:
        qtde_atualizacao += 1
        print('-' * 50)
        print(f'📊 Atualização nº {qtde_atualizacao}')
        print(f'Rompimento de alta',ALTA)
        print(f'Preço do ADA: R$ {ada_price:.2f}')
        print(f'Rompimento de baixa',BAIXA)
        print('-' * 50)

        if ada_price >= ALTA:
            print('📈 Alta detectada!')
            notifica_alta()
        if ada_price <= BAIXA:
            print('📉 Baixa detectada!')
            #notifica_baixa()

    else:
        qtde_erros += 1
        print('-' * 50)
        print(f"⚠️ Falha ao obter preço. Erros consecutivos: {qtde_erros}")
        print('-' * 50)
        if qtde_erros >= 5:
            print("🚨 Muitos erros seguidos. Encerrando...")
            break  # Sai do loop se falhar várias vezes seguidas

    # Contador regressivo para a próxima atualização
    for c in range(12, 0, -1):
        print(f'🔄 Atualizando em {c}s...', end='\r', flush=True)
        sleep(1)

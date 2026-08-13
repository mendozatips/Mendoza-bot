import os
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup


# CONFIGURAÇÃO
TOKEN = os.getenv("TOKEN")
CHAT_ID = -1002620087512
FUSO_HORARIO = ZoneInfo("America/Sao_Paulo")

BANCA = 100.00
VALOR_UNIDADE = 1.00


MENSAGEM_BOM_DIA = """
<b>🙏🏼 Bom dia, Tropaa!

Que Deus abençoe nosso dia, ilumine nossas decisões e nos conduza a grandes resultados.

Vamos pra cima! 🍀⚽️</b>
"""

MENSAGEM_GESTAO = """
💰 GESTÃO DE BANCA

🎯 Banca de referência: R$ 1.000,00

📊 Divisão: 50 unidades

🟢 1 unidade: R$ 20,00 = 2% da banca

🟡 0,5 unidade: R$ 10,00 = 1% da banca

🟢 0,25 unidade: R$ 5,00 = 0,5% da banca

🛡️ Regra principal: divida sua banca e respeite sempre o valor da unidade.

⚠️ Nunca aumente a entrada para tentar recuperar uma perda.

🧠 Gestão é proteção. Disciplina é liberdade.

🔥 Mendoza Tips
"""


# EDITE OS PALPITES AQUI
PALPITES = [
    {
        "horario": "17:56",
        "odd": "2.03",
        "gestao": "2%",
        "imagem": "bilhete01.jpg",
        "link": "https://superbet.bet.br/bilhete-compartilhado/8983-7QWB9N",
    },
]


async def enviar_bom_dia(bot):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=MENSAGEM_BOM_DIA,
        parse_mode="HTML",
    )
    print("✅ Bom dia enviado.")


async def enviar_gestao(bot):
    imagem = "gestao de banca.jpg"

    if os.path.exists(imagem):
        with open(imagem, "rb") as arquivo:
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=arquivo,
                caption=MENSAGEM_GESTAO,
            )
    else:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=MENSAGEM_GESTAO,
        )

    print("✅ Gestão enviada.")


async def enviar_palpite(bot, palpite):
    texto = f"""
<b>👑 PALPITE DO MENDOZA • TIPS 👑

🏦 SUPERBET
➡️ ODD - {palpite["odd"]}
💵 GESTÃO - {palpite["gestao"]}

+18 APOSTE COM RESPONSABILIDADE</b>
"""

    teclado = None
    link = palpite.get("link")

    if link and not link.startswith("COLOQUE_"):
        botao = InlineKeyboardButton(
            text="🎟 CLIQUE AQUI — BILHETE PRONTO",
            url=link,
        )
        teclado = InlineKeyboardMarkup([[botao]])

    imagem = palpite.get("imagem")

    if imagem and os.path.exists(imagem):
        with open(imagem, "rb") as arquivo:
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=arquivo,
                caption=texto,
                reply_markup=teclado,
                parse_mode="HTML",
            )
    else:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=texto,
            reply_markup=teclado,
            parse_mode="HTML",
        )

    print(f"✅ Palpite das {palpite['horario']} enviado.")


def proximo_horario(hora, minuto):
    agora = datetime.now(FUSO_HORARIO)

    alvo = agora.replace(
        hour=hora,
        minute=minuto,
        second=0,
        microsecond=0,
    )

    if alvo <= agora:
        alvo += timedelta(days=1)

    return alvo


async def esperar_ate(hora, minuto):
    alvo = proximo_horario(hora, minuto)
    agora = datetime.now(FUSO_HORARIO)
    segundos = (alvo - agora).total_seconds()

    print(f"⏰ Aguardando até {alvo.strftime('%d/%m/%Y %H:%M')}...")
    await asyncio.sleep(segundos)


async def rotina_diaria(bot):
    enviados = set()

    while True:
        agora = datetime.now(FUSO_HORARIO)
        hoje = agora.date()

        # Bom dia às 08:00
        chave_bom_dia = f"{hoje}_bom_dia"
        if agora.hour == 8 and agora.minute == 0 and chave_bom_dia not in enviados:
            enviados.add(chave_bom_dia)
            await enviar_bom_dia(bot)

        # Gestão às 08:01
        chave_gestao = f"{hoje}_gestao"
        if agora.hour == 8 and agora.minute == 1 and chave_gestao not in enviados:
            enviados.add(chave_gestao)
            await enviar_gestao(bot)

        # Palpites
        for palpite in PALPITES:
            horario = palpite["horario"]
            hora, minuto = map(int, horario.split(":"))
            chave = f"{hoje}_{horario}"

            if agora.hour == hora and agora.minute == minuto and chave not in enviados:
                enviados.add(chave)

                try:
                    await enviar_palpite(bot, palpite)
                except Exception as erro:
                    print(f"❌ Erro no palpite das {horario}: {erro}")

        # Mantém somente os registros do dia atual
        prefixo = str(hoje)
        enviados = {item for item in enviados if item.startswith(prefixo)}

        await asyncio.sleep(20)


async def main():
    if not TOKEN:
        print("❌ TOKEN não configurado no Railway.")
        return

    bot = Bot(token=TOKEN)

    try:
        me = await bot.get_me()
        print(f"✅ Bot conectado: @{me.username}")
        print("🔄 Rotina automática ativada.")
        await rotina_diaria(bot)
    except Exception as erro:
        print(f"❌ Erro no bot: {erro}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot encerrado.")

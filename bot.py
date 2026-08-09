import os
import asyncio

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# ============================================================
# CONFIGURAÇÃO
# ============================================================

TOKEN = "8838241901:AAH6vrjZhMXNYmThlXjaYVL9AtPN253uvdg"

CHAT_ID = -1002620087512

FUSO_HORARIO = ZoneInfo("America/Sao_Paulo")


# ============================================================
# CONFIGURAÇÃO DA BANCA
# ============================================================

BANCA = 100.00
VALOR_UNIDADE = 1.00


# ============================================================
# MENSAGEM DE BOM DIA
# ============================================================

MENSAGEM_BOM_DIA = """
<b>🙏🏼 Bom dia, Tropaa!

Que Deus abençoe nosso dia, ilumine nossas decisões e nos conduza a grandes resultados.

Vamos pra cima! 🍀⚽️</b>
"""


# ============================================================
# MENSAGEM DE GESTÃO
# ============================================================

MENSAGEM_GESTAO = """
💰 GESTÃO DE BANCA

🎯 Banca de referência: R$ 100,00

📊 Unidade: R$ 1,00

🟢 Entrada padrão: 1 unidade

⚠️ Nunca aumente a entrada para tentar recuperar uma perda.

🧠 O objetivo é manter uma gestão consistente e responsável.

🔥 Mendoza Tips
"""


# ============================================================
# PALPITES
# ============================================================
#
# Para adicionar um novo palpite, copie um bloco e altere:
#
# "horario"
# "odd"
# "gestao"
# "imagem"
# "link"
#
# ============================================================

PALPITES = [

    {
        "horario": "20:50",
        "odd": "5.75",
        "gestao": "2%",
        "imagem": "imagens/bilhete01.jpg",
        "link": "https://superbet.bet.br/bilhete-compartilhado/8995-E1KOA9"
    },

    {
        "horario": "12:00",
        "odd": "1.60",
        "gestao": "1%",
        "imagem": None,
        "link": "COLOQUE_O_LINK_AQUI"
    },

    {
        "horario": "15:00",
        "odd": "1.70",
        "gestao": "1%",
        "imagem": None,
        "link": "COLOQUE_O_LINK_AQUI"
    },

]


# ============================================================
# ENVIAR BOM DIA
# ============================================================

async def enviar_bom_dia(bot):

    await bot.send_message(
        chat_id=CHAT_ID,
        text=MENSAGEM_BOM_DIA,
        parse_mode="HTML"
    )

    print("✅ Bom dia enviado.")


# ============================================================
# ENVIAR GESTÃO
# ============================================================

async def enviar_gestao(bot):

    imagem = "imagens/gestao de banca.jpg"

    if os.path.exists(imagem):

        with open(imagem, "rb") as arquivo:

            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=arquivo,
                caption=MENSAGEM_GESTAO
            )

    else:

        await bot.send_message(
            chat_id=CHAT_ID,
            text=MENSAGEM_GESTAO
        )

    print("✅ Gestão enviada.")


# ============================================================
# ENVIAR PALPITE
# ============================================================

async def enviar_palpite(bot, palpite):

    texto = f"""
<b>👑 PALPITE DO MENDOZA․TIPS 👑

🏦 SUPERBET
➡️ ODD - {palpite["odd"]}
💵 GESTÃO - {palpite["gestao"]}

+18 APOSTE COM RESPONSABILIDADE</b>
"""

    link = palpite.get("link")

    teclado = None

    if link and not link.startswith("COLOQUE_"):

        botao = InlineKeyboardButton(
            text="🎟 CLIQUE AQUI — BILHETE PRONTO",
            url=link
        )

        teclado = InlineKeyboardMarkup(
            [[botao]]
        )

    imagem = palpite.get("imagem")

    if imagem and os.path.exists(imagem):

        with open(imagem, "rb") as arquivo:

            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=arquivo,
                caption=texto,
                reply_markup=teclado,
                parse_mode="HTML"
            )

    else:

        await bot.send_message(
            chat_id=CHAT_ID,
            text=texto,
            reply_markup=teclado,
            parse_mode="HTML"
        )

    print(
        f"✅ Palpite das {palpite['horario']} enviado."
    )


# ============================================================
# CALCULAR PRÓXIMO HORÁRIO
# ============================================================

def proximo_horario(hora, minuto):

    agora = datetime.now(FUSO_HORARIO)

    alvo = agora.replace(
        hour=hora,
        minute=minuto,
        second=0,
        microsecond=0
    )

    if alvo <= agora:
        alvo += timedelta(days=1)

    return alvo


# ============================================================
# AGUARDAR HORÁRIO
# ============================================================

async def esperar_ate(hora, minuto):

    alvo = proximo_horario(hora, minuto)

    agora = datetime.now(FUSO_HORARIO)

    segundos = (
        alvo - agora
    ).total_seconds()

    print(
        f"⏰ Aguardando até "
        f"{alvo.strftime('%d/%m/%Y %H:%M')}..."
    )

    await asyncio.sleep(segundos)


# ============================================================
# ROTINA DIÁRIA
# ============================================================

async def rotina_diaria(bot):

    ultimo_dia = None

    while True:

        agora = datetime.now(FUSO_HORARIO)

        hoje = agora.date()

        # ====================================================
        # NOVO DIA
        # ====================================================

        if hoje != ultimo_dia:

            ultimo_dia = hoje

            print()
            print("====================================")
            print(
                f"📅 NOVO DIA: "
                f"{hoje.strftime('%d/%m/%Y')}"
            )
            print("====================================")

            # ------------------------------------------------
            # BOM DIA - 08:00
            # ------------------------------------------------

            try:

                agora = datetime.now(FUSO_HORARIO)

                if agora.hour < 8:

                    await esperar_ate(8, 0)

                    await enviar_bom_dia(bot)

                elif agora.hour == 8 and agora.minute == 0:

                    await enviar_bom_dia(bot)

                else:

                    print(
                        "ℹ️ Bom dia já passou hoje."
                    )

            except Exception as erro:

                print(
                    f"❌ Erro no bom dia: {erro}"
                )


            # ------------------------------------------------
            # GESTÃO - 08:01
            # ------------------------------------------------

            try:

                agora = datetime.now(FUSO_HORARIO)

                alvo_gestao = agora.replace(
                    hour=8,
                    minute=1,
                    second=0,
                    microsecond=0
                )

                if agora < alvo_gestao:

                    await asyncio.sleep(
                        (
                            alvo_gestao - agora
                        ).total_seconds()
                    )

                    await enviar_gestao(bot)

                elif agora.hour == 8 and agora.minute == 1:

                    await enviar_gestao(bot)

                else:

                    print(
                        "ℹ️ Gestão já passou hoje."
                    )

            except Exception as erro:

                print(
                    f"❌ Erro na gestão: {erro}"
                )


        # ====================================================
        # VERIFICAR PALPITES
        # ====================================================

        agora = datetime.now(FUSO_HORARIO)

        for palpite in PALPITES:

            horario = palpite["horario"]

            hora, minuto = map(
                int,
                horario.split(":")
            )

            if (
                agora.hour == hora
                and agora.minute == minuto
            ):

                chave = (
                    f"{hoje}_"
                    f"{horario}"
                )

                if not hasattr(
                    rotina_diaria,
                    "enviados"
                ):

                    rotina_diaria.enviados = set()

                if chave not in rotina_diaria.enviados:

                    try:

                        await enviar_palpite(
                            bot,
                            palpite
                        )

                        rotina_diaria.enviados.add(
                            chave
                        )

                    except Exception as erro:

                        print(
                            f"❌ Erro no palpite "
                            f"{horario}: {erro}"
                        )


        # ====================================================
        # LIMPAR REGISTROS ANTIGOS
        # ====================================================

        if hasattr(
            rotina_diaria,
            "enviados"
        ):

            prefixo = str(hoje)

            rotina_diaria.enviados = {
                item
                for item in rotina_diaria.enviados
                if item.startswith(prefixo)
            }


        # ====================================================
        # VERIFICAR A CADA 20 SEGUNDOS
        # ====================================================

        await asyncio.sleep(20)


# ============================================================
# INICIAR BOT
# ============================================================

async def main():

    if TOKEN == "COLOQUE_SEU_NOVO_TOKEN_AQUI":

        print(
            "❌ ERRO: coloque o novo token "
            "do BotFather."
        )

        return


    bot = Bot(
        token=TOKEN
    )


    # ========================================================
    # TESTAR CONEXÃO
    # ========================================================

    try:

        me = await bot.get_me()

    except Exception as erro:

        print(
            "❌ Não foi possível conectar "
            "ao Telegram."
        )

        print(
            f"Erro: {erro}"
        )

        return


    # ========================================================
    # INFORMAÇÕES
    # ========================================================

    print()
    print("====================================")
    print("🤖 MENDOZA TIPS BOT")
    print("====================================")

    print(
        f"Bot: @{me.username}"
    )

    print(
        f"Canal: {CHAT_ID}"
    )

    print(
        f"Banca: R$ {BANCA:.2f}"
    )

    print(
        f"Unidade: R$ {VALOR_UNIDADE:.2f}"
    )

    print(
        "Fuso: America/Sao_Paulo"
    )

    print(
        "===================================="
    )

    print(
        "✅ Bot conectado com sucesso!"
    )

    print(
        "🔄 Rotina automática ativada."
    )

    print(
        "====================================")


    # ========================================================
    # INICIAR ROTINA
    # ========================================================

    await rotina_diaria(bot)


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print()
        print("🛑 Bot encerrado pelo usuário.")

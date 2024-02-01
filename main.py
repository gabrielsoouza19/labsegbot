import discord
from discord.ext import commands
import asyncio
import PyPDF2
import os
from threading import Thread
from datetime import datetime
from flask import Flask, render_template


#### keep-alive
app = Flask(__name__)
r = {}
r_s = 0
now = datetime.now()

@app.route('/')
def hello():
  return render_template('index.html',
                         now=now,
                         now2=datetime.now(),
                         code=r,
                         rs=r_s)

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
#######

prefix = '/' 
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

client.remove_command('help') 
client.remove_command('ping')

@client.event
async def on_ready():
    print(f'\nLogado como: {client.user}\nServidores: {len(client.guilds)}')

# Gerência de erros
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("The specified command doesn't exist")
    else:
        await ctx.send("An error occurred")
        print(error)

# Latência exemplo
@client.command(name="ping", description="Ping command")
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} ms')

# Parte do PDF
@client.command(name="convert", description="Converter PDF para Texto")
async def process_pdf(ctx):
    if not ctx.message.attachments:
        await ctx.send("Por favor, envie um arquivo para processar.")
        return

    attachment = ctx.message.attachments[0]
    await attachment.save('PDF.pdf')

    text = readpdf('PDF.pdf')

    temp_file_name = f"{'LabSeg_convert'}.txt"
    with open(temp_file_name, "w", encoding="utf-8") as temp_file:
        temp_file.write(text)

    with open(temp_file_name, "rb") as temp_file:
        await ctx.send(content="Texto extraído do PDF:", file=discord.File(temp_file))

    os.remove(temp_file_name)

def readpdf(path):
    with open(path, 'rb') as aqv:
        ler_pdf = PyPDF2.PdfReader(aqv)

# Ler o pdf
        full_text = ""
        for num in range(len(ler_pdf.pages)):
            page = ler_pdf.pages[num]
            text = page.extract_text()
            full_text += f"\n{text}\n"

        return full_text

#inicia o bot
if __name__ == "__main__":
  t = Thread(target=run)
  t.start()
    try:
        token = os.environ['TOKEN']
        client.run(token)
    except Exception as e:
        print('Deu algum erro:', e)

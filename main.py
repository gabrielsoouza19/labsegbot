import discord
from discord.ext import commands
import asyncio
import PyPDF2
import os

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

# inciar o bot 
client.run('MTA2MjAxMjQwMTg0NDc2MDY2Ng.G7HfLG.fTfhtLBnrLf7ZMm3Erhg6pU4i5k5F48Lns2zXo') 

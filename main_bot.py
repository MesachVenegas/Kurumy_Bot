# Código escrito por Mesach Venegas
# mesach.venegas@hotmail.com
from discord.ext import commands
from listener_checker import MessageCheck
from datetime import datetime
from urllib import parse, request
from word_list import links_int, type_prog
import discord, json, re, random

last_member = None
last_member_left = None
intentos = discord.Intents.default()
intentos.members = True
kurumy = commands.Bot(
    command_prefix= commands.when_mentioned_or('!'),
    description= None,
    help_command=None,
    intents= intentos,
    case_insensitive = True
)

# Carga de elementos desde archivo json.
with open('data.json') as file:
    data:dict = json.load(file)

# Cambio de estado de actividad del bot.
@kurumy.event
async def on_ready():
    await kurumy.change_presence(
        activity= discord.Activity(type = discord.ActivityType.listening, name='!info'),
        status= discord.Status.idle
    )
    print(f'''
--------------------------------------------------------------------------------
            ██╗░░██╗██╗░░░██╗██████╗░██╗░░░██╗███╗░░░███╗██╗░░░██╗
            ██║░██╔╝██║░░░██║██╔══██╗██║░░░██║████╗░████║╚██╗░██╔╝
            █████═╝░██║░░░██║██████╔╝██║░░░██║██╔████╔██║░╚████╔╝░
            ██╔═██╗░██║░░░██║██╔══██╗██║░░░██║██║╚██╔╝██║░░╚██╔╝░░
            ██║░╚██╗╚██████╔╝██║░░██║╚██████╔╝██║░╚═╝░██║░░░██║░░░
            ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░░░░╚═╝░░░╚═╝░░░
--------------------------------------------------------------------------------
        Bot el linea como: {kurumy.user}
        Comandos: {len(kurumy.commands)}
        API Version: {discord.__version__}
        Servidores: {len(kurumy.guilds)}
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
''')

# Bienvenida a nuevos miembros.
@kurumy.event
async def on_member_join(member):
    global last_member
    last_member = member.name
    guild = member.guild
    canal = kurumy.get_channel(936142236884815902)
    if guild.system_channel is not None:
        if last_member is None:
            mensaje = f'Bienvenido {member.mention}:partying_face:! Si necesitas ayuda visita {canal.mention}'
            await guild.system_channel.send(mensaje)
            await guild.system_channel.send('O ingresa **!comandos** para ver la lista de comandos disponibles.')
        else:
            await guild.system_channel.send(f"Ya te había visto por aquí, bienvenido de vuelta {member.mention}")
    print(f"Ultimo miembro en unirse: {last_member}|{guild}")

# Despedida de un miembro del servidor.
@kurumy.event
async def on_member_remove(member):
    global last_member_left
    name = member.name.upper()
    guild = member.guild
    last_member_left = member.name
    await guild.system_channel.send(f"Bueno y ahi uno abandona el barco espero regreses pronto **{name}**:back_of_hand:!")
    print(f"Ultimo miembro en dejar un servidor: {last_member_left}|{guild}")

# Escucha de entradas de texto.
@kurumy.event
async def on_message(message):
    mensaje = message.content.lower()
    # Si el mensaje es enviado por el bot regresa el flujo.
    if message.author == kurumy.user:
        return
    elif mensaje.startswith('!'):
        # Lanzamiento de comandos.
        mensaje= mensaje.split(' ', 1)
        cog_name= str(mensaje[0][1:])
        comando = kurumy.get_command(cog_name)
        await comando(message)
        print(f"Ultimo comando ejecutado: {comando}")
    # Interacion con el bot.
    else:
        if type(MessageCheck().chat(message)) is tuple:
            # revisa el mensaje en busca de palabras clave y retorna el resultado si hay coincidencia y los links de apoyo
            data, urls = MessageCheck().chat(message)
            if data and urls is not None:
                await message.channel.send(data)
                for enlace in urls:
                    await message.channel.send(enlace)
        else:
            # Revisa el mensaje en busca de palabras clave y devuelve un mensaje.
            data = MessageCheck().chat(message)
            if data is not None:
                await message.channel.send(data)

######################################## COMANDOS ########################################
# Muestra los comandos disponibles del bot.
@kurumy.command(description='Muestra esta lista de comandos disponibles.')
async def info(ctx):
    lista_comandos = kurumy.commands
    guild = ctx.guild
    emojis = guild.emojis
    emoji_dic = {}
    emoji_default = ":robot:"
    for emoji in emojis:
        emoji_dic[emoji.name]= emoji

    embed = discord.Embed(
        title='Comandos:',
        color= discord.Color.dark_teal(),
        timestamp= datetime.utcnow()
    )
    emoji_name = {
        "server" : ":shield:",
        "info": ":information_source:",
        "links": ":link:",
        "tipo" : ":tophat:",
        "invitar": ":incoming_envelope:",
        "drive": ":cloud:",
        "whatsapp" : emoji_dic['whats'],
        "telegram" : emoji_dic['telegram'],
        "youtube" : emoji_dic['youtube'],
    }
    for comando in lista_comandos:
        for key, value in emoji_name.items():
            if comando.name == key:
                emoji_default = value
        embed.add_field(name=f'{emoji_default} !{comando.name}', value=f'*{comando.description}*')
    await ctx.channel.send(embed = embed)

# Muestra información simple del servidor.
@kurumy.command(description='Muestra infomacion básica del server')
async def server(ctx):
    embed = discord.Embed(
        title= ctx.guild.name,
        color= discord.Color.dark_gold(),
        timestamp= datetime.utcnow(),
        description='*Información básica sobre el servidor que tal vez quiera ver.*')
    embed.add_field(name='Descripcion: ', value= ctx.guild.description)
    embed.add_field(name='Creado el: ', value= ctx.guild.created_at.strftime('%d/%m/%Y'))
    embed.add_field(name='Miembros: ', value= ctx.guild.member_count)
    embed.set_thumbnail(url= ctx.guild.icon_url)
    await ctx.channel.send(embed = embed)

# Juego que retorna  una frase al azar
@kurumy.command(description="Juego al azar donde te indica tu futuro como programador")
async def tipo(ctx):
    image = data['image']
    await ctx.channel.send(image)
    await ctx.channel.send(f'El sombrero seleccionador a determinado que eres el programador del tipo: {random.choice(type_prog)}')

# Devuelve el link o links con ejercicios y pdf's de programacion.
@kurumy.command(description="Links de interés con ejercicios y pdf's")
async def links(ctx):
    for key, values in links_int.items():
        if key == 'ejercicios':
            await ctx.channel.send(f"**{key.capitalize()} & Pdf's sobre programacion:**")
            for link in values:
                await ctx.channel.send(link)
        else:
            return

# Permite realizar un busqueda en youtube y retorna el resultado mas popular.
@kurumy.command(description="Busqueda de videos en youtube.")
async def youtube(ctx):
    content_search = ctx.content.split(' ',1)
    search_query = parse.urlencode({'search_query': content_search[1]})
    html = request.urlopen('https://www.youtube.com/results?' + search_query)
    result= re.findall('watch\?v=(.{11})', html.read().decode('utf-8'))
    await ctx.channel.send(f'https://www.youtube.com/watch?v={result[0]}')

# Devuelve el link para el grupo de Whatsapp
@kurumy.command(description="Link de invitación al grupo de Whatsapp")
async def whatsapp(ctx):
    await ctx.channel.send(links_int['whats'])

# Devuelve el link para el grupo de telegram.
@kurumy.command(description="Link de invitación al grupo de Telegram")
async def telegram(ctx):
    await ctx.channel.send(links_int['telegram'])

# Invitación al guild.
@kurumy.command(description="Devuelve el link de invitación al servidor.")
async def invitar(ctx):
    guild = ctx.guild
    if guild.id == 397122820510973971:
        invitation = await kurumy.fetch_invite("Tc9Fvk2Umn")
        await ctx.channel.send(invitation)

my_token = data['my_token']
kurumy.run(my_token)
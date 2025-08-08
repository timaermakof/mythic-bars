import discord
import requests
import api
from discord.ext import tasks, commands
from discord.utils import get

token=api.ip_bot
api_link=api.api_link

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/',sync_commands_debug=True,sync_commands =True, activity=discord.Activity(type=discord.ActivityType.playing,name="mc.lentiworld.ru"),intents=intents)
print(bot)
############################
# /online - Онлайн сервера #
############################
@bot.tree.command(name="online",description="Онлайн сервера")
async def online(interaction: discord.Interaction):
  api_online = requests.get("https://api.mcsrvstat.us/2/<ip вашего сервера>").json()
  if api_online.get('online') == "true":
      api_online = requests.get(api_link).json()
      online_max = str(api_online['players']['max'])
      onlines = api_online['players']['sample'][0]['name'].split("§r")
      online_total = onlines[1];online_auth = onlines[3];online_prison = onlines[5];
      online_botfilter = int(online_total)-(int(online_auth)+int(online_prison));
      await interaction.response.send_message(
        embed=discord.Embed(
          title="🌍 Сейчас `"+online_total+"` из `"+online_max+"` игроков на сервере.",
          description="**🤖 На проверке: **`"+str(online_botfilter)+"`\n**❤ Авторизация: **`"+online_auth+"`\n**⛏ Тюрьма: **`"+online_prison+"`",
          color=0x55ff55
        )
      )
  else:
    await interaction.response.send_message(
    embed=discord.Embed(
        title="💔 Сервер сейчас выключен.",
        color=0x55ff55
        )
    )
################################
# /list - Контакты сервера #
################################
@bot.tree.command(name="contacts",description="Контакты сервера")
async def contacts(interaction: discord.Interaction):
  embed=discord.Embed(
    title="Контакты",
    description="По данным контактам вы можете к нам обратиться:",
    color=0x55ff55
  )
  embed.add_field(name="VK",value='<Вк вашего сервера>")',inline=True)
  embed.add_field(name="Почта",value='<почта поддержки>',inline=True)
  await interaction.response.send_message(embed=embed)

################################
# /contacts - Контакты сервера #
################################
@bot.tree.command(name="list",description="Показать всех игроков на сервере")
async def player_list(interaction: discord.Interaction):
    api_online = requests.get("https://api.mcsrvstat.us/2/<ip вашего сервера>").json()
    if api_online.get('online') == "true":
        online_total = api_online['players']["online"]
        online_max = api_online['players']["max"]
        online_list = api_online['players']["list"]
        await interaction.response.send_message(
        embed=discord.Embed(
             title="💚 Сейчас `" + str(online_total)+"` из `" + str(online_max)+"` игроков на сервере.",
             description="`" + str("""
""".join(online_list)) + "`",
             color=0x55ff55
            )
        )
    else:
        await interaction.response.send_message(
        embed=discord.Embed(
             title="💔 Сервер выключен.",
             color=0x55ff55
            )
        )

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} подключён к дс')

bot.run(token)
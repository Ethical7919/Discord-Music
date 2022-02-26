import discord, time, wavelink
from discord.ext import commands

prefix = "" #Prefix Here
Token = "" #Bot Token Here

class Bot(commands.Bot):

    def __init__(self):
        super(Bot, self).__init__(command_prefix=[prefix])

        self.add_cog(Music(self))

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())
    
    async def start_nodes(self):
        await self.bot.wait_until_ready()
        await self.bot.wavelink.initiate_node(host='lavalink-repl.cales.repl.co', port=443, rest_uri='https://lavalink-repl.cales.repl.co/', password='youshallnotpass', identifier='NODE-MAIN-2', region='singapore', secure: True)

    @commands.command(name='ihL3RL3NdA', aliases=["LnqhjsZYXp"])
    async def connect_up(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.connect(channel.id)

    @commands.command(name='connect', aliases=["join"])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.connect(channel.id)
        await ctx.send(f'Connecting.')

    @commands.command()
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')
        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_up)

        await player.play(tracks[0])
        await ctx.send(f'Added {str(tracks[0])} to the queue.')
        
    @commands.command(name="stop")
    async def stop_(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.stop()
        
        await ctx.send("Stopped the queue.")
        
    @commands.command(name="disconnect", aliases=["leave"])
    async def disconnect_(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.disconnect()
        
        await ctx.send(f"Disconnect.")

bot = Bot()
bot.run(Token)

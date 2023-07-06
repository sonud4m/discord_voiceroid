import pyvcvox
import discord
import asyncio
import settings
from discord.ext import tasks
TKN = settings.TKN


class control(pyvcvox.vcvox):
    def __init__(self):
        self.speakertype="vox"
        self.ch = None
        pyvcvox.vcvox.__init__(self)
    def speakertype(self,text):
        if self.spekertype=="vox":
            with open("temp.wav", mode="wb") as f:
                f.write(self.texttosound(text))
    def __enter__(self):
        return "temp.wav"
    def __exit__(self, exception_type, exception_value, traceback):
        self.ch = None


with control() as ctrl:
    client = discord.Client(intents=discord.Intents.all())

    

    @client.event
    #起動
    async def on_ready():
        print("bot is online")
        await client.change_presence(activity=discord.Game(name="読み上げ"))
        ctrl.loadVoice(ctrl.listVoices()[0])

    @client.event
    async def on_message(message):
        #botは無視
        if message.auhtor.bot:
            return
        #ボイスチャンネルに参加
        if message.content == "!join":
            if message.author.voice is None:
                await message.channel.send("ボイスチャンネルに接続してください")
                return
            
            await message.author.voice.channel.connect()
            await message.channel.send("接続しました")

            ctrl.ch=message.channel

        #呼ばれたチャンネル以外は無視
        elif message.channel==ctrl.ch:
            #退出
            if message.content == "!leave":
                if message.guild.voice_client is None:
                    await message.channel.send("接続していません")
                    return
                
                await message.guild.voice_client.disconnect()

                await message.channel.send("切断しました")


            
            #話者IDの表示
            elif "!vclist" in message.content:
                if ctrl.speakertype=="vox":
                    await message.channel.send("2:四国めたん\n3:ずんだもん\n8春日つむぎ")
            
            #話者切り替え
            elif "!vcset" in message.content:
                if ctrl.speakertype=="vox":
                    number=message.content.split()
                    number=number[1]
                    ctrl.speaker=number

            #テキスト読み上げ
            else:
                while message.guild.voice_client.is_playing():
                    await asyncio.sllep(0.1)

                source=discord.FFmpegPCMAudio(ctrl.speak(message.content))
                message.guild.voice_client.play(source)

    client.run(TKN)
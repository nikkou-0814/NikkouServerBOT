import discord
from discord import app_commands
import os
import random
import datetime
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#------------------------------------------------------------------ 起動処理 ------------------------------------------------------------------

@client.event
async def on_ready():
  print("起動OK!!!")
  await tree.sync()
  await client.change_presence(activity=discord.Game(name="BOTの説明は/help | v1.0.6"))

#------------------------------------------------------------------ VC通知機能 ------------------------------------------------------------------

@client.event
async def on_voice_state_update(member, before, after):

    if before.channel != after.channel:
        # メッセージを書き込むtxtch
        botRoom = client.get_channel(1048499946007056444)

        # 入退室を監視するVC
        announceChannelIds = [1061920720294268938, 1018187083526975549, 1018187142205284454, 1054056759939039232, 1054056788376432660, 1057949512934629456]

        if before.channel is not None and before.channel.id in announceChannelIds:
            await botRoom.send("**" + before.channel.name + "** から、__" + member.name + "__  さんが退室しました！")
        if after.channel is not None and after.channel.id in announceChannelIds:
            await botRoom.send("**" + after.channel.name + "** に、__" + member.name + "__  さんが入室しました！")

#------------------------------------------------------------------ ヘルプ機能------------------------------------------------------------------

@tree.command(name="help",description="このBOTのコマンドなどを表示します。")
async def help_command(interaction: discord.Interaction):
  embed=discord.Embed(title="ヘルプ機能", description="このBOTのコマンドなどを表示します。", color=0xff00ff)
  embed.set_author(name="NikkouServerCommunityBOT Help", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="/help", value="BOTのコマンドを表示する。", inline=True)
  embed.add_field(name="/omikuzi", value="今日の運勢は〜", inline=True)
  embed.add_field(name="/commandlist", value="コマンド一覧を説明無しで一覧表示する。", inline=False)
  embed.add_field(name="/ping", value="BOTの応答速度を計測する。", inline=False)
  embed.add_field(name="/userreport",value="サーバー内での迷惑行為などを報告できます。", inline=False)
  embed.add_field(name="/bugreport",value="サーバー内でのバグを報告できます。",inline=False)
  embed.add_field(name="/helpreport",value="レポートがわからないときに使ってね。")
  embed.add_field(name="/helpmusic",value="ミュージック機能がわからないときに使ってね。")
  embed.set_footer(text="Version 1.0.6 | made by nikkou_0814 and aomona")
  await interaction.response.send_message(embed=embed,ephemeral=True)

#------------------------------------------------------------------ コマンド一覧表示機能 ------------------------------------------------------------------

@tree.command(name="commandlist",description="コマンド一覧を説明無しで表示する。")
async def commandlist_command(interaction: discord.Interaction):
  embed=discord.Embed(title="コマンド一覧", description="コマンド一覧を表示します。", color=0x00ffff)
  embed.set_author(name="NikkouServerCommunityBOT Command List", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="/help", value="", inline=False)
  embed.add_field(name="/omikuzi", value="", inline=False)
  embed.add_field(name="/commandlist", value="", inline=False)
  embed.add_field(name="/userreport", value="", inline=False)
  embed.add_field(name="/bugreport",value="",inline=False)
  embed.add_field(name="/helpreport",value="",inline=False)
  embed.add_field(name="/helpmusic",value="",inline=False)
  embed.set_footer(text="Version 1.0.6 | made by nikkou_0814 and aomona")
  await interaction.response.send_message(embed=embed,ephemeral=True)

#------------------------------------------------------------------ helpreport機能 ------------------------------------------------------------------

@tree.command(name="helpreport",description="reportの仕方がわからないときに使ってね！")
async def helpreport_command(interaction: discord.Interaction):
  embed=discord.Embed(title="レポートする方法", color=0x00ff59)
  embed.set_author(name="NikkouServerCommunityBOT help-report", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="レポート対象が人の場合", value="", inline=False)
  embed.add_field(name="手順1", value="通報内容がわかるスクリーンショットを用意できるなら用意します。", inline=False)
  embed.add_field(name="手順2", value="日光サーバーのdiscord内で、/reportコマンドを使用します。", inline=False)
  embed.add_field(name="違反者", value="違反者のdiscord名を入れてください。", inline=False)
  embed.add_field(name="本文", value="違反者の犯した違反の内容を記入してください", inline=False)
  embed.add_field(name="スクリーンショット", value="スクリーンショットの画像ファイルを指定してください。ない場合ははらなくてOKです。", inline=False)
  embed.add_field(name="レポート対象がバグの場合", value="", inline=False)
  embed.add_field(name="手順1", value="バグのスクリーンショットを用意できるなら用意します。", inline=False)
  embed.add_field(name="手順2", value="日光サーバーのdiscord内で、/bugreportコマンドを使用します。", inline=False)
  embed.add_field(name="本文", value="バグの内容をできるだけ詳しく説明してください。", inline=False)
  embed.add_field(name="スクリーンショット", value="スクリーンショットの画像ファイルを指定してください。ない場合ははらなくてOKです。", inline=False)
  embed.add_field(name="", value="お手数おかけいたしますが、バグや治安改善のためご協力ください。", inline=False)
  embed.set_footer(text="Version 1.0.6 | made by nikkou_0814 and aomona")
  await interaction.response.send_message(embed=embed, ephemeral=True)

#------------------------------------------------------------------ おみくじ機能 ------------------------------------------------------------------

@tree.command(name="omikuzi",description="今日の運勢は〜")
async def omikuzi_command(interaction: discord.Interaction):
  unsei = ["おめでとう！ 大吉 が出たよ！！明日はなんかいいことがあるかもね！！", "中吉！おめでとう！って言えるかはあなた次第！", "吉 が出たよ、なんとも言えないね", "小吉 が出たよ！マイナスだと思わず頑張ろう！！", "凶 だ..まぁ大凶より良いしぃ...", "大凶 が出たぞ..お前...強く生きろよ...."]
  choice = random.choice(unsei)
  await interaction.response.send_message(choice,ephemeral=True)

#------------------------------------------------------------------ userreport機能 ------------------------------------------------------------------

@tree.command(#プレーヤーレポート
      name="userreport",description="サーバー内での迷惑行為を報告できます。")
@app_commands.describe(違反者="違反者のユーザーを選んでください")
async def report_command(interaction: discord.Interaction,違反者:discord.Member,本文:str,スクリーンショット:discord.Attachment=None):
  送信したユーザー = interaction.user.name
  送信された時間 = datetime.datetime.now()
  channel = client.get_channel(1057957897197338624)

    # Interactionを確認する
  await interaction.response.defer(ephemeral=True)

  embed = discord.Embed(title="ユーザーレポート", color=0x00ff59)
  embed.set_author(name="NikkouServerCommunityBOT user-report", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="送信者", value=送信したユーザー, inline=False)
  embed.add_field(name="違反者", value=違反者, inline=False)
  embed.add_field(name="通報内容", value=本文, inline=False)

  if スクリーンショット == None:
      embed.add_field(name="画像",value="画像が存在しませんでした。",inline=False)
  else:
      embed.set_image(url=スクリーンショット.url)

  embed.add_field(name="送信時間", value=送信された時間)

  # Interactionに返信する
  await interaction.followup.send("送信しました!協力ありがとう!", ephemeral=True)
  embed.set_footer(text="Version 1.0.6 | made by nikkou_0814 and aomona")
  await channel.send(embed=embed)

#------------------------------------------------------------------ bugreport機能 ------------------------------------------------------------------

@tree.command(
  name="bugreport",
  description="BOTやマイクラのバグなどを報告できます。")
async def bugreport_command(
  interaction: discord.Interaction, 本文: str, スクリーンショット: discord.Attachment=None):
  送信したユーザー = interaction.user.name
  送信された時間 = datetime.datetime.now()
  channel = client.get_channel(1080052057307881514)

  # Interactionを確認する
  await interaction.response.defer(ephemeral=True)

  embed = discord.Embed(title="プレーヤーレポート", color=0x00ff59)
  embed.set_author(name="NikkouServerCommunityBOT bug-report", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="送信者", value=送信したユーザー, inline=False)
  embed.add_field(name="バグの内容", value=本文, inline=False)

  if スクリーンショット == None:
    embed.add_field(name="画像",value="画像が存在しませんでした。",inline=False)
  else:
    embed.set_image(url=スクリーンショット.url)

    embed.add_field(name="送信時間", value=送信された時間)

  # Interactionに返信する
  await interaction.followup.send("送信しました!協力ありがとう!", ephemeral=True)
  embed.set_footer(text="Version 1.0.6 | made by nikkou_0814 and aomona")
  await channel.send(embed=embed)

#------------------------------------------------------------------ welcome機能 ------------------------------------------------------------------

@tree.command(name="welcome",description="welcome!")
async def welcome_command(interaction: discord.Interaction):
  await interaction.response.send_message("> **日光サーバーへようこそ！**\n\nこのDiscordサーバーはマインクラフトサーバー '日光鯖' の公式Discordサーバーです！サーバーを運用する前に最初にこれをしてください！\n\n> **ステップ.1 | ルール確認**\n\nhttps://discord.com/channels/1010856148083150928/1010859953122189382 でルールを見ましょう。\n\n> **ステップ.2 | ロールカスタム**\n\nhttps://discord.com/channels/1010856148083150928/1057312947443077130 でロールを自分好みにカスタマイズしよう！\n\n> **ステップ.3 | その他**\n\n このBOTの使い方は/helpで表示できます！（このBOTのメッセージはすべて__**みんなには表示されない**__から安心して使ってね！）\n\nあとはルールを守りながらご自由にどうぞ！！\n\n **Enjoy your nikkou life!**\n\n @everyone \n\n version 1.0.6 | made by aomona and nikkou_0814 ",ephemeral=False)

#------------------------------------------------------------------ helpmusic機能 ------------------------------------------------------------------

@tree.command(name="helpmusic",description="ミュージック機能がわからないときに使ってね。")
async def helpmusic_command(interaction: discord.Interaction):
  embed=discord.Embed(title="ミュージック機能を使う方法", color=0x00ff59)
  embed.set_author(name="NikkouServerCommunityBOT help-music", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="ボイスチャットに参加させる", value="n!summon または n!sm", inline=True)
  embed.add_field(name="ボイスチャットから抜けさせる", value="n!disconnect または n!dc", inline=True)
  embed.add_field(name="現在再生中の曲の詳細を表示", value="n!np", inline=True)
  embed.add_field(name="再生したい曲の URL または 曲名 でもOK", value="n!play または n!p", inline=True)
  embed.add_field(name="現在再生中の曲をスキップ", value="n!skip または n!s", inline=True)
  embed.add_field(name="現在のキューを確認", value="n!queue", inline=True)
  embed.add_field(name="使用可能なミュージックコマンドすべて", value="n!help または n!help all")
  embed.set_footer(text="Version 1.0.6 | musicbot by https://just-some-bots.github.io/MusicBot")
  await interaction.response.send_message(embed=embed, ephemeral=True)
  
client.run(os.getenv('TOKEN'))

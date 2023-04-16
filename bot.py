import discord
from discord import app_commands
import os
import random
import datetime
from dotenv import load_dotenv
load_dotenv()

VER = "1.1.4"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#------------------------------------------------------------------ 起動処理 ------------------------------------------------------------------

@client.event
async def on_ready():
  print("Bot起動完了！")
  await tree.sync()
  await client.change_presence(activity=discord.Game(name=f"BOTの説明は/help | {(VER)}"))

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

@tree.command(name="ヘルプ",description="このBOTのコマンドなどを表示します。")
async def ヘルプ_command(interaction: discord.Interaction):
  embed=discord.Embed(title="ヘルプ機能", description="このBOTのコマンドなどを表示します。", color=0xff00ff)
  embed.set_author(name="NikkouServerBOT Help", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="/ヘルプ", value="BOTのコマンドを表示する。", inline=True)
  embed.add_field(name="/おみくじ", value="今日の運勢は〜", inline=True)
  embed.add_field(name="/コマンド一覧", value="コマンド一覧を説明無しで一覧表示する。", inline=False)
  embed.add_field(name="/ユーザーレポート",value="サーバー内での迷惑行為などを報告できます。", inline=False)
  embed.add_field(name="/バグレポート",value="サーバー内でのバグを報告できます。",inline=False)
  embed.add_field(name="/レポートヘルプ",value="レポートがわからないときに使ってね。")
  embed.add_field(name="/ミュージックヘルプ",value="ミュージック機能がわからないときに使ってね。")
  embed.add_field(name="/サイコロ",value="サイコロを振ります！")
  embed.set_footer(text=f"version {(VER)} | made by nikkou_0814 and aomona")
  await interaction.response.send_message(embed=embed,ephemeral=True)

#------------------------------------------------------------------ コマンド一覧機能 ------------------------------------------------------------------

@tree.command(name="コマンド一覧",description="コマンド一覧を説明無しで表示する。")
async def commandlist_command(interaction: discord.Interaction):
  embed=discord.Embed(title="コマンド一覧", description="コマンド一覧を表示します。", color=0x00ffff)
  embed.set_author(name="NikkouServerBOT Command List", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="/ヘルプ", value="", inline=False)
  embed.add_field(name="/おみくじ", value="", inline=False)
  embed.add_field(name="/コマンド一覧", value="", inline=False)
  embed.add_field(name="/ユーザーレポート", value="", inline=False)
  embed.add_field(name="/バグレポート",value="",inline=False)
  embed.add_field(name="/レポートヘルプ",value="",inline=False)
  embed.add_field(name="/ミュージックヘルプ",value="",inline=False)
  embed.add_field(name="/サイコロ",value="",inline=False)
  embed.set_footer(text=f"version {(VER)} | made by nikkou_0814 and aomona")
  await interaction.response.send_message(embed=embed,ephemeral=True)

#------------------------------------------------------------------ レポートヘルプ機能 ------------------------------------------------------------------

@tree.command(name="レポートヘルプ",description="reportの仕方がわからないときに使ってね！")
async def helpreport_command(interaction: discord.Interaction):
  embed=discord.Embed(title="レポートする方法", color=0x00ff59)
  embed.set_author(name="NikkouServerBOT help-report", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
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
  embed.set_footer(text=f"version {(VER)} | made by nikkou_0814 and aomona")
  await interaction.response.send_message(embed=embed, ephemeral=True)

#------------------------------------------------------------------ おみくじ機能 ------------------------------------------------------------------

@tree.command(name="おみくじ",description="今日の運勢は〜")
async def おみくじ_command(interaction: discord.Interaction):
  user = interaction.user.mention
  unsei = [f"おめでとう！ 大吉 が出たよ！！ {(user)}さん！ 明日はなんかいいことがあるかもね！！", f"中吉！おめでとう！って言えるかは {(user)}さん 次第！", f"吉 が出たよ、なんとも言えないね {(user)}さん ", f"小吉 が出たよ！ {(user)}さん！ マイナスだと思わず頑張ろう！！",f"{(user)}さん....凶 だ..まぁ大凶より良いしぃ...", f"大凶 が出たぞ.. {(user)} ...強く生きろよ...."]
  choice = random.choice(unsei)
  await interaction.response.send_message(f"{(choice)}",ephemeral=False)

#------------------------------------------------------------------ ユーザーレポート機能 ------------------------------------------------------------------

@tree.command(#プレーヤーレポート
      name="ユーザーレポート",description="サーバー内での迷惑行為を報告できます。")
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
  embed.set_footer(text=f"version {(VER)} | made by nikkou_0814 and aomona")
  await channel.send(embed=embed)

#------------------------------------------------------------------ バグレポート機能 ------------------------------------------------------------------

@tree.command(
  name="バグレポート",
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
  embed.set_footer(text=f"version {(VER)} | made by nikkou_0814 and aomona")
  await channel.send(embed=embed)

#------------------------------------------------------------------ welcome機能 ------------------------------------------------------------------

@tree.command(name="welcome",description="Admin-Commands")
@app_commands.checks.has_permissions(moderate_members=True)
async def welcome_command(interaction: discord.Interaction):
  await interaction.response.send_message(f"> **NikkouServerServiceへようこそ！**\n\nサーバーを運用する前に最初にこれをしてください！\n\n> **ステップ.1 | ルール確認**\n\nhttps://discord.com/channels/1010856148083150928/1010859953122189382 でルールを見ましょう。\n\n> **ステップ.2 | ロールカスタム**\n\nhttps://discord.com/channels/1010856148083150928/1057312947443077130 でロールを自分好みにカスタマイズしよう！\n\n> **ステップ.3 | その他**\n\n このBOTの使い方は/helpで表示できます！（このBOTのメッセージは、「/おみくじ」と「/サイコロ」以外すべて__**みんなには表示されない**__から安心して使ってね！）/\n\nあとはルールを守りながらご自由にどうぞ！！\n\n @everyone \n\n version {(VER)} | made by aomona and nikkou_0814 ",ephemeral=False)

#------------------------------------------------------------------ ミュージックヘルプ機能 ------------------------------------------------------------------

@tree.command(name="ミュージックヘルプ",description="ミュージック機能がわからないときに使ってね。")
async def helpmusic_command(interaction: discord.Interaction):
  embed=discord.Embed(title="ミュージック機能を使う方法", color=0x00ff59)
  embed.set_author(name="NikkouServerBOT help-music", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="ボイスチャットに参加させる", value="n!summon または n!sm", inline=True)
  embed.add_field(name="ボイスチャットから抜けさせる", value="n!disconnect または n!dc", inline=True)
  embed.add_field(name="現在再生中の曲の詳細を表示", value="n!np", inline=True)
  embed.add_field(name="再生したい曲の URL または 曲名 でもOK", value="n!play または n!p", inline=True)
  embed.add_field(name="現在再生中の曲をスキップ", value="n!skip または n!s", inline=True)
  embed.add_field(name="現在のキューを確認", value="n!queue", inline=True)
  embed.add_field(name="使用可能なミュージックコマンドすべて", value="n!help または n!help all")
  embed.set_footer(text=f"version {(VER)} | musicbot by https://just-some-bots.github.io/MusicBot")
  await interaction.response.send_message(embed=embed, ephemeral=True)

#------------------------------------------------------------------ サイコロ機能 ------------------------------------------------------------------

@tree.command(name="サイコロ",description="サイコロを振ります！")
async def サイコロ_command(interaction: discord.Interaction):
  unsei = ["サイコロの出目は...「1」です！", "サイコロの出目は...「2」です！", "サイコロの出目は...「3」です！", "サイコロの出目は...「4」です！", "サイコロの出目は...「5」です！", "サイコロの出目は...「6」です！"]
  choice = random.choice(unsei)
  await interaction.response.send_message(choice,ephemeral=False)

#------------------------------------------------------------------ リンク集機能 ------------------------------------------------------------------
@tree.command(name="リンク集",description="NikkouServerServiceのリンク集を表示します。")
async def リンク集_commnad(interaction: discord.Interaction):
  embed=discord.Embed(title="リンク集", color=0x00ff59)
  embed.set_author(name="NikkouServerBOT リンク集", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="Webサイト", value="https://se.nikkou.nagoya")
  embed.add_field(name="寄付(Fantia)", value="https://fantia.jp/fanclubs/488442")
  await interaction.response.send_message(embed=embed, ephemeral=True)
  
client.run(os.getenv('TOKEN'))
import discord
from discord import app_commands
import os
import random
import datetime
from dotenv import load_dotenv
from discord.ext import tasks,commands
import time
from time import sleep
from datetime import datetime, timedelta
import json
import pykakasi
import re
import romkan

load_dotenv()

VER = "1.2.4b"

kks = pykakasi.kakasi()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#------------------------------------------------------------------ 起動処理 ------------------------------------------------------------------

@client.event
async def on_ready():
  print("Bot起動完了！")
  await tree.sync()
  await client.change_presence(activity=discord.Game(name=f"BOTの説明は/ヘルプ | v{(VER)}"))

#------------------------------------------------------------------ 禁止ワード削除 ------------------------------------------------------------------

@client.event
async def on_message(message):
    message.content=remove_spaces(message.content)
    if not message.author.bot:
#        await message.channel.send(kks.convert(message.content))
        if check_text(message.content):
#            await message.channel.send(kks.convert(message.content))
            await message.delete()

#------------------------------------------------------------------ 禁止ワードリストに追加するためのコマンド ------------------------------------------------------------------

@tree.command(name="これはえっちすぎます", description="新種のえっちな言葉を追加")
@commands.has_permissions(administrator=True)
async def cloud(interaction: discord.Interaction,word: str):
    server_id = 1010856148083150928  # 指定するServer ID
    if interaction.guild.id != server_id:
        await interaction.response.send_message('このコマンドは許可されていません。')
    add_word_to_blacklist(word)
    await interaction.response.send_message('これからはこの言葉も死刑です！')
#------------------------------------------------------------------ 自動削除系関数 ------------------------------------------------------------------

#--ひらがなに変換--
def toKanji(s):
#    print(s)
    s = romkan.to_hiragana(s)
    return s

#--リスト追加--
def add_word_to_blacklist(word):
    json_file_path = 'blacklist.json'

    # 辞書の読み込み
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        word_list = json.load(json_file)

    # 新しい言葉を追加
    word_list.append(word)

    # 辞書を再保存
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(word_list, json_file, ensure_ascii=False, indent=4)

#--テキスト検査--
def check_text(text):
    json_file = open('blacklist.json', 'r')
    word_list = json.load(json_file)
#    print(word_list)
    for word in word_list:
#        print(kks.convert(word) in kks.convert(text))
        text=replace_ltu(text)
        print(text)
        kksword="";
        lkksword="";
        for kkswords in kks.convert(text):
            kksword=kksword+kkswords["passport"]
        for lkkswords in kks.convert(word):
            lkksword=lkksword+lkkswords["passport"]
        print(toKanji(kksword).replace("lつ", "っ"))
        print(lkksword +"  ms:"+ kks.convert(toKanji(kksword).replace("lつ", "っ"))[0]["passport"])
        if kks.convert(lkksword)[0]["passport"] in kks.convert(toKanji(kksword).replace("lつ", "っ"))[0]["passport"]:
            print("list:"+kks.convert(lkksword)[0]["passport"]+"  old:"+word)
            print("ms:"+kks.convert(toKanji(kksword))[0]["passport"])
#            print("削除します")
            return True
    return False
#--「死ね」の文脈検査(現在は使用していない)--
def check_before_shine(text):
    index = remove_spaces(text).find("しね")
    if index == -1 or index == 0:
        return False
    else:
        before_text = text[:index]
        if before_text.strip() == "":
            return False
        else:
            return True

#--文字からスペースを削除する--
def remove_spaces(text):
    # 半角スペース、改行、全角スペースを削除する正規表現パターン
    pattern = r'[ 　\n]'
    # 正規表現パターンにマッチする部分を空文字列で置換
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text
#--「つ」の変換--
def replace_ltu(string):
    return string.replace("っ", "ltu").replace("ッ", "ltu")

#------------------------------------------------------------------ VC通知機能 ------------------------------------------------------------------

@client.event
async def on_voice_state_update(member, before, after):

    if before.channel != after.channel:
        # メッセージを書き込むtxtch
        botRoom = client.get_channel(1048499946007056444)

        # 入退室を監視するVC
        announceChannelIds = [1018187083526975549, 1018187142205284454, 1054056759939039232, 1054056788376432660, 1061920720294268938,  1090228103705542706, 1099276311345778769]

        if before.channel is not None and before.channel.id in announceChannelIds:
            await botRoom.send("**" + before.channel.name + "** から、__" + member.name + "__  さんが退室しました！")
        if after.channel is not None and after.channel.id in announceChannelIds:
            await botRoom.send("**" + after.channel.name + "** に、__" + member.name + "__  さんが入室しました！")


#------------------------------------------------------------------ ヘルプ機能------------------------------------------------------------------

@tree.command(name="ヘルプ",description="このBOTのコマンドなどを表示します。")
async def ヘルプ_command(interaction: discord.Interaction):
  embed=discord.Embed(title="ヘルプ機能", description="このBOTのコマンドなどを表示します。", color=0xff00ff)
  embed.set_author(name="NikkouServerBOT ヘルプ", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="/ヘルプ", value="BOTのコマンドを表示する。", inline=True)
  embed.add_field(name="/おみくじ", value="今日の運勢は〜", inline=True)
  embed.add_field(name="/コマンド一覧", value="コマンド一覧を説明無しで一覧表示する。", inline=False)
  embed.add_field(name="/ユーザーレポート",value="サーバー内での迷惑行為などを報告できます。", inline=False)
  embed.add_field(name="/バグレポート",value="サーバー内でのバグを報告できます。",inline=False)
  embed.add_field(name="/レポートヘルプ",value="レポートがわからないときに使ってね。")
  embed.add_field(name="/ミュージックヘルプ",value="ミュージック機能がわからないときに使ってね。")
  embed.add_field(name="/サイコロ",value="サイコロを振ります！")
  embed.add_field(name="/newembed",value="埋め込みメッセージを送信")
  embed.set_footer(text=f"version {(VER)} | made by nikkou_0814 and aomona")
  await interaction.response.send_message(embed=embed,ephemeral=True)

#------------------------------------------------------------------ コマンド一覧機能 ------------------------------------------------------------------

@tree.command(name="コマンド一覧",description="コマンド一覧を説明無しで表示する。")
async def コマンド一覧_command(interaction: discord.Interaction):
  embed=discord.Embed(title="コマンド一覧", description="コマンド一覧を表示します。", color=0x00ffff)
  embed.set_author(name="NikkouServerBOT コマンド一覧", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="/ヘルプ", value="", inline=False)
  embed.add_field(name="/おみくじ", value="", inline=False)
  embed.add_field(name="/コマンド一覧", value="", inline=False)
  embed.add_field(name="/ユーザーレポート", value="", inline=False)
  embed.add_field(name="/バグレポート",value="",inline=False)
  embed.add_field(name="/レポートヘルプ",value="",inline=False)
  embed.add_field(name="/ミュージックヘルプ",value="",inline=False)
  embed.add_field(name="/サイコロ",value="",inline=False)
  embed.add_field(name="/newembed",value="",inline=False)
  embed.set_footer(text=f"version {(VER)} | made by nikkou_0814 and aomona")
  await interaction.response.send_message(embed=embed,ephemeral=True)

#------------------------------------------------------------------ レポートヘルプ機能 ------------------------------------------------------------------

@tree.command(name="レポートヘルプ",description="レポートの仕方がわからないときに使ってね！")
async def レポートヘルプ_command(interaction: discord.Interaction):
  embed=discord.Embed(title="レポートする方法", color=0x00ff59)
  embed.set_author(name="NikkouServerBOT レポートヘルプ", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name="レポート対象が人の場合", value="", inline=False)
  embed.add_field(name="手順1", value="通報内容がわかるスクリーンショットを用意できるなら用意します。", inline=False)
  embed.add_field(name="手順2", value="日光サーバーのdiscord内で、/ユーザーレポート コマンドを使用します。", inline=False)
  embed.add_field(name="違反者", value="違反者のdiscord名を入れてください。", inline=False)
  embed.add_field(name="本文", value="違反者の犯した違反の内容を記入してください", inline=False)
  embed.add_field(name="スクリーンショット", value="スクリーンショットの画像ファイルを指定してください。ない場合ははらなくてOKです。", inline=False)
  embed.add_field(name="レポート対象がバグの場合", value="", inline=False)
  embed.add_field(name="手順1", value="バグのスクリーンショットを用意できるなら用意します。", inline=False)
  embed.add_field(name="手順2", value="日光サーバーのdiscord内で、/バグレポート コマンドを使用します。", inline=False)
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
async def ユーザーレポート_command(interaction: discord.Interaction,違反者:discord.Member,本文:str,スクリーンショット:discord.Attachment=None):
  送信したユーザー = interaction.user.name
  送信された時間 = datetime.datetime.now()
  channel = client.get_channel(1057957897197338624)

    # Interactionを確認する
  await interaction.response.defer(ephemeral=True)

  embed = discord.Embed(title="ユーザーレポート", color=0x00ff59)
  embed.set_author(name="NikkouServerBOT user-report", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
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
async def バグレポート_command(
  interaction: discord.Interaction, 本文: str, スクリーンショット: discord.Attachment=None):
  送信したユーザー = interaction.user.name
  送信された時間 = datetime.datetime.now()
  channel = client.get_channel(1080052057307881514)

  # Interactionを確認する
  await interaction.response.defer(ephemeral=True)

  embed = discord.Embed(title="プレーヤーレポート", color=0x00ff59)
  embed.set_author(name="NikkouServerBOT bug-report", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
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

@tree.command(name="welcome",description="Admin-Command")
@app_commands.default_permissions(administrator=True)
async def welcome_command(interaction: discord.Interaction):
  allowed_mentions = discord.AllowedMentions(everyone = True)
  await interaction.response.send_message(f"> **NikkouServerServiceへようこそ！**\n\nサーバーを運用する前に最初にこちらをしてください！\n\n> **ステップ.1 | 認証しよう！**\n\nhttps://discord.com/channels/1010856148083150928/1107107150381187123 で認証ボタンをクリック！。\n\n> **ステップ.2 | ルール確認**\n\nhttps://discord.com/channels/1010856148083150928/1010859953122189382 でルールを見ましょう。\n\n> **ステップ.3 | ロールカスタム**\n\nhttps://discord.com/channels/1010856148083150928/1057312947443077130 でロールを自分好みにカスタマイズしよう！\n\n> **ステップ.4 | その他**\n\n このBOTの使い方は /ヘルプ で表示できます！（このBOTのメッセージは、「/おみくじ」と「/サイコロ」以外すべて__**みんなには表示されない**__から安心して使ってね！）\n\nあとはルールを守りながらご自由にどうぞ！！\n\n @everyone \n\n version {(VER)} | made by aomona and nikkou_0814 ",ephemeral=False, allowed_mentions = allowed_mentions)

#------------------------------------------------------------------ ミュージックヘルプ機能 ------------------------------------------------------------------

@tree.command(name="ミュージックヘルプ",description="ミュージック機能がわからないときに使ってね。")
async def ミュージックヘルプ_command(interaction: discord.Interaction):
  embed=discord.Embed(title="ミュージック機能を使う方法", color=0x00ff59)
  embed.set_author(name="NikkouServerBOT ミュージックヘルプ", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
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
  embed.add_field(name="Webサイト", value="https://ssnikkou.com")
  embed.add_field(name="マイクラサーバーWebサイト", value="https://mcnikkou.com")
  embed.add_field(name="寄付(Fantia)", value="https://fantia.jp/fanclubs/488442")
  embed.set_footer(text=f"version {(VER)} | made by nikkou_0814 and aomona")
  await interaction.response.send_message(embed=embed, ephemeral=True)

#------------------------------------------------------------------ Announce機能 ------------------------------------------------------------------

@tree.command(name="announce",description="Admin-command")
@app_commands.default_permissions(administrator=True)
async def announce_command(
  interaction: discord.Interaction, タイトル: str, テキスト: str, 画像: discord.Attachment=None):
  channel = client.get_channel(1057567216003973141)
  作成したユーザー = interaction.user.name
  
  await interaction.response.defer(ephemeral=True)

  embed=discord.Embed(title=f"[{(タイトル)}]", color=0x00ff59)
  embed.set_author(name="NikkouServerBOT アナウンス", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name=f"{(テキスト)}", value="", inline=False)

  if 画像 == None:
    embed.add_field(name="",value="",inline=False)
  else:
    embed.set_image(url=画像.url)

  await interaction.followup.send("送信完了", ephemeral=True)
  embed.set_footer(text=f"version {(VER)} | announce by {(作成したユーザー)}")
  await channel.send(embed=embed)
  
#------------------------------------------------------------------ newembed機能 ------------------------------------------------------------------

@tree.command(name="newembed",description="埋め込みメッセージを送信")
async def newembed_command(
  interaction: discord.Interaction, タイトル: str, name: str, ephemeral: bool,画像: discord.Attachment=None, value: str=None):
  ユーザー = interaction.user.name

  await interaction.response.defer(ephemeral=True)

  embed=discord.Embed(title=f"{(タイトル)}", color=0x00ff59)
  embed.set_author(name="NikkouServerBOT newembed", icon_url="https://img.tokuzouserver.net/ed06513f-20f9-432c-90c4-59c070971f6c.png")
  embed.add_field(name=f"{(name)}",value=f"{(value)}",inline=False)

  if 画像 == None:
     embed.add_field(name="",value="",inline=False)
  else:
     embed.set_image(url=画像.url)

  await interaction.followup.send("完了しました",ephemeral=True)
  embed.set_footer(text=f"version {(VER)} | embed by {(ユーザー)}")
  await interaction.followup.send(embed=embed,ephemeral=ephemeral)

#------------------------------------------------------------------ stop機能 ------------------------------------------------------------------

@tree.command(name="stop",description="Botを停止")
@app_commands.default_permissions(administrator=True)
async def test_command(interaction:discord.Interaction):
    await interaction.response.send_message("Botを停止します。",ephemeral=True)
    await client.close()

#------------------------------------------------------------------ clean機能 ------------------------------------------------------------------

@tree.command(name="clean", description="メッセージ削除")
@app_commands.checks.has_permissions(moderate_members=True)
async def clean_commnad(interaction: discord.Interaction, how:int):
  await interaction.response.defer()
  deleted = await interaction.channel.purge(limit=how+1)

client.run(os.getenv('TOKEN'))

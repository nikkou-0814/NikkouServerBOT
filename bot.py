# Discord Botの基本的なセットアップ
import discord
from discord import app_commands
from discord.ext import tasks, commands
from discord.ui import View, Select
import openai

# その他のPythonライブラリ
import os
import random
from datetime import datetime, timedelta
import json
import re
import asyncio
import requests
import sys
import time
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment

# 環境変数の読み込みに関連するライブラリ
from dotenv import load_dotenv


# テキストの変換に関連するライブラリ（ローマ字、かな変換など）
import pykakasi
import romkan


#その他の関数
load_dotenv()

if os.getenv('TOKEN') is None:
   print("Discordトークンが設定されていません。.envを確認してください。")
   sys.exit(1)

connected_channels = {}


VER = "1.7.2"


kks = pykakasi.kakasi()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
openai.api_key = os.getenv('OPEN_AI_TOKEN')

#------------------------------------------------------------------ 起動処理 ------------------------------------------------------------------


@client.event
async def on_ready():
 print("Bot起動完了！")
 await tree.sync()
 await client.change_presence(activity=discord.Game(name=f"v{(VER)} | パトロール中！"))


#------------------------------------------------------------------ 禁止ワード削除 ------------------------------------------------------------------


@client.event
async def on_message(message):
   if message.author.bot or not message.guild or message.channel.id == 1206374283450777690 or message.channel.id == 1206584805970677841 or message.channel.id == 1206372067474284566:
       if(message.channel.id == 1206374283450777690 or not read_violations(message.author.id) > 10):
        return
   # 接続コマンドが使用されたチャンネルのメッセージのみを読み上げる
   if message.guild.id in connected_channels and message.channel.id == connected_channels[message.guild.id]:
       await read_message(message.guild, message.content)
   oldm = message.content
   message.content = remove_spaces(message.content)
   if not message.author.bot:
       if check_text(message.content):
           await message.delete()
           violation_count = update_violations(message.author.id,message.author.global_name,message.author.name)  # 違反回数を更新し、回数を取得
           reason = f"おめでとう！記念すべき{violation_count}回目の違反だよ！おめでとう！"  # Your reason for the timeout
           follow_up_message = await message.channel.send(f"{message.author.mention} さん、おめでとう！記念すべき{violation_count}回目の違反だよ！おめでとう！ {violation_count}秒のタイムアウトをプレゼント！ ")
            # Calculate the duration for the timeout as a timedelta
           if(message.author.id == 990940800785481728):
            duration = timedelta(days=1)  # 1 day timeout
            await message.channel.send(f"あ、ごめんなさい。詐欺師さんは対象外でした。1日タイムアウトをプレゼント！")
           else:
            duration = timedelta(seconds=violation_count) 

            # Apply the timeout to the member
           if(not message.author.top_role.permissions.administrator):
            await message.author.timeout(duration, reason=reason)
           load_dotenv()
           user = await client.fetch_user("961065585213583420")
           username = await client.fetch_user(message.author.id)
           embed = discord.Embed(
               title="不審なメッセージを検知し削除しました。",
               colour=discord.Colour(0xff0000),
               description="下記が削除したメッセージの詳細です。",
               timestamp=datetime.fromtimestamp(time.time())
           )
           embed.add_field(name="ユーザー", value=f"<@{username.id}>")
           embed.add_field(name="メッセージ", value=f"{oldm}")
           embed.add_field(name="チャンネル", value=f"<#{message.channel.id}>")
           embed.add_field(name="違反回数", value=f"{violation_count}回")  # 違反回数をembedに追加
           embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
           await user.send(embed=embed)
          
           # フォローアップメッセージを5秒後に削除
           await asyncio.sleep(5)
           await follow_up_message.delete()




#編集したメッセージに対しても禁止ワードを検知
@client.event
async def on_message_edit(before, after):
   if after.author.bot or not after.guild or after.channel.id == 1206374283450777690 or after.channel.id == 1206584805970677841 or after.channel.id == 1206372067474284566:
    if(not after.channel.id == 1206374283450777690 and not read_violations(after.author.id) > 10):
       return
   if after.author.bot:
       return
   oldm = after.content
   after.content = remove_spaces(after.content)
   if check_text(after.content):
       await after.delete()
       violation_count = read_violations(after.author.id)  # 違反回数を更新し、回数を取得
       reason = f"おめでとう！記念すべき{violation_count}回目の違反だよ！おめでとう！"  # Your reason for the timeout
       follow_up_message = await after.channel.send(f"{after.author.mention} さん、おめでとう！記念すべき{violation_count}回目の違反だよ！おめでとう！ {violation_count}秒のタイムアウトをプレゼント！ ")
        # Calculate the duration for the timeout as a timedelta
       if(after.author.id == 990940800785481728):
        duration = timedelta(days=1)  # 1 day timeout
        await after.channel.send(f"あ、ごめんなさい。詐欺師さんは対象外でした。1日タイムアウトをプレゼント！")
       else:
        duration = timedelta(seconds=violation_count)  # 1 day timeout
        # Apply the timeout to the member
       if(not after.author.top_role.permissions.administrator):
        await after.author.timeout(duration, reason=reason)
       update_violations(after.author.id,after.author.global_name,message.author.global_name)
       load_dotenv()
       user = await client.fetch_user("961065585213583420")
       username = await client.fetch_user(after.author.id)
       embed = discord.Embed(
           title="編集した不適切なメッセージを削除しました。",
           colour=discord.Colour(0xff0000),
           description="下記が削除したメッセージの詳細です。",
           timestamp=datetime.fromtimestamp(time.time())
       )
       embed.add_field(name="ユーザー", value=f"<@{username.id}>")
       embed.add_field(name="メッセージ", value=f"{oldm}")
       embed.add_field(name="チャンネル", value=f"<#{after.channel.id}>")
       embed.add_field(name="違反回数", value=f"{violation_count}回")  # 違反回数をembedに追加
       embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
       await user.send(embed=embed)


       # フォローアップメッセージを5秒後に削除
       await asyncio.sleep(5)
       await follow_up_message.delete()


#------------------------------------------------------------------ 禁止ワードリストに追加するためのコマンド ------------------------------------------------------------------


@tree.command(name="ngword", description="アドミンしか使えないよ！")
@commands.has_permissions(administrator=True)
async def cloud(interaction: discord.Interaction,word: str):
   server_id = 1206276013076774924  # 指定するServer ID
   if interaction.guild.id != server_id:
       await interaction.response.send_message('このコマンドは許可されてないよ')
   add_word_to_blocklist(word)
   await interaction.response.send_message(f'禁止ワードを追加しました！')


#------------------------------------------------------------------ 自動削除系関数 ------------------------------------------------------------------
#--ひらがなに変換--
def toKanji(s):
#    print(s)
   s = romkan.to_hiragana(s)
   return s


#--リスト追加--
def add_word_to_blocklist(word):
   json_file_path = 'blocklist.json'


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
   json_file = open('blocklist.json', 'r')
   word_list = json.load(json_file)
#    print(word_list)
   for word in word_list:
       if  word in text:
           return True
   for word in word_list:
#        print(kks.convert(word) in kks.convert(text))
       text=replace_ltu(text)
#        print(text)
       kksword="";
       lkksword="";
       for kkswords in kks.convert(text):
           kksword=kksword+kkswords["passport"]
       for lkkswords in kks.convert(word):
           lkksword=lkksword+lkkswords["passport"]
#        print(toKanji(kksword).replace("lつ", "っ"))
#        print(lkksword +"  ms:"+ kks.convert(toKanji(kksword).replace("lつ", "っ"))[0]["passport"])
       if kks.convert(lkksword)[0]["passport"] in kks.convert(toKanji(kksword).replace("lつ", "っ"))[0]["passport"]:
#            print("list:"+kks.convert(lkksword)[0]["passport"]+"  old:"+word)
#            print("ms:"+kks.convert(toKanji(kksword))[0]["passport"])
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


violations_file_path = 'violations.json'


# 違反回数を更新する関数
def update_violations(user_id,name,handle):
   try:
       with open(violations_file_path, 'r', encoding='utf-8') as file:
           try:
               violations = json.load(file)
           except json.JSONDecodeError:
               violations = {}
   except FileNotFoundError:
       violations = {}

   if str(user_id) in violations:
       violations[str(user_id)]["count"] += 1
       violations[str(user_id)]["name"] = name
       violations[str(user_id)]["handle"] = handle
   else:
       violations[str(user_id)] = {}
       violations[str(user_id)]["count"] = 1
       violations[str(user_id)]["name"] = name
       violations[str(user_id)]["handle"] = handle

   # 更新されたデータをファイルに保存
   with open(violations_file_path, 'w', encoding='utf-8') as file:
       json.dump(violations, file, ensure_ascii=False, indent=4)
   return violations[str(user_id)]["count"] 

def read_violations(user_id):
   try:
       with open(violations_file_path, 'r', encoding='utf-8') as file:
           try:
               violations = json.load(file)
           except json.JSONDecodeError:
               violations = {}
   except FileNotFoundError:
       violations = {}
   count = 0
   if str(user_id) in violations:
       count = violations[str(user_id)]["count"]

   # 更新されたデータをファイルに保存
   with open(violations_file_path, 'w', encoding='utf-8') as file:
       json.dump(violations, file, ensure_ascii=False, indent=4)

   return count  # 更新された違反回数を返す


#------------------------------------------------------------------ VC通知機能 ------------------------------------------------------------------


@client.event
async def on_voice_state_update(member, before, after):
   now = datetime.now().strftime('%Y年%m月%d日 %H時%M分')
   # 特定のユーザーのIDを指定
   target_user_id = 1032489535457734697
   if member.id == target_user_id:
       if after.mute:
           await member.edit(mute=False)
       if after.deaf:
           await member.edit(deafen=False)


   # メッセージを書き込むテキストチャンネル
   text_channel_id = 1206289654274457682
   text_channel = client.get_channel(text_channel_id)


   # ボイスチャンネル間での移動を検出
   if before.channel is not None and after.channel is not None and before.channel != after.channel:
       embed = discord.Embed(title="VC移動通知",
                             description=f"🔀<@{member.id}> さんが <#{before.channel.id}> から <#{after.channel.id}> に移動しました。",
                             color=0x0091ff)
       embed.set_author(name=f"{client.user.name} 通知機能", icon_url=f"{client.user.avatar}")
       embed.set_footer(text=f"{now} | Version {(VER)}")
       await text_channel.send(embed=embed, silent=True)
       return  # この行を追加して、ボイスチャンネル間の移動時にはこれ以降のコードを実行しないようにする


   if before.channel != after.channel:
       if before.channel is not None:
           embed = discord.Embed(title="VC退室通知",
                                 description=f"👋<@{member.id}> さんが <#{before.channel.id}> から退室しました。",
                                 color=0xff0000)
           embed.set_author(name=f"{client.user.name} 通知機能", icon_url=f"{client.user.avatar}")
           embed.set_footer(text=f"{now} | Version {(VER)}")
           await text_channel.send(embed=embed, silent=True)
       if after.channel is not None:
           embed = discord.Embed(title="VC入室通知",
                                 description=f"🎉<@{member.id}> さんが <#{after.channel.id}> に入室しました。",
                                 color=0x00ff00)
           embed.set_author(name=f"{client.user.name} 通知機能", icon_url=f"{client.user.avatar}")
           embed.set_footer(text=f"{now} | Version {(VER)}")
           await text_channel.send(embed=embed, silent=True)


#------------------------------------------------------------------ おみくじ機能 ------------------------------------------------------------------


@tree.command(name="omikuzi",description="今日の運勢を見てみます！")
async def omikuzi_command(interaction: discord.Interaction):
 user = interaction.user.mention
 unsei = [f"おめでとう！ 大吉 が出たよ！！ {(user)}さん！ 明日はなんかいいことがあるかもね！！", f"中吉！おめでとう！って言えるかは {(user)}さん 次第！", f"吉 が出たよ、なんとも言えないね {(user)}さん ", f"小吉 が出たよ！ {(user)}さん！ マイナスだと思わず頑張ろう！！",f"{(user)}さん....凶 だ..まぁ大凶より良いしぃ...", f"大凶 が出たぞ.. {(user)} ...強く生きろよ...."]
 choice = random.choice(unsei)
 await interaction.response.send_message(f"{(choice)}",ephemeral=False)


#------------------------------------------------------------------ サイコロ機能 ------------------------------------------------------------------


@tree.command(name="saikoro", description="サイコロの最大値を指定して振りましょう！")
@app_commands.describe(max_value="サイコロの最大値を指定してください。（必須）")
async def saikoro_command(interaction: discord.Interaction, max_value: int):
   # ユーザーが指定した最大値でサイコロを振る
   dice_roll = random.randint(1, max_value)
   # 出目に応じたメッセージを生成
   message = f"サイコロの出目は...「{dice_roll}」です！最大値は{max_value}です！"
   # メッセージを送信
   await interaction.response.send_message(message, ephemeral=False)


#------------------------------------------------------------------ newembed機能 ------------------------------------------------------------------


@tree.command(name="newembed",description="埋め込みメッセージを送信する時に便利だよ！")
async def newembed_command(
 interaction: discord.Interaction, タイトル: str, name: str, ephemeral: bool,画像: discord.Attachment=None, value: str=None):
 ユーザー = interaction.user.name


 await interaction.response.defer(ephemeral=True)


 embed=discord.Embed(title=f"{(タイトル)}", color=0x00ff59)
 embed.set_author(name="埋め込みメッセージ", icon_url=f"{client.user.avatar}")
 embed.add_field(name=f"{(name)}",value=f"{(value)}",inline=False)


 if 画像 == None:
    embed.add_field(name="",value="",inline=False)
 else:
    embed.set_image(url=画像.url)


 await interaction.followup.send("出来たよ！",ephemeral=True)
 embed.set_footer(text=f"version {(VER)} | embed by {(ユーザー)}")
 await interaction.followup.send(embed=embed,ephemeral=ephemeral)


#------------------------------------------------------------------ stop機能 ------------------------------------------------------------------


@tree.command(name="stop",description="アドミンしか使えないよ！")
@app_commands.default_permissions(administrator=True)
async def stop_command(interaction:discord.Interaction):
   notify_user = await interaction.client.fetch_user("961065585213583420")  # 通知を送るユーザーのID
   embed = discord.Embed(colour=discord.Colour(0xff0000),
                         timestamp=datetime.fromtimestamp(time.time()),
                         title="Bot停止通知",
                         description="Botがユーザーによって停止されました。")
   embed.add_field(name="停止したユーザー", value=f"<@{interaction.user.id}>")
   embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
   await notify_user.send(embed=embed)
   await interaction.response.send_message("Botを停止します。",ephemeral=True)
   await client.close()


#------------------------------------------------------------------ clean機能 ------------------------------------------------------------------


@tree.command(name="clean", description="メッセージ消す時に役立ちます！")
@app_commands.checks.has_permissions(moderate_members=True)
async def clean_command(interaction: discord.Interaction, how: int):
   await interaction.response.defer(ephemeral=True)
   deleted = await interaction.channel.purge(limit=how+1)
   followup_message = await interaction.followup.send(f"{len(deleted)-1}件のメッセージを削除しました！", ephemeral=True)
  
   # ここで5秒待機
   await asyncio.sleep(5)
  
   # フォローアップメッセージを削除
   try:
       await followup_message.delete()
   except discord.NotFound:
       pass


#------------------------------------------------------------------ ping機能 ------------------------------------------------------------------


@tree.command(name="ping",description="Pingを確認するよ！")
async def ping_command(interaction: discord.Interaction):
 allowed_mentions = discord.AllowedMentions(everyone = True)
 pingg = client.latency
 ping = round(pingg * 1000)
 if ping <= 500:
   await interaction.response.send_message(f"Pingは{ping}(ms)うん！許容範囲内だね",ephemeral=False)
 else:
   await interaction.response.send_message(f"Pingは{ping}(ms)ちょっと遅いね<@961065585213583420>に文句でも言ってあげて",ephemeral=False,allowed_mentions = allowed_mentions)


#------------------------------------------------------------------ role機能 ------------------------------------------------------------------
  
@tree.command(name="role", description="ロールを追加したり消したりできるよ")
async def role_command(interaction: discord.Interaction):
   # 特定のロールIDとBotのロールを除外
   excluded_role_ids = [1206285933729546282,1206658971851817000,1207027883802099762,1206523282703126538]  # 除外したい特定のロールID
   roles = [role for role in interaction.guild.roles if role.id not in excluded_role_ids and not role.managed]


   # @everyone ロールも除外する
   roles = [role for role in roles if role.name != '@everyone']


   # RoleSelectとViewを作成し、インタラクションに応答として送信します。
   select = RoleSelect(roles=roles)
   view = View()
   view.add_item(select)
   await interaction.response.send_message('ロールを選択してね！:', view=view, ephemeral=True)


#ロール処理
class RoleSelect(discord.ui.Select):
   def __init__(self, roles):
       options = [discord.SelectOption(label=role.name, value=str(role.id)) for role in roles]
       super().__init__(placeholder='ロールを選択してください', min_values=1, max_values=1, options=options)


   async def callback(self, interaction: discord.Interaction):
       role_id = int(self.values[0])
       role = interaction.guild.get_role(role_id)
       notify_user = await interaction.client.fetch_user(961065585213583420)  # 通知を送るユーザーのID
      
       if role:
           if role in interaction.user.roles:
               embed = discord.Embed(colour=discord.Colour(0xff0000))
               await interaction.user.remove_roles(role)
               embed.title = "ロール削除"
               embed.description = f'あなたから**{role.name}** を削除しました！'
               await interaction.response.send_message(embed=embed, ephemeral=True)


               embed = discord.Embed(colour=discord.Colour(0xff0000),
                                     timestamp=datetime.fromtimestamp(time.time()),
                                     title="ロール削除通知",
                                     description="下記が削除したロールの詳細です。")
               embed.add_field(name="ユーザー", value=f"<@{interaction.user.id}>")
               embed.add_field(name="ロール", value=f"{role.name}")
               embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
           else:
               embed = discord.Embed(colour=discord.Colour(0x00ff00))
               await interaction.user.add_roles(role)
               embed.title = "ロール追加"
               embed.description = f'あなたに**{role.name}** を追加しました！'
               await interaction.response.send_message(embed=embed, ephemeral=True)
              
               embed = discord.Embed(colour=discord.Colour(0x00ff00),
                                     timestamp=datetime.fromtimestamp(time.time()),
                                     title="ロール追加通知",
                                     description="下記が追加したロールの詳細です。")
               embed.add_field(name="ユーザー", value=f"<@{interaction.user.id}>")
               embed.add_field(name="ロール", value=f"{role.name}")
               embed.set_footer(text=f"{client.user.name}", icon_url=f"{client.user.avatar}")
          
           try:
               await notify_user.send(embed=embed)
           except discord.HTTPException:
               print(f'ユーザー {notify_user} へのDM送信に失敗しました。')
       else:
           embed = discord.Embed(color=discord.Color.red())
           embed.title = "エラー"
           embed.description = "ロールが見つかりません。"
           await interaction.response.send_message(embed=embed, ephemeral=True)


class MyBot(commands.Bot):
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.synced = False


   async def on_ready(self):
       if not self.synced:
           await self.tree.sync(guild=discord.Object(id=1206276013076774924))  # サーバーIDを自分のものに置き換える
           self.synced = True
       print(f'{self.user} がログインしました。')
 #------------------------------------------------------------------ 読み上げ機能 ------------------------------------------------------------------
  
@tree.command(name="disconnect", description="ボイスチャンネルから切断します。")
async def disconnect(interaction: discord.Interaction):
   if interaction.guild.voice_client:
       await interaction.guild.voice_client.disconnect()
       del connected_channels[interaction.guild.id]
       await interaction.response.send_message("ボイスチャンネルから切断しました。", ephemeral=True)
   else:
       await interaction.response.send_message("ボイスチャンネルに接続されていません。", ephemeral=True)


@tree.command(name="connect", description="ボイスチャンネルに接続します。")
async def connect(interaction: discord.Interaction):
   channel = interaction.channel
   if interaction.user.voice:
       voice_channel = interaction.user.voice.channel
       if not interaction.guild.voice_client:
           await voice_channel.connect()
           connected_channels[interaction.guild.id] = channel.id  # 接続されたチャンネルを記録
           await read_message(interaction.guild, f"{voice_channel.name}に接続しました")
           await interaction.response.send_message("ボイスチャンネルに接続しました。このチャンネルのメッセージを読み上げます。", ephemeral=True)
       else:
           await interaction.response.send_message("既に接続されています。", ephemeral=True)
   else:
       await interaction.response.send_message("ボイスチャンネルに接続してください。", ephemeral=True)


async def read_message(guild, message):
   tts = gTTS(text=message, lang='ja')
   buffer = BytesIO()
   tts.write_to_fp(buffer)
   buffer.seek(0)


   audio = AudioSegment.from_file(buffer, format="mp3")
   playback = BytesIO()
   audio.export(playback, format="wav")
   playback.seek(0)


   if guild.voice_client:
       guild.voice_client.play(discord.FFmpegPCMAudio(playback, pipe=True), after=lambda e: print('読み上げ終了', e))


#------------------------------------------------------------------ vote機能 ------------------------------------------------------------------


@tree.command(name="vote", description="投票を作成します。")
async def vote(interaction: discord.Interaction, title: str, options: str):
   """
   スラッシュコマンドで投票を作成します。
   :param interaction: Interactionオブジェクト。
   :param title: 投票のタイトル。
   :param options: カンマで選択肢を増やせます。
   """
   options_list = options.split(',')
   if len(options_list) > 9:
       await interaction.response.send_message('選択肢は9個までです。', ephemeral=True)
       return
  
   emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
   message_text = f"**{title}**\n\n" + "\n".join([f"{emojis[i]}: {option.strip()}" for i, option in enumerate(options_list)])
   await interaction.response.send_message(message_text)


   # メッセージにリアクションを追加
   message = await interaction.original_response()
   for i in range(len(options_list)):
       # 数字の絵文字を追加
       await message.add_reaction(f"{i+0}\N{COMBINING ENCLOSING KEYCAP}")


#------------------------------------------------------------------ earthquake機能 ------------------------------------------------------------------


@tree.command(name='earthquake', description="最新の地震情報を表示します")
async def quake(interaction: discord.Interaction):
   # 処理中であることをユーザーに通知
   await interaction.response.defer()


   # P2P地震情報APIのエンドポイント
   api_url = "https://api.p2pquake.net/v2/jma/quake?limit=1"


   # APIから地震情報を取得
   response = requests.get(api_url)
   if response.status_code == 200:
       data = response.json()[0]  # 最新の地震情報
       title = data.get("earthquake", {}).get("hypocenter", {}).get("name")
       magnitude = data.get("earthquake", {}).get("hypocenter", {}).get("magnitude")
       depth = data.get("earthquake", {}).get("hypocenter", {}).get("depth")
       max_intensity = data.get("earthquake", {}).get("maxScale")
       tsunami_info = data.get("earthquake", {}).get("domesticTsunami")
       occurrence_time = data.get("earthquake", {}).get("time")


       # Embedの作成
       embed = discord.Embed(title="🌍 地震情報", color=0xff0000)
       embed.add_field(name="場所", value=title, inline=True)
       embed.add_field(name="マグニチュード", value=magnitude, inline=True)
       embed.add_field(name="深さ", value=f"{depth}km", inline=True)
       embed.add_field(name="最大震度", value=str(int(max_intensity / 10)), inline=True)
       if tsunami_info == "None":
           tsunami_status = "津波の心配なし"
       else:
           tsunami_status = tsunami_info
       embed.add_field(name="津波情報", value=tsunami_status, inline=True)
       embed.add_field(name="発生時間", value=occurrence_time, inline=True)
       embed.set_footer(text=f"{client.user.name}・情報提供: P2P地震情報、気象庁 | Version {(VER)}", icon_url=f"{client.user.avatar}")


       await interaction.followup.send(embed=embed)
   else:
       await interaction.followup.send("地震情報の取得に失敗しました。")

@tree.command(name='mod-beta-test', description="MODテスト")
async def quake(interaction: discord.Interaction, text: str,):
   # 処理中であることをユーザーに通知
   response = openai.moderations.create(input=text)
   #print(response.results[0])
   check = response.results[0].flagged
   print(check)
   if(check):
    await interaction.response.send_message("このメッセージは削除対象です")
   else:
    await interaction.response.send_message("問題なし")
      


client.run(os.getenv('TOKEN'))




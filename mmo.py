import random
import psycopg2
import math
import json
import os
import sys
import re
import time
import traceback
import ast
import datetime
from datetime import datetime
from xml.etree import ElementTree
import discord
from discord.ext import commands
from discord.ext import tasks
from discord import Embed, NotFound, Forbidden
import requests
import asyncio

MONSTER_NUM = 50
token = os.environ['DISCORD_BOT_TOKEN']

f = open('monsters.json', 'r', encoding="utf-8")
monsters = json.load(f)
f = open('tyougekirea.json', 'r', encoding="utf-8")
tyougekirea = json.load(f)
f = open('tyoukyouteki.json', 'r', encoding="utf-8")
tyoukyouteki = json.load(f)
f = open('rea.json', 'r', encoding="utf-8")
rea = json.load(f)
f = open('kyouteki.json', 'r', encoding="utf-8")
kyouteki = json.load(f)
f = open('training.json', 'r', encoding="utf-8")
training_set = json.load(f)
bot = commands.Bot(command_prefix='m!', description='ただ倒して行くやつよ')
bot.remove_command('help')
kidou = []
ban_member = []
login_zumi = []
all_commands_user, all_commands_channel = [], []
kidou.append("true")

@bot.event
async def on_ready():
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT channel_id FROM ban_member ORDER BY channel_id").fetchall()
    if not c.fetchall() == None:
        for ban in ans:
            ban_member.append(ban[0])
        print(ban_member)
    con.commit()
    # bot.load_extension("jishaku")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("{}鯖".format(len(bot.guilds)))
    print("{}".format(len(set(bot.get_all_members()))))
    print('------')
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    c = conn.cursor()
    c.execute("select count(*) from player")
    print(c.fetchone()[0])
    print('------')
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT channel_id, boss_level FROM channel_status ORDER BY boss_level DESC").fetchall()
    con.commit()
    channels = c.fetchall()
    guilds = {}
    for channel in channels:
        c = bot.get_channel(channel[0])
        if not c: continue
        guild = c.guild
        if not guild.id in guilds:
            guilds[guild.id] = [guild.name, channel[1]]
    print("{}".format("\n".join(
        "{}      Lv{}".format(a[0], a[1]) for i, a in enumerate(guilds.values()))), )
    print("------")
    kidou.remove("true")
    await bot.change_presence(activity=discord.Game(name="!!help ｜{}鯖".format(len(bot.guilds))))
    # await bot.change_presence(activity=discord.Game(name="敵を増やしてます ｜{}鯖".format(len(bot.guilds))))
    embed = discord.Embed(
        title="MMOが起動しました",
        description=f"```\nMMOが参加しているサーバー: {len(bot.guilds)}鯖\nユーザ数：{len(set(bot.get_all_members()))}```\n\n```メモリ使用率 {mem.percent}% [16G]\nCPU使用率 {cpu}%```\n\n```player数{count[0]}```",
        color=0x2ECC69
    )
    try:
        await asyncio.gather(*(c.send(embed=embed) for c in bot.get_all_channels() if c.name == 'mmo起動ログ'))
    except Exception as e:
        channel = bot.get_channel(689852184958861347)
        embede = discord.Embed(
            title="=== エラー内容 ===",
            description=f"type:```{str(type(e))}\n```\nargs:```{str(e.args)}\n```\nerror本体:```{traceback.format_exc()}\n```",
            color=0x2ECC69
        )
        await channel.send(embed=embede)
    while True:
        # await bot.change_presence(activity=discord.Game(name="新要素コード書きながら考え中..."))
        await bot.change_presence(activity=discord.Game(name="!!help ｜{}鯖".format(len(bot.guilds))))
        await asyncio.sleep(6)
        await bot.change_presence(activity=discord.Game(name="by りん#6364"))
        await asyncio.sleep(6)


async def process_commands(message):
    ctx = await bot.get_context(message)
    await bot.invoke(ctx)


@bot.event
async def on_message(message):
    if message.content.startswith("!!") and not message.webhook_id:
        if message.author.id in all_commands_user or message.author.id in all_commands_channel:
            return
        if message.author.id in ban_member:
            if message.content.startswith("!!ban"):
                return await process_commands(message)
            if message.content.startswith("!!unban"):
                return await process_commands(message)
            embed = discord.Embed(description=f"{message.author.mention}さん...\nBANされてます。")
            return await message.channel.send(embed=embed)
        if not message.author.id in all_commands_user or message.author.id in all_commands_channel:
            all_commands_user.append(message.author.id)
            all_commands_channel.append(message.channel.id)
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            await process_commands(message)
            all_commands_channel.remove(message.channel.id)
            all_commands_user.remove(message.author.id)
            c = con.cursor()
            c.execute("SELECT user_id FROM login ORDER BY user_id").fetchall()
            con.commit()
            login_user = c.fetchall()
            for i in login_user:
                if not i[0] in login_zumi:
                    login_zumi.append(i[0])
            if message.author.id in login_zumi:
                await process_commands(message)
                all_commands_channel.remove(message.channel.id)
                all_commands_user.remove(message.author.id)
                return
            else:
                if message.content == "!!login":
                    await process_commands(message)
                    all_commands_channel.remove(message.channel.id)
                    all_commands_user.remove(message.author.id)
                    return
                else:
                    embed = Embed(description=f"""{message.author.mention}さん、ログインしてください\n[コマンドは !!login です]""")
                    await message.channel.send(embed=embed)
                    all_commands_channel.remove(message.channel.id)
                    all_commands_user.remove(message.author.id)
                    return
            # else:
            #     if message.content == "!!login":
            #         all_commands_channel.remove(message.channel.id)
            #         all_commands_user.remove(message.author.id)
            #         return
            #     embed = Embed(description=f"""{message.author.mention}さん、ログインしてください\n[コマンドは`!!login`です]""")
            #     await message.channel.send(embed=embed)
            #     all_commands_channel.remove(message.channel.id)
            #     all_commands_user.remove(message.author.id)
            #     return
    # if message.content.startswith("!!") and not message.webhook_id:
    #     if message.author.id in all_commands_user or message.author.id in all_commands_channel:  # コマンドがまだ実行中の場合
    #         return
    #     else:
    #         all_commands_user.append(message.author.id)
    #         all_commands_channel.append(message.channel.id)
    #         if not message.author.id in ban_member:
    #             if message.content == "!!login":
    #                 await process_commands(message)
    #                 remove_from_list(message.author.id, message.channel.id)
    #             login_zumi = []
    #             login_user = conn.execute("SELECT user_id FROM login ORDER BY user_id").fetchall()
    #             for i in login_user:
    #                 login_zumi.append(i[0])
    #             if message.author.id in login_zumi:
    #                 await process_commands(message)
    #                 remove_from_list(user_id, message.channel.id)
    #             else:
    #                 embed = Embed(description=f"""{message.author.mention}さん、ログインしてください\n[コマンドは`!!login`です]""")
    #                 await message.channel.send(embed=embed)
    #                 remove_from_list(message.author.id, message.channel.id)
    #                 return

def predicate1(message, author, bot):
    def check(reaction, user):
        if reaction.message.id != message.id or user == bot.user or author != user:
            return False
        if reaction.emoji == "<:owov:668693724494299147>" or reaction.emoji == "<:owox:668693763035758612>":
            return True
        return False
    return check

@bot.command(name='ban')
async def ban(ctx, id=""):
    if ctx.message.author.id == 421971957081309194:
        embed = Embed(description=f"{bot.get_user(int(id))}さんをBANしますか？\nokかnoで答えてください")
        taiki = await ctx.send(embed=embed)
        kaitou = await bot.wait_for('message', check=lambda messages: messages.author.id == ctx.message.author.id)
        if kaitou.content == "ok":
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute(f"INSERT INTO ban_member values({id})")
            conn.commit()
            ban_member.append(id)
            await taiki.edit(embed=Embed(description=f"{bot.get_user(int(id))}さんをBANしました！"))
            return
        elif kaitou.content == "no":
            await taiki.edit(embed=Embed(description=f"{bot.get_user(int(id))}さんをBANしませんでした！"))
            return

@bot.command(name='unban')
async def ban(ctx, id=""):
    if ctx.message.author.id == 421971957081309194:
        embed = Embed(description=f"{bot.get_user(int(id))}さんをUNBANしますか？\nokかnoで答えてください")
        taiki = await ctx.send(embed=embed)
        kaitou = await bot.wait_for('message', check=lambda messages: messages.author.id == ctx.message.author.id)
        if kaitou.content == "ok":
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute(f"DELETE FROM ban_member WHERE channel={id}")
            ban_member.remove(int(id))
            conn.commit()
            await taiki.edit(embed=Embed(description=f"{bot.get_user(int(id))}さんをUNBANしました！"))
            return
        elif kaitou.content == "no":
            await taiki.edit(embed=Embed(description=f"{bot.get_user(int(id))}さんをUNBANしませんでした！"))
            return


@bot.command(name='kill')
async def kill(ctx):
    if ctx.message.author.id == 421971957081309194:
        await ctx.send("ログアウトします。")
        await ctx.bot.logout()


@bot.command(name='set')
async def lvset(ctx, clevel=''):
    if ctx.message.author.id == 421971957081309194:
        boss_level = int(clevel)
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        c = conn.cursor()
        c.execute("UPDATE channel_status SET boss_level=? WHERE channel_id=?", (boss_level, ctx.message.channel.id,))
        c.execute("UPDATE channel_status SET boss_hp=? WHERE channel_id=?",
                     (boss_level * 10 + 50, ctx.message.channel.id,))
        conn.commit()
        channel_id = ctx.message.channel.id
        if boss_level % MONSTER_NUM in [
            1, 4, 6, 8, 9, 12, 14, 16, 18, 19, 21, 22, 24, 26, 27, 28, 29, 31, 33, 36, 38, 39, 42, 43, 44
        ] and random.random() < 0.08:
            monster = rea[0]
            special_monster[channel_id] = monster
            if random.random() < 0.02:
                monster = tyougekirea[0]
                very_special_monster[channel_id] = monster
        else:
            number = random.randint(0, 42)
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (number, channel_id))
            conn.commit()
            if boss_level % MONSTER_NUM == 0:
                con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                c = con.cursor()
                c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (0, channel_id))
                conn.commit()
            elif boss_level % 5 == 0:
                number = random.randint(0, 9)
                con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                c = con.cursor()
                c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (number, channel_id))
                conn.commit()
        await ctx.send(f"このチャンネルのレベルを **{boss_level}** にセットしました！")
        return


@bot.command(name='ping')
async def pings(ctx):
    before = time.monotonic()
    embed = discord.Embed(description="```BOTの反応速度```\nPong!")
    msg = await ctx.send(embed=embed)
    # ping = (time.monotonic() - before) * 1000
    ping = (msg.created_at - ctx.message.created_at).microseconds // 1000
    embed = discord.Embed(description=f"```BOTの反応速度```\nPong! `{int(ping)}ms`")
    return await msg.edit(embed=embed)


@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name='info')
async def info(ctx):
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    c = conn.cursor()
    c.execute("select count(*) from player")
    embed = discord.Embed(
        title="MMOについて",
        description=f"```python\nMMOが参加しているサーバー: {len(bot.guilds)}鯖```\n\n```python\nメモリ使用率 {mem.percent}% [16G]\nCPU使用率 {cpu}%```\n\n```python\nplayer数{c.fetchone()[0]}```",
        color=0x2ECC69
    )
    await ctx.message.channel.send(embed=embed)

@bot.command(name='helpss', pass_context=True, description='helpを表示')
async def help(ctx):
    prefix = "!!"
    try:  # ERRORが起きるか起きないか。起きたらexceptに飛ばされる
            help_message = [
                f"```{prefix}help | このメッセージの表示をします\n{prefix}attack/atk | チャンネル上のモンスターに攻撃します\n{prefix}item/i アイテム名/アイテム名の頭文字(e,f,i)) |\n選択したアイテムを使用します [例 {prefix}i f]\n{prefix}status/st | 自分のステータスを表示します\n{prefix}reset/rs/re | バトルをやり直します\n{prefix}t | 4字熟語クイズトレーニングをします```",
                f"```{prefix}ranking/rank | ランキングをまとめました。\n{prefix}invite/inv | 導入URLなど```"
            ]
            embeds = []
            for embed in help_message:
                embeds.append(Embed(title=f"MMO Secondの遊び方", description=embed).set_thumbnail(
                    url=bot.user.avatar_url_as()))
            msg = await ctx.send(
                content=f"```diff\n1ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                embed=embeds[0])
            while True:  # 処理が終わる(return)まで無限ループ
                try:  # ERRORが起きるか起きないか。起きたらexceptに飛ばされる
                    msg_react = await bot.wait_for('message', check=lambda
                        m: m.author == ctx.author and m.content.isdigit() and 0 <= int(m.content) <= len(embeds),
                                                        timeout=30)
                    # await bot.wait_for('message')で返ってくるのは文字列型
                    if msg_react.content == "0":
                        # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                        return await msg.edit(content="‌")
                    await msg.edit(
                        content=f"```diff\n{int(msg_react.content)}ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                        embed=embeds[int(msg_react.content) - 1])
                except asyncio.TimeoutError:  # wait_forの時間制限を超過した場合
                    # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                    return await msg.edit(content="‌", embed=Embed(title=f"時間切れです..."))

    except (NotFound, asyncio.TimeoutError, Forbidden):  # 編集した際に文字が見つからなかった, wait_forの時間制限を超過した場合, メッセージに接続できなかった
        return

@bot.command(name='ranking', aliases=['rank'], pass_context=True)
async def ranking(ctx):
    try:
        allrank = {'0⃣': "論外ランキング", '1⃣': "プレイヤーランキング", '2⃣': "BOTランキング", '3⃣': "鯖ランキング"}
        msg = await ctx.send(embed=Embed(
            description="\n".join([f"{r[0]}：`{r[1]}`" for r in list(allrank.items())]) + "\n見たい番号を発言してください。").set_author(
            name="全Ranking一覧:"))
        msg_react = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.content.isdigit() and 0 <= int(message.content) <= len(list(allrank.keys())) - 1, timeout=15)
        if msg_react.content == "0":
            try:
                r_dict = {'1⃣': "論外プレイヤーランキング", '2⃣': "論外BOTランキング", '3⃣': "論外が倒した数ランキング"}
                await msg.edit(embed=Embed(description="\n".join([f"{r[0]}：`{r[1]}`" for r in list(r_dict.items())]) + "\n見たい番号を発言してください。").set_author(name="【論外】Ranking一覧:"))
                # mmsg_react = await bot.wait_for('message', check=lambda
                #     message: message.author == ctx.author and message.content.isdigit() and 0 <= int(
                #     message.content) <= len(list(r_dict.keys())) - 1, timeout=30)
                mmsg_react = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.content.isdigit() and 0 <= int(message.content) <= len(list(r_dict.keys())), timeout=10)
                if mmsg_react.content == "1":
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id, experience FROM player ORDER BY experience DESC").fetchall()
                    con.commit()
                    playerlist = c.fetchall()
                    kekka = {}
                    rongaina = []
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
                    con.commit()
                    playerlist = c.fetchall()
                    rongai = c.fetchall()
                    for a in rongai:
                        rongaina.append(a[0])
                    for players in playerlist:
                        p = bot.get_user(int(players[0]))  # ユーザーID
                        if not p: continue
                        user = p
                        if not user.id in kekka:
                            for r in rongaina:
                                if user.id == r:
                                    kekka[user.id] = [user.name, int(math.sqrt(players[1]))]
                        if len(kekka) > 99: break
                    players_rank = "\n".join(
                        "{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
                    # データ10個ごとにページ分け
                    ranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
                    author = "世界Top100論外プレイヤー"
                if mmsg_react.content == "2":
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute(
                        "SELECT user_id, experience FROM player WHERE bot=1 ORDER BY experience DESC").fetchall()
                    con.commit()
                    playerlist = c.fetchall()
                    kekka = {}
                    rongaina = []
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
                    con.commit()
                    playerlist = c.fetchall()
                    rongai = c.fetchall()
                    for a in rongai:
                        rongaina.append(a[0])
                    for players in playerlist:
                        p = bot.get_user(int(players[0]))  # ユーザーID
                        if not p: continue
                        user = p
                        if not user.id in kekka:
                            if user.id in rongaina:
                                kekka[user.id] = [user.name, int(math.sqrt(players[1]))]
                        if len(kekka) > 99: break
                    players_rank = "\n".join(
                        "{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
                    ranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
                    author = "世界Top100論外BOT"
                if mmsg_react.content == "3":
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id, count FROM monster_count ORDER BY count DESC").fetchall()
                    con.commit()
                    playerlist = c.fetchall()
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id FROM player WHERE bot=0 ORDER BY user_id").fetchall()
                    con.commit()
                    isbot = c.fetchall()
                    all = []
                    kekka = {}
                    rongaina = []
                    rongai = conn.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
                    for a in rongai:
                        rongaina.append(a[0])
                    for a in isbot:
                        all.append(a[0])
                    for players in playerlist:
                        p = bot.get_user(int(players[0]))  # ユーザーID
                        if not p: continue
                        user = p
                        if not user.id in kekka:
                            if user.id in rongaina:
                                if user.id in all:
                                    kekka[user.id] = [user.name, int(players[1])]
                        if len(kekka) > 99: break
                    players_rank = "\n".join(
                        "{}位：`{}` ({}体)".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
                    # データ10個ごとにページ分け
                    ranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
                    author = "倒した数論外プレイヤーTop100"
                if not list(filter(lambda a: a != '', ranking_msgs)):
                    return await msg.edit(embed=Embed(description="まだデータはないようだ..."))

                embeds = []
                for embed in list(filter(lambda a: a != '', ranking_msgs)):
                    embeds.append(Embed(description=embed, color=0xff0000).set_author(name=author))

                await msg.edit(
                    content=f"```diff\n1ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                    embed=embeds[0])
                while True:  # 処理が終わる(return)まで無限ループ
                    try:  # ERRORが起きるか起きないか。起きたらexceptに飛ばされる
                        msg_react = await bot.wait_for('message', check=lambda
                            m: m.author == ctx.author and m.content.isdigit() and 0 <= int(m.content) <= len(embeds),
                                                       timeout=30)
                        # await bot.wait_for('message')で返ってくるのは文字列型
                        if msg_react.content == "0":
                            # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                            return await msg.edit(content="‌")
                        await msg.edit(
                            content=f"```diff\n{int(msg_react.content)}ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                            embed=embeds[int(msg_react.content) - 1])
                    except asyncio.TimeoutError:  # wait_forの時間制限を超過した場合
                        # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                        return await msg.edit(content="‌", embed=Embed(title=f"時間切れです..."))

            except (NotFound, asyncio.TimeoutError, Forbidden):  # 編集した際に文字が見つからなかった, wait_forの時間制限を超過した場合, メッセージに接続できなかった
                return

        elif msg_react.content == "1":
            try:
                r_dict = {'1⃣': "プレイヤーランキング", '2⃣': "倒した数ランキング"}
                await msg.edit(embed=Embed(description="\n".join([f"{r[0]}：`{r[1]}`" for r in list(r_dict.items())]) + "\n見たい番号を発言してください。").set_author(name="プレイヤーRanking一覧:"))
                mmsg_react = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.content.isdigit() and 0 <= int(message.content) <= len(list(r_dict.keys())), timeout=10)
                # await bot.wait_for('message')で返ってくるのは文字列型
                if mmsg_react.content == "1":
                  # ユーザーはisbotの中身を0で登録してるのでそこで判断して全データを取得させます。
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id, experience FROM player WHERE bot=0 ORDER BY experience DESC").fetchall()
                    con.commit()
                    playerlist = c.fetchall()
                    bkekka = {}
                    kekka = {}
                    rongaina = {}
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
                    con.commit()
                    rongai = c.fetchall()
                    for players in playerlist:
                        p = bot.get_user(int(players[0]))  # ユーザーID
                        if not p: continue
                        user = p
                        if not user.id in bkekka:
                            bkekka[user.id] = [user.name, int(math.sqrt(players[1]))]
                        if len(bkekka) > 99: break
                    for a in rongai:
                        rongaina[a] = [a]
                    for i in rongaina:
                        if i[0] in bkekka:
                            del bkekka[i[0]]
                    for players in playerlist:
                        p = bot.get_user(int(players[0]))  # ユーザーID
                        if not p: continue
                        user = p
                        if not user.id in kekka:
                            kekka[user.id] = [user.name, int(math.sqrt(players[1]))]
                        if len(kekka) > (100 - len(bkekka) + 100): break
                    for a in rongai:
                        rongaina[a] = [a]
                    for i in rongaina:
                        if i[0] in kekka:
                            del kekka[i[0]]
                    players_rank = "\n".join("{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
                  # データ10個ごとにページ分け
                    rranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
                    author = "世界Top100プレイヤー"
                else:
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id, count FROM monster_count ORDER BY count DESC").fetchall()
                    con.commit()
                    playerlist = c.fetchall()
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id FROM player WHERE bot=0 ORDER BY user_id").fetchall()
                    con.commit()
                    isbot = c.fetchall()
                    all = []
                    kekka = {}
                    rongaina = []
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
                    con.commit()
                    rongai = c.fetchall()
                    for a in rongai:
                        rongaina.append(a[0])
                    for e in isbot:
                        all.append(e[0])
                    for players in playerlist:
                        p = bot.get_user(int(players[0]))  # ユーザーID
                        if not p: continue
                        user = p
                        if not user.id in kekka:
                            if not user.id in rongaina:
                                if user.id in all:
                                    kekka[user.id] = [user.name, int(players[1])]
                        if len(kekka) > 99: break
                        print(kekka)
                    players_rank = "\n".join("{}位：`{}` ({}体)".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
                  # データ10個ごとにページ分け
                    rranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
                    author = "倒した数Top100プレイヤー"

                if not list(filter(lambda a: a != '', rranking_msgs)):
                    return await msg.edit(embed=Embed(description="まだデータはないようだ..."))

                embeds = []
                for embed in list(filter(lambda a: a != '', rranking_msgs)):
                    embeds.append(Embed(description=embed, color=0xff0000).set_author(name=author))

                await msg.edit(content=f"```diff\n1ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```", embed=embeds[0])
                while True: # 処理が終わる(return)まで無限ループ
                    try: # ERRORが起きるか起きないか。起きたらexceptに飛ばされる
                        mmsg_react = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.content.isdigit() and 0 <= int(m.content) <= len(embeds), timeout=30)
                      # await bot.wait_for('message')で返ってくるのは文字列型
                        if mmsg_react.content == "0":
                          # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                            return await msg.edit(content="‌")
                        await msg.edit(content=f"```diff\n{int(mmsg_react.content)}ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```", embed=embeds[int(mmsg_react.content)-1])
                    except asyncio.TimeoutError: # wait_forの時間制限を超過した場合
                      # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                        return await msg.edit(content="‌", embed=Embed(title=f"時間切れです..."))

            except (NotFound, asyncio.TimeoutError, Forbidden): # 編集した際に文字が見つからなかった, wait_forの時間制限を超過した場合, メッセージに接続できなかった
                return

        elif msg_react.content == "2":
            try:
                r_dict = {'1⃣': "BOTランキング", '2⃣': "倒した数ランキング"}
                await msg.edit(embed=Embed(description="\n".join(
                    [f"{r[0]}：`{r[1]}`" for r in list(r_dict.items())]) + "\n見たい番号を発言してください。").set_author(
                    name="BOTRanking一覧:"))
                mmsg_react = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.content.isdigit() and 0 <= int(message.content) <= len(list(r_dict.keys())), timeout=10)
                # await bot.wait_for('message')で返ってくるのは文字列型
                if mmsg_react.content == "1":
                  # BOTはisbotの中身を1で登録してるのでそこで判断して全データを取得させます。
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute(
                      "SELECT user_id, experience FROM player WHERE bot=1 ORDER BY experience DESC").fetchall()
                    con.commit()
                    playerlist = c.fetchall()
                    kekka = {}
                    rongaina = []
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
                    con.commit()
                    rongai = c.fetchall()
                    for a in rongai:
                        rongaina.append(a[0])
                    for players in playerlist:
                        p = bot.get_user(int(players[0]))  # ユーザーID
                        if not p: continue
                        user = p
                        if not user.id in kekka:
                            for r in rongaina:
                                if not user.id == r:
                                    kekka[user.id] = [user.name, int(math.sqrt(players[1]))]
                        if len(kekka) > 99: break
                    players_rank = "\n".join("{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
                  # データ10個ごとにページ分け
                    ranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
                    author = "世界Top100ボット"
                else:
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id, count FROM monster_count ORDER BY count DESC").fetchall()
                    con.commit()
                    playerlist = c.fetchall()
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id FROM player WHERE bot=1 ORDER BY user_id").fetchall()
                    con.commit()
                    isbot = c.fetchall()
                    all = []
                    kekka = {}
                    rongaina = []
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
                    con.commit()
                    rongai = c.fetchall()
                    for a in rongai:
                        rongaina.append(a[0])
                    for a in isbot:
                        all.append(a[0])
                    for players in playerlist:
                        p = bot.get_user(int(players[0]))  # ユーザーID
                        if not p: continue
                        user = p
                        if not user.id in kekka:
                            if not user.id in rongaina:
                                if user.id in all:
                                    kekka[user.id] = [user.name, int(players[1])]
                        if len(kekka) > 99: break
                    players_rank = "\n".join(
                        "{}位：`{}` ({}体)".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
                    # データ10個ごとにページ分け
                    ranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
                    author = "BOTが倒した数Top100"

                if not list(filter(lambda a: a != '', ranking_msgs)):
                    return await mmsg.edit(embed=Embed(description="まだデータはないようだ..."))

                embeds = []
                for embed in list(filter(lambda a: a != '', ranking_msgs)):
                    embeds.append(Embed(description=embed, color=0xff0000).set_author(name=author))

                await msg.edit(
                    content=f"```diff\n1ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                    embed=embeds[0])
                while True:  # 処理が終わる(return)まで無限ループ
                    try:  # ERRORが起きるか起きないか。起きたらexceptに飛ばされる
                        msg_react = await bot.wait_for('message', check=lambda
                            m: m.author == ctx.author and m.content.isdigit() and 0 <= int(m.content) <= len(embeds),
                                                       timeout=30)
                        # await bot.wait_for('message')で返ってくるのは文字列型
                        if msg_react.content == "0":
                            # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                            return await msg.edit(content="‌")
                        await msg.edit(
                            content=f"```diff\n{int(msg_react.content)}ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                            embed=embeds[int(msg_react.content) - 1])
                    except asyncio.TimeoutError:  # wait_forの時間制限を超過した場合
                        # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                        return await msg.edit(content="‌", embed=Embed(title=f"時間切れです..."))

            except (NotFound, asyncio.TimeoutError, Forbidden):  # 編集した際に文字が見つからなかった, wait_forの時間制限を超過した場合, メッセージに接続できなかった
                return

        elif msg_react.content == "3":
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT channel_id, boss_level FROM channel_status ORDER BY boss_level DESC").fetchall()
            con.commit()
            channels = c.fetchall()
            guilds = {}
            for channel in channels:
                c = bot.get_channel(channel[0])
                if not c: continue
                guild = c.guild
                if not guild.id in guilds:
                    guilds[guild.id] = [guild.name, channel[1]]
                if len(guilds) > 99: break
            players_rank = "\n".join("{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(guilds.values()))
            # データ10個ごとにページ分け
            ranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
            author = "世界Top100サーバー"

            if not list(filter(lambda a: a != '', ranking_msgs)):
                return await mmsg.edit(embed=Embed(description="まだデータはないようだ..."))

            embeds = []
            for embed in list(filter(lambda a: a != '', ranking_msgs)):
                embeds.append(Embed(description=embed, color=0xff0000).set_author(name=author))

            await msg.edit(
                content=f"```diff\n1ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                embed=embeds[0])
            while True:  # 処理が終わる(return)まで無限ループ
                try:  # ERRORが起きるか起きないか。起きたらexceptに飛ばされる
                    msg_react = await bot.wait_for('message', check=lambda
                        m: m.author == ctx.author and m.content.isdigit() and 0 <= int(m.content) <= len(embeds),
                                                   timeout=30)
                    # await bot.wait_for('message')で返ってくるのは文字列型
                    if msg_react.content == "0":
                        # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                        return await msg.edit(content="‌")
                    await msg.edit(
                        content=f"```diff\n{int(msg_react.content)}ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```",
                        embed=embeds[int(msg_react.content) - 1])
                except asyncio.TimeoutError:  # wait_forの時間制限を超過した場合
                    # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
                    return await msg.edit(content="‌", embed=Embed(title=f"時間切れです..."))

    except (NotFound, asyncio.TimeoutError, Forbidden):  # 編集した際に文字が見つからなかった, wait_forの時間制限を超過した場合, メッセージに接続できなかった
        return
# @bot.command(name='rranking', aliases=['rrank'], pass_context=True, description='ユーザーコマンド') # コマンド名:『ranking』 省略コマンド:『rank』
# async def ranking(ctx): #既に存在する関数名だったらERROR出るのでもし今後コマンドを追加するならコマンド名と同じ関数名にして下さい。
#     f"""
#     各種ランキングの表示
#     各種100位まで表示するようにしております。
#     10位ごとに勝手にページが分けられます。
#     f"""
#     try: # ERRORが起きるか起きないか。起きたらexceptに飛ばされる
#         r_dict = {'0⃣': "プレイヤーランキング", '1⃣': "BOTランキング", '2⃣': "倒した数ランキング"}
#         msg = await ctx.send(embed=Embed(description="\n".join([f"{r[0]}：`{r[1]}`" for r in list(r_dict.items())]) + "\n見たい番号を発言してください。").set_author(name="【論外】Ranking一覧:"))
#         msg_react = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.content.isdigit() and 0 <= int(message.content) <= len(list(r_dict.keys())) - 1, timeout=10)
#       # await bot.wait_for('message')で返ってくるのは文字列型
#         if msg_react.content == "0":
#             playerlist = conn.execute("SELECT user_id, experience FROM player ORDER BY experience DESC").fetchall()
#             kekka = {}
#             rongaina = []
#             rongai = conn.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
#             for a in rongai:
#                 rongaina.append(a[0])
#             for players in playerlist:
#                 p = bot.get_user(int(players[0]))  # ユーザーID
#                 if not p: continue
#                 user = p
#                 if not user.id in kekka:
#                     for r in rongaina:
#                         if user.id == r:
#                             kekka[user.id] = [user.name, int(math.sqrt(players[1]))]
#                 if len(kekka) > 99: break
#             players_rank = "\n".join("{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
#             # データ10個ごとにページ分け
#             ranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
#             author = "世界Top100論外プレイヤー"
#         if msg_react.content == "1":
#             # BOTはisbotの中身を1で登録してるのでそこで判断して全データを取得させます。
#             playerlist = conn.execute(
#                 "SELECT user_id, experience FROM player WHERE bot=1 ORDER BY experience DESC").fetchall()
#             kekka = {}
#             rongaina = []
#             rongai = conn.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
#             for a in rongai:
#                 rongaina.append(a[0])
#             for players in playerlist:
#                 p = bot.get_user(int(players[0]))  # ユーザーID
#                 if not p: continue
#                 user = p
#                 if not user.id in kekka:
#                     if user.id in rongaina:
#                         kekka[user.id] = [user.name, int(math.sqrt(players[1]))]
#                 if len(kekka) > 99: break
#             players_rank = "\n".join("{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
#             # データ10個ごとにページ分け
#             ranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
#             author = "世界Top100論外ボット"
#         elif msg_react.content == "2":
#             playerlist = conn.execute("SELECT user_id, count FROM monster_count ORDER BY count DESC").fetchall()
#             isbot = conn.execute("SELECT user_id FROM player WHERE bot=0 ORDER BY user_id").fetchall()
#             all = []
#             kekka = {}
#             rongaina = []
#             rongai = conn.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
#             for a in rongai:
#                 rongaina.append(a[0])
#             for a in isbot:
#                 all.append(a[0])
#             for players in playerlist:
#                 p = bot.get_user(int(players[0]))  # ユーザーID
#                 if not p: continue
#                 user = p
#                 if not user.id in kekka:
#                     if user.id in rongaina:
#                         if user.id in all:
#                             kekka[user.id] = [user.name, int(players[1])]
#                 if len(kekka) > 99: break
#             players_rank = "\n".join("{}位：`{}` ({}体)".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))
#           # データ10個ごとにページ分け
#             ranking_msgs = ["\n".join(players_rank.split("\n")[i:i + 10]) for i in range(0, 100, 10)]
#             author = "倒した数論外プレイヤーTop100"
#
#         if not list(filter(lambda a: a != '', ranking_msgs)):
#             return await ctx.send(embed=Embed(description="まだデータはないようだ..."))
#
#         embeds = []
#         for embed in list(filter(lambda a: a != '', ranking_msgs)):
#             embeds.append(Embed(description=embed, color=0xff0000).set_author(name=author))
#
#         await msg.edit(content=f"```diff\n1ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```", embed=embeds[0])
#         while True: # 処理が終わる(return)まで無限ループ
#             try: # ERRORが起きるか起きないか。起きたらexceptに飛ばされる
#                 msg_react = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.content.isdigit() and 0 <= int(m.content) <= len(embeds), timeout=30)
#               # await bot.wait_for('message')で返ってくるのは文字列型
#                 if msg_react.content == "0":
#                   # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
#                     return await msg.edit(content="‌")
#                 await msg.edit(content=f"```diff\n{int(msg_react.content)}ページ/{len(embeds)}ページ目を表示中\n見たいページを発言してください。\n30秒経ったら処理は止まります。\n0と発言したら強制的に処理は止まります。```", embed=embeds[int(msg_react.content)-1])
#             except asyncio.TimeoutError: # wait_forの時間制限を超過した場合
#               # このcontentの中にはゼロ幅スペースが入っています。Noneでもいいのですが編集者はこっちの方が分かりやすいからこうしています。
#                 return await msg.edit(content="‌", embed=Embed(title=f"時間切れです..."))
#
#     except (NotFound, asyncio.TimeoutError, Forbidden): # 編集した際に文字が見つからなかった, wait_forの時間制限を超過した場合, メッセージに接続できなかった
#         return


@bot.command(name='help', pass_context=True, description='helpを表示')
async def help(ctx):
    embed = discord.Embed(
        title="MMO Second(仮)の遊び方",
        description=f"[このBOTの招待](<https://discordapp.com/api/oauth2/authorize?client_id=606313830288588811&permissions=904257&scope=bot>) ,[このBOTの公式サーバー](<https://discord.gg/vfCXj33>)\n現在**{len(bot.guilds)}**鯖がこのBOTを導入しています\n```\nselfBOTやマクロでのゲームプレイはBAN案件ですのでご了承ください\n```",
        color=0x2ECC69
    )
    embed.set_thumbnail(
        url=bot.user.avatar_url
    )
    embed.add_field(
        name="!!help",
        value="このメッセージを表示します",
        inline=False,
    )
    embed.add_field(
        name="!!attack/atk",
        value="チャンネル上のモンスターに攻撃します",
        inline=False,
    )
    embed.add_field(
        name="!!item/i",
        value="アイテム名/アイテム名の頭文字(e,f,i))**\n**選択したアイテムを使用します [例 ::i f]",
        inline=False,
    )
    embed.add_field(
        name="!!status/st",
        value="自分のステータスを表示します",
        inline=False,
    )
    embed.add_field(
        name="!!reset/re",
        value="バトルをやり直します",
        inline=False,
    )
    embed.add_field(
        name="!!srank",
        value="TOP10サーバーを表示します",
        inline=False,
    )
    embed.add_field(
        name="!!prank",
        value="TOP10プレーヤーを表示します",
        inline=False,
    )
    embed.add_field(
        name="!!t",
        value="4字熟語クイズトレーニングをします",
        inline=False,
    )
    embed.add_field(
        name="!!q",
        value="4択クイズトレーニングをします",
        inline=False,
    )
    embed.add_field(
        name="!!invite/inv",
        value="招待リンクなどを表示します",
        inline=False,
    )
    await ctx.message.channel.send(embed=embed)

@tasks.loop(seconds=1)
async def login_loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M:%S')
    if now == '00:00:00':
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT user_id FROM login ORDER BY user_id").fetchall()
        con.commit()
        kazu = c.fetchall()
        for log in kazu:
            conn.execute(f"DELETE FROM login WHERE user_id={log[0]}")


@bot.command(name="login")
async def login(ctx):
    if ctx.message.author.id in login_zumi:
        embed = Embed(description=f"""{ctx.message.author.mention}さん、\n今日はもうログイン済みです！""")
        await ctx.send(embed=embed)
        return
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute(f"INSERT INTO login values({ctx.message.author.id})")
        con.commit()
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute(f"SELECT count FROM item WHERE user_id={ctx.message.author.id} AND item_id=-9").fetchone()
        con.commit()
        acount = c.fetchone()
        if not acount:
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute(f"INSERT INTO item values({ctx.message.author.id}, -9, 1)")
            con.commit()
            embed = Embed(description=f"""{ctx.message.author.mention}さん、ログインを確認しました。\n現在1日目です！""")
            await ctx.send(embed=embed)
            embedl = discord.Embed(
                description=f"""名前：**{ctx.message.author.name}**\nid:{ctx.message.author.id}\n日数：1日目""")
            await bot.get_channel(713413670239076434).send(embed=embedl)
            return
        else:
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute(f"SELECT count FROM item WHERE user_id={ctx.message.author.id} AND item_id=-9").fetchone()
            con.commit()
            bcount = c.fetchone()
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute(f"UPDATE item SET count={bcount[0] + 1} WHERE user_id={ctx.message.author.id} AND item_id=-9")
            con.commit()
            embed = Embed(description=f"""{ctx.message.author.mention}さん、ログインを確認しました。\n現在{bcount[0] + 1}日目です！""")
            await ctx.send(embed=embed)
            embedl = discord.Embed(
                description=f"""名前：**{ctx.message.author.name}**\nid:{ctx.message.author.id}\n日数：{bcount[0] + 1}日目""")
            await bot.get_channel(713413670239076434).send(embed=embedl)
            return



@bot.command(name='invite', aliases=['inv'], pass_context=True, description='このBOTの導入方法')
async def invite(ctx):
    """このbotの導入方法を表示します"""
    up = discord.Color(random.randint(0, 0xFFFFFF))
    embed = discord.Embed(title="このBOTの導入",
                          description=f"[このBOTの招待](<https://discordapp.com/api/oauth2/authorize?client_id=606313830288588811&permissions=904257&scope=bot>) ,[このBOTの公式サーバー](<https://discord.gg/vfCXj33>)\n現在**{len(bot.guilds)}**鯖がこのBOTを導入しています",
                          color=up)
    return await ctx.send(embed=embed)


@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(671318322394169345)
    up = discord.Color(random.randint(0, 0xFFFFFF))
    embed = discord.Embed(title="追放されたログ",
                          description=f"鯖名：{guild.name}\nID：{guild.id}\n鯖Owner：{guild.owner}\n鯖",
                          color=up)
    await channel.send(embed=embed)
    await bot.change_presence(activity=discord.Game(name="!!help ｜{}鯖".format(len(bot.guilds))))


@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(671317297318854668)
    up = discord.Color(random.randint(0, 0xFFFFFF))
    embed = discord.Embed(title="導入ログ",
                          description=f"鯖名：{guild.name}\nID：{guild.id}\n鯖Owner：{guild.owner}\n鯖",
                          color=up)
    await channel.send(embed=embed)
    await bot.change_presence(activity=discord.Game(name="!!help ｜{}鯖".format(len(bot.guilds))))


channel_in_transaction = []
special_monster = {}
very_special_monster = {}
kyou_teki = {}
tyoukyou_teki = {}

counts = 0

no = '👎'
ok = '👍'
left = '⏪'
right = '⏩'
counts = 0


# def insert_returns(body):
#     # insert return stmt if the last expression is a expression statement
#     if isinstance(body[-1], ast.Expr):
#         body[-1] = ast.Return(body[-1].value)
#         ast.fix_missing_locations(body[-1])
#
#     # for if statements, we insert returns into the body and the orelse
#     if isinstance(body[-1], ast.If):
#         insert_returns(body[-1].body)
#         insert_returns(body[-1].orelse)
#
#     # for with blocks, again we insert returns into the body
#     if isinstance(body[-1], ast.With):
#         insert_returns(body[-1].body)
#
#
# @bot.command(name='eval')
# async def eval_fn(ctx, *, cmd):
#     fn_name = "_eval_expr"
#
#     cmd = cmd.strip("` ")
#     cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
#     body = f"async def {fn_name}():\n{cmd}"
#
#     parsed = ast.parse(body)
#     body = parsed.body[0].body
#
#     insert_returns(body)
#
#     env = {
#         'bot': ctx.bot,
#         'discord': discord,
#         'commands': commands,
#         'ctx': ctx,
#         '__import__': __import__
#     }
#     exec(compile(parsed, filename="<ast>", mode="exec"), env)
#
#     result = (await eval(f"{fn_name}()", env))
#     await ctx.send(result)

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@bot.command(name='eval')
async def eval_fn(ctx, *, cmd):
    if ctx.message.author.id == 421971957081309194 or ctx.message.author.id == 673421485003636747 or ctx.message.author.id == 586157827400400907:
        if ctx.author.id == 673421485003636747 or ctx.message.author.id == 586157827400400907:
            if ".delete(" in cmd or ".ban(" in cmd or ".kick(" in cmd or "token" in cmd or "os." in cmd or "conn" in cmd or "json" in cmd:
                await ctx.send("危険なコードを仕込むんなねぇ！！")
                if ctx.message is not None: return await ctx.message.add_reaction("‼")
            else:
                try:
                    if ctx.message: await ctx.message.add_reaction("<:owo1:668823024195207198>")
                    await ctx.send(f"<@{ctx.message.author.id}> によるevalです！")
                    if cmd.startswith("```py"):
                        cmd = f"{cmd}"[5:][:-3]
                    elif cmd.startswith("```"):
                        cmd = f"{cmd}"[3:][:-3]
                    fn_name = "_eval_expr"
                    cmd = cmd.strip("` ")
                    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
                    body = f"async def {fn_name}():\n{cmd}"
                    parsed = ast.parse(body)
                    env = {
                        'bot': ctx.bot,
                        'discord': discord,
                        'asyncio': asyncio, 'random': random, 'datetime': datetime, 're': re,
                        'commands': commands,
                        'ctx': ctx,
                        'json': json,
                        'sqlite3': sqlite3,
                        'os': os,
                        'conn': sqlite3.connect("mmo.db"),
                        '__import__': __import__
                    }
                    exec(compile(parsed, filename="<ast>", mode="exec"), env)
                    await eval(f"{fn_name}()", env)
                    if ctx.message is not None:
                        await ctx.message.remove_reaction("<:owo1:668823024195207198>", ctx.guild.me)
                        await ctx.message.add_reaction("✅")
                except Exception as e:
                    await ctx.send([e])
                    if ctx.message is not None:
                        await ctx.message.remove_reaction("<:owo1:668823024195207198>", ctx.guild.me)
                        await ctx.message.add_reaction("‼")
        else:
            try:
                if ctx.message: await ctx.message.add_reaction("<:owo1:668823024195207198>")
                if cmd.startswith("```py"):
                    cmd = f"{cmd}"[5:][:-3]
                elif cmd.startswith("```"):
                    cmd = f"{cmd}"[3:][:-3]
                fn_name = "_eval_expr"
                cmd = cmd.strip("` ")
                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
                body = f"async def {fn_name}():\n{cmd}"
                parsed = ast.parse(body)
                env = {
                    'bot': ctx.bot,
                    'discord': discord,
                    'asyncio': asyncio, 'random': random, 'datetime': datetime, 're': re,
                    'commands': commands,
                    'ctx': ctx,
                    'json': json,
                    'sqlite3': sqlite3,
                    'os': os,
                    'conn': sqlite3.connect("mmo.db"),
                    '__import__': __import__
                }
                exec(compile(parsed, filename="<ast>", mode="exec"), env)
                await eval(f"{fn_name}()", env)
                if ctx.message is not None:
                    await ctx.message.remove_reaction("<:owo1:668823024195207198>", ctx.guild.me)
                    await ctx.message.add_reaction("✅")
            except Exception as e:
                await ctx.send([e])
                if ctx.message is not None:
                    await ctx.message.remove_reaction("<:owo1:668823024195207198>", ctx.guild.me)
                    await ctx.message.add_reaction("‼")


@bot.command(name='db')
async def eval_fn(ctx, *, cmd):
    if not ctx.message.author.id == 421971957081309194:
        return
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
    body = f"async def {fn_name}():\n    conn.execute('{cmd}').fetchall()[0]"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'json': json,
        'sqlite3': sqlite3,
        'os': os,
        'datetime': datetime,
        'ctx': ctx,
        'conn': sqlite3.connect("mmo.db"),
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    await ctx.send(result)


# @bot.event
# async def on_command_error(ctx, error):
#     if ctx.channel.permissions_for(ctx.guild.me).send_messages is not False:
#         if isinstance(error, commands.CommandNotFound):
#             return
#         elif isinstance(error, commands.CommandInvokeError):
#             if not ctx.author.id == 421971957081309194:
#                 embed = discord.Embed(description="エラーが出ました", color=0xe74c3c)
#                 await ctx.send(embed=embed)
#             elif ctx.author.id == 421971957081309194:
#                 embeder = discord.Embed(description=f"エラーが出ました\n```py\n{error}```", color=0xe74c3c)
#                 await ctx.send(embed=embeder)
#     _channel = bot.get_channel(689852184958861347)
#     embed = discord.Embed(
#         description=f"```py\n{error}```\n`{ctx.message.content}`\n\n`{ctx.guild.name}`の<#{ctx.message.channel.id}>(`{ctx.message.channel.name}`)",
#         color=0xe74c3c)
#     await _channel.send(embed=embed)


@bot.event
async def on_command(ctx):
    if ctx.message.author.id == 673421485003636747:
        if "!!eval" in ctx.message.content:
            embed = discord.Embed(
                description=f"{ctx.message.content} guild: {ctx.message.guild.name} in: <#{ctx.message.channel.id}> ")
            await bot.get_channel(690605523824934963).send(embed=embed)
            return
    #
    # embed = discord.Embed(
    #     description=f"{ctx.message.content} guild: {ctx.message.guild.name} in: <#{ctx.message.channel.id}>  `{ctx.message.channel.name}`")
    # return await bot.get_channel(690086615447502868).send(embed=embed)


# @bot.event
# async def on_command(ctx):
#     if ctx.message.author.id == 453874448035086337:
#     embed = discord.Embed(description=ctx.message.content)
#     embed.set_author(icon_url=ctx.author.avatar_url_as(format="png"),name=str(ctx.author))
#     embed.set_footer(icon_url=ctx.guild.icon_url_as(format="png"), text=f"{ctx.guild.name}[{ctx.channel.name}]")
#     await bot.get_channel(690086615447502868).send(embed=embed)

# @bot.command(name="sinfo")
# async def sinfo(ctx):


@bot.command(name='attack', aliases=['atk'], pass_context=True, description='チャンネル内の敵に攻撃します。敵の反撃を受けます。')
async def attack(ctx):
    """攻撃する"""
    channel_id = ctx.message.channel.id
    # if channel_id in channel_in_transaction:
    #     return  # await ctx.send("`攻撃失敗。ゆっくりコマンドを打ってね。`")
    # try:
    #     channel_in_transaction.append(channel_id)
    await _attack(ctx, ctx.message.author.id, channel_id)
    conn.commit()
    # finally:
    #     channel_in_transaction.remove(channel_id)


async def _attack(ctx, user_id, channel_id):
    player_hp, error_message = into_battle(ctx, user_id, channel_id)
    embed = discord.Embed(description=error_message,
                          color=0xff0000)
    if error_message: return await ctx.send(embed=embed)
    player_level = get_player_level(ctx, user_id)
    boss_level, boss_hp = get_boss_level_and_hp(channel_id)
    rand = random.random()
    player_attack = get_player_attack(player_level, boss_level, rand)
    boss_hp = boss_hp - player_attack
    if channel_id in special_monster:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT monster FROM channel_status WHERE channel_id=?", (channel_id,)).fetchone()
        con.commit()
        monster_num = c.fetchone()
        monster_name = rea[monster_num[0]]["name"]
    elif channel_id in very_special_monster:
        monster_name = tyougekirea[0]["name"]
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT monster FROM channel_status WHERE channel_id=?", (channel_id,)).fetchone()
        con.commit()
        monster_num = c.fetchone()
        monster_name = monsters[monster_num[0]]["name"]
        if boss_level % MONSTER_NUM == 0:
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster_num = c.fetchone()
            monster_name = tyoukyouteki[monster_num[0]]["name"]
        elif boss_level % 5 == 0:
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster_num = c.fetchone()
            monster_name = kyouteki[monster_num[0]]["name"]
    attack_message = get_attack_message(user_id, player_attack, monster_name, rand)
    if boss_hp <= 0:
        win_message = win_process(ctx, channel_id, boss_level, monster_name)
        up = discord.Color(random.randint(0, 0xFFFFFF))
        embedwin = discord.Embed(
            title="戦闘結果",
            description=f"{win_message}",
            color=up,
        )
        atk_msg = f"```diff\n{attack_message}```"
        await ctx.send(atk_msg, embed=embedwin)
        await reset_battle(ctx, channel_id, level_up=True)
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE channel_status SET boss_hp=? WHERE channel_id=?", (boss_hp, channel_id,))
        con.commit()
        boss_attack_message = boss_attack_process(user_id, player_hp, player_level, monster_name, boss_level,
                                                  channel_id)
        attack_messagee = f"{attack_message}\n- {monster_name}のHP:{boss_hp}/{boss_level * 10 + 50}\n\n{boss_attack_message}"
        up = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(description=f"```diff\n{attack_messagee}```",
                              color=0x36393f)
        await ctx.send(embed=embed)


def into_battle(ctx, user_id, channel_id):
    error_message = ""
    player_level = get_player_level(ctx, user_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT channel_id, player_hp FROM in_battle WHERE user_id=?", (user_id,)).fetchone()
    con.commit()
    in_battle = c.fetchone()
    if not in_battle:
        player_hp = player_level * 5 + 50  # player_max_hp
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("INSERT INTO in_battle values(?,?,?)", (channel_id, user_id, player_hp))
        con.commit()
        return player_hp, error_message
    in_battle_channel_id = in_battle[0]
    battle_channel = bot.get_channel(in_battle_channel_id)
    if not battle_channel:  # if deleted the battle_channel
        player_hp = player_level * 5 + 50
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("DELETE FROM in_battle WHERE channel_id=?", (in_battle_channel_id,))
        con.commit()
        player_hp = player_level * 5 + 50
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("INSERT INTO in_battle values(?,?,?)", (channel_id, user_id, player_hp))
        con.commit()
        return player_hp, error_message
    player_hp = in_battle[1]
    if in_battle_channel_id != channel_id:
        battle_field2 = f"どこかの鯖の<#{in_battle_channel_id}>"
        error_message = "<@{}>は'{}'で既に戦闘中だ。".format(user_id, battle_field2)
    elif player_hp == 0:
        error_message = "<@{}>はもうやられている！（戦いをやり直すには「!!reset」だ）".format(user_id, )
    return player_hp, error_message


def get_attack_message(user_id, player_attack, monster_name, rand):
    if player_attack == 0:
        user_name = bot.get_user(user_id).name
        return f"! {user_name}>の攻撃！{monster_name}にかわされてしまった...！！"
    else:
        kaishin = "会心の一撃！" if rand > 0.96 else ""
        user_name = bot.get_user(user_id).name
        return f"+ {user_name}の攻撃！{kaishin}{monster_name}に{player_attack}のダメージを与えた！"


def win_process(ctx, channel_id, boss_level, monster_name):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT * FROM in_battle WHERE channel_id=?", (channel_id,)).fetchall()
    con.commit()
    mem = c.fetchall()
    battle_members = [m for m in mem()]
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT user_id FROM in_battle WHERE channel_id=?", (channel_id,)).fetchall()
    con.commit()
    count_battle_members = c.fetchall()
    for m in count_battle_members:
        m = m[0]
        monster_count(m)
    level_up_comments = []
    members = ""
    a_members = ""
    b_members = ""
    c_members = ""
    d_members = ""
    e_members = ""
    r_members = ""
    fire_members = ""
    elixir_members = ""
    pray_members = ""
    is_cicero = channel_id in special_monster
    is_gekirea = channel_id in very_special_monster
    if is_cicero or boss_level % MONSTER_NUM == 0:
        exp = boss_level * 9
    elif is_gekirea:
        exp = boss_level * 150
    elif boss_level % 5 == 0:
        if boss_level % 5 == 0:
            exp = boss_level * 4
    else:
        exp = boss_level
    if is_gekirea:
        for battle_member in battle_members:
            member_id = battle_member[1]
            a = 5
            b = 3
            c = 2.5
            d = 2
            e = 1.5
            r = 100
            if rongai_check(member_id):
                level_up_comments.append(experiment(ctx, member_id, exp * r))
                r_members += "<@{}> ".format(member_id)
            if get_player_level(ctx, member_id) > 10000 or get_player_level(ctx, member_id) == 10000:
                level_up_comments.append(experiment(ctx, member_id, exp))
                members += "<@{}> ".format(member_id)
            if get_player_level(ctx, member_id) > 8000 and get_player_level(ctx, member_id) < 10000 or get_player_level(ctx,
                    member_id) == 8000:
                level_up_comments.append(experiment(ctx, member_id, exp * e))
                e_members += "<@{}> ".format(member_id)
            elif get_player_level(ctx, member_id) > 6000 and get_player_level(ctx, member_id) < 8000 or get_player_level(ctx,
                    member_id) == 6000:
                level_up_comments.append(experiment(ctx, member_id, exp * d))
                d_members += "<@{}> ".format(member_id)
            elif get_player_level(ctx, member_id) > 4000 and get_player_level(ctx, member_id) < 6000 or get_player_level(ctx,
                    member_id) == 4000:

                level_up_comments.append(experiment(ctx, member_id, exp * c))
                c_members += "<@{}> ".format(member_id)
            elif get_player_level(ctx, member_id) > 2000 and get_player_level(ctx, member_id) < 4000 or get_player_level(ctx,
                    member_id) == 2000:

                level_up_comments.append(experiment(ctx, member_id, exp * b))
                b_members += "<@{}> ".format(member_id)
            elif get_player_level(ctx, member_id) < 2000:
                level_up_comments.append(experiment(ctx, member_id, exp * a))
                a_members += "<@{}> ".format(member_id)
            if is_gekirea:
                elixir_members += "<@{}> ".format(member_id)
                e_obtain_an_item(member_id)
            if is_gekirea:
                fire_members += "<@{}> ".format(member_id)
                fbi_obtain_an_item(member_id, 2)
            if is_gekirea:
                pray_members += "<@{}> ".format(member_id)
                fbi_obtain_an_item(member_id, 3)
        if fire_members:
            fire_members += "は`ファイアボールの書`を100個手に入れた！"
        if elixir_members:
            elixir_members += "は`エリクサー`を手10個に入れた！"
        if pray_members:
            pray_members += "は`祈りの書`を100個手に入れた！"
        if members:
            members += f"は`{exp}`の経験値を得た"
        if a_members:
            a_members += f"は`{exp * a}`の経験値を得た"
        if b_members:
            b_members += f"は`{exp * b}`の経験値を得た"
        if c_members:
            c_members += f"は`{exp * c}`の経験値を得た"
        if d_members:
            d_members += f"は`{exp * d}`の経験値を得た"
        if e_members:
            e_members += f"は`{exp * e}`の経験値を得た"
        if r_members:
            r_members += f"は`{exp * r}`の経験値を得た"
        level_up_comment = "\n".join([y for y in level_up_comments if y])
        item_get = "\n".join(x for x in [elixir_members, fire_members, pray_members] if x)
        member = "\n".join(z for z in [members, a_members, b_members, c_members, d_members, e_members, r_members] if z)
        kekka = "{0}を倒した！\n\n{1}\n{2}\n{3}".format(monster_name, member, level_up_comment,
                                                   item_get)
        return (kekka)
    else:
        for battle_member in battle_members:
            member_id = battle_member[1]
            a = 5
            b = 3
            c = 2.5
            d = 2
            e = 1.5
            r = 100
            rongaina = {}
            rongai = conn.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
            for u in rongai:
                if member_id == u[0]:
                    rongaina[member_id] = [u[0]]
            if member_id in rongaina:
                level_up_comments.append(experiment(ctx, member_id, exp * r))
                r_members += "<@{}> ".format(member_id)
            else:
                if get_player_level(ctx, member_id) > 10000 or get_player_level(ctx, member_id) == 10000:
                    level_up_comments.append(experiment(ctx, member_id, exp))
                    members += "<@{}> ".format(member_id)
                if get_player_level(ctx, member_id) > 8000 and get_player_level(ctx, member_id) < 10000 or get_player_level(ctx,
                        member_id) == 8000:
                    level_up_comments.append(experiment(ctx, member_id, exp * e))
                    e_members += "<@{}> ".format(member_id)
                elif get_player_level(ctx, member_id) > 6000 and get_player_level(ctx, member_id) < 8000 or get_player_level(ctx,
                        member_id) == 6000:
                    level_up_comments.append(experiment(ctx, member_id, exp * d))
                    d_members += "<@{}> ".format(member_id)
                elif get_player_level(ctx, member_id) > 4000 and get_player_level(ctx, member_id) < 6000 or get_player_level(ctx,
                        member_id) == 4000:
                    level_up_comments.append(experiment(ctx, member_id, exp * c))
                    c_members += "<@{}> ".format(member_id)
                elif get_player_level(ctx, member_id) > 2000 and get_player_level(ctx, member_id) < 4000 or get_player_level(ctx,
                        member_id) == 2000:
                    level_up_comments.append(experiment(ctx, member_id, exp * b))
                    b_members += "<@{}> ".format(member_id)
                elif get_player_level(ctx, member_id) < 2000:
                    level_up_comments.append(experiment(ctx, member_id, exp * a))
                    a_members += "<@{}> ".format(member_id)
            p = min(0.02 * boss_level * boss_level / get_player_exp(ctx, member_id), 0.1)
            if boss_level % 50 == 0 or is_cicero:
                if not is_gekirea:
                    elixir_members += "<@{}> ".format(member_id)
                    obtain_an_item(member_id, 1)
            if random.random() < p or is_cicero:
                if not is_gekirea:
                    fire_members += "<@{}> ".format(member_id)
                    obtain_an_item(member_id, 2)
            if random.random() < p * 2 or is_cicero:
                if not is_gekirea:
                    pray_members += "<@{}> ".format(member_id)
                    obtain_an_item(member_id, 3)
        if fire_members:
            fire_members += "は`ファイアボールの書`を手に入れた！"
        if elixir_members:
            elixir_members += "は`エリクサー`を手に入れた！"
        if pray_members:
            pray_members += "は`祈りの書`を手に入れた！"
        if members:
            members += f"は`{exp}`の経験値を得た"
        if a_members:
            a_members += f"は`{exp * a}`の経験値を得た"
        if b_members:
            b_members += f"は`{exp * b}`の経験値を得た"
        if c_members:
            c_members += f"は`{exp * c}`の経験値を得た"
        if d_members:
            d_members += f"は`{exp * d}`の経験値を得た"
        if e_members:
            e_members += f"は`{exp * e}`の経験値を得た"
        if r_members:
            r_members += f"は`{exp * r}`の経験値を得た"
        level_up_comment = "\n".join([y for y in level_up_comments if y])
        item_get = "\n".join(x for x in [elixir_members, fire_members, pray_members] if x)
        member = "\n".join(z for z in [members, a_members, b_members, c_members, d_members, e_members, r_members] if z)
        kekka = "{0}を倒した！\n\n{1}\n{2}\n{3}".format(monster_name, member, level_up_comment,
                                                   item_get)
        return (kekka)


def rongai_check(user_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
    con.commit()
    rongai = c.fetchall()
    for a in rongai:
        if user_id == a[0]:
            break
            return True
        else:
            break
            return False


def boss_attack_process(user_id, player_hp, player_level, monster_name, boss_level, channel_id):
    boss_attack = get_boss_attack(boss_level)
    player_hp = player_hp - boss_attack
    if boss_attack == 0:
        user_name = bot.get_user(user_id).name
        return "! {0}の攻撃！{1}は華麗にかわした！\n- <@{1}>のHP:{2}/{3}".format(
            monster_name, user_name, player_hp, player_level * 5 + 50)
    elif player_hp <= 0:
        user_name = bot.get_user(user_id).name
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE in_battle SET player_hp=0 WHERE user_id=?", (user_id,))
        con.commit()
        return "+ {0}の攻撃！{1}は{2}のダメージを受けた。\n- {1}のHP:0/{3}\n- {1}はやられてしまった。。。".format(
            monster_name, user_name, boss_attack, player_level * 5 + 50)
    else:
        user_name = bot.get_user(user_id).name
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE in_battle SET player_hp=? WHERE user_id=?", (player_hp, user_id,))
        con.commit()
        return "+ {0}の攻撃！{1}は{2}のダメージを受けた。\n- {1}のHP:{3}/{4}".format(
            monster_name, user_name, boss_attack, player_hp, player_level * 5 + 50)


def get_player_attack(player_level, boss_level, rand):
    if boss_level % MONSTER_NUM in [20, 40, 49] and rand < 0.1:
        player_attack = 0
    elif boss_level % MONSTER_NUM in [2, 7, 13, 23, 34] and rand < 0.05:
        player_attack = 0
    elif rand < 0.01:
        player_attack = 0
    elif boss_level % MONSTER_NUM in [3, 11, 17, 32, 41]:
        plus = rand / 3 + 0.5 if rand < 0.96 else 3
        player_attack = int(player_level * plus + 10)
    elif boss_level % 5 == 0:
        plus = rand / 2 + 0.8 if rand < 0.96 else 3
        player_attack = int(player_level * plus + 10)
    else:
        plus = rand / 2 + 1 if rand < 0.96 else 3
        player_attack = int(player_level * plus + 10)
    return player_attack


def get_boss_attack(boss_level):
    if random.random() < 0.01:
        return 0
    if boss_level % 50 == 0:
        return int(boss_level * random.random() * 256)
    elif boss_level % 50 in [37, 46, 47, 48]:
        return int(boss_level * random.random())
    elif boss_level % 5 == 0:
        return int(boss_level * (1 + random.random()) * 3)
    else:
        return int(boss_level * (2 + random.random()) + 5)


@bot.command(name='status', aliases=['st'], pass_context=True, description='自分のステータスを確認する')
async def status(ctx, id=""):
    """自分のステータスを確認する"""
    # author_name = bot.get_user(ctx.message.author.id)
    # embed = discord.Embed(
    #     description=f"""```コマンド:[!!status]\n発言鯖:{ctx.message.guild.name} | チャンネル名:{ctx.message.channel.name}\n発言者:{author_name} | ID:{ctx.message.id}```""",
    #     color=0x1d1d1d)
    # channel = bot.get_channel(661122218847109130)
    # await channel.send(embed=embed)
    if id == "":
        user_id = ctx.message.author.id
        player_exp = get_player_exp(ctx, user_id)
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT channel_id, player_hp FROM in_battle WHERE user_id=?", (user_id,)).fetchone()
        con.commit()
        in_battle = c.fetchone()
        item_comment = ""
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("select count(*) from item where item_id=-10").fetchone()
        con.commit()
        kazu = c.fetchone()[0]
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT item_id FROM item WHERE user_id=?", (user_id,)).fetchall()
        con.commit()
        aaa = c.fetchall()
        for my_item in aaa:
            if my_item[0] == -10:
                item_comment += "【論外の証】を持っている。\n"
            if my_item[0] == -9:
                item_comment += "【サポーターの証】を持っている。\n"
        player_level = int(math.sqrt(player_exp))
        # monster_countt = conn.execute(f"SELECT count FROM monster_count WHERE user_id={ctx.message.author.id}").fetchall()[0]
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT item_id, count FROM item WHERE user_id=? ORDER BY item_id",
                                (ctx.message.author.id,)).fetchall()
        con.commit()
        my_items = c.fetchall()
        item_list = "\n".join("{} : {}個".format(items[i[0]], i[1]) for i in my_items)
        if item_list:
            item_list = "\n".join("{} : {}個".format(items[i[0]], i[1]) for i in my_items)
        else:
            item_list = "アイテムを持ってない！"
        status_comment = f"<@{user_id}>のステータス\nLv: {player_level}\nHP: {player_level * 5 + 50} \n攻撃力: {player_level * 2 + 10}\nEXP: {player_exp}\n次のレベルまで {(player_level + 1) ** 2 - player_exp}exp\n{item_comment}\nプレイヤーランクは{rank}位だ！"
        embed = discord.Embed(
            title=f"{bot.get_user(ctx.message.author.id).name}のステータス:",
        )
        embed.set_thumbnail(
            url=ctx.author.avatar_url
        )
        embed.add_field(
            name="Lv",
            value=f"{player_level}"
        )
        embed.add_field(
            name="HP",
            value=f"{player_level * 5 + 50}"
        )
        embed.add_field(
            name="攻撃力",
            value=f"{player_level * 2 + 10}"
        )
        embed.add_field(
            name="EXP",
            value=f"{player_exp}"
        )
        embed.add_field(
            name="次のレベルまで",
            value=f"{(player_level + 1) ** 2 - player_exp}exp"
        )
        embed.add_field(
            name="所持アイテム",
            value=f"{item_list}"
        )
        embed.add_field(
            name="敵を倒した数",
            value=f"{monster_hyouzi(ctx.message.author.id)}体"
        )
        embed.add_field(
            name="プレーヤーランク",
            value=f"{rank(user_id)}位"
        )
        if in_battle:
            battle_channel = bot.get_channel(in_battle[0])
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("select count(*) from item where item_id=-10").fetchone()
            con.commit()
            kazu = c.fetchone()[0]
            if not battle_channel:  # if deleted the battle_channel
                con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                c = con.cursor()
                c.execute("DELETE FROM in_battle WHERE channel_id=?", (in_battle[0]), )
                con.commit()
            else:
                con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                c = con.cursor()
                c.execute("SELECT channel_id FROM in_battle WHERE user_id=?", (user_id,)).fetchone()
                con.commit()
                in_battle = c.fetchone()
                in_battle_channel_id = in_battle[0]
                battle_field = f"どこかの鯖の<#{in_battle_channel_id}>"
                # status_comment = "<@{}>のステータス\nLv: {}\nHP: {} / {}\n攻撃力: {}\nEXP: {}\n次のレベルまで {}exp\n\n{}で戦闘中！\n{}\nプレイヤーランクは{}位だ！".format(
                #     user_id, player_level, in_battle[1], player_level * 5 + 50, player_level * 2 + 10,
                #     player_exp, (player_level + 1) ** 2 - player_exp, battle_field, item_comment, rank
                # )
                embed = discord.Embed(
                    title=f"{bot.get_user(ctx.message.author.id).name}のステータス:",
                )
                embed.set_thumbnail(
                    url=ctx.author.avatar_url
                )
                embed.add_field(
                    name="Lv",
                    value=f"{player_level}"
                )
                embed.add_field(
                    name="HP",
                    value=f"{player_level * 5 + 50}"
                )
                embed.add_field(
                    name="攻撃力",
                    value=f"{player_level * 2 + 10}"
                )
                embed.add_field(
                    name="EXP",
                    value=f"{player_exp}"
                )
                embed.add_field(
                    name="次のレベルまで",
                    value=f"{(player_level + 1) ** 2 - player_exp}exp"
                )
                embed.add_field(
                    name="所持アイテム",
                    value=f"{item_list}"
                )
                embed.add_field(
                    name="敵を倒した数",
                    value=f"{monster_hyouzi(ctx.message.author.id)}体"
                )
                embed.add_field(
                    name="プレーヤーランク",
                    value=f"{rank(user_id)}位"
                )
                embed.add_field(
                    name="戦闘場所",
                    value=f"errorなので待って"
                )
        await ctx.send(embed=embed)

    if ctx.message.author.id == 421971957081309194:
        if id:
            user_id = int(id)
            player_exp = get_player_exp(ctx, user_id)
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT channel_id, player_hp FROM in_battle WHERE user_id=?",
                                     (user_id,)).fetchone()
            con.commit()
            in_battle = c.fetchone()
            item_comment = ""
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("select count(*) from item where item_id=-10").fetchone()
            con.commit()
            kazu = c.fetchone()
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT item_id FROM item WHERE user_id=?", (user_id,)).fetchall()
            con.commit()
            aaa = c.fetchall()
            for my_item in aaa:
                if my_item[0] == -10:
                    item_comment += "【論外の証】を持っている。\n"
                if my_item[0] == -9:
                    item_comment += "【サポーターの証】を持っている。\n"
            player_level = int(math.sqrt(player_exp))
            # monster_countt = conn.execute(f"SELECT count FROM monster_count WHERE user_id={ctx.message.author.id}").fetchall()[0]
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT item_id, count FROM item WHERE user_id=? ORDER BY item_id",
                      (ctx.message.author.id,)).fetchall()
            con.commit()
            my_items = c.fetchall()
            item_list = "\n".join("{} : {}個".format(items[i[0]], i[1]) for i in my_items)
            if item_list:
                item_list = "\n".join("{} : {}個".format(items[i[0]], i[1]) for i in my_items)
            else:
                item_list = "アイテムを持ってない！"
            status_comment = f"<@{user_id}>のステータス\nLv: {player_level}\nHP: {player_level * 5 + 50} \n攻撃力: {player_level * 2 + 10}\nEXP: {player_exp}\n次のレベルまで {(player_level + 1) ** 2 - player_exp}exp\n{item_comment}\nプレイヤーランクは{rank}位だ！"
            embed = discord.Embed(
                title=f"{bot.get_user(user_id).name}のステータス:",
            )
            embed.set_thumbnail(
                url=bot.get_user(user_id).avatar_url
            )
            embed.add_field(
                name="Lv",
                value=f"{player_level}"
            )
            embed.add_field(
                name="HP",
                value=f"{player_level * 5 + 50}"
            )
            embed.add_field(
                name="攻撃力",
                value=f"{player_level * 2 + 10}"
            )
            embed.add_field(
                name="EXP",
                value=f"{player_exp}"
            )
            embed.add_field(
                name="次のレベルまで",
                value=f"{(player_level + 1) ** 2 - player_exp}exp"
            )
            embed.add_field(
                name="所持アイテム",
                value=f"{item_list}"
            )
            embed.add_field(
                name="敵を倒した数",
                value=f"{monster_hyouzi(int(id))}体"
            )
            embed.add_field(
                name="プレーヤーランク",
                value=f"{rank(user_id)}位"
            )
            if in_battle:
                battle_channel = bot.get_channel(in_battle[0])
                con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                c = con.cursor()
                c.execute("select count(*) from item where item_id=-10").fetchone()
                con.commit()
                kazu = c.fetchone()[0]
                if not battle_channel:  # if deleted the battle_channel
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("DELETE FROM in_battle WHERE channel_id=?", (in_battle[0]), )
                    con.commit()
                else:
                    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
                    c = con.cursor()
                    c.execute("SELECT channel_id FROM in_battle WHERE user_id=?", (user_id,)).fetchone()
                    con.commit()
                    in_battle = c.fetchall()
                    in_battle_channel_id = in_battle[0]
                    battle_field = f"どこかの鯖の<#{in_battle_channel_id}>"
                    # status_comment = "<@{}>のステータス\nLv: {}\nHP: {} / {}\n攻撃力: {}\nEXP: {}\n次のレベルまで {}exp\n\n{}で戦闘中！\n{}\nプレイヤーランクは{}位だ！".format(
                    #     user_id, player_level, in_battle[1], player_level * 5 + 50, player_level * 2 + 10,
                    #     player_exp, (player_level + 1) ** 2 - player_exp, battle_field, item_comment, rank
                    # )
                    embed = discord.Embed(
                        title=f"{bot.get_user(int(id)).name}のステータス:",
                    )
                    embed.set_thumbnail(
                        url=bot.get_user(int(id)).avatar_url
                    )
                    embed.add_field(
                        name="Lv",
                        value=f"{player_level}"
                    )
                    embed.add_field(
                        name="HP",
                        value=f"{player_level * 5 + 50}"
                    )
                    embed.add_field(
                        name="攻撃力",
                        value=f"{player_level * 2 + 10}"
                    )
                    embed.add_field(
                        name="EXP",
                        value=f"{player_exp}"
                    )
                    embed.add_field(
                        name="次のレベルまで",
                        value=f"{(player_level + 1) ** 2 - player_exp}exp"
                    )
                    embed.add_field(
                        name="所持アイテム",
                        value=f"{item_list}"
                    )
                    embed.add_field(
                        name="敵を倒した数",
                        value=f"{monster_hyouzi(int(id))}体"
                    )
                    embed.add_field(
                        name="プレーヤーランク",
                        value=f"{rank(user_id)}位"
                    )
                    embed.add_field(
                        name="戦闘場所",
                        value=f"errorなので待って"
                    )
            await ctx.send(embed=embed)


def rank(user_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
    con.commit()
    rongailist = c.fetchall()
    for a in rongailist:
        if user_id == a[0]:
            print(bot.get_user(user_id))
            return "論外に順位はな"
            break
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT user_id, experience FROM player ORDER BY experience DESC").fetchall()
    con.commit()
    playerlist = c.fetchall()
    kekka = {}
    rongaikekka = {}
    rongaina = []
    c = 0
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
    con.commit()
    rongai = c.fetchall()
    for u in rongai:
        rongaina.append(u[0])
    for players in playerlist:
        p = bot.get_user(int(players[0]))  # ユーザーID
        if not p: continue
        user = p
        if not user.id in kekka:
            if not user.id in rongaina:
                kekka[user.id] = [c + 1]
                c += 1
    return kekka[user_id][0]


@bot.command(name='inquiry', aliases=['inq'], pass_context=True, description='チャンネルのバトルの状態を確認する')
async def inquiry(ctx):
    """チャンネルのバトルの状態を確認する"""
    # author_name = bot.get_user(ctx.message.author.id)
    # embed = discord.Embed(
    #     description=f"""```コマンド:[!!inquiry]\n発言鯖:{ctx.message.guild.name} | チャンネル名:{ctx.message.channel.name}\n発言者:{author_name} | ID:{ctx.message.id}```""",
    #     color=0x1d1d1d)
    # channel = bot.get_channel(661122218847109130)
    # await channel.send(embed=embed)
    channel_id = ctx.message.channel.id
    boss_level, boss_hp = get_boss_level_and_hp(channel_id)
    if channel_id in special_monster:
        monster = special_monster[channel_id]
    elif channel_id in very_special_monster:
        monster = very_special_monster[channel_id]
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT monster FROM channel_status WHERE channel_id=?", (channel_id,)).fetchone()
        con.commit()
        monster_num = c.fetchone()
        monster = monsters[monster_num[0]]
        if boss_level % MONSTER_NUM == 0:
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster_num = c.fetchone()
            monster = tyoukyouteki[monster_num[0]]
        elif boss_level % 5 == 0:
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster_num = c.fetchone()
            monster = kyouteki[monster_num[0]]
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("""SELECT in_battle.user_id, player.experience, in_battle.player_hp 
    FROM in_battle, player WHERE in_battle.channel_id=? AND player.user_id=in_battle.user_id""",
                              (channel_id,)).fetchall()
    con.commit()
    in_battles = c.fetchall()
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("""SELECT 
        (SELECT Count(0) FROM channel_status WHERE channel_status.boss_level > channel_status1.boss_level) + 1 AS rank 
         FROM channel_status AS channel_status1 WHERE channel_id=?""", (ctx.message.channel.id,)).fetchone()
    con.commit()
    rank = c.fetchone()[0]
    rank_say = 'このチャンネルの世界ランキングは「{}位」だ！'.format(rank)
    if in_battles:
        members = "\n ".join("<@{}> Lv.{} 残りHP: {}".format(
            in_battle[0], int(math.sqrt(in_battle[1])), in_battle[2]) for in_battle in in_battles)
        embed = discord.Embed(
            description="{0}\n\nLv:{1}の{2}と戦闘中だ！\n{2}のHP:{3}/{4}\n\n戦闘中のメンバー:\n{5}".format(
                rank_say, boss_level, monster["name"], boss_hp, boss_level * 10 + 50, members),
            color=0x36393f)
        embed.set_image(url="{}".format(monster["img"]))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            description="{0}\n\nLv: {1}の{2}が待ち構えている。\n{2}のHP:{3}\n".format(
                rank_say, boss_level, monster["name"], boss_level * 10 + 50),
            color=0x36393f)
        embed.set_image(url="{}".format(monster["img"]))
        await ctx.send(embed=embed)


@bot.command(name='reset', aliases=['re'], pass_context=True, description='戦いをやり直す')
async def reset(ctx):
    """戦いをやり直す"""
    if "true" in kidou:
        embed = discord.Embed(description="現在起動中です。しばらくお待ちください。",
                              color=0xff0000)
        return await ctx.send(embed=embed)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT 0 FROM in_battle WHERE channel_id=?", (ctx.message.channel.id,)).fetchone()
    con.commit()
    resee = c.fetchone()
    if resee:
        await reset_battle(ctx, ctx.message.channel.id, False)
    else:
        await ctx.send("このチャンネルでは戦いは行われていないようだ。")


@bot.command(pass_context=True, description='四字熟語の読み方をひらがなで入力し、正解すると経験値がもらえるぞ。')
async def t(ctx):
    """トレーニングをする"""
    if ctx.message.author.id == 279506636828311553:
        return await ctx.send("セルフですよね....?")
    if "true" in kidou:
        embed = discord.Embed(description="現在起動中です。しばらくお待ちください。",
                              color=0xff0000)
        return await ctx.send(embed=embed)
    # author_name = bot.get_user(ctx.message.author.id)
    # embed = discord.Embed(
    #     description=f"""```コマンド:[!!t]\n発言鯖:{ctx.message.guild.name} | チャンネル名:{ctx.message.channel.name}\n発言者:{author_name} | ID:{ctx.message.id}```""",
    #     color=0x1d1d1d)
    # channel = bot.get_channel(661122218847109130)
    # await channel.send(embed=embed)
    user = ctx.message.author
    q_id = random.randint(0, 619)
    await ctx.send("「{}」の読み方をひらがなで答えなさい。".format(training_set[q_id][0]))
    answer = training_set[q_id][1]
    exp = math.ceil(get_player_level(ctx, user.id))

    kaitou = await bot.wait_for('message', timeout=12.0, check=lambda messages: messages.author.id == user.id)
    if kaitou is None:
        await ctx.send('時間切れだ。正解は「{}」だ。'.format(answer))
        return
    if kaitou.content == answer:
        comment = experiment(ctx, user.id, exp * 4)
        if random.random() < 0.005:
            comment += "\n`エリクサー`を手に入れた！"
            obtain_an_item(user.id, 1)
        if random.random() < 0.1:
            comment += "\n`ファイアボールの書`を手に入れた！"
            obtain_an_item(user.id, 2)
        if random.random() < 0.1:
            comment += "\n`祈りの書`を手に入れた！"
            obtain_an_item(user.id, 3)
        conn.commit()
        await ctx.send('正解だ！{}の経験値を得た。\n{}'.format(exp, comment))
    else:
        await ctx.send('残念！正解は「{}」だ。'.format(answer))


@bot.command(pass_context=True, description='クイズに解答し、正解すると経験値がもらえるぞ。')
async def q(ctx):
    """トレーニングをする"""
    embed = discord.Embed(description="クイズのapi死亡のため使用できません")
    return await ctx.send(embed=embed)
    # author_name = bot.get_user(ctx.message.author.id)
    # embed = discord.Embed(
    #     description=f"""```コマンド:[!!q]\n発言鯖:{ctx.message.guild.name} | チャンネル名:{ctx.message.channel.name}\n発言者:{author_name} | ID:{ctx.message.id}```""",
    #     color=0x1d1d1d)
    # channel = bot.get_channel(661122218847109130)
    # await channel.send(embed=embed)
    user = ctx.message.author
    resp = requests.get(url='http://24th.jp/test/quiz/api_quiz.php')
    quiz_xml = ElementTree.fromstring(resp.text.encode('utf-8'))[1]
    quiz_set = [quiz_xml[2].text, quiz_xml[3].text, quiz_xml[4].text, quiz_xml[5].text]
    random.shuffle(quiz_set)
    await ctx.send("Q. {}\n 1. {}\n 2. {}\n 3. {}\n 4. {}".format(quiz_xml[1].text, *quiz_set))
    answer_num = quiz_set.index(quiz_xml[2].text) + 1
    exp = math.ceil(get_player_level(ctx, user.id) / 10)

    guess = await bot.wait_for('message', timeout=12.0, check=lambda messages: messages.author.id == user.id)
    if guess is None:
        await ctx.send('時間切れだ。正解は「{}」だ。'.format(quiz_xml[2].text))
        return
    if guess.content.isdigit() and int(guess.content) == answer_num:
        comment = experiment(user.id, exp * 4)
        if random.random() < 0.07:
            comment += "\n`エリクサー`を手に入れた！"
            obtain_an_item(user.id, 1)
        if random.random() < 0.4:
            comment += "\n`ファイアボールの書`を手に入れた！"
            obtain_an_item(user.id, 2)
        if random.random() < 0.4:
            comment += "\n`祈りの書`を手に入れた！"
            obtain_an_item(user.id, 3)
        conn.commit()
        await ctx.send('正解だ！{}の経験値を得た。\n{}'.format(exp, comment))
    else:
        await ctx.send('残念！正解は「{}」だ。'.format(quiz_xml[2].text))


items = {-10: "論外の証", -9: "loginの証", -8: "古参の証", 1: "エリクサー", 2: "ファイアボールの書", 3: "祈りの書", }
item_description = """アイテムの説明
エリクサー:チャンネルの全員を全回復させる。
ファイアボールの書:遠隔攻撃する。
祈りの書:仲間一人を復活させる。
サポーターの証:MMOくんをサポートしてくれた証だ！
"""


@bot.command(name='exp', aliases=['e'], pass_context=True, description="権限無し人間は使えません(/・ω・)/")
async def exp(ctx, mentions, addexp=''):
    """不正でEXPを付与する　　※権限無し人間は使えません(/・ω・)/"""
    user_id = ctx.message.mentions[0].id
    if ctx.message.author.id == 476567173775753227 or ctx.message.author.id == 421971957081309194:
        player_exp = get_player_exp(user_id)
        current_level = int(math.sqrt(player_exp))
        afterexp = player_exp + int(addexp)
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE player SET experience=? WHERE user_id=?", (afterexp, user_id,))
        con.commit()
        next_exp = afterexp
        if next_exp < (current_level + 1) ** 2:
            next_level = int(math.sqrt(next_exp))
            return await ctx.send("<@{}>は`{}exp`を得た！".format(user_id, addexp, current_level, next_level))
        elif next_exp > (current_level + 1) ** 2:
            next_level = int(math.sqrt(next_exp))
            await ctx.send(
                "<@{}>は`{}exp`を得たそしてレベルアップした！`Lv.{} -> Lv.{}`".format(user_id, addexp, current_level, next_level))
            return


@bot.command(name='item', aliases=['i'], pass_context=True, description=item_description)
async def item(ctx, item_name=""):
    """アイテムを使う"""
    channel_id = ctx.message.channel.id
    # if not ctx.message.author.id == 421971957081309194:
    #     return await ctx.send("超激レアの調整中です。")
    if "true" in kidou:
        embed = discord.Embed(description="現在起動中です。しばらくお待ちください。",
                              color=0xff0000)
        return await ctx.send(embed=embed)
    if channel_id in channel_in_transaction:
        return await ctx.send("`アイテム使用失敗。ゆっくりコマンドを打ってね。`")
    try:
        channel_in_transaction.append(channel_id)
        await _item(ctx, ctx.message.author.id, channel_id, item_name, ctx.message.mentions)
        conn.commit()
    finally:
        channel_in_transaction.remove(channel_id)


async def _item(ctx, user_id, channel_id, item_name, mentions):
    if not item_name:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT item_id, count FROM item WHERE user_id=? ORDER BY item_id",
                                (user_id,)).fetchall()
        con.commit()
        my_items = c.fetchall()
        item_list = "\n".join("{} : {}個".format(items[i[0]], i[1]) for i in my_items)
        user_name = bot.get_user(user_id).name
        up = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(
            title=f"{user_name}が所有するアイテム",
            description=f"{item_list}",
            color=up
        )
        return await ctx.send(embed=embed)
    elif item_name == "エリクサー":
        up = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(
            description=f"{elixir(user_id, channel_id)}",
            color=up
        )
        return await ctx.send(embed=embed)
    elif item_name == "e":
        up = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(
            description=f"{elixir(user_id, channel_id)}",
            color=up
        )
        return await ctx.send(embed=embed)
    elif item_name == "ファイアボールの書":
        return await fireball(ctx, user_id, channel_id)
    elif item_name == "f":
        return await fireball(ctx, user_id, channel_id)
    elif item_name == "祈りの書":
        embed = discord.Embed(
            description=f"{pray(user_id, channel_id, mentions)}",
            color=0xff0000
        )
        return await ctx.send(embed=embed)
    elif item_name == "i":
        embed = discord.Embed(
            description=f"{pray(user_id, channel_id, mentions)}",
            color=0xff0000
        )
        return await ctx.send(embed=embed)


def elixir(user_id, channel_id):
    if not consume_an_item(user_id, 1):
        return "<@{}>はエリクサーを持っていない！".format(user_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "SELECT player.user_id, player.experience FROM in_battle, player WHERE in_battle.channel_id=? AND player.user_id=in_battle.user_id",
        (channel_id,)).fetchall()
    con.commit()
    in_battles = c.fetchall()
    for in_battle in in_battles:
        full_hp = int(math.sqrt(in_battle[1])) * 5 + 50
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE in_battle SET player_hp=? WHERE user_id=?", (full_hp, in_battle[0],))
        con.commit()
    return "<@{}>はエリクサーを使った！このチャンネルの仲間全員が全回復した！".format(user_id)


async def fireball(ctx, user_id, channel_id):
    player_hp, error_message = into_battle(ctx, user_id, channel_id)
    embed = discord.Embed(description=error_message,
                          color=0xff0000)
    if error_message: return await ctx.send(embed=embed)
    if not consume_an_item(user_id, 2):
        return await ctx.send("<@{}>はファイアボールの書を持っていない！".format(user_id))
    player_level = get_player_level(ctx, user_id)
    boss_level, boss_hp = get_boss_level_and_hp(channel_id)
    player_attack = int(player_level * (1 + random.random()) / 10)
    boss_hp = boss_hp - player_attack
    if channel_id in special_monster:
        monster_name = special_monster[channel_id]["name"]
    elif channel_id in very_special_monster:
        monster_name = very_special_monster[channel_id]["name"]
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT monster FROM channel_status WHERE channel_id=?", (channel_id,)).fetchone()
        con.commit()
        monster_num = c.fetchone()
        monster_name = monsters[monster_num[0]]["name"]
        if boss_level % MONSTER_NUM == 0:
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster_num = c.fetchone()
            monster_name = tyoukyouteki[monster_num[0]]["name"]
        elif boss_level % 5 == 0:
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster_num = c.fetchone()
            monster_name = kyouteki[monster_num[0]]["name"]
    user_name = bot.get_user(user_id).name
    attack_message = "ファイアボール！{}は{}に{}のダメージを与えた！".format(user_name, monster_name, player_attack)
    if boss_hp <= 0:
        win_message = win_process(ctx, channel_id, boss_level, monster_name)
        up = discord.Color(random.randint(0, 0xFFFFFF))
        embedwin = discord.Embed(title="戦闘結果",
                                 description=f"```{attack_message}```\n\n{win_message}",
                                 color=up)
        await ctx.send(embed=embedwin)
        await reset_battle(ctx, channel_id, level_up=True)
    else:

        conn.execute("UPDATE channel_status SET boss_hp=? WHERE channel_id=?", (boss_hp, channel_id,))
        up = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(
            description="```{}\n{}のHP:{}/{}```".format(attack_message, monster_name, boss_hp, boss_level * 10 + 50),
            color=up
        )
        await ctx.send(embed=embed)


def pray(user_id, channel_id, mentions):
    if not mentions:
        return "祈りの書は仲間を復活させます。祈る相手を指定して使います。\n例)!!item 祈りの書 @ユーザー名".format(user_id)
    prayed_user_id = mentions[0].id
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT player_hp FROM in_battle WHERE channel_id=? and user_id=?",
                               (channel_id, prayed_user_id,)).fetchone()
    con.commit()
    prayed_user = c.fetchone()
    if not prayed_user:
        return "<@{}>は戦闘に参加していない！".format(prayed_user_id)
    if prayed_user[0] != 0:
        return "<@{}>はまだ生きている！".format(prayed_user_id)
    player_hp, error_message = into_battle(ctx, user_id, channel_id)
    if error_message: return error_message
    if not consume_an_item(user_id, 3):
        return "<@{}>は祈りの書を持っていない！".format(user_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("UPDATE in_battle SET player_hp=1 WHERE user_id=?", (prayed_user_id,))
    con.commit()
    return "<@{0}>は祈りを捧げ、<@{1}>は復活した！\n<@{1}> 残りHP: 1".format(user_id, prayed_user_id, )


@bot.command(description='上位10サーバーのランキングを表示する')
async def srank(ctx):
    """上位10サーバーのランキングを表示する"""
    embed = Embed(description="`!!ranking`を使ってください")
    await ctx.send(embed=embed)
    return
    # if "true" in kidou:
    #     embed = discord.Embed(description="現在起動中です。しばらくお待ちください。",
    #                           color=0xff0000)
    #     return await ctx.send(embed=embed)
    # channels = conn.execute("SELECT channel_id, boss_level FROM channel_status ORDER BY boss_level DESC").fetchall()
    # guilds = {}
    # for channel in channels:
    #     c = bot.get_channel(channel[0])
    #     if not c: continue
    #     guild = c.guild
    #     if not guild.id in guilds:
    #         guilds[guild.id] = [guild.name, channel[1]]
    #     if len(guilds) > 19: break
    # embed = discord.Embed(title="上位サーバーランキング",
    #                       description="{}".format("\n".join(
    #                           "{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(guilds.values()))),
    #                       color=0x9326ff)
    # await ctx.send(embed=embed)

@bot.command(description='上位10プレーヤーのランキングを表示する')
async def brank(ctx):
    """上位10プレーヤーのランキングを表示する"""
    embed = Embed(description="`!!ranking`を使ってください")
    await ctx.send(embed=embed)
    return
    # playerlist = conn.execute("SELECT user_id, experience FROM player WHERE bot=1 ORDER BY experience DESC").fetchall()
    # kekka = {}
    # for players in playerlist:
    #     p = bot.get_user(int(players[0]))  # ユーザーID
    #     if not p: continue
    #     user = p
    #     if not user.id in kekka:
    #         kekka[user.id] = [user.name, int(math.sqrt(players[1]))]
    #     if len(kekka) > 9: break
    # embed = discord.Embed(title="上位10プレーヤランキング",
    #                       description="{}".format("\n".join(
    #                           "{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))),
    #                       color=0x9326ff)
    # await ctx.send(embed=embed)


@bot.command(description='上位10プレーヤーのランキングを表示する')
async def prank(ctx):
    """上位10プレーヤーのランキングを表示する"""
    embed = Embed(description="`!!ranking`を使ってください")
    await ctx.send(embed=embed)
    return
    # playerlist = conn.execute("SELECT user_id, experience FROM player WHERE bot=0 ORDER BY experience DESC").fetchall()
    # bkekka = {}
    # kekka = {}
    # rongaina = {}
    # rongai = conn.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
    # for players in playerlist:
    #     p = bot.get_user(int(players[0]))  # ユーザーID
    #     if not p: continue
    #     user = p
    #     if not user.id in bkekka:
    #         bkekka[user.id] = [user.name, int(math.sqrt(players[1]))]
    #     if len(bkekka) > 9: break
    # for a in rongai:
    #     rongaina[a] = [a]
    # for i in rongaina:
    #     if i[0] in bkekka:
    #         del bkekka[i[0]]
    # for players in playerlist:
    #     p = bot.get_user(int(players[0]))  # ユーザーID
    #     if not p: continue
    #     user = p
    #     if not user.id in kekka:
    #         kekka[user.id] = [user.name, int(math.sqrt(players[1]))]
    #     if len(kekka) > (10 - len(bkekka) + 10): break
    # for a in rongai:
    #     rongaina[a] = [a]
    # for i in rongaina:
    #     if i[0] in kekka:
    #         del kekka[i[0]]
    # embed = discord.Embed(title="上位10プレーヤランキング",
    #                       description="{}".format("\n".join(
    #                           "{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))),
    #                       color=0x9326ff)
    # await ctx.send(embed=embed)

# @bot.command(description='上位10プレーヤーのランキングを表示する')
# async def rrank(ctx):
#     """上位10プレーヤーのランキングを表示する"""
#     embed = Embed(description="`!!ranking`を使ってください")
#     await ctx.send(embed=embed)
#     return
#     playerlist = conn.execute("SELECT user_id, experience FROM player ORDER BY experience DESC").fetchall()
#     kekka = {}
#     rongaina = {}
#     rongai = conn.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
#     for a in rongai:
#         rongaina[a] = [a]
#     for players in playerlist:
#         p = bot.get_user(int(players[0]))  # ユーザーID
#         if not p: continue
#         user = p
#         if not user.id in kekka:
#             for r in rongaina:
#                 if user.id == r[0]:
#                     kekka[user.id] = [user.name, int(math.sqrt(players[1]))]
#         if len(kekka) > 9: break
#     embed = discord.Embed(title="【論外】上位10プレーヤランキング",
#                           description="{}".format("\n".join(
#                               "{}位：`{}` (Lv{})".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))),
#                           color=0x9326ff)
#     await ctx.send(embed=embed)


@bot.command(description='上位10モンスターランキングを表示する')
async def mrank(ctx):
    """上位10プレーヤーのランキングを表示する"""
    embed = Embed(description="`!!ranking`を使ってください")
    await ctx.send(embed=embed)
    return
    # playerlist = conn.execute("SELECT user_id, count FROM monster_count ORDER BY count DESC").fetchall()
    # kekka = {}
    # for players in playerlist:
    #     p = bot.get_user(int(players[0]))  # ユーザーID
    #     if not p: continue
    #     user = p
    #     if not user.id in kekka:
    #         kekka[user.id] = [user.name, int(players[1])]
    #     if len(kekka) > 9: break
    # embed = discord.Embed(title="上位10敵を倒した数ランキング",
    #                       description="{}".format("\n".join(
    #                           "{}位：`{}` ({}体)".format(i + 1, a[0], a[1]) for i, a in enumerate(kekka.values()))),
    #                       color=0x9326ff)
    # await ctx.send(embed=embed)


def get_player_exp(ctx, user_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT experience FROM player WHERE user_id=?", (user_id,)).fetchone()
    con.commit()
    monster_num = c.fetchone()
    player = c.fetchone()
    if not player:
        conn.execute("INSERT INTO player values( ?, ?, ?)", (user_id, 10000, 1 if ctx.author.bot else 0))
        player = [1, ]
    return player[0]


def get_player_level(ctx, user_id, player_exp=None):
    if player_exp:
        return int(math.sqrt(player_exp))
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT experience FROM player WHERE user_id=?", (user_id,)).fetchone()
    con.commit()
    player = c.fetchone()
    if not player:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("INSERT INTO player values( ?, ?, ?)", (user_id, 10000, 1 if ctx.author.bot else 0))
        con.commit()
        player = [1, ]
    return int(math.sqrt(player[0]))


def get_boss_level_and_hp(channel_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT boss_level, boss_hp FROM channel_status WHERE channel_id=?",
                                  (channel_id,)).fetchone()
    con.commit()
    channel_status = c.fetchone()
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(f"SELECT user_id FROM item WHERE item_id=-10 ORDER BY user_id")
    con.commit()
    monster_num = c.fetchone()
    if not channel_status:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("INSERT INTO channel_status values( ?, ?, ?, ?)", (channel_id, 1, 50, 1))
        con.commit()
        channel_status = [1, 50]
    return channel_status[0], channel_status[1]


def experiment(ctx, user_id, exp):
    player_exp = get_player_exp(ctx, user_id)
    next_exp = player_exp + exp
    current_level = int(math.sqrt(player_exp))
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("UPDATE player SET experience=? WHERE user_id=?", (next_exp, user_id,))
    con.commit()
    if next_exp > (current_level + 1) ** 2:
        next_level = int(math.sqrt(next_exp))
        return "<@{}>はレベルアップした！`Lv.{} -> Lv.{}`".format(user_id, current_level, next_level)
    return ""


def obtain_an_item(user_id, item_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT count FROM item WHERE user_id=? and item_id=?", (user_id, item_id)).fetchone()
    con.commit()
    item_count = c.fetchone()
    if item_count:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE item SET count=? WHERE user_id=? and item_id=?", (item_count[0] + 1, user_id, item_id,))
        con.commit()
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("INSERT INTO item VALUES(?,?,1)", (user_id, item_id,))
        con.commit()


def monster_count(user_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(f"SELECT count FROM monster_count WHERE user_id=?", (user_id,)).fetchone()
    con.commit()
    monstercount = c.fetchone()
    if monstercount:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE monster_count SET count=? WHERE user_id=?", (monstercount[0] + 1, user_id,))
        con.commit()
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("INSERT INTO monster_count VALUES(?,0)", (user_id,))
        con.commit()


def monster_hyouzi(user_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT count FROM monster_count WHERE user_id=?", (user_id,)).fetchone()
    con.commit()
    monstercount = c.fetchone()
    if monstercount:
        m = monstercount[0]
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("INSERT INTO monster_count VALUES(?,1)", (user_id,)).fetchone()
        con.commit()
        m = 1
    return m


def rongai_check(user_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT user_id FROM item WHERE item_id=-10 ORDER BY item_id").fetchall()
    con.commit()
    rongai = c.fetchall()
    for a in rongai:
        if user_id == a[0]:
            break
            return True
        else:
            break
            return False


def fbi_obtain_an_item(user_id, item_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT count FROM item WHERE user_id=? and item_id=?", (user_id, item_id)).fetchone()
    con.commit()
    item_count = c.fetchone()
    if item_count:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE item SET count=? WHERE user_id=? and item_id=?", (item_count[0] + 100, user_id, item_id,))
        con.commit()


def e_obtain_an_item(user_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT count FROM item WHERE user_id=? and item_id=?", (user_id, 1)).fetchone()
    con.commit()
    item_count = c.fetchone()
    if item_count:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE item SET count=? WHERE user_id=? and item_id=?", (item_count[0] + 10, user_id, 1,))
        con.commit()
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("INSERT INTO item VALUES(?,1,1)", (user_id,))
        con.commit()


def consume_an_item(user_id, item_id):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("SELECT count FROM item WHERE user_id=? and item_id=?", (user_id, item_id)).fetchone()
    con.commit()
    current_count = c.fetchone()
    if not current_count:
        return False
    if current_count[0] <= 1:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("DELETE FROM item WHERE user_id=? and item_id=?", (user_id, item_id))
        con.commit()
    else:
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE item SET count=? WHERE user_id=? and item_id=?", (current_count[0] - 1, user_id, item_id))
        con.commit()
    return True


@bot.command(name="rea")
async def mamenoki_syoukan(ctx, num=""):
    if ctx.author.id == 421971957081309194:
        numm = {"1", "2", "3", "4", "5", "6"}
        if num in numm:
            if ctx.message.channel.id in special_monster: del special_monster[ctx.message.channel.id]
            if ctx.message.channel.id in very_special_monster: del very_special_monster[ctx.message.channel.id]
            if ctx.message.channel.id in tyoukyou_teki: del tyoukyou_teki[ctx.message.channel.id]
            if ctx.message.channel.id in kyou_teki: del kyou_teki[ctx.message.channel.id]
            boss_level, _ = get_boss_level_and_hp(ctx.message.channel.id)
            channel_id = ctx.message.channel.id
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (num, channel_id))
            monster_num = conn.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster = rea[monster_num[0]]
            special_monster[channel_id] = monster
            up = discord.Color(random.randint(0, 0xFFFFFF))
            embed = discord.Embed(
                title="{}が待ち構えている...！\nLv.{}  HP:{}".format(monster["name"], boss_level, boss_level * 10 + 50), color=up
            )
            embed.set_image(
                url="{}".format(monster["img"])
            )
            print("{}が待ち構えている...！Lv.{}      guild:{}   channel:{}   author:{}".format(monster["name"], boss_level,
                                                                                      ctx.message.guild.name,
                                                                                      ctx.message.channel.name,
                                                                                      ctx.message.author.name))
            channel = bot.get_channel(ctx.message.channel.id)
            await channel.send(embed=embed)


@bot.command(name="tyougeki")
async def tyougeki_syoukan(ctx):
    if ctx.author.id == 421971957081309194:
        if ctx.message.channel.id in special_monster: del special_monster[ctx.message.channel.id]
        if ctx.message.channel.id in very_special_monster: del very_special_monster[ctx.message.channel.id]
        if ctx.message.channel.id in tyoukyou_teki: del tyoukyou_teki[ctx.message.channel.id]
        if ctx.message.channel.id in kyou_teki: del kyou_teki[ctx.message.channel.id]
        boss_level, _ = get_boss_level_and_hp(ctx.message.channel.id)
        number = random.randint(0, 1)
        channel_id = ctx.message.channel.id
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (number, channel_id))
        con.commit()
        monster = tyougekirea[0]
        very_special_monster[channel_id] = monster
        up = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(
            title="{}が待ち構えている...！\nLv.{}  HP:{}".format(monster["name"], boss_level, boss_level * 10 + 50), color=up
        )
        embed.set_image(
            url="{}".format(monster["img"])
        )
        print("{}が待ち構えている...！Lv.{}      guild:{}   channel:{}   author:{}".format(monster["name"], boss_level,
                                                                                  ctx.message.guild.name,
                                                                                  ctx.message.channel.name,
                                                                                  ctx.message.author.name))
        channel = bot.get_channel(ctx.message.channel.id)
        await channel.send(embed=embed)


async def reset_battle(ctx, channel_id, level_up=False):
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("DELETE FROM in_battle WHERE channel_id=?", (channel_id,))
    con.commit()
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    query = "UPDATE channel_status SET {} WHERE channel_id=?".format(
        "boss_level=boss_level+1, boss_hp=boss_level*10+60" if level_up else "boss_hp=boss_level*10+50"
    )
    c.execute(query, (channel_id,))
    con.commit()
    boss_level, _ = get_boss_level_and_hp(channel_id)
    if level_up and boss_level % MONSTER_NUM in [
        1, 4, 6, 8, 9, 12, 14, 16, 18, 19, 21, 22, 24, 26, 27, 28, 29, 31, 33, 36, 38, 39, 42, 43, 44
    ] and random.random() < 0.1:
        number = random.randint(0, 6)
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (number, channel_id))
        con.commit()
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT monster FROM channel_status WHERE channel_id=?", (channel_id,)).fetchone()
        con.commit()
        monster_num = c.fetchone()
        monster = rea[monster_num[0]]
        special_monster[channel_id] = monster
        if random.random() < 0.1:
            if channel_id in special_monster: del special_monster[channel_id]
            number = random.randint(0, 1)
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (number, channel_id))
            con.commit()
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster_num = c.fetchone()
            monster = tyougekirea[0]
            very_special_monster[channel_id] = monster
    else:
        number = random.randint(0, 50)
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (number, channel_id))
        con.commit()
        con = psycopg2.connect(os.environ.get("DATABASE_URL"))
        c = con.cursor()
        c.execute("SELECT monster FROM channel_status WHERE channel_id=?", (channel_id,)).fetchone()
        con.commit()
        monster_num = c.fetchone()
        monster = monsters[monster_num[0]]
        if boss_level % MONSTER_NUM == 0:
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (0, channel_id))
            con.commit()
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster_num = c.fetchone()
            tyoukyou_teki[channel_id] = monster
            monster = tyoukyouteki[monster_num[0]]
        elif boss_level % 5 == 0:
            number = random.randint(0, 9)
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("UPDATE channel_status SET monster=? WHERE channel_id=?", (number, channel_id))
            con.commit()
            con = psycopg2.connect(os.environ.get("DATABASE_URL"))
            c = con.cursor()
            c.execute("SELECT monster FROM channel_status WHERE channel_id=?",
                                       (channel_id,)).fetchone()
            con.commit()
            monster_num = c.fetchone()
            monster = kyouteki[monster_num[0]]
            kyou_teki[channel_id] = monster

        # elif not boss_level % MONSTER_NUM == 0 and boss_level % 5 == 0:
        #     monster = monsters[random.randint(0, 38)]
        if channel_id in special_monster: del special_monster[channel_id]
        if channel_id in very_special_monster: del very_special_monster[channel_id]
        if channel_id in tyoukyou_teki: del tyoukyou_teki[channel_id]
        if channel_id in kyou_teki: del kyou_teki[channel_id]
    up = discord.Color(random.randint(0, 0xFFFFFF))
    embed = discord.Embed(
        title="{}が待ち構えている...！\nLv.{}  HP:{}".format(monster["name"], boss_level, boss_level * 10 + 50), color=up
    )
    embed.set_image(
        url="{}".format(monster["img"])
    )
    print("{}が待ち構えている...！Lv.{}      guild:{}   channel:{}   author:{}".format(monster["name"], boss_level,
                                                                              ctx.message.guild.name,
                                                                              ctx.message.channel.name,
                                                                              ctx.message.author.name))
    await ctx.send(embed=embed)
    embed = discord.Embed(
        description=f"""敵の名前：**{monster["name"]}**\nLv：**{boss_level}**\n鯖名：**{ctx.message.guild.name}**\nチャンネル：**{ctx.message.channel.name}**\n出した人：**{ctx.message.author.name}**id:{ctx.message.author.id}""")
    await bot.get_channel(661129255933050882).send(embed=embed)

login_loop.start()
bot.run(token)

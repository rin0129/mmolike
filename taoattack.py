import discord
import asyncio
import os
import json
import re

client = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']

id = 659936594559631370

@client.event
async def on_ready():
    clientt_channel = client.get_channel(id)
    await clientt_channel.send("起動")
    while True:
        await asyncio.sleep(240)
        client.t_ch = client.get_channel(id)
        await client.t_ch.send("::i i <@564407708770631683> 300")

@client.event
async def on_message(message):
    if message.author.id == 421971957081309194:
        if message.content == "!res":
            print("コマンド再起動")
            os.system("python taoplay.py")
            return

    if message.content.startswith("msay"):
        if not message.author.id == 421971957081309194:
            return await message.channel.send("あなたは、使えません。\n出直してきてね")
        sayd = message.content[5:]
        await message.channel.send(f"{sayd}")
        await message.delete()
        return

    if message.content == "botst":
        await message.channel.send("::st")
        return

    if message.channel != client.get_channel(id):
        return
    tao = message.guild.get_member(688300266331701273)
    if message.author == tao:

        def author_tao_check(msg):
            return msg.author == tao

        if not message.embeds:

            if "ダメージ" in message.content:
                if "HP" in message.content:
                    # まだ倒し切れていない判定
                    if message.guild.me.display_name in message.content:
                        # そのメッセージ対象がPETでない判定
                        await asyncio.sleep(1)
                        await client.get_channel(id).send("::")
                        try:
                            await client.wait_for("message", timeout=3, check=lambda messages: messages.author.id == 688300266331701273)

                        except asyncio.TimeoutError:
                            await message.channel.send(":: waitt")
                            return

                        else:
                            pass

            elif "攻撃失敗" in message.content:
                print("攻撃に失敗しました。")
                await asyncio.sleep(3)
                await message.channel.send("::atk")
                # 再度攻撃

            elif "ログイン失敗" in message.content:
                print("ログインに失敗しました。")
                await asyncio.sleep(10)
                await message.channel.send("::login")
                # 再度ログイン

            elif "リセット失敗" in message.content:
                print("リセットに失敗しました。")
                await asyncio.sleep(10)
                await message.channel.send("::reset")
                # 再度リセット

        else:
            embed = message.embeds[0]

            # def battle_check(m):
            #     # そのメッセージが戦闘開始のメッセージであるかを判定する。
            #     if not m.embeds:
            #         return 0
            #     if not m.embeds[0].title:
            #         return 0
            # 
            #     return "待ち構えている" in m.embeds[0].title

            # if battle_check(message):
            #     print("a")
                # await client.get_channel(id).send(":: 開始1")
                # try:
                #     await client.wait_for("message", timeout=3, check=lambda messages: messages.author.id == 526620171658330112)
                # except asyncio.TimeoutError:
                #     await client.get_channel(id).send("::atk wait")
                #     return
                #
                # else:
                #     pass
                # await clientt_channel.send("::atk 開始2")




            if embed.description:
                if embed.description.startswith("このチャンネルは"):
                    print("このチャンネルは使用できません。")
                    client.send_flag = False

                elif "<@564407708770631683>はエリクサーを使った！" in embed.description:
                    print("リセットします。")
                    await client.get_channel(id).send("::atk")
                    await asyncio.sleep(3)
                    await client.get_channel(id).send("::atk")

                elif "<@564407708770631683>はもうやられている！" in embed.description:
                    await client.get_channel(id).send("::i i <@564407708770631683>")
                    try:
                        await client.wait_for("message", timeout=3,
                                              check=lambda messages: messages.author.id == 688300266331701273)

                    except asyncio.TimeoutError:
                        await message.channel.send("::i i <@564407708770631683> 3wait")
                        return

                    else:
                        pass

                # elif "<@564407708770631683>はもうやられている！（戦いをやり直すには「::reset」だ）" in embed.description:
                #     print("リセットします。")
                #     await asyncio.sleep(2)
                #     await client.get_channel(id).send("::atk e")

                elif "::login" in embed.description:
                    await message.channel.send("::login")
                    await client.wait_for("message", check=author_tao_check)
                    await message.channel.send("::atk")



client.run(token)

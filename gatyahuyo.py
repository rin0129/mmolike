import discord
import numpy
import os



bot = discord.Client()

token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print(bot.user.name)
    print('ログイン完了じゃぁぁぁ')

@bot.event
async def on_message(message):
    global get
    if message.content == "ccct":
        get = message.author
        if message.author.bot:
            return
        random = numpy.random.choice(['中から綺麗な紙がでてきた!　役職:【レア】電光石火 と書いてある!おめでとうございます!', 'ガチャガチャ....ポン! 残念ですがはずれです!', 'ガチャガチャ...ポン! 隠しメッセージ　m 1番', 'ガチャガチャ...ポン! カプセルの中からnormalガチャチケットが出てきました!おめでとうございます! またチャレンジしてね!'], p=[0.1, 0.7, 0.1, 0.1])
        embed = discord.Embed(
            title="無料ガチャ",
            description=f"{message.author.mention}さんのガチャは果たして....",
            color=0x2ECC69
        )
        embed.set_thumbnail(
            url=message.author.avatar_url
        )
        embed.add_field(
            name="[結果]",
            value=random,
        )
        await message.channel.send(embed=embed)

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "ガチャガチャ...ポン! カプセルの中からnormalガチャチケットが出てきました!おめでとうございます! またチャレンジしてね!" in field.value:
                            await message.channel.send(file=discord.File('nomal.png',))
                            role = discord.utils.get(message.guild.roles, name='normalチケット')
                            await get.add_roles(role)
                            await message.channel.send("```normalチケット```を付与したよ！！")

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "中から綺麗な紙がでてきた!　役職:【レア】電光石火 と書いてある!おめでとうございます!" in field.value:
                            role = discord.utils.get(message.guild.roles, name='【レア】電光石火')
                            await get.add_roles(role)
                            await message.channel.send("```【レア】電光石火」を付与したよ！！```")


    if message.content == "nnnnct":
        get = message.author
        if message.author.bot:
            return
        random = numpy.random.choice(['中から光るようにピカピカな紙が出てきた。【ノーマル】異星の深淵　と書いてある。 おめでとうございます!またチャレンジしてね!', '中から光るようにピカピカな紙が出てきた。【ノーマル】ヘビー級のキケンなヤツら と書いてある。 おめでとうございます!', '中から光るようにピカピカな紙が出てきた。【ノーマル】戦いの基本は近接戦 と書いてある。 おめでとうございます!', 'ガチャガチャ...ポン! 隠しメッセージ　m 2番 またチャレンジしてね!', '痛ッ... 顔に紙がついていた! 紙の正体はレアガチャチケットだった! おめでとうございます!またチャレンジしてね!', 'ガチャガチャ....ポン! 残念ですがはずれです!'], p=[0.07, 0.07, 0.07, 0.04, 0.03, 0.72])
        embed = discord.Embed(
            title="normalガチャ",
            description=f"{message.author.mention}さんのガチャは果たして....",
            color=0x2ECC69
        )
        embed.set_thumbnail(
            url=message.author.avatar_url
        )
        embed.add_field(
            name="[結果]",
            value=random,
        )
        await message.channel.send(embed=embed)

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "中から光るようにピカピカな紙が出てきた。【ノーマル】異星の深淵　と書いてある。 おめでとうございます!またチャレンジしてね!" in field.value:
                            role = discord.utils.get(message.guild.roles, name='【ノーマル】異星の深淵')
                            await get.add_roles(role)
                            await message.channel.send("```【ノーマル】異星の深淵```を付与したよ！！")

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "中から光るようにピカピカな紙が出てきた。【ノーマル】ヘビー級のキケンなヤツら と書いてある。 おめでとうございます!" in field.value:
                            role = discord.utils.get(message.guild.roles, name='【ノーマル】ヘビー級のキケンなヤツら')
                            await get.add_roles(role)
                            await message.channel.send("```【ノーマル】ヘビー級のキケンなヤツら```を付与したよ！！")

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "中から光るようにピカピカな紙が出てきた。【ノーマル】戦いの基本は近接戦 と書いてある。 おめでとうございます!" in field.value:
                            role = discord.utils.get(message.guild.roles, name='【ノーマル】戦いの基本は近接戦')
                            await get.add_roles(role)
                            await message.channel.send("```【ノーマル】戦いの基本は近接戦```を付与したよ！！")

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "痛ッ... 顔に紙がついていた! 紙の正体はレアガチャチケットだった! おめでとうございます!またチャレンジしてね!" in field.value:
                            await message.channel.send(file=discord.File('rare.png',))
                            role = discord.utils.get(message.guild.roles, name='Rareチケット')
                            await get.add_roles(role)
                            await message.channel.send("```レアガチャチケット```を付与したよ！！")


    if message.content == "rrrct":
        get = message.author
        if message.author.bot:
            return
        random = numpy.random.choice(['中から光るようにピカピカな紙が出てきた。【レア】きのこの山派　と書いてある。 おめでとうございます!またチャレンジしてね!', '中から光るようにピカピカな紙が出てきた。【レア】選ばれたのは綾鷹でした と書いてある。 おめでとうございます!', '中から光るようにピカピカな紙が出てきた。【レア】たけのこの里派 と書いてある。 おめでとうございます!', 'ガチャガチャ...ポン! 隠しメッセージ　o 3番 またチャレンジしてね!', '痛ッ... 顔に紙がついていた! 紙の正体はGodガチャチケットだった! おめでとうございます!またチャレンジしてね!', 'ガチャガチャ....ポン! 残念ですがはずれです!'], p=[0.07, 0.07, 0.07, 0.04, 0.03, 0.72])
        embed = discord.Embed(
            title="rareガチャ",
            description=f"{message.author.mention}さんのガチャは果たして....",
            color=0x2ECC69
        )
        embed.set_thumbnail(
            url=message.author.avatar_url
        )
        embed.add_field(
            name="[結果]",
            value=random,
        )
        await message.channel.send(embed=embed)

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "中から光るようにピカピカな紙が出てきた。【レア】きのこの山派　と書いてある。 おめでとうございます!またチャレンジしてね!" in field.value:
                            role = discord.utils.get(message.guild.roles, name='【レア】きのこの山派')
                            await get.add_roles(role)
                            await message.channel.send("```【レア】きのこの山派```を付与したよ！！")

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "中から光るようにピカピカな紙が出てきた。【レア】選ばれたのは綾鷹でした と書いてある。 おめでとうございます!" in field.value:
                            role = discord.utils.get(message.guild.roles, name='【レア】選ばれたのは綾鷹でした')
                            await get.add_roles(role)
                            await message.channel.send("```【レア】選ばれたのは綾鷹でした```を付与したよ！！")

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "中から光るようにピカピカな紙が出てきた。【レア】たけのこの里派 と書いてある。 おめでとうございます!" in field.value:
                            role = discord.utils.get(message.guild.roles, name='【レア】たけのこの里派')
                            await get.add_roles(role)
                            await message.channel.send("```【レア】たけのこの里派```を付与したよ！！")

    if len(message.embeds) != 0:
        for embeds in message.embeds:
            if embeds.fields:
                for field in embeds.fields:
                    if field.name == "[結果]":
                        if "痛ッ... 顔に紙がついていた! 紙の正体はGodガチャチケットだった! おめでとうございます!またチャレンジしてね!" in field.value:
                            await message.channel.send(file=discord.File('god.png', ))
                            role = discord.utils.get(message.guild.roles, name='GODチケット')
                            await get.add_roles(role)
                            await message.channel.send("```GODチケット```を付与したよ！！")



@bot.event
async def on_ready():
    return await bot.change_presence(activity=discord.Game(name='データベースのテスト中...'))


client.run(token)

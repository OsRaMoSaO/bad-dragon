#all imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import random, time
import requests
import hikari
from hikari import embeds
import lightbulb
from lightbulb.utils.pag import EmbedPaginator
import  re
import miru

#Databse stuff
cred = credentials.Certificate('certificate.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bad-dragon-bot-default-rtdb.europe-west1.firebasedatabase.app/'
})
cmdStats = db.reference('Stats/commands used/cmd used')
imgStats = db.reference("Stats/images generated/images")



#api tags
#r34
from rule34Py import rule34Py
r34Py = rule34Py()
#e621
from e621 import E621
api = E621()
session = requests.Session()

#Add ur own token here
from tokens import Main, Test
bot = lightbulb.BotApp(token=Main, prefix='!')
miru.load(bot)



#current tags
tags = ['anthro',' female',' male',' solo',' genitals',' clothing',' breasts',' hair',' fur',' penis',' bodily_fluids',' nude',
        ' simple_background',' nipples',' video_games',' clothed',' text',' balls',' sex',' genital_fluids',' smile',' erection',
        ' butt',' gay',' pussy']



#BUTTONS
class DiceView(miru.View):
    @miru.button(label="1d6", style=hikari.ButtonStyle.PRIMARY)
    async def btn(self, button: miru.Button, ctx: miru.Context) -> None:
        print("rolling6")
        roll = random.randint(1,6)
        await ctx.respond(f"You rolled a **{roll}**!")

    @miru.button(label="1d20", emoji="❌", style=hikari.ButtonStyle.PRIMARY)
    async def btn_roll(self, button: miru.Button, ctx: miru.Context) -> None:
        roll = random.randint(1, 20)
        await ctx.edit_response(f"You rolled a **{roll}**!")

    @miru.button(label="Close", style=hikari.ButtonStyle.PRIMARY)
    async def btn_close(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.edit_response("the menu was closed", components=[])
        self.stop()


#button test
#@bot.command()
#@lightbulb.command('roll', 'Displays buttons to roll a d6 and d20')
#@lightbulb.implements(lightbulb.SlashCommand)
#async def roll(ctx):
    #view = DiceView()
    #await   ctx.respond("Roll your dice!", components=view.build())
    #view.start()



#E621 search
@bot.command
@lightbulb.option("tag", "select a valid e621 tag (multiple tags can be separated by a space)", type=str, autocomplete=True)
@lightbulb.option("amount", "how many images do you want to see (max 10 at a time)", type=int)
@lightbulb.command("e621", "search e621 for any picture or video")
@lightbulb.implements(lightbulb.SlashCommand)
async def e621(ctx: lightbulb.Context):
    amount = ctx.options.amount
    #Database
    e621 = cmdStats.child("e621")
    e621Uses = db.reference("Stats/commands used/cmd used/e621").get()
    e621UsesString = str(e621Uses)
    pattern = "[0-999999]+"
    currente621uses = re.findall(pattern, e621UsesString)
    curusesint = int(currente621uses[0])
    newInt = curusesint + 1
    e621.update({
        "usage": newInt
    })
    #Images generated databse
    e621IMG = imgStats.child("e621")
    e621IMGUses = db.reference("Stats/images generated/images/e621").get()
    e621IMGUsesString = str(e621IMGUses)
    pattern = "[0-999999]+"
    currente621IMGuses = re.findall(pattern, e621IMGUsesString)
    curusesintIMG = int(currente621IMGuses[0])
    newIntIMG = curusesintIMG + amount
    e621IMG.update({
        "generated": newIntIMG
    })
    #buttons

    #actual command
    tags = str(ctx.options.tag)
    tagsArray = tags.split()
    post = api.posts.search(tagsArray)
    max = len(post)
    if amount == 1:
        postrand = post[random.randrange(0, max)]
        if postrand.file.ext == "webm":
            embed = (
                hikari.Embed(
                    title="Artist: " + postrand.tags.artist[0] + " [E621 link]",
                    url="https://e621.net/posts/" + str(postrand.id),
                    colour=0x010942
                )
                    .set_footer(text="Video above from e621.net",
                                icon="https://i1.kym-cdn.com/entries/icons/facebook/000/016/852/e621_logo.png")
            )
            await ctx.respond(postrand.file.url)
            await ctx.respond(embed)
        elif postrand.file.ext == "png" or "jpeg" or "gif":
            if postrand.file.ext != "swf":
                embed = (
                    hikari.Embed(
                        title="Artist: " + postrand.tags.artist[0] + " [E621 link]",
                        url="https://e621.net/posts/" + str(postrand.id),
                        colour=0x010942
                    )
                        .set_footer(text="Picture from e621.net",
                                    icon="https://i1.kym-cdn.com/entries/icons/facebook/000/016/852/e621_logo.png")
                        .set_image(postrand.file.url)
                )
                await ctx.respond(embed)
            else:
                await ctx.respond("This file type is not currently supported! (swf, flash)")
        else:
            await ctx.respond("This file type is not currently supported! (swf, flash)")
    elif amount <= 10:
        q = 0
        for q in range(amount):
            time.sleep(0.75)
            postrand = post[random.randrange(0, max)]
            if postrand.file.ext == "webm":
                embed = (
                    hikari.Embed(
                        title="Artist: " + postrand.tags.artist[0] + " [E621 link]",
                        url="https://e621.net/posts/" + str(postrand.id),
                        colour=0x010942
                    )
                        .set_footer(text="Video above from e621.net",
                                    icon="https://i1.kym-cdn.com/entries/icons/facebook/000/016/852/e621_logo.png")
                )
                await ctx.respond(postrand.file.url)
                await ctx.respond(embed)
            elif postrand.file.ext == "png" or "jpeg" or "gif":
                if postrand.file.ext != "swf":
                    embed = (
                        hikari.Embed(
                            title="Artist: " + postrand.tags.artist[0] + " [E621 link]",
                            url="https://e621.net/posts/" + str(postrand.id),
                            colour=0x010942
                        )
                            .set_footer(text="Picture from e621.net",
                                        icon="https://i1.kym-cdn.com/entries/icons/facebook/000/016/852/e621_logo.png")
                            .set_image(postrand.file.url)
                    )
                    await ctx.respond(embed)
                else:
                    await ctx.respond("This file type is not currently supported! (swf, flash)")
            else:
                await ctx.respond("This file type is not currently supported! (swf, flash)")
    else:
        await ctx.respond("max 10 pics/vids at a time :)")



#Autocomplete
@e621.autocomplete("tag")
async def e621_autocomplete(opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction):
    death = False
    data = []
    optlist = opt.value.split()
    for times in range(len(optlist)):
        for auto_correct_choices in tags:
            if len(optlist) >= 1:
                if len(optlist) >= 2:
                   death = True
                if optlist[len(optlist) - 1].lower() in auto_correct_choices.lower() and death == False:
                    data.append(auto_correct_choices)
        return data


#R34 search
@bot.command
@lightbulb.option("tag", "select a valid rule34 tag (multiple tags can separated by a space)", type=str)
@lightbulb.option("amount", "how many images do you want to see (max 10 at a time)", type=int)
@lightbulb.command("rule34", "search rule34 for any picture or video")
@lightbulb.implements(lightbulb.SlashCommand)
async def r34(ctx):
    amount = ctx.options.amount
    # Database
    rule34= cmdStats.child("rule34")
    rule34Uses = db.reference("Stats/commands used/cmd used/rule34").get()
    rule34UsesString = str(rule34Uses)
    pattern = "[0-999999]+"
    print(rule34UsesString)
    currente621uses = re.findall(pattern, rule34UsesString)
    print(currente621uses)
    curusesint = int(currente621uses[0])
    newInt = curusesint + 1
    newIntStr = str(newInt)
    print(newInt)
    rule34.update({
        "usage": newInt
    })
    #Images generated
    rule34IMG = imgStats.child("rule34")
    rule34IMGUses = db.reference("Stats/images generated/images/rule34").get()
    rule34IMGUsesString = str(rule34IMGUses)
    pattern = "[0-999999]+"
    currentrule34IMGuses = re.findall(pattern, rule34IMGUsesString)
    curusesintIMG = int(currentrule34IMGuses[0])
    newIntIMG = curusesintIMG + amount
    rule34IMG.update({
        "generated": newIntIMG
    })


    # actual command
    tags = str(ctx.options.tag)
    tagsArray = tags.split()
    if amount == 1:
        result = r34Py.random_post(tagsArray)
        embed = (
            hikari.Embed(
                title="Artist: " "W.I.P" + " [R34 link]",
                url=f"https://rule34.xxx/index.php?page=post&s=view&id={result.id}",
                colour=0xbdecb6
            )
                .set_footer(text="Picture from rule34.xxx",
                            icon="https://en.wikifur.com/w/images/thumb/2/24/Rule34_logo.png/220px-Rule34_logo.png")
                .set_image(result.image)

        )
        await ctx.respond(embed)


    elif amount <= 10:
        q = 0
        for q in range(amount):
            result = r34Py.random_post(tagsArray)
            embed = (
                hikari.Embed(
                    title="Artist: " "W.I.P" + " [R34 link]",
                    url=f"https://rule34.xxx/index.php?page=post&s=view&id={result.id}",
                    colour=0xbdecb6
                )
                    .set_footer(text="Picture from rule34.xxx",
                                icon="https://en.wikifur.com/w/images/thumb/2/24/Rule34_logo.png/220px-Rule34_logo.png")
                    .set_image(result.image)
            )
            await ctx.respond(embed)
            time.sleep(1)

    else:
        await ctx.respond("max 10 pics at a time :)")



#Help
@bot.command
@lightbulb.command("help", "shows available bot commands")
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title="Lis of commands", description="Comands:")
    embed.add_field("/e621", "lets you search e621 using any tags through discord")
    embed.add_field("/rule34", "lets you search rule34 using any tags through discord")
    embed.set_thumbnail("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.gHvXG2mIOSSZufGmiEhZPAHaHO%26pid%3DApi&f=1")
    embed.set_footer("Bad dragon TM (commands work in dms too <3)")
    await ctx.respond(embed)  # or respond(embed=embed)


#error
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent):
    #await event.context.respond("Oopsie woopsies, somthing went wrong sowwy abowt that")
    print(event)
bot.run()



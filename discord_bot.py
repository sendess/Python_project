import discord
import random
import datetime
import asyncio
import json
import youtube_dl
from discord.ext import commands, tasks
from discord import Game
from itertools import cycle
from youtube_dl import YoutubeDL

BOT_PREFIX = '!'
message = joined = 0
messages = joined = 0
players = {}

def read_token():
    with open("token.txt", 'r') as f:
        lines = f.readlines()
        return lines[0].strip()
token = read_token()

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_guild_join(guild):
    global BOT_PREFIX
    BOT_PREFIX = "!"
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "!"
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.command()
async def changeprefix(ctx, prefix):
    global BOT_PREFIX
    BOT_PREFIX = prefix
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)
    await ctx.send(f"""My prefix was successfully changed to '{prefix}'""")

statuses = cycle([
    f"for {BOT_PREFIX}help",
    "on my own",
    f"for {BOT_PREFIX}help",
    " you",
    f"for {BOT_PREFIX}help",
    " nothing at all",
    f"for {BOT_PREFIX}help",
    " your messages",
    f"for {BOT_PREFIX}help",
    " everything!!"
])

async def update_stats():
    await client.wait_until_ready()
    global messages, joined
    id = client.get_guild(712150647704649748)
    while not client.is_closed():
        try:
            with open("stats.txt", "a+") as f:
                f.write(f"Time: {datetime.datetime.utcnow()}, Messages:  {messages} , New Members Joined: {joined} , Total Members count = {id.member_count} \n")
            messages = 0 
            joined = 0

            await asyncio.sleep(3600)        
        except Exception as e:
            print(e)
            await asyncio.sleep(3600)


@client.event 
async def on_member_update(before, after): 
    n = after.nick 
    if n: 
       if n.lower().count("sanity") > 0: 
            last = before.nick
            if last: 
                await after.edit(nick = last)
            else: 
                await after.edit(nick = "choose sth else")


@client.event
async def on_ready():   
    change_status.start()
    #await client.change_presence(status = discord.Status.idle) activity = discord.Game(" with your feelings.")) #removed after the command was updated over time automatically.
    print("Logged in as " + client.user.name)
    #await client.guild.channel.send("I am up if anyone needs me.")

@tasks.loop(seconds = 5)
async def change_status():
    await client.change_presence(status = discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name= next(statuses)))
    #await client.change_presence(status = discord.Status.idle, activity = discord.Streaming(next(status)))


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"""Welcome {member.mention}""")

@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"""{member.mention} has left the server""")

@client.command(aliases = ['hi', 'hey', 'hola', 'greetings','namaste', 'namaskar'])
async def hello(ctx):
    possible_responses = [
        'Hey there!! ',
        'Hi ',
        'Greetings, ',
        'Hello ',
        'Hola ',
        'Namaste ',
        'Namaskar '
    ]
    await ctx.send(random.choice(possible_responses) + f"""{ctx.author.mention}""")

@client.command(aliases = ['adios', 'byebye','byeee', 'byee'])
async def bye(ctx):
    possible_responses = [
        "Please stay with me. :'( ", 
        'Everyone must go one day, Byee',
        'Bye byeeeee ',
        'Come again soon, ',
        'ba-byeeee!! ',
        'Are you going to leave me?\n Its okay but come again soon ',
        'I will miss you, ',
        'Goodbye!! '
    ]
    await ctx.send(random.choice(possible_responses) + f"""{ctx.author.mention}""")
@client.command(aliases = ['hehe','hahaha','lol','rofl','lul','lel','lmao','hehehe'])
async def haha(ctx):
    possible_response = [
        'Haha somethings was funny, I missed it though.',
        'I wish I could laugh as you do, But i feel nothing.',
        'Haha stop it, you dont wanna hear a bot laugh'
    ]
    await ctx.send(random.choice(possible_response))



@client.command()
async def ping(ctx):
    possible_responses = [
        'Pong!!',
        'Ping what?? ',
        'Delay is for kids.',
        'I cant hear you!!',
        ''
    ]
    response = random.choice(possible_responses)
    if response == '':
        await ctx.send(f"""Ping is = {round(client.latency * 1000)} ms.""")    
    else:
        await ctx.send(response + f"""  Just kidding , ping is = {round(client.latency * 1000)} ms.""")
    print("pinged")

@client.command()
async def connect(ctx, *, channel: discord.VoiceChannel = None):
    if not channel:
        channel = ctx.author.voice.channel
    vc = ctx.voice_client
    if vc:
        if vc.channel.id == channel.id:
            return
        await vc.move_to(channel)
    else:
        await channel.connect()
    await ctx.send(f'Connected to: **{channel}**', delete_after=20)

# @client.command()
# async def leave(ctx):
#     guild = ctx.message.guild
#     voice_client = guild.voice_client
#     await voice_client.disconnect()

@commands.command()
async def leave(ctx):
    vc = ctx.voice_client
    
    if not vc or not vc.is_connected():
        await ctx.send('I am not currently playing anything!', delete_after=20)
    else:
        channel = ctx.author.voice.channel
        await channel.disconnect()


# @client.command()
# async def play (ctx, *, url):
#     connect(ctx)
#     url = "https://www.youtube.com/results?search_query=" + url
#     guild = ctx.message.guild
#     voice_client = guild.voice_client 
#     player = await voice_client.create_ytdl_player(url)
#     players[server.id] = player
#     player.start()


# @commands.command()
# async def play(ctx, *, search: str):
#     await ctx.trigger_typing()
#     bot = ctx.bot
#     vc = ctx.voice_client
    
#     if not vc:
#        await ctx.invoke(connect)

#     player = players[ctx.guild.id]

#         # If download is False, source will be a dict which will be used later to regather the stream.
#         # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
#     source = await YTDLSource.create_source(ctx, search, loop=bot.loop, download=False)

#     await player.queue.put(source)


@client.command()
async def ask(ctx, *, question):
    reply = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes – definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        "Don't count on it.",
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.',
        'Pardon.',
        'Very much!'
    ]
    await ctx.send(f"""Question: {question}\n Answer: {random.choice(reply)}""")

@client.command()
async def roast(ctx, *, member):
    roasts = ["My phone battery lasts longer than your business.",
        "Oh you’re talking to me, I thought you only talked behind my back.",
        "My name must taste good because it’s always in your mouth.", 
        "Don’t you get tired of putting make up on two faces every morning?",
        "Too bad you can’t count jumping to conclusions and running your mouth as exercise.",
        "Is your drama going to an intermission soon?",
        "I’m an acquired taste. If you don’t like me, acquire some taste.",
        "It’s a shame you can’t Photoshop your personality.",
        "I don’t sugarcoat shit. I’m not Willy Wonka.",
        "Acting like a prick doesn’t make yours grow bigger.",
        "The smartest thing that ever came out of your mouth was a puke.",
        "Calm down. Take a deep breath and then hold it for about twenty minutes.",
        "Jealousy is a disease. Get well soon.",
        "When karma comes back to punch you in the face, I want to be there in case it needs help.",
        "You have more faces than Mount Rushmore.",
        "Sorry, sarcasm falls out of my mouth like bullshit falls out of yours.",
        "Don’t mistake my silence for weakness. No one plans a murder out loud.",
        "I’m sorry you got offended that one time you were treated the way you treat everyone all the time.",
        "Maybe you should eat make-up so you’ll be pretty on the inside too.",
        "You’re entitled to your incorrect opinion.",
        "Whoever told you to be yourself gave you really bad advice.",
        "If I had a face like yours I’d sue my parents.",
        "Where’s your off button?",
        "I didn’t change. I grew up. You should try it sometime.",
        "I thought I had the flu, but then I realized your face makes me sick to my stomach.",
        "The people who know me the least have the most to say.",
        "I’m jealous of people who don’t know you.",
        "I’m sorry that my brutal honesty inconvenienced your ego.",
        "You sound reasonable… Time to up my medication.",
        "Aww, it’s so cute when you try to talk about things you don’t understand.",
        "Is there an app I can download to make you disappear?",
        "I’m sorry, you seem to have mistaken me with a woman who will take your shit.",
        "I’m visualizing duck tape over your mouth.",
        "90 percent of your ‘beauty’ could be removed with a Kleenex.",
        "I suggest you do a little soul searching. You might just find one.",
        "Some people should use a glue stick instead of chapstick.",
        "My hair straightener is hotter than you.",
        "I have heels higher than your standards.",
        "I’d smack you, but that would be animal abuse.",
        "Why is it acceptable for you to be an idiot but not for me to point it out?",
        "If you’re offended by my opinion, you should hear the ones I keep to myself.",
        "If you’re going to be a smart person, first you have to be smart, otherwise you’re just a person.",
        "Your face is fine but you will have to put a bag over that personality.",
        "Hey, I found your nose, it’s in my business again!",
        "I’m not an astronomer but I am pretty sure the earth revolves around the sun and not you.",
        "I might be crazy, but crazy is better than stupid.",
        "It’s scary to think people like you are allowed to vote.",
        "Keep rolling your eyes. Maybe you’ll find your brain back there.",
        "No, no. I am listening. It just takes me a moment to process so much stupid information all at once.",
        "I’m sorry, what language are you speaking? It sounds like bullshit.",
        "Everyone brings happiness to a room. I do when I enter, you do when you leave.",
        "I keep thinking you can’t get any dumber and you keep proving me wrong. ",
        "I’m not shy. I just don’t like you.",
        "Your crazy is showing. You might want to tuck it back in.",
        "I am allergic to stupidity, so I break out in sarcasm.",
        "You’re like a plunger. You like to bring up old shit.",
        "I am not ignoring you. I am simply giving you time to reflect on what an idiot you are being.",
        "I hide behind sarcasm because telling you to go fuck yourself is rude in most social situations.",
        "You’re the reason I prefer animals to people.",
        "You’re not pretty enough to have such an ugly personality.",
        "I’d explain it to you but I left my English-to-Dumbass Dictionary at home.",
        "You don’t like me, then get out. Problem solved."
    ]
    formality = [
        'Here you go, ',
        'Get ready!! ',
        'I have got one, ',
        'Sure, ',
        'Want a roast? ,',
        'Anyone said roast? ,'
    ]
    await ctx.send(f"""{random.choice(formality)} \n {random.choice(roasts)}""")

@client.command(aliases = ['funfacts'])
async def funfact(ctx):
    fun_facts = [
        "Babies have around 100 more bones than adults",
        "The Eiffel Tower can be 15 cm taller during the summer",
        "20 percent of Earth’s oxygen is produced by the Amazon rainforest",
        "Some metals are so reactive that they explode on contact with water",
        "A teaspoonful of neutron star would weigh 6 billion tons",
        "Hawaii moves 7.5cm closer to Alaska every year",
        "Chalk is made from trillions of microscopic plankton fossils",
        "In 2.3 billion years it will be too hot for life to exist on Earth",
        "Polar bears are nearly undetectable by infrared cameras",
        "It takes 8 minutes, 19 seconds for light to travel from the Sun to the Earth",
        "If you took out all the empty space in our atoms, the human race could fit in the volume of a sugar cube",
        " Stomach acid is strong enough to dissolve stainless steel",
        "The Earth is a giant magnet",
        "Venus is the only planet to spin clockwise",
        "A flea can accelerate faster than the Space Shuttle",
        "Water can boil and freeze at the same time",
        "Lasers can get trapped in a waterfall",
        "We've got spacecraft hurtling towards the edge of our Solar System really, really fast",
        "An egg looks like a crazy jellyfish underwater",
        "You can prove Pythagoras' theorem with fluid",
        "Popping your knuckles isn't necessarily bad for you",
        "A single solar flare can release the equivalent energy of millions of 100-megaton atomic bombs",
        "Cats always land on their feet, thanks to physics",
        "You'd be better off surviving a grenade on land rather than underwater",
        "If you spin a ball as you drop it, it flies",
        "A human organ that no-one knew about has been hiding in plain sight all this time, Called mesentery.",
        "The Earth appears to have a whole new underground continent called Zealandia.",
        "The Earth appears to have a whole new underground continent called Zealandia.",
        "Pugs’ cute little flat faces are the result of a genetic mutation.",
        "For the first time in human history, gene-editing has been performed to fix a mutation for an inherited disease in embryos.",
        "Giant penguins about the size of a grown man waddled around New Zealand about 59 million years ago.",
        "The world’s smallest fidget spinner is 100 microns wide.\nIt is smaller than the width of a human hair and is barely visible to the naked eye.",
        "Lungs do more than help us breathe – a surprising discovery has found they also make blood. ",
        "A new state of matter exists (alongside solid, liquid and gaseous states) and it is known as time crystals.",
        "Great apes, including chimpanzees and orangutans, have absolutely no appreciation of music whatsoever.\nResearch has shown they can’t tell the difference between Beethoven and Bieber, and that music is all just meaningless sound to them.",
        "Humans accidentally created a protective bubble around Earth.\nDecades of use of very low frequency (VLF) radio communications have resulted in an artificial cocoon that could help protect the planet from solar flares and radiation particles.",
        "Precious metals on earth, such as gold and platinum, may have originated in the stars.",
        "The Kepler-90 star system has as many planets as our own solar system, making us tied for the most planets revolving around a single star known so far.",
        "Pandas are black and white because their patterns serve as a combination of communication and camouflage, according to a study published in Behavioral Ecology.",
        "Scientists may finally have an answer to why eggs come in different shapes and, apparently, it is all down to the bird’s flying ability.",
        "Scientists at Harvard have stored a GIF animation of a galloping horse in the DNA of bacteria, using the Crispr-Cas9 tool.",
        "Bees have been shown to understand the concept of zero.\nScientists discovered this after training the insects to count shapes, following previous research that revealed they can count to four.",
        "Flea's can jump 130 times higher than their own height. In human terms this is equal to a 6ft. person jumping 780 ft. into the air.",
        "The world's largest amphibian is the giant salamander. It can grow up to 5 ft. in length.",
        "100 years ago: The first virus was found in both plants and animals.",
        "The smallest bone in the human body is the stapes or stirrup bone located in the middle ear. It is approximately .11 inches (.28 cm) long.",
        "The longest cells in the human body are the motor neurons. They can be up to 4.5 feet (1.37 meters) long and run from the lower spinal cord to the big toe.",
        "The blue whale can produce sounds up to 188 decibels. This is the loudest sound produced by a living animal and has been detected as far away as 530 miles.",
        "The largest man-made lake in the U.S. is Lake Mead, created by Hoover Dam.",
        "The human eye blinks an average of 4,200,000 times a year.",
        "It takes approximately 12 hours for food to entirely digest.",
        "Human jaw muscles can generate a force of 200 pounds (90.8 kilograms) on the molars.",
        "The Skylab astronauts grew 1.5 - 2.25 inches (3.8 - 5.7 centimeters) due to spinal lengthening and straightening as a result of zero gravity.",
        "An inch (2.5 centimeters) of rain water is equivalent to 15 inches (38.1 centimeters) of dry, powdery snow.",
        "The longest living cells in the body are brain cells which can live an entire lifetime.",
        "Armadillos, opossums, and sloth's spend about 80percent of their lives sleeping",
        "The fastest computer in the world is the CRAY Y-MP C90 supercomputer. It has two gigabytes of central memory and 16 parallel central processor units.",
        "The heaviest human brain ever recorded weighed 5 lb. 1.1 oz. (2.3 kg.).",
        "The ears of a cricket are located on the front legs, just below the knee.",
        "The leg muscles of a locust are about 1000 times more powerful than an equal weight of human muscle.",
        "In a full grown rye plant, the total length of fine root hairs may reach 6600 miles (10,645 km).",
        "A large sunspot can last for about a week.",
        "If you could throw a snowball fast enough, it would totally vaporize when it hit a brick wall.",
        "Boron nitride (BN) is the second hardest substance known to man.",
        "The seeds of an Indian Lotus tree remain viable for 300 to 400 years.",
        "The only letter not appearing on the Periodic Table is the letter 'J'",
        "Velcro was invented by a Swiss guy who was inspired by the way burrs attached to clothing.",
        "Hershey's Kisses are called that because the machine that makes them looks like it's kissing the conveyor belt.",
        "The microwave was invented after a researcher walked by a radar tube and a chocolate bar melted in his pocket.",
        "Super Glue was invented by accident. The researcher was trying to make optical coating materials, and would test their properties by putting them between two prisms and shining light through them. When he tried the cyano-acrylate, he couldn't get the prisms apart.",
        "No matter its size or thickness, no piece of paper can be folded in half more than 7 times.",
        "A car traveling at 80 km/h uses half its fuel to overcome wind resistance.",
        "Knowledge is growing so fast that ninety per cent of what we will know in fifty years time, will be discovered in those fifty years.",
        "The typewriter was invented in 1829, and the automatic dishwasher in 1889.",
        "According to an old English system of time units, a moment is one and a half minutes.",
        "When glass breaks, the cracks move at speeds of up to 3,000 miles per hour.",
        "By raising your legs slowly and laying on your back, you can't sink in quicksand.",
        "Ten minutes of one hurricane contains enough energy to match the nuclear stockpiles of the world.",
        "Cars were first made with ignition keys in 1949.",
        "Alexander Graham Bell, who invented the telephone, also set a world water-speed record of over seventy miles an hour at the age of seventy two.",
        "It is energy-efficient to turn off a fluorescent light only if it will not be used again within an hour or more. This is because of the high voltage needed to turn it on, and the shortened life this high voltage causes.",
        "The Earth's average velocity orbiting the sun is 107,220 km per hour.",
        "The United States consumes 25 percent of all the world’s energy.",
        "Flying from London to New York by Concord, due to the time zones crossed, you can arrive 2 hours before you leave.",
        "There is enough fuel in a full tank of a Jumbo Jet to drive an average car four times around the world.",
        "The surface speed record on the moon is 10.56 miles per hour. It was set with the lunar rover.",
        "The moon is one million times drier than the Gobi Desert.",
        "A Boeing 707 uses four thousand gallons of fuel in its take-off climb.",
        "The planet Saturn has a density lower than water. So, if placed in water it would float.",
        "It takes 70 percent less energy to produce a ton of paper from recycled paper than from trees.",
        "Every year in the US, 625 people are struck by lightning.",
        "Hawaii is moving toward Japan 4 inches every year.",
        "The rocket engine has to supply its own oxygen so it can burn its fuel in outer space.",
        "A stroke of lightning discharges from 10 to 100 million volts & 30,000 amperes of electricity.",
        "A bolt of lightning is about 54,000°F (30,000°C); six times hotter than the Sun.",
        "Hydrogen is the most abundant element in the Universe (75%).",
        "The Earth weighs 6.6 sextillion tons, or 5.97 x 1024 kg.",
        "The highest temperature on Earth was 136°F (58°C) in Libya in 1922.",
        "The lowest temperature on Earth was -128.6°F (-89.6°C) in Antarctica in 1983.",
        "The average ocean floor is 12,000 feet.",
        "The temperature can be determined by counting the number of cricket chirps in fourteen seconds and adding 40.",
        "House flies have a lifespan of two weeks.",
        "Chimps are the only animals that can recognize themselves in a mirror.",
        "Starfish don't have brains.",
        "The average person falls asleep in seven minutes.",
        "The longest recorded flight of a chicken is thirteen seconds",
        "Cats have over one hundred vocal sounds, while dogs only have about ten. ",
        "An iguana can stay under water for twenty-eight minutes.",
        "The common goldfish is the only animal that can see both infra-red and ultra-violet light.",
        "The pupil of an octopus' eye is rectangular.",
        "The leg bones of a bat are so thin that no bat can walk.",
        "Tigers have striped skin, not just striped fur.",
        "A cat's jaws cannot move sideways.",
        "There are more beetles than any other kind of creature in the world.",
        "Certain frogs that can survive the experience of being frozen.",
        "Only humans sleep on their backs.",
        "The human brain is 80% water.",
        "Everyone's tongue print is different."
        "As an adult, you have more than 20 square feet of skin on your body--about the same square footage as a blanket for a queen-sized bed."
        "In your lifetime, you'll shed over 40 pounds of skin."
        "15 million blood cells are produced and destroyed in the human body every second."
        "Every minute, 30-40,000 dead skin cells fall from your body."
        "The brain uses more than 25% of the oxygen used by the human body."
        "If your mouth was completely dry, you would not be able to distinguish the taste of anything."
        "There are more living organisms on the skin of a single human being than there are human beings on the surface of the earth."
        "Muscles are made up of bundles from about 5 in the eyelid to about 200 in the buttock muscle."
        "Muscles in the human body (640 in total) make up about half of the body weight."
        "The human body has enough fat to produce 7 bars of soap."
        "The human head is a quarter of our total length at birth, but only an eighth of our total length by the time we reach adulthood."
        "Most people blink about 17,000 times a day."
        "Moths have no stomach."
        "Hummingbirds can't walk."
        "Sea otters have 2 coats of fur."
        "A starfish can turn its stomach inside out."
        "A zebra is white with black stripes."
        "The animal with the largest brain in relation to its body is the ant."
        "The largest eggs in the world are laid by a shark."
        "A crocodile’s tongue is attached to the roof of its mouth."
        "Crocodiles swallow stones to help them dive deeper."
        "Giraffes are unable to cough."
        "Sharks are immune to cancer."
        "Despite the hump, a camel’s spine is straight."
        "Cheetah's can accelerate from 0 to 70 km/h in 3 seconds."
        "A giraffe's neck contains the same number of vertebrae as a human."
        "The heart of giraffe is two feet long, and can weigh as much as twenty four pounds."
        "On average, Elephants sleep for about 2 hours per day."
        "Lobsters have blue blood."
        "Shark's teeth are literally as hard as steel."
        "A mosquito has 47 teeth."
        "Oxygen, carbon, hydrogen and nitrogen make up 90% of the human body."
        "Seventy percent of the dust in your home consists of shed human skin"
        "Fish are the only vertebrates that outnumber birds."
        "A cockroach can live for several weeks without its head."
        "The average human produces a quart of saliva a day -- about 10,000 gallons in a lifetime"
        "Elephants have been known to remain standing after they die."
        "The embryos of tiger sharks fight each other while in their mother's womb, the survivor being the baby shark that is born."
        "Ants do not sleep."
        "Nearly a third of all bottled drinking water purchased in the US is contaminated with bacteria."
        "Rats multiply so quickly that in 18 months, two rats could have over 1 million descendents."
        "An Astronaut can be up to 2 inches taller returning from space. The cartilage disks in the spine expand in the absence of gravity."
        "The oldest known fossil is of a single-celled organism, blue-green algae, found in 3.2 billion year-old stones in South Africa."
        "The oldest multicellular fossils date from ~700 million years ago."
        "The earliest cockroach fossils are about 280 million years old."
        "Healthy nails grow about 2 cm each year. Fingernails grow four times as fast as toenails."
        "20/20 vision means the eye can see normally at 20 feet. 20/15 is better; the eye can see at 20 feet what another eye sees at 15 feet."
        "The average person has 100,000 hairs on his/her head. Each hair grows about 5 inches (12.7 cm) every year."
        "There are 60,000 miles (97,000 km) in blood vessels in every human."
    ]
    formality = [
        'Here you go, ',
        'Quick facts ',
        'I have got one, ',
        'Sure, ',
        'Want a fun fact? ,'
    ]
    await ctx.send(f"""{random.choice(formality)} \n {random.choice(fun_facts)}""")

@client.command(aliases = ['jokes', 'fun', 'funny'])
async def joke(ctx):
    jokes_list = [
        'Teacher: "Kids, what does the chicken give you?"\nStudent: "Meat!"\nTeacher: "Very good! Now what does the pig give you?"\nStudent: "Bacon!"\nTeacher: "Great! And what does the fat cow give you?"\nStudent: "Homework!"',
        'A child asked his father, "How were people born?" So his father said, "Adam and Eve made babies, then their babies became adults and made babies, and so on." The child then went to his mother, asked her the same question and she told him, "We were monkeys then we evolved to become like we are now." The child ran back to his father and said, "You lied to me!" His father replied, "No, your mom was talking about her side of the family',
        'My friend thinks he is smart. He told me an onion is the only food that makes you cry, so I threw a coconut at his face.',
        "What happens to a frog's car when it breaks down?\n It gets toad away.",
        "Q: Is Google male or female?\n A: Female, because it doesn't let you finish a sentence before making a suggestion.",
        'Mr. and Mrs. Brown had two sons. One was named Mind Your Own Business & the other was named Trouble. One day the two boys decided to play hide and seek. Trouble hid while Mind Your Own Business counted to one hundred. Mind Your Own Business began looking for his brother behind garbage cans and bushes. Then he started looking in and under cars until a police man approached him and asked, "What are you doing?" "Playing a game," the boy replied. "What is your name?" the officer questioned. "Mind Your Own Business." Furious the policeman inquired, "Are you looking for trouble?!" The boy replied, "Why, yes."',
        'Q: What did the duck say when he bought lipstick?\nA: "Put it on my bill."',
        'Reaching the end of a job interview, the Human Resources Officer asks a young engineer fresh out of the Massachusetts Institute of Technology, "And what starting salary are you looking for?" The engineer replies, "In the region of $125,000 a year, depending on the benefits package." The interviewer inquires, "Well, what would you say to a package of five weeks vacation, 14 paid holidays, full medical and dental, company matching retirement fund to 50% of salary, and a company car leased every two years, say, a red Corvette?" The engineer sits up straight and says, "Wow! Are you kidding?" The interviewer replies, "Yeah, but you started it."',
        'A blonde and a redhead have a ranch. They have just lost their bull. The women need to buy another, but only have $500. The redhead tells the blonde, "I will go to the market and see if I can find one for under that amount. If I can, I will send you a telegram." She goes to the market and finds one for $499. Having only one dollar left, she goes to the telegraph office and finds out that it costs one dollar per word. She is stumped on how to tell the blonde to bring the truck and trailer. Finally, she tells the telegraph operator to send the word "comfortable." Skeptical, the operator asks, "How will she know to come with the trailer from just that word?" The redhead replies, "Shes a blonde so she reads slow: Come for ta bull."',
        'A boy asks his fath9er, "Dad, are bugs good to eat?" "Thats disgusting. Dont talk about things like that over dinner," the dad replies. After dinner the father asks, "Now, son, what did you want to ask me?" "Oh, nothing," the boy says. "There was a bug in your soup, but now it’s gone."',
        'Q: Why was six scared of seven?\nA: Because seven "ate" nine.',
        "Q: Why did the witches' team lose the baseball game?\nA: Their bats flew away.",
        "Q: Can a kangaroo jump higher than the Empire State Building?\nA: Of course. The Empire State Building can't jump.",
        "Q: Why couldn't the leopard play hide and seek?\nA: Because he was always spotted.",
        "Q: Did you hear about the kidnapping at school?\nA: It's okay. He woke up.",
        "Q: Why did the can crusher quit his job?\nA: Because it was soda pressing."    ,
        'Math Teacher: "If I have 5 bottles in one hand and 6 in the other hand, what do I have?"\nStudent: "A drinking problem."',
        'Q: Why did Adele cross the road?\nA: To sing, "Hello from the other side!"',
        'How is Christmas like your job? You do all the work and the fat guy in the suit gets all the credit.',
        'Teacher: "Which book has helped you the most in your life?"\nStudent: "My fathers check book!"',
        'A mom texts, "Hi! Son, what does IDK, LY, & TTYL mean?" He texts back, "I Dont Know, Love You, & Talk To You Later." The mom texts him, "Its ok, dont worry about it. Ill ask your sister, love you too.',
        'Q: Can February march?\nA: No, but April may.',
        'I was wondering why the ball kept getting bigger and bigger, and then it hit me.',
        "Don't break anybody's heart; they only have 1. Break their bones; they have 206.",
        'Two guys are walking through a game park & they come across a lion that has not eaten for days. The lion starts chasing the two men. They run as fast as they can and the one guy starts getting tired and decides to say a prayer, "Please turn this lion into a Christian, Lord." He looks to see if the lion is still chasing and he sees the lion on its knees. Happy to see his prayer answered, he turns around and heads towards the lion. As he comes closer to the lion, he hears the it saying a prayer: "Thank you Lord for the food I am about to receive."',
        'Q: Why does Humpty Dumpty love autumn?\nA: Because Humpty Dumpty had a great fall.',
        "A: I have the perfect son.\nB: Does he smoke?\nA: No, he doesn’t.\nB: Does he drink whiskey?\nA: No, he doesn’t.\nB: Does he ever come home late?\nA: No, he doesn’t.\nB: I guess you really do have the perfect son. How old is he?\nA: He will be six months old next Wednesday.",
        "Q: What do you call a pig that does karate?\nA: A pork chop.",
        'A police officer attempts to stop a car for speeding and the guy gradually increases his speed until hes topping 100 mph. The man eventually realizes he cant escape and finally pulls over. The cop approaches the car and says, "Its been a long day and my shift is almost over, so if you can give me a good excuse for your behavior, Ill let you go." The guy thinks for a few seconds and then says, "My wife ran away with a cop about a week ago. I thought you might be that officer trying to give her back!"',
        "A man got hit in the head with a can of Coke, but he was alright because it was a soft drink.",
        'A bank robber pulls out gun points it at the teller, and says, "Give me all the money or youre geography!" The puzzled teller replies, "Did you mean to say or youre history?" The robber says, "Dont change the subject!"'
        'Q: How do you make a tissue dance?\nA: Put a little boogie in it.',
        "Q: Why can't you trust an atom?\nA: Because they make up everything.",
        'Brunette: "Where were you born?"\nBlonde: "The United States."\nBrunette: "Which part?"\nBlonde: "My whole body."',
        "Q: Why did the fish blush?\nA: Because it saw the ocean's bottom.",
        "Q: What do computers eat for a snack?\nA: Microchips!",
        "Q: What's the difference between a guitar and a fish?\nA: You can tune a guitar, but you can't tuna fish.",
        "Did you hear about the guy whose whole left side was cut off? He's all right now.",
        "Why is it that your nose runs, but your feet smell?",
        "If Mary had Jesus, and Jesus is the lamb of God, does that mean Mary had a little lamb?",
        "If you ever get cold, just stand in the corner of a room for a while. They're normally around 90 degrees.",
        "Q: What is the tallest building in the entire world?\nA: The library, because it has so many stories.",
        "Q: Why did the school kids eat their homework?\nA: Because their teacher told them it was a piece of cake.",
        "Q: If you have 13 apples in one hand and 10 oranges in the other, what do you have?\nA: Big hands.",
        "Whoever invented knock knock jokes should get a no bell prize.",
        "Q: What did the green grape say to the purple grape?\nA: 'Breathe, stupid!'",
        "The energizer bunny was arrested on a charge of battery.",
        'Bob: "Holy crap, I just fell off a 50 ft ladder."\nJim: "Oh my God, are you okay?"\n\nBob: "Yeah its a good thing I fell off the first step."',
        'Teacher: "What is the chemical formula for water?"\nStudent: "HIJKLMNO."\nTeacher: "What are you talking about?"\nStudent: "Yesterday you said itss H to O!"',
        'Teacher: "Anyone who thinks hes stupid may stand up!"\nNobody stands up\nTeacher: "Im sure there are some stupid students over here!!"\nLittle Johnny stands up\nTeacher: "Ohh, Johnny you think youre stupid?"\nLittle Johnny: "No... i just feel bad that youre standing alone..."',
        "If the right side of the brain controls the left side of the body, then lefties are the only ones in their right mind.",
        'How many snowboarders does it take to screw in a lightbulb? 50: 3 to die trying, 1 to actually pull it off, and 46 other to say, "man, I could do that!"',
        "Q: How many politicians does it take to change a light bulb?\nA: Two: one to change it and another one to change it back again.",
        "Q: How do trees access the internet?\nA: They log in.",
        "Q: What do you get when you cross a fish and an elephant?\nA: Swimming trunks.",
        'Q: What is the difference between a teacher and a train?\nA: One says, "Spit out your gum," and the other says, "Choo choo choo!"',
        'Q. What do clouds do when they become rich?\nA. They make it rain!'
        'Q. What is the color of the wind?\nA. Blew.',
        "Q: Why shouldn't you write with a broken pencil?\nA: Because it’s pointless!"
    ]
    formality = [
        'A joke: ',
        'This is funny, ',
        'Joke coming right along ',
        'I burst out at this',
        "Come have a laugh off ,"
    ]
    await ctx.send(f"""{random.choice(formality)} \n\n {random.choice(jokes_list)}""")

@client.command(alaises = ['riddles'])
async def riddle(ctx):
    riddles_list =[
        "Riddle: What has to be broken before you can use it?\nAnswer: An egg",
        "Riddle: I’m tall when I’m young, and I’m short when I’m old. What am I?\nAnswer: A candle",
        "Riddle: What month of the year has 28 days?\nAnswer: All of them",
        "Riddle: What is full of holes but still holds water?\nAnswer: A sponge",
        "Riddle: What question can you never answer yes to?\nAnswer: Are you asleep yet?",
        "Riddle: What is always in front of you but can’t be seen?\nAnswer: The future",
        "Riddle: There’s a one-story house in which everything is yellow. Yellow walls, yellow doors, yellow furniture. What color are the stairs?\nAnswer: There aren’t any—it’s a one-story house.",
        "Riddle. What can you break, even if you never pick it up or touch it?\nAnswer: A promise",
        "Riddle: What goes up but never comes down?\nAnswer: Your age",
        "Riddle: A man who was outside in the rain without an umbrella or hat didn’t get a single hair on his head wet. Why?\nAnswer: He was bald.",
        "Riddle: What gets wet while drying?\nAnswer: A towel",
        "Riddle: What can you keep after giving to someone?\nAnswer: Your word",
        "Riddle: I shave every day, but my beard stays the same. What am I?\nAnswer: A barber",
        "Riddle: You see a boat filled with people, yet there isn’t a single person on board. How is that possible?\nAnswer: All the people on the boat are married.",
        "Riddle: You walk into a room that contains a match, a kerosene lamp, a candle and a fireplace. What would you light first?\nAnswer: The match",
        "Riddle: A man dies of old age on his 25 birthday. How is this possible?\nAnswer: He was born on February 29.",
        "Riddle: I have branches, but no fruit, trunk or leaves. What am I?\nAnswer: A bank",
        "Riddle: What can’t talk but will reply when spoken to?\nAnswer: An echo",
        "Riddle: The more of this there is, the less you see. What is it?\nAnswer: Darkness",
        "Riddle: David’s parents have three sons: Snap, Crackle, and what’s the name of the third son?\nAnswer: David",
        "Riddle: I follow you all the time and copy your every move, but you can’t touch me or catch me. What am I?\nAnswer: Your shadow",
        "Riddle: What has many keys but can’t open a single lock?\nAnswer: A piano",
        "Riddle: What can you hold in your left hand but not in your right?\nAnswer: Your right elbow",
        "Riddle: What is black when it’s clean and white when it’s dirty?\nAnswer: A chalkboard",
        "Riddle: What gets bigger when more is taken away?\nAnswer: A hole",
        "Riddle: I’m light as a feather, yet the strongest person can’t hold me for five minutes. What am I?\nAnswer: Your breath",
        "Riddle: I’m found in socks, scarves and mittens; and often in the paws of playful kittens. What am I?\nAnswer: Yarn",
        "Riddle: Where does today come before yesterday?\nAnswer: The dictionary",
        "Riddle: What invention lets you look right through a wall?\nAnswer: A window",
        "Riddle: If you’ve got me, you want to share me; if you share me, you haven’t kept me. What am I?\nAnswer: A secret",
        "Riddle: What can’t be put in a saucepan?\nAnswer: It’s lid",
        "Riddle: What goes up and down but doesn’t move?\nAnswer: A staircase",
        "Riddle: If you’re running in a race and you pass the person in second place, what place are you in?\nAnswer: Second place",
        "Riddle: It belongs to you, but other people use it more than you do. What is it?\nAnswer: Your name",
        "Riddle: What has lots of eyes, but can’t see?\nAnswer: A potato",
        "Riddle: What has one eye, but can’t see?\nAnswer: A needle",
        "Riddle: What has many needles, but doesn’t sew?\nAnswer: A Christmas tree",
        "Riddle: What has hands, but can’t clap?\nAnswer: A clock",
        "Riddle: What has legs, but doesn’t walk?\nAnswer: A table",
        "Riddle: What has one head, one foot and four legs?\nAnswer: A bed",
        "Riddle: What can you catch, but not throw?\nAnswer: A cold",
        "Riddle: What kind of band never plays music?\nAnswer: A rubber band",
        "Riddle: What has many teeth, but can’t bite?\nAnswer: A comb",
        "Riddle: What is cut on a table, but is never eaten?\nAnswer: A deck of cards",
        "Riddle: What has words, but never speaks?\nAnswer: A book",
        "Riddle: What runs all around a backyard, yet never moves?\nAnswer: A fence ",
        "Riddle: What can travel all around the world without leaving its corner?\nAnswer: A stamp",
        "Riddle: What has a thumb and four fingers, but is not a hand?\nAnswer: A glove",
        "Riddle: What has a head and a tail but no body?\nAnswer: A coin",
        "Riddle: Where does one wall meet the other wall?\nAnswer: On the corner",
        "Riddle: What building has the most stories?\nAnswer: The library ",
        "Riddle: What tastes better than it smells?\nAnswer: Your tongue",
        "Riddle: What has 13 hearts, but no other organs?\nAnswer: A deck of cards",
        "Riddle: It stalks the countryside with ears that can’t hear. What is it?\nAnswer: Corn",
        "Riddle: What kind of coat is best put on wet?\nAnswer: A coat of paint",
        "Riddle: What has a bottom at the top?\nAnswer: Your legs",
        "Riddle: What has four wheels and flies?\nAnswer: A garbage truck",
        "Riddle: I am an odd number. Take away a letter and I become even. What number am I?\nAnswer: Seven",
        "Riddle: If two’s company, and three’s a crowd, what are four and five?\nAnswer: Nine",
        "Riddle: What three numbers, none of which is zero, give the same result whether they’re added or multiplied?\nAnswer: One, two and three",
        "Riddle: Mary has four daughters, and each of her daughters has a brother. How many children does Mary have?\nAnswer: Five—each daughter has the same brother.",
        "Riddle: Which is heavier: a ton of bricks or a ton of feathers?\nAnswer: Neither—they both weigh a ton.",
        "Riddle: Three doctors said that Bill was their brother. Bill says he has no brothers. How many brothers does Bill actually have?\nAnswer: None. He has three sisters.",
        "Riddle: Two fathers and two sons are in a car, yet there are only three people in the car. How?\nAnswer: They are a grandfather, father and son.",
        "Riddle: The day before yesterday I was 21, and next year I will be 24. When is my birthday?\nAnswer: December 31; today is January 1.",
        "Riddle: A little girl goes to the store and buys one dozen eggs. As she is going home, all but three break. How many eggs are left unbroken?\nAnswer: Three",
        "Riddle: A man describes his daughters, saying, 'They are all blonde, but two; all brunette but two; and all redheaded but two.' How many daughters does he have?\nAnswer: Three: A blonde, a brunette and a redhead",
        "Riddle: If there are three apples and you take away two, how many apples do you have?\nAnswer: You have two apples.",
        "Riddle: A girl has as many brothers as sisters, but each brother has only half as many brothers as sisters. How many brothers and sisters are there in the family?\nAnswer: Four sisters and three brothers",
        "Riddle: What five-letter word becomes shorter when you add two letters to it?\nAnswer: Short",
        "Riddle: What begins with an “e” and only contains one letter?\nAnswer: An envelope",
        "Riddle: A word I know, six letters it contains, remove one letter and 12 remains. What is it?\nAnswer: Dozens",
        "Riddle: What would you find in the middle of Toronto?\nAnswer: The letter 'o''",
        "Riddle: You see me once in June, twice in November and not at all in May. What am I?\nAnswer: The letter 'e'",
        "Riddle: Two in a corner, one in a room, zero in a house, but one in a shelter. What is it?\nAnswer: The letter 'r'",
        "Riddle: I am the beginning of everything, the end of everywhere. I’m the beginning of eternity, the end of time and space. What am I?\nAnswer: Also the letter 'e'",
        "Riddle: What 4-letter word can be written forward, backward or upside down, and can still be read from left to right?\nAnswer: NOON",
        "Riddle: Forward I am heavy, but backward I am not. What am I?\nAnswer: The word 'not'",
        "Riddle: What is 3/7 chicken, 2/3 cat and 2/4 goat?\nAnswer: Chicago",  
        "Riddle: I am a word of letters three; add two and fewer there will be. What word am I?\nAnswer: Few",
        "Riddle: What word of five letters has one left when two are removed?\nAnswer: Stone",
        "Riddle: What is the end of everything?\nAnswer: The letter “g”",
        "Riddle: What word is pronounced the same if you take away four of its five letters?\nAnswer: Queue",
        "Riddle: I am a word that begins with the letter “i.” If you add the letter “a” to me, I become a new word with a different meaning, but that sounds exactly the same. What word am I?\nAnswer: Isle (add “a” to make “aisle”)",
        "Riddle: What word in the English language does the following: The first two letters signify a male, the first three letters signify a female, the first four letters signify a great, while the entire world signifies a great woman. What is the word?\nAnswer: Heroine",
        "Riddle: What is so fragile that saying its name breakWs it?\nAnswer: Silence.",
        "Riddle: What can run but never walks, has a mouth but never talks, has a head but never weeps, has a bed but never sleeps?\nAnswer: A river",
        "Riddle: Speaking of rivers, a man calls his dog from the opposite side of the river. The dog crosses the river without getting wet, and without using a bridge or boat. How?\nAnswer: The river was frozen.",
        "Riddle: What can fill a room but takes up no space?\nAnswer: Light",
        "Riddle: If you drop me I’m sure to crack, but give me a smile and I’ll always smile back. What am I?\nAnswer: A mirror",
        "Riddle: The more you take, the more you leave behind. What are they?\nAnswer: Footsteps",
        "Riddle: I turn once, what is out will not get in. I turn again, what is in will not get out. What am I?\nAnswer: A key",   
        "Riddle: People make me, save me, change me, raise me. What am I?\nAnswer: Money",
        "Riddle: What breaks yet never falls, and what falls yet never breaks?\nAnswer: Day, and night",
        "Riddle: What goes through cities and fields, but never moves?\nAnswer: A road",
        "Riddle: I am always hungry and will die if not fed, but whatever I touch will soon turn red. What am I?\nAnswer: Fire",
        "Riddle: The person who makes it has no need of it; the person who buys it has no use for it. The person who uses it can neither see nor feel it. What is it?\nAnswer: A coffin",
        "Riddle: A man looks at a painting in a museum and says, “Brothers and sisters I have none, but that man’s father is my father’s son.” Who is in the painting?\nAnswer: The man’s son",
        "Riddle: With pointed fangs I sit and wait; with piercing force I crunch out fate; grabbing victims, proclaiming might; physically joining with a single bite. What am I?\nAnswer: A stapler",
        "Riddle: I have lakes with no water, mountains with no stone and cities with no buildings. What am I?\nAnswer: A map",
        "Riddle: What does man love more than life, hate more than death or mortal strife; that which contented men desire; the poor have, the rich require; the miser spends, the spendthrift saves, and all men carry to their graves?\nAnswer: Nothing"
    ]
    formality = [
        'A riddle: ',
        'This is nice, ',
        'Riddle incoming... ',
        'you will have to be clever with this',
        "twist your brain a bit,"
    ]
    await ctx.send(f"""{random.choice(formality)} \n\n {random.choice(riddles_list)}""")

@client.command()
async def twister(ctx):
    twisters_list = [
        "Peter Piper picked a peck of pickled peppers\nA peck of pickled peppers Peter Piper picked\nIf Peter Piper picked a peck of pickled peppers\nWhere’s the peck of pickled peppers Peter Piper picked?",
        "Betty Botter bought some butter\nBut she said the butter’s bitter\nIf I put it in my batter, it will make my batter bitter\nBut a bit of better butter will make my batter better\nSo ‘twas better Betty Botter bought a bit of better butter",
        "How much wood would a woodchuck chuck if a woodchuck could chuck wood?\nHe would chuck, he would, as much as he could, and chuck as much wood\nAs a woodchuck would if a woodchuck could chuck wood",
        "She sells seashells by the seashore",
        "How can a clam cram in a clean cream can?",
        "I scream, you scream, we all scream for ice cream",
        "I saw Susie sitting in a shoeshine shop",
        "Susie works in a shoeshine shop. Where she shines she sits, and where she sits she shines",
        "Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair. Fuzzy Wuzzy wasn’t fuzzy, was he?",
        "Can you can a can as a canner can can a can?",
        "I have got a date at a quarter to eight; I’ll see you at the gate, so don’t be late",
        "You know New York, you need New York, you know you need unique New York",
        "I saw a kitten eating chicken in the kitchen",
        "If a dog chews shoes, whose shoes does he choose?",
        "I thought I thought of thinking of thanking you",
        "I wish to wash my Irish wristwatch",
        "Near an ear, a nearer ear, a nearly eerie ear",
        "Eddie edited it",
        "Willie’s really weary",
        "A big black bear sat on a big black rug",
        "Tom threw Tim three thumbtacks",
        "He threw three free throws",
        "Nine nice night nurses nursing nicely",
        "So, this is the sushi chef",
        "Four fine fresh fish for you",
        "Wayne went to wales to watch walruses",
        "Six sticky skeletons (x3)",
        "Which witch is which? (x3)",
        "Snap crackle pop (x3)",
        "Flash message (x3)",
        "Red Buick, blue Buick (x3)",
        "Red lorry, yellow lorry (x3)",
        "Thin sticks, thick bricks (x3)",
        "Stupid superstition (x3)",
        "Eleven benevolent elephants (x3)",
        "Two tried and true tridents (x3)",
        "Rolling red wagons (x3)",
        "Black back bat (x3)",
        "She sees cheese (x3)",
        "Truly rural (x3)",
        "Good blood, bad blood (x3)",
        "Pre-shrunk silk shirts (x3)",
        "Ed had edited it. (x3)",
        "We surely shall see the sun shine soon",
        "Which wristwatches are Swiss wristwatches?",
        "Fred fed Ted bread, and Ted fed Fred bread",
        "I slit the sheet, the sheet I slit, and on the slitted sheet I sit",
        "A skunk sat on a stump and thunk the stump stunk, but the stump thunk the skunk stunk",
        "Lesser leather never weathered wetter weather better",
        "Of all the vids I’ve ever viewed, I’ve never viewed a vid as valued as Alex’s engVid vid",
        "The thirty-three thieves thought that they thrilled the throne throughout Thursday.",
        "Something in a thirty-acre thermal thicket of thorns and thistles thumped and thundered threatening the three-D thoughts of Matthew the thug – although, theatrically, it was only the thirteen-thousand thistles and thorns through the underneath of his thigh that the thirty-year-old thug thought of that morning.",
        "Thirty-three thousand feathers on a thrushes throat.",
        "Send toast to ten tense stout saints’ ten tall tents.",
        "Rory the warrior and Roger the worrier were reared wrongly in a rural brewery.",
        "Imagine an imaginary menagerie manager managing an imaginary menagerie.",
        "Can you can a canned can into an un-canned can like a canner can can a canned can into an un-canned can?",
        "Six sick hicks nick six slick bricks with picks and sticks.",
        "Brisk brave brigadiers brandished broad bright blades, blunderbusses, and bludgeons — balancing them badly.",
        "If you must cross a course cross cow across a crowded cow crossing, cross the cross coarse cow across the crowded cow crossing carefully.",
        "She sells seashells by the seashore of Seychelles.",
        "Round and round the rugged rocks the ragged rascal ran.",
        "I looked right at Larry’s rally and left in a hurry.",
        "Lucky rabbits like to cause a ruckus.",
        "Rory’s lawn rake rarely rakes really right.",
        "A really leery Larry rolls readily to the road.",
        "Red lorry, yellow lorry.",
        "I slit the sheet, the sheet I slit, and on the slitted sheet I sit.",
        "How much ground would a groundhog hog, if a groundhog could hog ground? A groundhog would hog all the ground he could hog, if a groundhog could hog ground.",
        "Birdie birdie in the sky laid a turdie in my eye.\nIf cows could fly I’d have a cow pie in my eye.",
        "Yally Bally had a jolly golliwog. Feeling folly, Yally Bally Bought his jolly golli’ a dollie made of holly! The golli’, feeling jolly, named the holly dollie, Polly. So Yally Bally’s jolly golli’s holly dollie Polly’s also jolly!",
        "Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair. Fuzzy Wuzzy wasn’t very fuzzy, was he?",
        "Betty’s big bunny bobbled by the blueberry bush.",
        "Green glass globes glow greenly.",
        "If a dog chews shoes, whose shoes does he choose?",
        "Rubber baby buggy bumpers.",
        "A happy hippo hopped and hiccupped.",
        "Six sleek swans swam swiftly southwards.",
        "Pad kid poured curd pulled cod.",
        "From a cheap and chippy chopper on a big black block!",
        "Freezy trees made these trees’ cheese freeze",
        "How many boards\nCould the Mongols hoard\nIf the Mongol hordes got bored?",
        "Can you can a can as a canner can can a can?",
        "Out in the pasture the nature watcher watches the catcher. While the catcher watches the pitcher who pitches the balls. Whether the temperature's up or whether the temperature's down, the nature watcher, the catcher and the pitcher are always around. The pitcher pitches, the catcher catches and the watcher watches. So whether the temperature's rises or whether the temperature falls the nature watcher just watches the catcher who's watching the pitcher who's watching the balls."        
    ]
    formality = [
        'A Tongue Twister: ',
        'This is challenging, ',
        'Tongue Twister incoming... ',
        'you will have hard time with this',
        "twist your tongue a bit,"
    ]
    await ctx.send(f"""{random.choice(formality)} \n\n {random.choice(twisters_list)}""")

@client.command(aliases = ['coin', 'coinflip', 'flipcoin'])
async def flip(ctx):
    outcomes = [
        "HEADS",
        "TAILS"
    ]
    await ctx.send(f"""{ctx.author.mention} flipped {random.choice(outcomes)}""")

@client.command(aliases = ['roll', 'rolldice', 'diceroll'])
async def dice(ctx):
    outcomes = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
    ]
    await ctx.send(f"""{ctx.author.mention} rolled {random.choice(outcomes)}""")

@client.command(aliases = ['giggle', 'chuckle'])
async def laugh(ctx):
    laugh_patterns = [
        'Hahahahhahahahahahahaa',
        'Aaaahahhahahahahaa',
        'Heheheheheeeeeeeee',
        'aaaarhahahahahhaa',
        'wooooohohohohohooho',
        'khkhkhkhkhhkhhkhhkhh'
    ]
    tail = [
        'but i dont sound good',
        'its too much',
        'this is the most I have ever laughed'
    ]
    await ctx.send(f"""{random.choice(laugh_patterns)} {random.choice(tail)}""")

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount + 1)

def is_it_me(ctx):
    return ctx.author.id  == 339564758133112844

@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send (f"""Hi i am {ctx.author}""")


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f"""{member.mention} was kicked by {ctx.author}. \n Reason: {reason}""")

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"""{member.mention} was banned by {ctx.author}. \n Reason: {reason}""")



@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"""Unbanned {user.name}#{user.discriminator}""")
            return
@client.command()
async def users(ctx):
    formality = [
        'The total number of members in this server ',
        'In total the number of users here is ',
        '# of users ',
        'Number of users here '
    ]
    await ctx.send(f"""{random.choice(formality)} = {ctx.guild.member_count}""")

@client.remove_command("help")

@client.command()
async def help(ctx):
    print("Help called!")
@client.event
async def on_message(message):
    global messages
    messages += 1
    id = client.get_guild(712150647704649748)
    bad_words = ["nigga", "nigger", "shit", "crap", "fuck", "nonce", "bellend", "dick", "dickhead", "fucker" , "mampakha", "muji", "laude", "madarchod", "gandu", "randi"]
    
    for word in bad_words:
        word = word.lower()
        if message.content.count(word) > 0:
            print(f"""A bad word was said by {message.author}""")
            await message.channel.purge(limit=1)
            embed = discord.Embed(title = 'Oops', description = "I hope you did'nt catch a glimpse of that.\n", colour=discord.Colour.blue())
            await message.channel.send(content=None, embed=embed)
            await message.channel.send(f"""Removed a bad line used by {message.author.mention}.\n Warning !!!!!! dont repeat, Peace!!!""")
    
    if message.content == "!help":
        embed = discord.Embed(title = "Sanity_bot Command List", description = "Some useful commands (note that bot_prefix should lead the commands)", colour=discord.Colour.green())
        embed.add_field(name = "hello", value = "Greets the user")
        embed.add_field(name = "bye", value = "Bids the user goodbye")
        embed.add_field(name = "users", value = "Display number of users")
        embed.add_field(name = "kick @user", value = "Kicks the mentioned user from server")
        embed.add_field(name = "ban @user", value = "Bans the mentioned user from server")
        embed.add_field(name = "unban user_name#user_id", value = "Unbans the user if the user exists in banlist of server.")
        embed.add_field(name = "roast @user", value = "Roasts the mentioned user")
        embed.add_field(name = "funfact", value = "Provides a fun fact")
        embed.add_field(name = "joke", value = "Provides a funny joke")
        embed.add_field(name = "flip", value = "Flips a coin")
        embed.add_field(name = "roll", value = "Rolls a dice")  
        embed.add_field(name = "ping", value = "Displays the latency of the bot") 
        embed.add_field(name = "connect", value = "Connects to a voice channel") 
        embed.add_field(name = "haha", value = "Irony text for a bot cant haha") 
        embed.add_field(name = "laugh", value = "Displays a laugh text") 
        embed.add_field(name = "changeprefix new_prefix", value = "Changes the prefix of the bot for the server.") 
        embed.add_field(name = "riddle", value = "Provides a Riddle")
        embed.add_field(name = "twister", value = "Provides a tongue twister")
        await message.channel.send(content = None, embed = embed)
        embed_1 = discord.Embed(title = "", description = "Do not try to change nickname to mine (sanity ) And \n Do not use rough languages here please. Thankyou.", colour=discord.Colour.red())
        await message.channel.send(content = None, embed = embed_1)
        embed_2 = discord.Embed(title = "Multiple ways to call", description = "The commands have multiple ways of calling such as: ", colour=discord.Colour.green())
        embed_2.add_field(name = "hello", value = "'hi', 'hey', 'hola', 'greetings','namaste', 'namaskar'", inline = False)
        embed_2.add_field(name = "bye", value = "'adios', 'byebye','byeee', 'byee'", inline = False)
        embed_2.add_field(name = "funfact", value = "'funfacts'", inline = False)
        embed_2.add_field(name = "joke", value = "'jokes', 'fun', 'funny'", inline = False)
        embed_2.add_field(name = "flip", value = "'coin', 'coinflip', 'flipcoin'", inline = False)
        embed_2.add_field(name = "roll", value = "'dice', 'rolldice', 'diceroll'", inline = False)  
        embed_2.add_field(name = "haha", value = "'hehe','hahaha','lol','rofl','lul','lel','lmao','hehehe'", inline = False) 
        embed_2.add_field(name = "laugh", value = "'giggle', 'chuckle'", inline=False)
        await message.channel.send(content = None, embed = embed_2)
    await client.process_commands(message)

client.loop.create_task(update_stats())
client.run(token)  
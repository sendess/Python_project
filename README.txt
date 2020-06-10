    ____   _____      /\      ____               |\    /|   _______
   |    | |          /  \    |     \             | \  / |  |
   |___/  |____     /____\   |     |             |  \/  |  |_____
   |   \  |        /      \  |     |             |      |  |
   |    \ |_____  /        \ |____ /             |      |  |_______

----------------------------------------------------------------------------------------------------------------------------------------
                                                         Discord Bot

----------------------------------------------------------------------------------------------------------------------------------------
                 ___    ____        _____    
|\  /|     /\   |    \ |           |     \   \  /
| \/ |    /__\  |    | |---        |----<     \/
|    |   /    \ |___ / |____    ,  |_____/     |
 
 
  ____                   ___    _____  _____  
 /         /\    |\   | |    \ |      /       |     |
 \____    /  \   | \  | |    | |____  \_____  |_____|
      \  /____\  |  \ | |    | |            \ |     |
 _____/ /      \ |   \| |____/ |______ _____/ |     |
  
A project made with modules (discord.py, youtube_dl**) used for controlling the discord bot.
The discord bot so built has more than 20 commands and many monitoring/moderation functions over the server.
I have tried to make this bot a fully flexible and very much similar to the bots shared online.
                                                                                              
                                                                  ** youtube.dl was not able to be utilized ,
                                                                    as of the the completion of project deadline
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

I created every command for the bot myself with the motivation of why not make my own full fledge bot.
The discord bots are added to a server and my bot gives 20! command features and 

----------------------------------------------------------------------------------------------------------------------------------------
                                           Commands and Moderation Features of the bot
----------------------------------------------------------------------------------------------------------------------------------------
NOTE : All the following detail can be obtained by code !help on the server!!

Commands and modertion procedures of bot in a server:  

on joining server the bot defaults the prefix to "!" for every server it is invited in a json file.

Welcomes new user to server with different lines each time.

Greets user on giving any command such as !hi , !hello, !greetings, !namaste

displays server to bot delay on !ping

roasts mentioned user on command !roast@user

answers a yes or no question in different ways on !ask question

does not let the user to rename anyone with 'sanity', changes their nickname to 'choose sth else' if they didnt have a nickname and reverts to old nickname if there was a nickname earlier

kicks a mentioned user on command !kick @user reason   ,   only on the command recieved from user with permission to do so from server.

bans a mentioned user on command !ban @user reason   ,   only on the command recieved from user with permission to do so from server.

unbans a banned user on command !unban user_name#user_ID  ,   only on the command recieved from user with permission from server.

automatically looks out for a bad word in every mesage on server and removes the entire message if found any with an alert message.

the prefix can be changed to anything with the command !changeprefix new_prefix and updates in the json file.

can remove message on server channel with command !clear number_of_messages  . if no number is passed , default value is 1. only people with manage_message permission from server can operate this command.

displays the number of users in the current server (including bots) with command !users.

logs every detail of server (UTC time, total number of members, new member joined, number of messages done ) on daily basis.

connects to a voice channel the calling user is currently in, on command  !connect (wanted to add music features while the code went through some severe issues), will update it.

On removing(kicking) the bot from a server, the prefix saved for that particualr server is also removed from the json file.

gives fun fact on command !funfact

replys irony when commanded !haha, !hehe,  !lol ,!rofl,etc

bids goodbye to the user   on comman   !bye, !byebye , !byee,etc

provides a joke when commanded !joke, !fun ,!funny ,etc

flips a coin on command !flip ,!coin, !coinflip

rolls a dice on command !dice ,!roll, !rolldice

laughs on text after command !laugh, !chuckle, !giggle

provides a riddle on command !riddle

provides a tongue twister on the command !twister

provides a random value on command !ran value,    where the value has default 100 (i.e. random number is chosen from within 1 and value)


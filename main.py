import discord
import asyncio
import os
import random

client = discord.Client()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
TOKEN = os.getenv('TOKEN')

tealist = ['Earl Grey','English breakfast tea','lapsang souchong','Assam','Russian Caravan','chai','sencha','Darjeeling','oolong tea','Jasmine tea','Moroccan mint','chamomile']

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
@asyncio.coroutine
def on_message(message):
    #print(message.content)
    if message.content.startswith('$'):
        args = message.content[1:].split()
        print(args)
        cmd = args[0]
        args = [] if len(args)==1 else args[1:]
        chan = message.channel
        
        if cmd=='dance':
            tmp = yield from client.send_message(chan, ':D|-<')
            for i in range(2):
                yield from client.edit_message(tmp, ':D/-<')
                yield from client.edit_message(tmp, ':D|-<')
                yield from client.edit_message(tmp, ':D\\\\-<')
                yield from client.edit_message(tmp, ':D|-<')
        
        if cmd=='beer' and len(args)>0:
            yield from client.send_message(chan, '_slides a beer to %s, courtesy of %s._' % (' '.join(args), message.author.display_name))
        
        if cmd=='coffee' and len(args)>0:
            yield from client.send_message(chan, '_brews a fresh cup of java for %s, courtesy of %s._' % (' '.join(args), message.author.display_name))
        
        if cmd=='tea' and len(args)>0:
            yield from client.send_message(chan, '_hands %s a cup of %s, brewed by %s._' % (' '.join(args), random.choice(tealist), message.author.display_name))
        
        if cmd=='slap' and len(args)>0:
            yield from client.send_message(chan, '_slaps %s around a bit with a large trout._' % ' '.join(args))
        
        if cmd=='google' and len(args)>0:
            yield from client.send_message(chan, 'http://www.google.com/search?q=%s' % '+'.join(args))
        
        
    

client.run(TOKEN)
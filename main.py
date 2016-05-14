import discord
import asyncio
import os
import random

client = discord.Client()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
TOKEN = os.getenv('TOKEN')

tealist = ['Earl Grey','English breakfast tea','lapsang souchong','Assam','Russian Caravan','chai','sencha','Darjeeling','oolong tea','Jasmine tea','Moroccan mint','chamomile']

belair = """
Now, this is a story all about how
My life got flipped-turned upside down
And I'd like to take a minute
Just sit right there
I'll tell you how I became the prince of a town called Bel-Air

In west Philadelphia born and raised
On the playground was where I spent most of my days
Chillin' out maxin' relaxin' all cool
And all shooting some b-ball outside of the school
When a couple of guys who were up to no good
Started making trouble in my neighborhood
I got in one little fight and my mom got scared
She said 'You're movin' with your auntie and uncle in Bel-Air'

I begged and pleaded with her day after day
But she packed my suitcase and sent me on my way
She gave me a kiss and then she gave me my ticket.
I put my Walkman on and said, 'I might as well kick it'.

First class, yo this is bad
Drinking orange juice out of a champagne glass.
Is this what the people of Bel-Air living like?
Hmm this might be alright.

But wait I hear they're prissy, bourgeois, all that
Is this the type of place that they just send this cool cat?
I don't think so
I'll see when I get there
I hope they're prepared for the prince of Bel-Air

Well, the plane landed and when I came out
There was a dude who looked like a cop standing there with my name out
I ain't trying to get arrested yet
I just got here
I sprang with the quickness like lightning, disappeared

I whistled for a cab and when it came near
The license plate said fresh and it had dice in the mirror
If anything I could say that this cab was rare
But I thought 'Nah, forget it' - 'Yo, home to Bel-Air'

I pulled up to the house about 7 or 8
And I yelled to the cabbie 'Yo home smell ya later'
I looked at my kingdom
I was finally there
To sit on my throne as the Prince of Bel-Air
"""

# modified from http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
class Markov(object):

	def __init__(self, text, chain_size=3):
		self.chain_size = chain_size
		self.cache = {}
		self.text = text
		self.words = self.text_to_words()
		self.word_size = len(self.words)
		self.database()

	def text_to_words(self):
		words = self.text.split()
		return words

	def words_at_position(self, i):
		"""Uses the chain size to find a list of the words at an index."""
		chain = []
		for chain_index in range(0, self.chain_size):
			chain.append(self.words[i + chain_index])
		return chain

	def chains(self):
		"""Generates chains from the given data string based on passed chain size.
		So if our string were:
			"What a lovely day"
		With a chain size of 3, we'd generate:
			(What, a, lovely)
		and
			(a, lovely, day)
		"""

		if len(self.words) < self.chain_size:
			return

		for i in range(len(self.words) - self.chain_size - 1):
			yield tuple(self.words_at_position(i))

	def database(self):
		for chain_set in self.chains():
			key = chain_set[:self.chain_size - 1]
			next_word = chain_set[-1]
			if key in self.cache:
				self.cache[key].append(next_word)
			else:
				self.cache[key] = [next_word]

	def generate_markov_text(self, size=25):
		seed = random.randint(0, self.word_size - 3)
		gen_words = []
		seed_words = self.words_at_position(seed)[:-1]
		gen_words.extend(seed_words)
		for i in range(size):
			last_word_len = self.chain_size - 1
			last_words = gen_words[-1 * last_word_len:]
			next_word = random.choice(self.cache[tuple(last_words)])
			gen_words.append(next_word)
		return ' '.join(gen_words)

belairmarkov = Markov(belair, chain_size=2)

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
        
        if cmd=='belair':
            length = random.randrange(5,25)
            if len(args)>0:
                try:
                    length = int(args[0])
                except:
                    print('invalid length')
            yield from client.send_message(chan, belairmarkov.generate_markov_text(length))
        
        
    

client.run(TOKEN)
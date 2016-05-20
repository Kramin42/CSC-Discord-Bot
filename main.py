import discord
import asyncio
import os
import random
import lispy

client = discord.Client()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
TOKEN = os.getenv('TOKEN')

tealist = ['Earl Grey','English breakfast tea','lapsang souchong','Assam','Russian Caravan','chai','sencha','Darjeeling','oolong tea','Jasmine tea','Moroccan mint','chamomile']

with open('thrones', 'r') as f:
    thrones=f.read()

# modified from http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
# and https://gist.github.com/dellis23/6174914
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

class DynamicMarkov(object):

    def __init__(self, filename, chain_size=3):
        self.chain_size = chain_size
        self.cache = {}
        self.filename = filename
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()

    def file_to_words(self):
        with open(self.filename, 'r') as f:
            data = f.read()
        words = data.split()
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
    
    def update(self, text):
        text = text+' ENDOFLINEINDICATOR\n'
        newwords = text.split()
        self.words+= newwords
        self.word_size = len(self.words)
        if len(newwords) < self.chain_size:
            return
        
        newchains = []
        for i in range(len(newwords) - self.chain_size - 1):
            chain = []
            for chain_index in range(0, self.chain_size):
                chain.append(newwords[i + chain_index])
            newchains.append(tuple(chain))
        
        for chain_set in newchains:
            key = chain_set[:self.chain_size - 1]
            next_word = chain_set[-1]
            if key in self.cache:
                self.cache[key].append(next_word)
            else:
                self.cache[key] = [next_word]
        
        with open(self.filename, 'a') as f:
            f.write(text)
        

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
            try:
                next_word = random.choice(self.cache[tuple(last_words)])
            except KeyError:
                print('key not found for markov chain')
                break
            gen_words.append(next_word)
        return ' '.join(gen_words)

#belairmarkov = Markov(belair, chain_size=2)
#shadesmarkov = Markov(shades, chain_size=3)
thronesmarkov = Markov(thrones, chain_size=3)
markov = DynamicMarkov('markov', chain_size=2)

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
    if not message.author.bot:
        print(message.content)
        if len(message.content.split())>4:
            markov.update(message.content)
    
    if message.content.startswith('$'):
        args = message.content[1:].split()
        print(args)
        cmd = args[0]
        args = [] if len(args)==1 else args[1:]
        chan = message.channel
        
        if cmd=='lisp':
            yield from client.send_message(chan, lispy.rep(' '.join(args)))
        
        if cmd=='dance':
            tmp = yield from client.send_message(chan, ':D|-<')
            for i in range(2):
                yield from client.edit_message(tmp, ':D/-<')
                yield from client.edit_message(tmp, ':D|-<')
                yield from client.edit_message(tmp, ':D\\\\-<')
                yield from client.edit_message(tmp, ':D|-<')
        
        if cmd=='echo':
            yield from client.send_message(chan, ' '.join(args))
        
        if cmd=='glasses':
            # ( ••)    ( ••)>⌐■-■    (⌐■_■)
            tmp = yield from client.send_message(chan, '( ••)')
            yield from asyncio.sleep(1)
            yield from client.edit_message(tmp, '( ••)>⌐■-■')
            yield from asyncio.sleep(1)
            yield from client.edit_message(tmp, '(⌐■_■)')
        
        if cmd=='deal':
            glasses ='    ⌐■-■    '
            glasson ='   (⌐■_■)   '
            dealwith='deal with it'
            lines = ['            ',\
                     '            ',\
                     '            ',\
                     '    ( ••)   ']
            tmp = yield from client.send_message(chan, '```%s```' % '\n'.join(lines))
            yield from asyncio.sleep(1)
            yield from client.edit_message(tmp, '```%s```' % '\n'.join([glasses]+lines[1:]))
            yield from asyncio.sleep(1)
            yield from client.edit_message(tmp, '```%s```' % '\n'.join(lines[:1]+[glasses]+lines[2:]))
            yield from asyncio.sleep(1)
            yield from client.edit_message(tmp, '```%s```' % '\n'.join(lines[:2]+[glasses]+lines[3:]))
            yield from asyncio.sleep(1)
            yield from client.edit_message(tmp, '```%s```' % '\n'.join(lines[:1]+[dealwith]+lines[2:3]+[glasson]))
            
        
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
        
        if cmd=='marquee' and len(args)>0:
            display = '                    '
            tmp = yield from client.send_message(chan, '```%s```' % display)
            text = ' '.join(args)+display
            for char in text:
                display = display[1:]+char
                yield from client.edit_message(tmp, '```%s```' % display)
            yield from asyncio.sleep(2)
            yield from client.delete_message(tmp)
                
            
        
        # if cmd=='belair':
        #     length = random.randrange(5,25)
        #     if len(args)>0:
        #         try:
        #             length = int(args[0])
        #         except:
        #             print('invalid length')
        #     yield from client.send_message(chan, belairmarkov.generate_markov_text(length))
        
        # if cmd=='shades':
        #     length = random.randrange(20,50)
        #     if len(args)>0:
        #         try:
        #             length = int(args[0])
        #         except:
        #             print('invalid length')
        #     yield from client.send_message(chan, shadesmarkov.generate_markov_text(length))
        
        if cmd=='thrones':
            length = random.randrange(50,150)
            if len(args)>0:
                try:
                    length = int(args[0])
                except:
                    print('invalid length')
            generated = thronesmarkov.generate_markov_text(length)
            generated = '.'.join(generated.split('.')[1:-1])
            yield from client.send_message(chan, generated)
        
        if cmd=='markov':
            length = random.randrange(10,40)
            if len(args)>0:
                try:
                    length = int(args[0])
                except:
                    print('invalid length')
            # ENDOFLINEINDICATOR
            generated = markov.generate_markov_text(length)
            generated = generated.replace('ENDOFLINEINDICATOR','\n')
            yield from client.send_message(chan, generated)
        
        
    

client.run(TOKEN)
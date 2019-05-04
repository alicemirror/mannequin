# AI and natural language processor classes
# Including methods for speech to text and vice-versa
import random
import re
from collections import namedtuple
import subprocess
import sys
import json
import time

# ----------------------
# Classes and methods
# ----------------------

# Set the key objects in the contorl file based on the sencence words
class Key:
    # Data acquisition for the keyrods
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps

# Set the decomposition pattern parameters
class Decomp:
    # Data acquisition for decomposition. Includes the reassembly pattern
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0

# The class processing the sentence
class AI:
    # --- CONSTANTS
    # Speech to text shell command
    __STT = '/home/pi/speech_to_text.sh'
    # Text to speech command and parameters
    # Parameters: -sp = speak, -n = narrator voice
    __TTS = [ 'trans', '-sp' ]
    # Recording shell command
    __REC = "/home/pi/getSample.sh"
    # Self-destruction explosion
    __EXPLODE = "/home/pi/Explode.sh"
    # Play a sentence for someone speaking
    __ASK_FOR_SPEAK = "/home/pi/borg_call.sh"
    # Sentence to request an immediate shutdown
    __SHUTDOWN_REQUEST = "self destroy"
    # Mnimum confidence level of the spokent sentence to
    # consider it trustable
    __MIN_TRUST_LEVEL = 0.10
    # Maximum number of sentences per session
    __MAX_SENTENCES = 12
    # Number of tries for someone speaking before playing
    # a random phrase
    __MAX_WAIT_FOR_SPEAK = 20

    # --- Dictionary keys
    __TTS_RESULTS = "results"
    __TTS_ALTERNATIVES = "alternatives"
    __TTS_CONFIDENCE = "confidence"
    __TTS_TRANSCRIPT = "transcript"

    # Set the words management arrays for initial and inal discussion
    # pre and post substitution process, synonims matching, keywords
    # and temporary saved data (remembering process)
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []

    # Load the contrl script file and arrange the content in the
    # respective arrays.
    def load(self, path):
        key = None
        decomp = None
        with open(path) as file:
            for line in file:
                if not line.strip():
                    continue
                tag, content = [part.strip() for part in line.split(':')]
                if tag == 'initial':
                    self.initials.append(content)
                elif tag == 'final':
                    self.finals.append(content)
                elif tag == 'quit':
                    self.quits.append(content)
                elif tag == 'pre':
                    parts = content.split(' ')
                    self.pres[parts[0]] = parts[1:]
                elif tag == 'post':
                    parts = content.split(' ')
                    self.posts[parts[0]] = parts[1:]
                elif tag == 'synon':
                    parts = content.split(' ')
                    self.synons[parts[0]] = parts
                elif tag == 'key':
                    parts = content.split(' ')
                    word = parts[0]
                    weight = int(parts[1]) if len(parts) > 1 else 1
                    key = Key(word, weight, [])
                    self.keys[word] = key
                elif tag == 'decomp':
                    parts = content.split(' ')
                    save = False
                    if parts[0] == '$':
                        save = True
                        parts = parts[1:]
                    decomp = Decomp(parts, save, [])
                    key.decomps.append(decomp)
                elif tag == 'reasmb':
                    parts = content.split(' ')
                    decomp.reasmbs.append(parts)

    # Check for the matching sentence decomposition
    def _match_decomp_r(self, parts, words, results):
        if not parts and not words:
            return True
        if not parts or (not words and parts != ['*']):
            return False
        if parts[0] == '*':
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self._match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith('@'):
            root = parts[0][1:]
            if not root in self.synons:
                raise ValueError("Unknown synonym root {}".format(root))
            if not words[0].lower() in self.synons[root]:
                return False
            results.append([words[0]])
            return self._match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self._match_decomp_r(parts[1:], words[1:], results)

    # Check for the matching sentence decomposition
    def _match_decomp(self, parts, words):
        results = []
        if self._match_decomp_r(parts, words, results):
            return results
        return None

    # Reassemble the next index position
    def _next_reasmb(self, decomp):
        index = decomp.next_reasmb_index
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

    # Reassemble the whole new sentence
    def _reassemble(self, reasmb, results):
        output = []
        for reword in reasmb:
            if not reword:
                continue
            if reword[0] == '(' and reword[-1] == ')':
                index = int(reword[1:-1])
                if index < 1 or index > len(results):
                    raise ValueError("Invalid result index {}".format(index))
                insert = results[index - 1]
                for punct in [',', '.', ';']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
            else:
                output.append(reword)
        return output

    # Find the output word from sub sentence
    def _sub(self, words, sub):
        output = []
        for word in words:
            word_lower = word.lower()
            if word_lower in sub:
                output.extend(sub[word_lower])
            else:
                output.append(word)
        return output

    # Search a word matching keyword to build the return sentence
    def _match_key(self, words, key):
        for decomp in key.decomps:
            results = self._match_decomp(decomp.parts, words)
            if results is None:
                continue
            results = [self._sub(words, self.posts) for words in results]
            reasmb = self._next_reasmb(decomp)
            if reasmb[0] == 'goto':
                goto_key = reasmb[1]
                if not goto_key in self.keys:
                    raise ValueError("Invalid goto key {}".format(goto_key))
                return self._match_key(words, self.keys[goto_key])
            output = self._reassemble(reasmb, results)
            if decomp.save:
                self.memory.append(output)
                continue
            return output
        return None

    # Build the reassembled respose sentence
    def respond(self, text):
        if text in self.quits:
            return None

        text = re.sub(r'\s*\.+\s*', ' . ', text)
        text = re.sub(r'\s*,+\s*', ' , ', text)
        text = re.sub(r'\s*;+\s*', ' ; ', text)

        words = [w for w in text.split(' ') if w]

        words = self._sub(words, self.pres)

        keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys]
        keys = sorted(keys, key=lambda k: -k.weight)

        output = None

        for key in keys:
            output = self._match_key(words, key)
            if output:
                break
        if not output:
            if self.memory:
                index = random.randrange(len(self.memory))
                output = self.memory.pop(index)
            else:
                output = self._next_reasmb(self.keys['xnone'].decomps[0])

        return " ".join(output)

    # Randomly select one of the initial sentences (on discussion opening)
    def initial(self):
        return random.choice(self.initials)

    # Radomly select one of the final sentences
    def final(self):
        return random.choice(self.finals)

    # Executes the textual sentence-response on terminal chat
    # in an infinite loop
    def run(self):
        print(self.initial())

        while True:
            sent = input('> ')

            output = self.respond(sent)
            if output is None:
                break

            print(output)

        print(self.final())

    # Execute a subprocess command managing the return value, stdout, stderr
    # and the return code (0 or not 0 if error occurred)
    def __runCmd(self, cmd):
        proc = subprocess.Popen(cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()
     
        return proc.returncode, stdout, stderr

    # Retrieve the json text returned by the speech to text string
    # and parse it to extract the textual content and its confidence
    # value in a json dictionary. The dictionary referred keywords are
    # defined as constants in this class.
    #
    # Note that the jsonText paramer is a bytes string so it need a conversion
    # before json parsing
    def __getTextFromJson(self, jsonText):
        if(jsonText == b'{}\n'):
            # Nothing spoken, force a high confidence level with an empty
            # string
            return '', 9
        else:
            jDict = json.loads(jsonText.decode())
            return jDict[self.__TTS_RESULTS][0][self.__TTS_ALTERNATIVES][0][self.__TTS_TRANSCRIPT], jDict[self.__TTS_RESULTS][0][self.__TTS_ALTERNATIVES][0][self.__TTS_CONFIDENCE]

    # Executes immediate shutdown of the system
    def __shutdown(self):
        command = "/usr/bin/sudo /sbin/shutdown now"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

    # Speech a text sentence
    def __speech(self, sentence):
        self.__runCmd([self.__TTS[0], self.__TTS[1], sentence])           

    # Wait for a spoken sentence and convert it to text.
    # Return the sentence or speak an understanding error asking to
    # repeat it if it is not sufficiently clear.
    # If the sentence if fully understood, return the textural spokent
    # sentence for further processing
    def __getSTT(self):
        # Understanding sentence state to exit from the
        # function
        understood = False

        while understood is not True:
            # Google speech to text acquiring the json return from stduout
            # using pipe
            code, out, err = self.__runCmd([self.__STT])
            # Check the return code from speech to text
            if(code is not 0):
                self.__speech("Something went wrong in my circuits, please repeat")
            else:
                # Extract the text from the returned json object
                speechTT, trust = self.__getTextFromJson(out)
                # If the text is not trustable, ask to repeat the sentence
                if(trust < self.__MIN_TRUST_LEVEL):
                    self.__speech("I can't understand. Can you repeat?")
                else:
                    if(speechTT == ''):
                        # Empty sentence
                        self.__speech("You told nothing! Tell me what you have in mind")
                    else:
                        # Everything is ok, the sentence has been understood and
                        # is trustable. Exit from the loop
                        understood = True

        # Check if the user asked for "shutdown now" to execute
        # a system shutdown
        if(speechTT == self.__SHUTDOWN_REQUEST):
            self.__speech("Self-destruction sequence activated. System will explode in five seconds.")
            self.__runCmd([self.__EXPLODE])
            self.__shutdown()
        else:
            return speechTT

    # Check if someone spoke something in the microphone, to activate
    # a discussion with the engine.
    def __checkSpeak(self):
        # Record five seconds of audio from the mic
        code, out, err = self.__runCmd([self.__REC])
        # Convert the return audio file statistics to an array
        # based on the new line character.
        stats = err.split(b'\n')
        # The sox command fourth position if the Maximum amplitude
        # from where we extract the value
        if(float(stats[3][18:]) > 0.07):
            return True
        else:
            return False

    # Executes the textual sentence-response by chat
    def runSpeech(self):
        startDiscussion = False
        sentences = 0
        waitForSpeak = self.__MAX_WAIT_FOR_SPEAK
                                       
        while startDiscussion is not True:
            if(waitForSpeak >= self.__MAX_WAIT_FOR_SPEAK):
                # Play a speak request sentence
                self.__runCmd([self.__ASK_FOR_SPEAK])
                waitForSpeak = 0
            else:
                # Increment the counts
                waitForSpeak += 1
                
            # Check if someone is speaking
            startDiscussion = self.__checkSpeak()
            
        # Say the initial sentence
        self.__runCmd([self.__TTS[0], self.__TTS[1], self.initial()])

        while sentences < self.__MAX_SENTENCES:
            sent = self.__getSTT()

            output = self.respond(sent)
            if output is None:
                # Force counter to exit
                sentences = self.__MAX_SENTENCES

            # say a response and increment the sentences counter
            self.__runCmd([self.__TTS[0], self.__TTS[1], output])
            sentences += 1

        # Exit block
        output = self.final()
        self.__runCmd([self.__TTS[0], self.__TTS[1], output])


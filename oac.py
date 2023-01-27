"""-------------------------------------------------------------------
# OAC- OpenAI Console
-------------------------------------------------------------------"""
__author__ = "z0nd3rl1ng" + "0xAsFi"
__version__ = "0.0.1"

"""----------------------------------------------------------------"""
# MODULE IMPORTS
import random, os
from os import environ
"""----------------------------------------------------------------"""
# THIRD PARTY MODULE REQUIREMENT CHECK
try:
    import openai
except ModuleNotFoundError:
    print("[*] install missing module: openai")
    os.system("pip3 install openai")
    import openai
"""----------------------------------------------------------------"""
# GLOBAL VARIABLES
openai.api_key = ""
ENGINE = "text-davinci-002"
TEMPERATURE = 0
MAX_TOKENS = 2048
"""----------------------------------------------------------------"""




# FUNCTION TO SET OPEN AI API KEY AS ENVIRONMENT VARIABLE
def setEnvKey():
    token = input("[OpenAI API Key]╼> ")
    os.system("export OPENAI_API_KEY='"+token+"'")

# FUNCTION TO LIST AND SET AVAILABLE ENGINES, TEMPERATURE, MAX_TOKENS
def setFinetuning():
    engineslist = openai.Engine.list()
    for ids in engineslist.data:
        print(ids.id) # LIST ALL ENGINES
    ENGINE = input("[Select Engine]╼> ") # SET ENGINE
    TEMPERATURE = float(input("[Set Temperature]╼> ")) # SET TEMPERATURE
    MAX_TOKENS = int(input("[Set Max Tokens]╼> ")) # SET MAX_TOKENS

# FUNCTION FOR THE OPENAI QUERY PROMPT
def openaiConsole():
    while True:
        interact = input("[OAC]╼> ")
        if interact == "exit":
            exit()
        elif interact == "fine-tuning":
            setFinetuning()
        elif interact == "set api-key":
            setEnvKey()
        elif interact == "help":
            print("\nCOMMANDS\tDESCRIPTION\n")
            print("set api-key\tsave your OpenAI API key as environment variable")
            print("fine-tuning\tlaunch configuration menu for fine-tuning")
            print("exit\t\tquit oac\n")
        elif interact == "banner":
            banner()
        else:
            response = openai.Completion.create(
                engine=ENGINE,
                prompt=(f"{interact}"),
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                stop=None
            )
            response = response["choices"][0]["text"]
            print(response)
            
def banner():
	padding = '  '
	O = [[' ','┌','─','┐'],
	     [' ','│',' ','│'],
	     [' ','└','─','┘']]
	A = [[' ','┌','─','┐'],
	     [' ','├','─','┤'],
	     [' ','┴',' ','┴']]
	C = [[' ','┌','─','─'],
	     [' ','│',' ',' '],
	     [' ','└','─','─']]
	
	banner = [O,A,C]
	final = []
	print('\r')
	init_color = random.randint(10,40)
	txt_color = init_color
	cl = 0

	for charset in range(0, 3):
		for pos in range(0, len(banner)):
			for i in range(0, len(banner[pos][charset])):
				clr = f'\033[38;5;{txt_color}m'
				char = f'{clr}{banner[pos][charset][i]}'
				final.append(char)
				cl += 1
				txt_color = txt_color + 36 if cl <= 3 else txt_color

			cl = 0

			txt_color = init_color
		init_color += 31

		if charset < 2: final.append('\n   ')

	print(f"   {''.join(final)}")
	print(f'{padding}by z0nd3rl1ng & \n       0xAsFi\n')

if __name__ == "__main__":
    banner()
    openaiConsole()

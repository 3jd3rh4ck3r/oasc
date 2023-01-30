"""-------------------------------------------------------------------
# OASC - OpenAI Security Console
-------------------------------------------------------------------"""
__author__ = "z0nd3rl1ng" + "0xAsFi"
__version__ = "0.0.1"

"""----------------------------------------------------------------"""
# MODULE IMPORTS
import random, os
from os import environ
# THIRD PARTY REQUIREMENT CHECK
try:
    # TRY TO IMPORT OPENAI
    import openai
except ModuleNotFoundError:
    # IF ERROR PIP INSTALL OPENAI + IMPORT
    print("[*] install missing module: openai")
    os.system("pip3 install openai")
    import openai
"""----------------------------------------------------------------"""
# GLOBAL VARIABLES
openai.api_key = "[PUT YOUR API KEY HERE]"
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
  
# FUNCTION TO LIST HELP MENU - COULD BE SWAGGED UP ;)
def help():
    print("\nCOMMANDS\tDESCRIPTION\n")
    print("banner\t\tprint banner")
    print("api-key\t\texport OpenAI API-Key to environment")
    print("fine-tuning\tconfiguration menu for fine-tuning queries")
    print("exit\t\tquit oasc\n")

# FUNCTION FOR THE OPENAI QUERY PROMPT (CORE-SYSTEM)
def openaiSecurityConsole():
    while True:
        interact = input("[OASC]╼> ")
        # SYSTEM COMMAND HANDLER 
        if interact == "exit":
            exit()
        elif interact == "fine-tuning":
            setFinetuning()
        elif interact == "api-key":
            setEnvKey()
        elif interact == "help":
            help()
        elif interact == "banner":
            banner()
        else:
            # ACTUAL OPENAI REQUEST - COULD BE OUTSOURCED AS FUNCTION
            response = openai.Completion.create(
                engine=ENGINE,
                prompt=(f"{interact}"),
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                stop=None
            )
            response = response["choices"][0]["text"]
            print(response)

# FUNCTION FOR A CALLABLE BANNER
# TBH GOOGLED THIS SOMEHOW TOGETHER BUT I RLY LIKE THE GRADIENT SO I MOSTLY USE IT <3
def banner():
	padding = '  '
	O = [[' ','┌','─','┐'],
	     [' ','│',' ','│'],
	     [' ','└','─','┘']]
	A = [[' ','┌','─','┐'],
	     [' ','├','─','┤'],
	     [' ','┴',' ','┴']]
	S = [[' ','┌','─','┐'],
	     [' ','└','─','┐'],
	     [' ','└','─','┘']]
	C = [[' ','┌','─','┐'],
	     [' ','│',' ',' '],
	     [' ','└','─','┘']]
	
	banner = [O,A,S,C]
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
	print(f'{padding}  by z0nd3rl1ng & \n\t 0xAsFi\n')

# MAIN FUNCTION (ENTRY-POINT)
if __name__ == "__main__":
    banner()
    openaiSecurityConsole()

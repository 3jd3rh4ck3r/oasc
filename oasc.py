"""-------------------------------------------------------------------
# OASC - OpenAI Security Console
-------------------------------------------------------------------"""
__author__ = "z0nd3rl1ng" + "0xAsFi"
__version__ = "0.0.1"

"""----------------------------------------------------------------"""

# MODULE REQUIREMENT CHECK
try:
    import random, os
    import openai, requests
    from bs4 import BeautifulSoup as bs
except ModuleNotFoundError:
    print("[*] installing missing modules")
    os.system("pip3 install requests")
    os.system("pip3 install openai")
    os.system("pip3 install beautifulsoup4")
    os.system("pip3 install lxml")
    import openai, requests
    from bs4 import BeautifulSoup as bs
"""----------------------------------------------------------------"""

# GLOBAL VARIABLES
openai.api_key = "[ENTER YOUR API KEY HERE]"
ENGINE = "text-davinci-002"
TEMPERATURE = 0
MAX_TOKENS = 2048
"""----------------------------------------------------------------"""


# FUNCTION TO SET OPEN AI API KEY AS ENVIRONMENT VARIABLE -> It's not working -.-"
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


# FUNCTION TO EXPORT CONTENT TO FILE
def exportContent(data, path):
    with open(path, "w") as file:
        file.write(str(bs(data)))


# FUNCTION TO IMPORT CONTENT FROM FILE
def importContent(path):
    with open(path, "r") as file:
        content = file.readlines()
    content = "".join(content)
    prettyprompt = bs(content, "lxml")
    return prettyprompt


# FUNCTION FOR AN OPENAI REQUEST
def openaiRequest(type, interact):
    if type == "console":
        response = openai.Completion.create(
            engine=ENGINE,
            prompt=(f"{interact}"),
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stop=None
        )
        response = response["choices"][0]["text"]
        return response


# FUNCTION FOR GOOGLE DORK REQUEST
def googleDorkRequest(query):
    params = {'q': query}
    response = requests.get('https://www.google.com/search', params=params)
    return response.text


# FUNCTION TO ANALYZE FILE CONTENT
def analyzer():
    path = input("[File Path]╼> ")
    content = importContent(path)
    prompt = "Describe following file content: " + str(content)
    type = "console"
    response = openaiRequest(type, prompt)
    print(response)


# FUNCTION TO CREATE FILE TEMPLATE
def creator():
    data = input("[Describe Content]╼> ")
    path = input("[File Path]╼> ")
    type = "console"
    response = openaiRequest(type, data)
    exportContent(response, path)


# FUNCTION TO LIST SOCIAL AND REVERSE ENGINEERING MENU
def social():
    print("\nSOCIAL AND REVERSE ENGINEERING MENU\n")
    print("(1)Analyze File Content")
    print("(2)Generate Template\n")
    mode = input("[Select Mode]╼> ")    
    if mode == "1":
        analyzer()
    elif mode == "2":
        creator()
    else:
        social()


# FUNCTION TO LIST OSINT MENU
def osint():
    print("\nOSINT MENU\n")
    print("(1)Reconnaissance")
    print("(2)Enumeration")
    print("(3)Email Search")
    print("(4)Username Search")
    print("(5)People Search")
    print("(6)Phone Number")
    print("(7)Google Dorking")
    print("(0)Back\n")

    def reconnaissance():
        print("\nScanning target for information.\n")
        
    def enumeration():
        print("\nGathering data through active connections.\n")

    def emailSearch():
        print("\nSearching for email addresses.\n")
        
    def usernameSearch():
        print("\nSearching for usernames.\n")
    
    def peopleSearch():
        print("\nSearching for information about individuals.\n")
    
    def phoneNumber():
        print("\nSearching for phone number information.\n")

    def googleDorking():
        print("\nAdvanced search techniques using Google.\n")
        # THIS IS HOW YOU COULD USE IT FURTHER FROM HERE
        results = googleDorkRequest("inurl:login site:tiktok.com")  # OPERATORS MIGHT BE SET DIFFERENT OR EXTENDED
        exportContent(results, "dork-report.html")  # SAVE RESPONSE
        
    mode = input("[Select Mode]╼> ")
    if mode == "1":
        reconnaissance()
    elif mode == "2":
        enumeration()
    elif mode == "3":
        emailSearch()
    elif mode == "4":
        usernameSearch()
    elif mode == "5":
        peopleSearch()
    elif mode == "6":
        phoneNumber()
    elif mode == "7":
        googleDorking()
    elif mode == "0":
        os.system("clear")
        banner()
        openaiSecurityConsole()
    else:
        os.system("clear")
        print("Wrong input, try again.")
        osint()


# FUNCTION TO LIST HELP MENU - COULD BE SWAGGED UP ;)
def help():
    print("\nCOMMANDS\tDESCRIPTION\n")
    print("banner\t\tprint banner")
    print("social\t\tcall social and reverse engineering menu")
    print("osint\t\tcall osint menu")
    print("api-key\t\tset OpenAI API to environment")
    print("fine-tuning\tconfiguration menu for fine-tuning queries")
    print("exit\t\tquit oasc\n")


# FUNCTION FOR THE OPENAI QUERY PROMPT (CORE-SYSTEM)
def openaiSecurityConsole():
    while True:
        interact = input("[OASC]╼> ")
        # SYSTEM COMMAND HANDLER 
        if interact == "exit":
            exit()
        elif interact == "social":
            social()
        elif interact == "osint":
            osint()
        elif interact == "fine-tuning":
            setFinetuning()
        elif interact == "api-key":
            setEnvKey()
        elif interact == "help":
            help()
        elif interact == "banner":
            banner()
        else:
            type = "console"
            response = openaiRequest(type, interact)
            print(response)


# FUNCTION FOR A CALLABLE BANNER
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


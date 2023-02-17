"""-------------------------------------------------------------------
# OASC - OpenAI Security Console
-------------------------------------------------------------------"""
__author__ = "z0nd3rl1ng" + "0xAsFi"
__version__ = "0.0.1"

"""----------------------------------------------------------------"""

# MODULE REQUIREMENT CHECK
try:
    import random, os, json
    import openai, requests
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from web3 import Web3
    import stem
    import stem.connection
    import stem.process
    from requests.structures import CaseInsensitiveDict
    from censys.search import CensysHosts
except ModuleNotFoundError:
    print("[*] checking requirements ...")
    os.system("pip3 install requests")
    os.system("pip3 install openai")
    os.system("pip3 install beautifulsoup4")
    os.system("pip3 install lxml")
    os.system("pip3 install pandas")
    os.system("pip3 install web3")
    os.system("pip3 install censys")
    os.system("pip3 install stem")
    import random, os, json
    import openai, requests
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from web3 import Web3
    from censys.search import CensysHosts
    import stem
    import stem.connection
    import stem.process
    from requests.structures import CaseInsensitiveDict
"""----------------------------------------------------------------"""

# GLOBAL VARIABLES
openai.api_key = "[ENTER YOUR API KEY HERE]"
numlookupapikey = "[PUT YOUR API KEY HERE]"  # NUMLOOKUPAPI HAS 100 REQUEST PER MONTH FOR FREE
cenapikey = "[ENTER YOUR API ID HERE]"
censecret = "[ENTER YOUR API SECRET HERE]"
ENGINE = "text-davinci-002"
TEMPERATURE = 0
MAX_TOKENS = 2048
"""----------------------------------------------------------------"""


# FUNCTION TO EXPORT ENVIRONMENT VARIABLES
def setEnvKeys():
    openaitoken = input("[OpenAI API Key]╼> ")
    os.system("export OPENAI_API_KEY='"+openaitoken+"'")
    numlookuptoken = input("[Numlookup API Key]╼> ")
    os.system("export NUMLOOKUP_API_KEY='" + numlookuptoken + "'")
    cenapitoken = input("[CenSys API Key]╼> ")
    os.system("export CENSYS_API_KEY='" + cenapitoken + "'")
    censecrettoken = input("[CenSys Secret Key]╼> ")
    os.system("export CENSYS_SECRET_KEY='" + censecrettoken + "'")


# FUNCTION TO SET FINETUNING FOR OPENAI REQUEST
def openaiFinetuning(engine, temperature, max_tokens):
    ENGINE = engine
    TEMPERATURE = temperature
    MAX_TOKENS = max_tokens


# FUNCTION TO LIST OPENAI ENGINES
def openaiEngines():
    engines = openai.Engine.list()
    for ids in engines.data:
        print(ids.id)


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


# FUNCTION FOR TOR NETWORK REQUEST
def torRequest():
    # SET TOR AS PROXY
    session = requests.session()
    session.proxies = {'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
    return session


# FUNCTION FOR A BLOCKCHAIN REQUEST
def blockchainRequest(network, address):
    if network == "1":
        blockchain = 'https://blockchain.info/rawaddr/' + address
        wallet = pd.read_json(blockchain, lines=True)
        balance = float(wallet.final_balance) / 100000000
        inbound = float(wallet.total_received) / 100000000
        outbound = float(wallet.total_sent) / 100000000
        print("[*] BALANCE:\t" + str(balance) + " BTC")
        print("[*] RECEIVED:\t" + str(inbound) + " BTC")
        print("[*] SENT:\t" + str(outbound) + " BTC")
    elif network == "2":
        blockchain = 'https://mainnet.infura.io/v3/64e9df670efb49ac9b71f9984f29dccd'
        web3 = Web3(Web3.HTTPProvider(blockchain))
        if web3.isConnected():
            balance = web3.eth.getBalance(address)
            print(web3.fromWei(balance, "ETH"))
    else:
        print(network+" is not supported yet!")


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


def onionDump():
    # CREATE A TOR PROCESS AND SAVE RESPONSE TO FILE
    tor_process = stem.process.launch_tor_with_config(config={'SocksPort': str(9050), 'ControlPort': str(9051)})
    onionurl = input("[Onion Url]╼> ")
    path = input("[File Path]╼> ")
    try:
        request = torRequest()
        response = request.get(onionurl)
        exportContent(response, path)
    finally:
        tor_process.kill()


# FUNCTION FOR A CENSYS API REQUEST
def censysRequest(query):
    censyshost = CensysHosts(cenapikey,censecret)
    results = censyshost.search(query, per_page=5, pages=2)
    rs = results.view_all()
    hosts = censyshost.search(query, per_page=5, virtual_hosts="ONLY")
    hs = hosts()
    export = str(rs)+str(hs)
    exportContent(export, "report-"+query)


# FUNCTION TO GENERATE AI IMAGE WITH OPENAI
def openaiImageCreator(interact):
    response = openai.Image.create(prompt=interact, n=1, size="1024x1024")
    print("\n"+response['data'][0]['url'])


# FUNCTION TO ANALYZE FILE CONTENT
def openaiFileAnalyzer():
    path = input("[File Path]╼> ")
    content = importContent(path)
    prompt = "Describe following file content: " + str(content)
    type = "console"
    response = openaiRequest(type, prompt)
    print(response)


# FUNCTION TO CREATE FILE TEMPLATE
def openaiFileCreator():
    data = input("[Describe Content]╼> ")
    path = input("[File Path]╼> ")
    type = "console"
    response = openaiRequest(type, data)
    exportContent(response, path)


# FUNCTION FOR NUMLOOKUP API REQUEST
def numlookupRequest(mobilenumber):
    url = "https://api.numlookupapi.com/v1/validate/"+mobilenumber
    headers = CaseInsensitiveDict()
    headers["apikey"] = numlookupapikey
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        country_code = data["country_code"]
        carrier = data["carrier"]
        line_type = data["line_type"]
        country = data["country_name"]
        print("\nMobile Number:\t", mobilenumber)
        print("Country Code:\t", country_code)
        print("Carrier:\t", carrier)
        print("Line Type:\t", line_type)
        print("Country:\t", country)
    else:
        print("\nError retrieving data for mobile number:", mobilenumber)


# FUNCTION TO LIST SOCIAL AND REVERSE ENGINEERING MENU
def file():
    print("\nFILE MENU\n")
    print("(1)Analyze File Content ")
    print("(2)Generate File Template")
    print("(3)Generate Image")
    print("(0)Back\n")
    mode = input("[Select Mode]╼> ")    
    if mode == "1":
        openaiFileAnalyzer()
    elif mode == "2":
        openaiFileCreator()
    elif mode == "3":
        interact = input("[Description]╼> ")
        openaiImageCreator(interact)
    elif mode == "0":
        banner()
        openaiSecurityConsole()
    else:
        banner()
        print("Wrong input, try again.")
        file()


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
    print("(8)Coin Hunter")
    print("(0)Back\n")

    def reconnaissance():
        print("\nScanning target with censys search\n")
        query = input("[Domain]╼> ")
        censysRequest(query)
        
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
        mobilenumber = input("[Mobile Number]╼> ")
        numlookupRequest(mobilenumber)

    def googleDorking():
        print("\nAdvanced search techniques using Google.\n")
        # THIS IS HOW YOU COULD USE IT FURTHER FROM HERE
        results = googleDorkRequest("inurl:login site:tiktok.com")  # OPERATORS MIGHT BE SET DIFFERENT OR EXTENDED
        exportContent(results, "dork-report.html")  # SAVE RESPONSE

    def coinHunter():
        print("\nCoin Hunter - Crypto Wallet Tracker\n")
        print("(1)Bitcoin Mainnet")
        print("(2)Ethereum Mainnet")
        network = input("[Select Network]╼> ")
        address = input("[Wallet Address]╼> ")
        if network == "1":
            blockchainRequest("1", address)
        if network == "2":
            blockchainRequest("2", address)
        else:
            banner()
            print("Wrong input, try again.")
            osint()

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
    elif mode == "8":
        coinHunter()
    elif mode == "0":
        banner()
        openaiSecurityConsole()
    else:
        banner()
        print("Wrong input, try again.")
        osint()


# FUNCTION TO LIST HELP MENU - COULD BE SWAGGED UP ;)
def help():
    print("\nCOMMANDS\tDESCRIPTION\n")
    print("banner\t\tprint banner")
    print("file\t\tcall file menu")
    print("osint\t\tcall osint menu")
    print("exit\t\tquit oasc\n")


# FUNCTION FOR THE OPENAI QUERY PROMPT (CORE-SYSTEM)
def openaiSecurityConsole():
    while True:
        interact = input("[OASC]╼> ")
        # SYSTEM COMMAND HANDLER 
        if interact == "exit":
            exit()
        elif interact == "file":
            file()
        elif interact == "osint":
            osint()
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
    os.system("clear")

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


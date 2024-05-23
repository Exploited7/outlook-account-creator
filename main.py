from bs4 import BeautifulSoup
import re
import httpx
import base64
import os
import time
import random
import string
import json
import tls_client
from execjs import compile as js_compile
import requests
from colorama import init, Fore
import capsolver
import yaml
from datetime import datetime
import concurrent.futures
import ctypes
import imaplib

config = yaml.safe_load(open("config.yml", "r").read())

init()

print(f'''

{Fore.CYAN}

                ░█████╗░██╗░░░██╗████████╗██╗░░░░░░█████╗░░█████╗░██╗░░██╗
                ██╔══██╗██║░░░██║╚══██╔══╝██║░░░░░██╔══██╗██╔══██╗██║░██╔╝
                ██║░░██║██║░░░██║░░░██║░░░██║░░░░░██║░░██║██║░░██║█████═╝░
                ██║░░██║██║░░░██║░░░██║░░░██║░░░░░██║░░██║██║░░██║██╔═██╗░
                ╚█████╔╝╚██████╔╝░░░██║░░░███████╗╚█████╔╝╚█████╔╝██║░╚██╗
                ░╚════╝░░╚═════╝░░░░╚═╝░░░╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝
                https://github.com/exploited7/outlook-account-creator
                https://guns.lol/exploited7


''')





class Encryptor:
    def __init__(self):
        self._cipher = js_compile(open("cipher_value.js").read())

    def encrypt_value(self, password, num, key) -> str:
        return self._cipher.call("encrypt", password, num, key)


GENNED = 0
LOCKED = 0

def solvecap(proxy,arkoseBlob):
        try:
            if config['solver'] == 'CAPSOLVER':
                apiKeyyy = config['capKey']
                payload = {
                        "clientKey":apiKeyyy,
                        "appId":"8C7C8A1B-0404-4E00-80C8-1C05A569CB57",
                        "task": {
                            "type": "FunCaptchaTask",
                            "websitePublicKey": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
                            "websiteURL": "https://www.signu.live.com",
                            "data": '{"blob": "' + arkoseBlob + '"}',
                            "proxy":proxy
                        }
                        }

                result = requests.post("https://api.capsolver.com/createTask", json=payload)
                task_id = result.json()["taskId"]
                payload = {"taskId": task_id,"clientKey":apiKeyyy}
                while True:
                        result = requests.post("https://api.capsolver.com/getTaskResult",json=payload)
                        data = result.json()
                        if data["status"] != "ready":
                            continue
                        capkey = data["solution"]["token"]
                        return capkey


            elif config['solver'] == 'EZ-CAPTCHA':
                apiKeyyy = config['capKey']
                payload = {
                        "clientKey": apiKeyyy,
                        "appId":"79258",
                        "task": {
                        "websiteURL": "https://iframe.arkoselabs.com/",
                        "websiteKey": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
                        "type": "FuncaptchaTaskProxyless",
                        "data": arkoseBlob,
                        "funcaptchaApiJSSubdomain": ""
                        }
                        }

                result = requests.post("https://api.ez-captcha.com/createTask", json=payload)
                task_id = result.json()["taskId"]
                payload = {"taskId": task_id,"clientKey":apiKeyyy}
                while True:
                        result = requests.post("https://api.ez-captcha.com/getTaskResult",json=payload)
                        data = result.json()
                        if data["status"] != "ready":
                            continue
                        capkey = data["solution"]["token"]
                        return capkey
                    
        except Exception as e:
            return solvecap(proxy,arkoseBlob)

def set_cmd_window_title(GENNED, LOCKED):
    title = f"[Exploited7 justmanooo]  |  [ Generated : {GENNED} ]  [ Failed : {LOCKED} ]"
    ctypes.windll.kernel32.SetConsoleTitleW(title)


# Example usage:
# Replace 'server', 'username', and 'password' with your IMAP server details.
# imap_connection = connect_to_imap('imap.example.com', 'your_username', 'your_password')

set_cmd_window_title(GENNED, LOCKED)


def get_timestamp():
    time_idk = time.strftime("%H:%M:%S")
    timestamp = f"{time_idk}"
    return timestamp


def decode_url(encoded_string):
    decoded_string = re.sub(
        r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), encoded_string
    )
    return decoded_string


def generate_ai_session():
    session_id = base64.urlsafe_b64encode(os.urandom(16)).decode("utf-8").rstrip("=")

    timestamp = str(int(time.time() * 1000))

    ai_session = f"{session_id}|{timestamp}|{timestamp}"

    return ai_session


password = config["password"]


def generate_random_gmail():
    username = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = username
    return email


def decode_enc(encoded_string):
    decoded_string = encoded_string.replace("\\\\", "\\")

    decoded_string = re.sub(
        r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), decoded_string
    )

    return decoded_string


def read_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]


proxies = read_proxies("input/proxies.txt")
proxy_index = 0

def get_next_proxy():
    global proxy_index
    if not proxies:
        return None
    proxy = proxies[proxy_index]
    proxy_index = (proxy_index + 1) % len(proxies)
    return proxy


def gen():
    global GENNED, LOCKED
    proxy = get_next_proxy()
 
    email = f"{generate_random_gmail()}@outlook.com"
    session = httpx.Client(proxies=f"http://{proxy}",verify=False)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": "signup.live.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }
    resp1 = session.get("https://signup.live.com/signup", headers=headers)
    soup = BeautifulSoup(resp1.text, "html.parser")
    link_tag = soup.find("a")
    if link_tag:
        href_value = link_tag.get("href")
    coo1 = resp1.cookies
    cookies = {
        "amsc": coo1.get("amsc"),
    }
    headers["Host"] = "login.live.com"

    resp2 = session.get(href_value, headers=headers, cookies=cookies)

    coo2 = resp2.cookies
    uaid = coo2.get("uaid")

    headers["Host"] = "signup.live.com"
    resp3 = session.get(
        f"https://signup.live.com/signup?lic=1&amp;uaid={uaid}",
        headers=headers,
        cookies=cookies
    )

    coo3 = resp3.cookies
    cookies = {
        "amsc": coo3.get("amsc"),
    }
    js_content = resp3.text
    match = re.search(r'https://fpt\.live\.com/\?[^"\']+', js_content)
    if match:
        fptLink1 = match.group(0)

    api_canary_match = re.search(r'"apiCanary"\s*:\s*"([^"]+)"', js_content)
    if api_canary_match:
        api_canary_value = api_canary_match.group(1)
    else:
        return None
    api_canary_match = re.search(r'"SKI"\s*:\s*"([^"]+)"', js_content)
    if api_canary_match:
        api_canary_value = api_canary_match.group(1)
    else:
        okok = None
    api_canary_match = re.search(r'"fid"\s*:\s*"([^"]+)"', js_content)
    if api_canary_match:
        fid = api_canary_match.group(1)
    else:
        return None
    hpgid_match = re.search(r'"hpgid"\s*:\s*(\d+)', js_content)
    if hpgid_match:
        hpgid_value = hpgid_match.group(1)
    else:
        hpgid_value = 200225

    i_ui_flavor_match = re.search(r'"iUiFlavor":\s*(\d+)', js_content)
    if i_ui_flavor_match:
        i_ui_flavor_value = int(i_ui_flavor_match.group(1))

    else:
        i_ui_flavor_match2 = re.search(r'"uiflvr":\s*(\d+)', js_content)
        i_ui_flavor_value = i_ui_flavor_match2.group(1)

    scenario_id_match = re.search(r'"iScenarioId"\s*:\s*(\d+)', js_content)
    if scenario_id_match:
        scenario_id = int(scenario_id_match.group(1))

    else:
        scenario_id_match2 = re.search(r'"scid"\s*:\s*(\d+)', js_content)
        scenario_id = int(scenario_id_match2.group(1))

    key_match = re.search(r'var\s+Key\s*=\s*"([^"]+)"', js_content)
    random_num_match = re.search(r'var\s+randomNum\s*=\s*"([^"]+)"', js_content)
    ski_match = re.search(r'var\s+SKI\s*=\s*"([^"]+)"', js_content)

    if key_match and random_num_match and ski_match:
        key = key_match.group(1)
        random_num = random_num_match.group(1)
        ski = ski_match.group(1)

    else:
        return None
    
    headers['Referer'] = "https://signup.live.com/"
    headers['Host'] = "fpt.live.com"
    resp4 = session.get(
        fptLink1, headers=headers, cookies=cookies
    )  # -> https://fpt.live.com/?session_id=0ebabd70fbb44990a3d667010dc1e625&amp;CustomerId=33e01921-4d64-4f8c-a055-5bdaffd5e33d&amp;PageId=SU

    coo4 = resp4.cookies  # # fptctx2 , muid ( fake one )
    html_content = resp4.text
    soup = BeautifulSoup(html_content, "html.parser")
    script_content = None
    for script in soup.find_all("script"):
        if script.string and "txnId" in script.string:
            script_content = script.string
            break
    if script_content:
        txnId = re.search(r"txnId\s*=\s*'([^']+)'", script_content).group(1)
        ticks = re.search(r"ticks\s*=\s*'([^']+)'", script_content).group(1)
        rid = re.search(r"rid\s*=\s*'([^']+)'", script_content).group(1)
        authKey = re.search(r"authKey\s*=\s*'([^']+)'", script_content).group(1)
        cid = re.search(r"cid\s*=\s*'([^']+)'", script_content).group(1)

    else:
        return None
    
    headers['Referer'] = "https://fpt.live.com/"
    headers['Host'] = "fpt2.microsoft.com"
    resp5 = session.get(
        f"https://fpt2.microsoft.com/Clear.HTML?ctx=Ls1.0&amp;wl=False&amp;session_id={txnId}&amp;id={rid}&amp;w={ticks}&amp;tkt={authKey}&amp;CustomerId={cid}",
        headers=headers,
    )

    coo5 = resp5.cookies  # muid (real)

    data = {
        "signInName": email,
        "uaid": uaid,
        "includeSuggestions": True,
        "uiflvr": 1001,
        "scid": 100118,
        "hpgid": 200639,
    }

    cookies = {
        "amsc": coo3.get("amsc"),
        "ai_session": generate_ai_session(),
        "MUID": coo5.get("MUID"),
        "fptctx2": coo4.get("fptctx2"),
        "_pxvid": "5bbc9e2f-13e0-11ef-ba24-69de9190bebd",
        "_px3": "303fa43a2a720026c7440d0b95bf90b9bd2853cd4060a3bf40a62798b034d00d%3AHyCHygk9SecaEgt3KTvuIvTZ7UdAeUOUjiMgZoHfiTA8ed388dghd%2FC0rCd30nc1JwFa3KUlvlqu02uYtSDijg%3D%3D%3A1000%3APccVug%2B7WU1UnCvkHBEXYSMbb%2B6ZLc7Ks32%2B8VJOCCEWlnC%2BuWf2R7GtC6RpX5gkv2NzIUEUgWFYJl9AXrARBqXndpQd0PVWYzb4O6Bp6OX%2Bt0FVnTQ419fwXou0BQY58QeLmqLdFXNQOiaYtvFV72KkC6PSgRD85ecuLSv%2FgUWKHEsbYzCaQ8nd0E%2FTxbHxXK47wJHHBXY4KoJEdQsYXRvPLGRZHPj%2Fy43PL75PPRk%3D",
        "_pxde": "34858ae13dd0c46cca55769a4bc1e180cd7753f885234f7f72262df626f2ab1d%3AeyJ0aW1lc3RhbXAiOjE3MTU5MDM5ODE4MzUsImZfa2IiOjAsImlwY19pZCI6W119",
    }
    decoded = decode_url(api_canary_value)

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "canary": decoded,
        "Cookie": "; ".join([f"{k}={v}" for k, v in cookies.items() if v is not None]),
        "Connection": "keep-alive",
        "Content-Length": str(len(json.dumps(data))),
        "Content-type": "application/json; charset=utf-8",
        "correlationId": uaid,
        "Host": "signup.live.com",
        "hpgact": "0",
        "hpgid": hpgid_value,
        "Origin": "https://signup.live.com",
        "Referer": f"https://signup.live.com/signup?lic=1&amp;amp;uaid={uaid}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }

    resp6 = session.post(
        f"https://signup.live.com/API/CheckAvailableSigninNames",
        headers=headers,
        json=data,
    )

    apiCanary = resp6.json()["apiCanary"]
    telemetryContext = resp6.json()["telemetryContext"]
    timestamp = str(int(time.time() * 1000))

    data = {
        "pageApiId": 200640,
        "clientDetails": [],
        "country": "EG",
        "userAction": "Action_ClientSideTelemetry",
        "source": "PageView",
        "clientTelemetryData": {
            "category": "PageView",
            "pageName": "200640",
            "eventInfo": {
                "timestamp": timestamp,
                "enforcementSessionToken": None,
                "appVersion": None,
                "networkType": None,
            },
        },
        "cxhFunctionRes": None,
        "netId": None,
        "uiflvr": 1001,
        "uaid": uaid,
        "scid": 100118,
        "hpgid": 200640,
    }

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "canary": apiCanary,
        "Connection": "keep-alive",
        "Content-Length": str(len(json.dumps(data))),
        "Content-Type": "application/json",
        "Cookie": f'amsc={coo3.get("amsc")}; MicrosoftApplicationsTelemetryDeviceId=dfa874b8-9e17-4654-bb56-42187176e7ad; MUID={coo5.get("MUID")}; fptctx2={coo4.get("fptctx2")}; clrc={{"19861":["d7PFy/1V","+VC+x0R6","FutSZdvn"]}}; ai_session={generate_ai_session()}',
        "Host": "signup.live.com",
        "hpgid": "200640",
        "Origin": "https://signup.live.com",
        "Referer": "https://signup.live.com/?lic=1",
        "scid": "100118",
        "tcxt": telemetryContext,
        "uaid": uaid,
        "uiflvr": "1001",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "x-ms-apiTransport": "xhr",
        "x-ms-apiVersion": "2",
    }
    res = session.post(
        "https://signup.live.com/API/ReportClientEvent?lic=1",
        headers=headers,
        json=data,
    )

    apiCanary = res.json()["apiCanary"]
    telemetryContext = res.json()["telemetryContext"]

    current_time = datetime.utcnow()

    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    encryptor = Encryptor()
    encrypted_value = encryptor.encrypt_value(password, random_num, key)
    data = {
        "RequestTimeStamp": formatted_time,
        "MemberName": email,
        "CheckAvailStateMap": [f"{email}:undefined"],
        "EvictionWarningShown": [],
        "UpgradeFlowToken": {},
        "FirstName": 'justmanooo',
        "LastName": 'exploited7',
        "MemberNameChangeCount": 1,
        "MemberNameAvailableCount": 1,
        "MemberNameUnavailableCount": 0,
        "CipherValue": encrypted_value,
        "SKI": ski,
        "BirthDate": "17:11:1999",
        "Country": "EG",
        "IsOptOutEmailDefault": False,
        "IsOptOutEmailShown": True,
        "IsOptOutEmail": False,
        "LW": True,
        "SiteId": "68692",
        "IsRDM": 0,
        "WReply": None,
        "ReturnUrl": None,
        "SignupReturnUrl": None,
        "uiflvr": 1001,
        "uaid": uaid,
        "SuggestedAccountType": "EASI",
        "HFId": fid,
        "encAttemptToken": "",
        "dfpRequestId": "",
        "PhoneRepRiskScoreDetails": "",
        "RiskAssessmentDetails": "",
        "RepMapRequestIdentifierDetails": "",
        "scid": 100118,
        "hpgid": 200650,
    }
    headersx = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "canary": apiCanary,
        "Connection": "keep-alive",
        "Content-Length": str(len(json.dumps(data))),
        "Content-Type": "application/json",
        "Cookie": f'amsc={coo3.get("amsc")}; MicrosoftApplicationsTelemetryDeviceId=dfa874b8-9e17-4654-bb56-42187176e7ad; MUID={coo5.get("MUID")}; fptctx2={coo4.get("fptctx2")}; clrc={{"19861":["d7PFy/1V","+VC+x0R6","FutSZdvn"]}}; ai_session={generate_ai_session()}',
        "Host": "signup.live.com",
        "hpgid": "200650",
        "Origin": "https://signup.live.com",
        "Referer": "https://signup.live.com/?lic=1",
        "scid": "100118",
        "tcxt": telemetryContext,
        "uaid": uaid,
        "uiflvr": "1001",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "x-ms-apiTransport": "xhr",
        "x-ms-apiVersion": "2",
    }
    resp7 = session.post(
        "https://signup.live.com/API/CreateAccount?lic=1", headers=headersx, json=data
    )
    resp_data = json.loads(resp7.text)

    if "error" in resp_data:
        error_data = resp_data["error"]
        if "telemetryContext" in error_data:
            telemetryContext = error_data["telemetryContext"]
            if "data" in error_data:
                data = json.loads(error_data["data"])
                if "encAttemptToken" in data:
                    encAttemptToken = data["encAttemptToken"]
                if "repMapRequestIdentifierDetails" in data:
                    repMapRequestIdentifierDetails = data[
                        "repMapRequestIdentifierDetails"
                    ]
                if "dfpRequestId" in data:
                    dfpRequestId = data["dfpRequestId"]
                if "arkoseBlob" in data:
                    arkoseBlob = data["arkoseBlob"]

    else:
        return None

    solution = solvecap(proxy,arkoseBlob)
    print(f"{Fore.LIGHTBLACK_EX}[{get_timestamp()}] [+] {Fore.CYAN} Solved Captcha {solution[0:25]}****")

    timestamp = str(int(time.time() * 1000))

    data = {
        "pageApiId": 201040,
        "clientDetails": [],
        "country": "EG",
        "userAction": "Action_LoadEnforcement,Action_ClientSideTelemetry",
        "source": "UserAction",
        "clientTelemetryData": {
            "category": "UserAction",
            "pageName": "201040",
            "eventInfo": {
                "timestamp": timestamp,
                "enforcementSessionToken": None,
                "appVersion": None,
                "networkType": None,
            },
        },
        "cxhFunctionRes": None,
        "netId": None,
        "uiflvr": 1001,
        "uaid": uaid,
        "scid": 100118,
        "hpgid": 201040,
    }
    headers['Content-Length'] = str(len(json.dumps(data)))
    headers['tcxt'] = telemetryContext
    headers['uaid'] = uaid
    headers['canary'] = apiCanary
    headers['Cookie'] = f'amsc={coo3.get("amsc")}; MUID={coo5.get("MUID")}; fptctx2={coo4.get("fptctx2")}; clrc={{"19861":["d7PFy/1V","+VC+x0R6","FutSZdvn"]}}; ai_session={generate_ai_session()}'
    
    x = session.post(
        "https://signup.live.com/API/ReportClientEvent?lic=1",
        headers=headers,
        json=data,
    )
    apiCanary = x.json()["apiCanary"]
    telemetryContext = x.json()["telemetryContext"]

    zz = solution
    data = {
        "pageApiId": 201040,
        "clientDetails": [],
        "country": "EG",
        "userAction": "Action_CompleteEnforcement,Action_ClientSideTelemetry",
        "source": "UserAction",
        "clientTelemetryData": {
            "category": "UserAction",
            "pageName": "201040",
            "eventInfo": {
                "timestamp": 1715957630419,
                "enforcementSessionToken": zz,
                "appVersion": None,
                "networkType": None,
            },
        },
        "cxhFunctionRes": None,
        "netId": None,
        "uiflvr": 1001,
        "uaid": uaid,
        "scid": 100118,
        "hpgid": 201040,
    }
    # headers['Content-Length'] = str(len(json.dumps(data)))
    headers.pop('Content-Length')
    headers['tcxt'] = telemetryContext
    headers['uaid'] = uaid
    headers['canary'] = apiCanary
    headers['Cookie'] = f'amsc={coo3.get("amsc")}; MUID={coo5.get("MUID")}; fptctx2={coo4.get("fptctx2")}; clrc={{"19861":["d7PFy/1V","+VC+x0R6","FutSZdvn"]}}; ai_session={generate_ai_session()}'

    c = session.post(
        "https://signup.live.com/API/ReportClientEvent?lic=1",
        headers=headers,
        json=data,
    )
    apiCanary = c.json()["apiCanary"]
    telemetryContext = c.json()["telemetryContext"]
    current_time = datetime.utcnow()

    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    encryptor = Encryptor()
    encrypted_value = encryptor.encrypt_value(password, random_num, key)
    data = {
        "RequestTimeStamp": formatted_time,
        "MemberName": email,
        "CheckAvailStateMap": [f"{email}:undefined"],
        "EvictionWarningShown": [],
        "UpgradeFlowToken": {},
        "FirstName": "manuel",
        "LastName": "emad",
        "MemberNameChangeCount": 1,
        "MemberNameAvailableCount": 1,
        "MemberNameUnavailableCount": 0,
        "CipherValue": encrypted_value,
        "SKI": ski,
        "BirthDate": "17:11:1999",
        "Country": "EG",
        "IsOptOutEmailDefault": False,
        "IsOptOutEmailShown": True,
        "IsOptOutEmail": False,
        "LW": True,
        "SiteId": "68692",
        "IsRDM": 0,
        "WReply": None,
        "ReturnUrl": None,
        "SignupReturnUrl": None,
        "uiflvr": 1001,
        "uaid": uaid,
        "SuggestedAccountType": "EASI",
        "HFId": fid,
        "HType": "enforcement",
        "HSol": zz,
        "HPId": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
        "encAttemptToken": encAttemptToken,
        "dfpRequestId": dfpRequestId,
        "PhoneRepRiskScoreDetails": "",
        "RiskAssessmentDetails": "",
        "RepMapRequestIdentifierDetails": repMapRequestIdentifierDetails,
        "scid": 100118,
        "hpgid": 201040,
    }
    
    headersx.pop('Content-Length')
    headersx['Cookie'] = f'amsc={coo3.get("amsc")}; MicrosoftApplicationsTelemetryDeviceId=dfa874b8-9e17-4654-bb56-42187176e7ad; MUID={coo5.get("MUID")}; fptctx2={coo4.get("fptctx2")}; clrc={{"19861":["d7PFy/1V","+VC+x0R6","FutSZdvn"]}}; ai_session={generate_ai_session()}'
    headersx['tcxt'] = telemetryContext
    headersx['uaid'] = uaid
    headersx['canary'] = apiCanary
    d = session.post(
        "https://signup.live.com/API/CreateAccount?lic=1", headers=headers, json=data
    )
    if d.status_code == 200:
        print(f"{Fore.LIGHTBLACK_EX}[{get_timestamp()}] [+] {Fore.LIGHTCYAN_EX} Account created {email}:{password}")

        with open("output/Genned.txt", "a") as f:
            f.write(f"{email}:{password}\n")

        GENNED += 1
        set_cmd_window_title(GENNED, LOCKED)

    else:
        print(d.text)



MAX_CONCURRENT_TASKS = config["threads"]


def main():
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_TASKS) as executor:
            futures = [executor.submit(gen) for _ in range(MAX_CONCURRENT_TASKS)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result(timeout=60)
                except Exception as e:
                    # print(e)
                    pass

if __name__ == "__main__":
    main()

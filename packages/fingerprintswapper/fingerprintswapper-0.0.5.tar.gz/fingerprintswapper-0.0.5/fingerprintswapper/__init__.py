import requests
import json as js
from enum import Enum
#from playwright.sync_api import Page,BrowserContext
#from selenium.webdriver.remote.webdriver import WebDriver
class Framework(Enum):
    SELENIUM="selenium"
    PLAYWRIGHT="playwright"
class Components:
    def __init__(self,json):
        try:
            if isinstance(json,str):json=js.loads(json)
            self.fonts=json.get("fonts",None)
            self.domBlockers=json.get("domBlockers",None)
            self.fontPreferences=json.get("fontPreferences",None)
            self.audio=json.get("audio",None)
            self.screenFrame=json.get("screenFrame",None)
            self.canvas=json.get("canvas",None)
            self.languages=json.get("languages",None)
            self.colorDepth=json.get("colorDepth",None)
            self.deviceMemory=json.get("deviceMemory",None)
            self.screenResolution=json.get("screenResolution",None)
            self.hardwareConcurrency=json.get("hardwareConcurrency",None)
            self.timezone=json.get("timezone",None)
            self.sessionStorage=json.get("sessionStorage",None)
            self.localStorage=json.get("localStorage",None)
            self.indexedDB=json.get("indexedDB",None)
            self.openDatabase=json.get("openDatabase",None)
            self.platform=json.get("platform",None)
            self.fpluginsonts=json.get("plugins",None)
            self.touchSupport=json.get("touchSupport",None)
            self.vendor=json.get("vendor",None)
            self.vendorFlavors=json.get("vendorFlavors",None)
            self.cookiesEnabled=json.get("cookiesEnabled",None)
            self.colorGamut=json.get("colorGamut",None)
            self.forcedColors=json.get("forcedColors",None)
            self.monochrome=json.get("monochrome",None)
            self.contrast=json.get("contrast",None)
            self.reducedMotion=json.get("reducedMotion",None)
            self.reducedTransparency=json.get("reducedTransparency",None)
            self.hdr=json.get("hdr",None)
            self.math=json.get("math",None)
            self.pdfViewerEnabled=json.get("pdfViewerEnabled",None)
            self.architecture=json.get("architecture",None)
            self.applePay=json.get("applePay",None)
            self.audioBaseLatency=json.get("audioBaseLatency",None)
            self.dateTimeLocale=json.get("dateTimeLocale",None)
            self.webGlBasics=json.get("webGlBasics",None)
            self.webGlExtensions=json.get("webGlExtensions",None)
        except:pass
    def json(self):return js.dumps(self.__dict__)
    def __repr__(self):return self.json()
    def __str__(self):return self.json()
class Fingerprint:
    def __init__(self,id:str,userAgent:str,json):
        try:
            if isinstance(json,str):json=js.loads(json)
            self.components=Components(json["components"])
            self.version=json["version"]
            self.userAgent=userAgent
            self.id=id
        except:self=None
    def mobile(self):
        try:
            c=self.components
            if not c.get("platform") or not c.get("vendor") or not c.get("touchSupport"):return False
            ua=self.userAgent.lower()
            platform=c.platform.lower()
            vendor=c.vendor.lower()
            ts=c.touchSupport
            return(
                "iphone" in ua or
                "ipad" in ua or
                "ipod" in ua or
                "android" in ua or
                "ios" in platform or
                ("mac" in platform and "touch" in str(ts).lower() )or
                "arm" in platform or
                c.screenResolution[0]<=800 or
                ts.get("touchEvent",False) or
                "adreno" in c.webGlBasics.get("rendererUnmasked","").lower() or
                ("apple" in vendor and ts.get("maxTouchPoints",0)>1)
            )
        except:return False
    def json(self):return js.dumps({"id":self.id,"userAgent":self.userAgent,"fingerprint":"###$$$^^^"}).replace("###$$$^^^",self.components.json())
    def __repr__(self):return self.json()
    def __str__(self):return self.json()
class FingerprintSwapper:
    def __init__(self,driver,framework:Framework):
        self.framework=framework
        self.driver=driver
    def _get(self,keyword:str=None,mobile:bool=False):
        R=requests.get("https://dex.mba/fingerprint/fp.php?g"+("&mobile" if mobile else ""),headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3"})
        if R.status_code==200:
            j=R.json()
            return j if j.get("status",False) else None
        else:return None
    def get(self,keyword:str=None,mobile:bool=False):
        R=self._get(keyword,mobile)
        if R is None:return None
        R=R.get("data",None)
        if R is None:return None
        id=R.get("id",None)
        ua=R.get("userAgent",None)
        fp=R.get("fingerprint",None)
        return None if id is None or ua is None or fp is None else Fingerprint(id,ua,fp)
    def apply(self,fingerprint:Fingerprint):
        if self.framework==Framework.SELENIUM:
            self._apply_selenium(fingerprint)
        elif self.framework==Framework.PLAYWRIGHT:
            self._apply_playwright(fingerprint)
    def _apply_selenium(self,fp:Fingerprint):
        cdp=self.driver.execute_cdp_cmd
        fp.components.deviceMemory=fp.components.deviceMemory or 1.0
        fp.components.screenResolution=fp.components.screenResolution or [1920,1080]
        cdp("Network.setUserAgentOverride",{"userAgent":fp.userAgent})
        cdp("Emulation.setLocaleOverride",{"locale":fp.components.dateTimeLocale})
        cdp("Emulation.setTimezoneOverride",{"timezoneId":fp.components.timezone})
        cdp("Emulation.setDeviceMetricsOverride",{
            "width":fp.components.screenResolution[0],
            "height":fp.components.screenResolution[1],
            "deviceScaleFactor":fp.components.deviceMemory,
            "mobile":fp.mobile()
        })
        spoof_script=f"""
        Object.defineProperties(navigator,{{
            platform:{{get:()=>"{fp.components.platform}"}},
            languages:{{get:()=>{fp.components.languages}}},
            hardwareConcurrency:{{get:()=>{fp.components.hardwareConcurrency}}},
            plugins:{{get:()=>{fp.components.fpluginsonts}}},
            vendor:{{get:()=>"{fp.components.vendor}"}},
            cookieEnabled:{{get:()=>{str(fp.components.cookiesEnabled).lower()}}},
            maxTouchPoints:{{get:()=>{fp.components.touchSupport['maxTouchPoints']}}},
            deviceMemory:{{get:()=>{fp.components.deviceMemory}}}
        }});
        const originalGetContext=HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext=function(type,attributes){{
            const ctx=originalGetContext.call(this,type,attributes);
            ctx.getParameter=function(param){{
                if(param===37446)return"{fp.components.webGlBasics['rendererUnmasked']}";
                if(param===7937)return"{fp.components.webGlBasics['renderer']}";
                return originalGetContext(param);
            }};
            return ctx;
        }};
        """
        self.driver.execute_script(spoof_script)
    def _apply_playwright(self,fp:Fingerprint):
        fp.components.deviceMemory=fp.components.deviceMemory or 1.0
        fp.components.screenResolution=fp.components.screenResolution or [1920,1080]
        context_args={
            "user_agent":fp.userAgent,
            "locale":fp.components.dateTimeLocale,
            "timezone_id":fp.components.timezone,
            "viewport":{"width":fp.components.screenResolution[0],"height":fp.components.screenResolution[1]},
            "device_scale_factor":fp.components.deviceMemory,
            "java_script_enabled":True,
            "is_mobile":fp.mobile()
        }
        context=self.driver.browser.new_context(**context_args)
        spoof_script=f"""
        Object.defineProperties(navigator,{{
            platform:{{get:()=>"{fp.components.platform}"}},
            languages:{{get:()=>{fp.components.languages}}},
            hardwareConcurrency:{{get:()=>{fp.components.hardwareConcurrency}}},
            plugins:{{get:()=>{fp.components.fpluginsonts}}},
            vendor:{{get:()=>"{fp.components.vendor}"}},
            cookieEnabled:{{get:()=>{str(fp.components.cookiesEnabled).lower()}}},
            maxTouchPoints:{{get:()=>{fp.components.touchSupport['maxTouchPoints']}}},
            deviceMemory:{{get:()=>{fp.components.deviceMemory}}}
        }});
        const originalGetContext=HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext=function(type,attributes){{
            const ctx=originalGetContext.call(this,type,attributes);
            ctx.getParameter=function(param){{
                if(param===37446)return"{fp.components.webGlBasics['rendererUnmasked']}";
                if(param===7937)return"{fp.components.webGlBasics['renderer']}";
                return originalGetContext(param);
            }};
            return ctx;
        }};
        """
        context.add_init_script(spoof_script)
        self.driver=context.new_page()
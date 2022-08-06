import requests

base_url = "https://www.youtube.com/youtubei/v1/next?"

class ContinuationFetcher:
    params = {}
    offset = 0
    def __init__(self, videoId, offsetMs = 0):
        self.initializeParams(videoId)
        self.offset = offsetMs

    def initializeParams(self, videoId):
        self.params["context"] = self.initializeContext()
        self.params["videoId"] = videoId
        self.params["params"] = ""
        self.params["racyCheckOk"] = False
        self.params["contentCheckOk"] = False
        self.params["autonavState"] = "STATE_NONE"
        self.params["playbackContext"] = {}
        self.params["captionRequested"] = False

    def initializeContext(self, offsetRequest = True):
        context = {}
        context["client"] = self.initializeClient()
        context["user"]= {"lockedSafetyMode" : False}
        context["request"] = {}
        context["clickTracking"] = {}
        context["adSignalsInfo"] = {}

        if offsetRequest:
            context["currentPlayerState"] = {"playerOffsetMs" : "100000"}
        
        return context
    
    def initializeClient(self):
        client = {}
        client["hl"] = "en"
        client["gl"] = "US"
        client["visitorData"] = ""
        client["remoteHost"] = ""
        client["deviceMake"] = ""
        client["deviceModel"] = ""
        client["userAgent"] = ""
        client["clientName"] = "WEB"
        client["clientVersion"] = "2.20220801.00.00"
        client["osName"] = ""
        client["osVersion"] = ""
        client["originalUrl"] = ""
        client["platform"] = "DESKTOP"
        client["clientFormFactor"] = "UNKNOWN_FORM_FACTOR"
        client["configInfo"] = {"appInstallData" : ""}
        client["userInterfaceTheme"] = "USER_INTERFACE_THEME_DARK"
        client["timezone"] = ""
        client["browserName"] = ""
        client["browserVersion"] = ""
        client["screenWidthPoints"] = "1920"
        client["screenHeightPoints"] = "955"
        client["screenPixelDensity"] = 1
        client["screenDensityFloat"] = 1
        client["utcOffsetMinutes"] = -240
        client["clientScreen"] = "WATCH"
        client["mainAppWebInfo"] = {"graftUrl": "", "webDisplayMode" : "WEB_DISPLAY_MODE_BROWSER", "isWebNativeShareAvailable" : False}
        
        return client


        
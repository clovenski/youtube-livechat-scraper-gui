from sqlite3 import Timestamp
import requests
from continuation_builder import ContinuationFetcher
from continuation_requestor import ContinuationRequestor
from livechat_requestor import livechatRequestor
from livechat_parser import livechatParser
from player_state import PlayerState
from subsequent_requestor import SubsequentRequestor
import json
from types import SimpleNamespace
import ast
from initialDocumentExtractor import initialExtractor
from initialDocumentRequestor import initialDocumentRequestor
import sys

CONTINUATION_FETCH_BASE_URL = "https://www.youtube.com/youtubei/v1/next?"

class LiveChatScraper:
    videoId = None
    videoUrl = None
    continuation = ''
    playerState = None
    contentSet = []
    content = ''
    currentOffsetTimeMsec = 0

    def __init__(self, videoUrl):
        #TODO save videoID from URL
        self.videoUrl= videoUrl
        self.extractVideoID(videoUrl)

    def getEndTime(self):
        documentRequestor = initialDocumentRequestor()
        initialDocument = documentRequestor.getContent(self.videoUrl)
        endTimeSeeker = initialExtractor()
        # print(str(initialDocument.text))
        initialContent = endTimeSeeker.buildAndGetScript(initialDocument.text)
        return initialContent["annotations"][0]["playerAnnotationsExpandedRenderer"]["featuredChannel"]["endTimeMs"]

    def extractVideoID(self, videoUrl):
        keyStart = videoUrl.find('=')+1
        keyEnd = keyStart+11
        self.videoId = videoUrl[keyStart:keyEnd]

    def getContinuation(self):
        continuationRequestor = ContinuationRequestor(self.videoId)
        continuationRequestor.buildFetcher()
        continuationRequestor.makeRequest()

        self.continuation = continuationRequestor.continuation

    def getInitialLiveChatContents(self):
        liveChatContents = livechatRequestor(self.continuation)
        liveChatContents.buildURL()
        return liveChatContents.getLiveChatData()

    def parseInitialContents(self, initialContents):
        parser = livechatParser('html.parser')
        parser.buildParser(initialContents)
        content = parser.findContent()
        self.continuation = parser.initialContinuation
        self.playerState = PlayerState()
        self.playerState.continuation = self.continuation
        # for c in content[1::]:
        #     self.content += str(c["replayChatItemAction"])
        #     c["replayChatItemAction"]["batch"] = "INITIAL"
            # self.contentSet.append(c["replayChatItemAction"])
        # self.playerState.playerOffsetMs = 0
        

    def parseSubsequentContents(self):
        subRequestor = SubsequentRequestor(self.videoId, self.playerState)
        subRequestor.buildFetcher()
        subRequestor.makeRequest()
        content = subRequestor.response["continuationContents"]["liveChatContinuation"]["actions"][1::]
        self.playerState.continuation = subRequestor.updateContinuation(subRequestor.response)
        for c in content:
            self.content += str(c["replayChatItemAction"])
            self.contentSet.append(c["replayChatItemAction"])
        self.playerState.playerOffsetMs = self.findOffsetTimeMsecFinal()

    def findOffsetTimeMsecFinal(self):
        finalContent = self.contentSet[-1]
        return finalContent["videoOffsetTimeMsec"]

    def outputContent(self):
        for c in self.contentSet:
            comment = ''
            timestamp = ''
            author = ''
            giftContent = False
            superChatContent = False
            if("addLiveChatTickerItemAction" in c["actions"][0] 
               or "liveChatSponsorshipsGiftPurchaseAnnouncementRenderer" in c["actions"][0]["addChatItemAction"]["item"]  
               or "liveChatTickerSponsorItemRenderer" in c["actions"][0]["addChatItemAction"]["item"]):
                giftContent = True
            elif("liveChatPaidMessageRenderer" in c["actions"][0]["addChatItemAction"]["item"]):
                superChatContent = True

            if not giftContent and not superChatContent:
                if("liveChatMembershipItemRenderer" in c["actions"][0]["addChatItemAction"]["item"]):
                    timestamp = c["actions"][0]["addChatItemAction"]["item"]["liveChatMembershipItemRenderer"]["timestampText"]["simpleText"] 
                    author = c["actions"][0]["addChatItemAction"]["item"]["liveChatMembershipItemRenderer"]["authorName"]["simpleText"]
                    comment = c["actions"][0]["addChatItemAction"]["item"]["liveChatMembershipItemRenderer"]["message"]["runs"][0]["text"]
                elif("emoji" in c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"][0]):
                    timestamp = c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]
                    author = c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["authorName"]["simpleText"]
                    comment =  c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"][0]["emoji"]["image"]["accessibility"]["accessibilityData"]["label"]
                else:
                    timestamp = c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]
                    author = c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["authorName"]["simpleText"]
                    comment = c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"][0]["text"]
                    # print(c["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"][0]["text"])
                print("({0}) {1}: {2}".format(timestamp, author, comment))
    
if(len(sys.argv) == 1):
    print("No ID provided")
    sys.exit()
scraper = LiveChatScraper(sys.argv[1])
scraper.getContinuation()
contents = scraper.getInitialLiveChatContents()
scraper.parseInitialContents(contents)
scraper.parseSubsequentContents()
endTimeMs = int(scraper.getEndTime())
# print(endTimeMs)
while(int(scraper.playerState.playerOffsetMs) < endTimeMs):
    print(scraper.playerState.playerOffsetMs)
    scraper.parseSubsequentContents()

with open('output.txt', 'w', encoding='utf-8') as writer:
    writer.write(scraper.outputContent())
# scraper.outputContent()


'''
    step 1: 
        Grab initial continuation value  using continuation builder and requestors, these will require the videoId
    
    step 2:
        Use initial continuation value to fetch first livechat request using livechat_requestor and livechat_parser.
        The first livechat contents will be returned in a script embedded in a HTML document, which is why the parser is required
        to extract the contents.

        Ensure the continuation value updates after the livechat_requestor is done executing. The continuation value will update 
        each time a request is made as it is used to keep track of where we are on the video's timeline.

    step 3:
        Use subsequent_requestor and start a loop to grab each block of livechat data. Each time a request is made, the continuation
        value MUST be update to ensure the next obtained block of data does not contain any duplicates or missed values.
'''

# scraper = LiveChatScraper('https://www.youtube.com/watch?v=EezhXfjR1_k')
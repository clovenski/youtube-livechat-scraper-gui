""""example to see how the live chat scraper scrapes and outputs data."""
import sys
import time
from livechat_scraper.messages.membership_gifted_message import MembershipGiftedMessage
from livechat_scraper.messages.superchat_message import SuperChatMessage
from livechat_scraper.scrapers import livechat_scraper
from livechat_scraper.constants import scraper_constants as sCons


def test_scraper_output(video_url):
    """"livechat scraper example, scrapes a video URL and outputs the content 
        to a JSON, txt, and raw file.
    """
    start_time = time.time()
    scraper = livechat_scraper.LiveChatScraper(video_url)
    scraper.scrape()
    # saves all messages in a file as a json object
    scraper.write_to_file(sCons.OUTPUT_JSON, "testJson_"+scraper.output_filename)
    # saves all messages in a txt file, each line is a message entry
    scraper.write_to_file(sCons.OUTPUT_TEXT, "testText_"+scraper.output_filename)
    # saves all messages in a json file preserving the raw json that comes over when making the request call to youtube
    scraper.write_to_file(sCons.OUTPUT_RAW, "testRaw_"+scraper.output_filename)
    # filtering for specific message types
    scraper.write_to_file(sCons.OUTPUT_JSON, "testJson_filtered"+scraper.output_filename, message_type_whitelist=(SuperChatMessage, MembershipGiftedMessage))
    end_time = time.time()
    print(f'program runtime: {end_time - start_time}')

if len(sys.argv) == 1:
    test_scraper_output("https://www.youtube.com/watch?v=u33Cg5zoci0")
else:
    test_scraper_output(sys.argv[1])

# youtube-livechat-scraper-gui

A small tool to scrape youtube livechat data. It rips almost all data from a VOD's livechat including the following:

- Superchats
- Memberships gifted and received

Use this tool in case you'd like to, for example, see who is the top super chat donator for a stream, or to see how many memberships were gifted for a stream.

## Usage

1. Enter the YouTube URL of the stream vod.
2. Click the `Scrape` button to start scraping the live chat for that past stream.
3. Once done, checkmark which message types you'd like to display (either superchats only, gifted members only, or both, etc.).
4. The messages will appear in the table.
5. You can also save the message results displayed on the table into a CSV (comma separated values) file. You would do this if you'd like to do further processing on the results; for example, adding up all the gifted members.

## Development

Requires the following python3 packages:

- NOTE: These packages will be installed via pip when installing the scraper.
- BeautifulSoup
- Requests

Regarding the engine:

- Import the LiveChatScraper from scrapers.liveChatScraper to wherever you want to make the scraping call.
- Find a VOD URL and copy it
- Create a LiveChatScraper object and pass in the VOD's URL.
- Call the scrape() method on the created scraper object and the scrape will run.
- Once the scrape is completed, you can call ouputMessages() to get a dictionary with all the scraped data.
- You can all save the scraped data as a JSON to a fill by calling the writeToFile method passing the OUTPUT_JSON constant

- example.py has a working example which saves the data to different formats

Regarding the GUI:

`python gui.py` to run locally.

For building the single exe:

```powershell
pyinstaller -w --add-data ".\assets\;.\assets\" --add-data ".\livechat_scraper\;.\livechat_scraper\" --add-data ".\ui\;.\ui\" --hidden-import "json" --hidden-import "tkinter.messagebox" --hidden-import "tkinter.filedialog" --hidden-import "uuid" --hidden-import "requests" --hidden-import "bs4" --hiddenimport 'tkinter.ttk' -n yt-livechat-scraper --icon ".\assets\icon-32px.ico"  .\gui.py
```

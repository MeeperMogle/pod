# pod
Objects of the class read through it's specified Feed URL, downloading all new (.mp3) files that are caught in the user-provided Regular Expression.

What files are new are determined by locally stored text files with the .downloaded extension, one per feed.

_A method for filling in the .downloaded file (for the user to just edit out the newest ones they want) is available._

---

Example usage, one feed:
```python
from pod import pod

feedUrl = "http://thepipodcast.com/feed/"
friendlyName = "The Pi Podcast"
regularExpression = '(?<=<enclosure url=")http.+redirect\.mp3.+\.mp3(?=" length=")'

podcast = pod(feedUrl,friendlyName,regularExpression)
podcast.downloadAnyNewFiles()
```

---

Useful, optional object constructor parameters:

- **outputFolder**: *(Defaults to "./")* Where to put the downloaded files
- **prepend**: *(Defaults to "")* Useful for relative links; adds to the start of each link to download
- **append**: *(Defaults to "")* Useful for relative links; adds to the end of each link to download
- **downloadedLogsFolder**: *(Defaults to "./")* Where to store the "remembered" downloaded filenames
- **fileExtensionsRegex**: *(Defaults to "\\.mp3")* Matches the target file extension(s) in the feed to find and download

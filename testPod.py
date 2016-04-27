from pod import pod

feedUrl = "http://thepipodcast.com/feed/"
friendlyName = "The Pi Podcast"
regularExpression = '(?<=<enclosure url=")http.+redirect\.mp3.+\.mp3(?=" length=")'

podcast = pod(feedUrl,friendlyName,regularExpression)
podcast.downloadAnyNewFiles()
from os import cpu_count

CHAPTERS = "chapters"
CONTENT = "content"
DESCRIPTION = "description"
ENCLOSURE_DL_PATH = "enclosureDownloadPath"
ENCLOSURE_URL = "enclosureUrl"
EPISODES = "episodes"
EPISODES_EXTENDED = "episodes_extended"
FEEDS = "feeds"
FEEDS_EXTENDED = "feeds_extended"
FEED_ID = "feedId"
FEED_TITLE = "feedTitle"
FEED_XML_URL = "feedXmlUrl"
GUID = "guid"
IMAGE = "image"
INCLUDE_PODCAST_IDS = "includePodcastIds"
LAST_UPDATED = "lastUpdated"
LINK = "link"
OVERCAST_ID = "overcastId"
PLAYLISTS = "playlists"
PROGRESS = "progress"
PUB_DATE = "pubDate"
SMART = "smart"
SORTING = "sorting"
SOURCE = "source"
TIME = "time"
TITLE = "title"
TRANSCRIPT_DL_PATH = "transcriptDownloadPath"
TRANSCRIPT_TYPE = '"podcast:transcript:type"'
TRANSCRIPT_URL = '"podcast:transcript:url"'
URL = "url"
USER_REC_DATE = "userRecommendedDate"
USER_UPDATED_DATE = "userUpdatedDate"
XML_URL = "xmlUrl"

_CPU_COUNT = cpu_count() or 6
BATCH_SIZE = _CPU_COUNT * 2

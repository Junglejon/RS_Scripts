import requests
import json

# Scrub data from RS
def GrabTheDataFromRS():
    request = "https://ugc-retail.ib.ubi.com/v1/songLibrary/songs/withoutArrangements"
    param = {"page": 1, "pageSize": 25, "sortKey": "songName", "descOrder": "false"}
    
    #
    # Grab an auth token from dev view of your browser on
    # https://www.ubisoft.com/en-us/game/rocksmith/plus/rocksmith-workshop/without-arrangements
    header = {
        "authorization": "" } 
    

    responses = []
    keepGoing = True
    while keepGoing:
        x = requests.get(request, params=param, headers=header)
        rsJson = x.json()
        responses.append(rsJson)

        keepGoing = param["page"] < 257
        param["page"] = param["page"] + 1

    jsonSave = json.dumps(responses)

    with open("RocksmithOutput.json", "w", encoding="utf-8") as rsFile:
        rsFile.write(jsonSave)

# Organize the data
def ParseTheData():
    print("Do Stuff!!")

    rsFile = open("RocksmithOutput.json", encoding="utf-8")
    allTheContent = json.load(rsFile)        
    
    songs = {}
    for page in allTheContent:
        theData = page["data"]

        if theData:
            for song in theData:
                if song["artistName"] in songs.keys():
                    artist = songs[song["artistName"]]
                    if song["albumName"] in artist.keys():
                        artist[song["albumName"]].append(song["songName"])
                    else:
                        artist[song["albumName"]] = [song["songName"]]
                else:
                    songs[song["artistName"]] = {song["albumName"]: [song["songName"]]}

    res = {key: val for key, val in sorted(songs.items(), key = lambda ele:ele[0])}
    print(res)

    with open("RocksmithParsed.json", "w") as rsFile:
        rsFile.write(json.dumps(res))

# Match against local library exports to prioritize
# what to transcribe, count of artist in library determines sort priority
# TODO: Change to weight on plays and weighting
def matchFromRocksmith():
	artists = json.load(open(r"Rocksmith\RocksmithParsed.json"))    
	music = json.load(open(r"Rocksmith\music.json"))
	matchedArtists = set(music.keys()) & set(artists.keys())

	filtered = []
	for matchedArtist in matchedArtists:
		filtered.append({"artist": matchedArtist, "albums": artists[matchedArtist], "Priority": music[matchedArtist]})

	filtered = sorted(filtered, key=lambda d: d['Priority'], reverse=True)

	json_object = json.dumps(filtered, indent=4)
	
	with open("filteredRocksmith.json", "w") as seekFile:
		seekFile.write(json_object)

#GrabTheDataFromRS()
#ParseTheData()
#matchFromRocksmith()

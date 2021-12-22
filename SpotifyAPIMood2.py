import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Authentication process using Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope = "user-read-recently-played,playlist-modify-private,playlist-modify-public",client_id='3b17a2138f654ee2af635167b3a14e3a', client_secret='26309b0980754c04992edc602e9ac31e', redirect_uri = "http://localhost:8080"))

def getRecentTracks():

    # Gets recently played songs
    results = sp.current_user_recently_played(limit = 50) 
    return results

    
   
def printRecentTracks(results):

    # Prints recent tracks
    for i, item in enumerate(results['items']):
        track = item['track']
        print(i + 1, track['artists'][0]['name'], " – ", track['name'])
    
        
          
def getFeatures(results):

    # Seperates track IDs
    spotifyID = []
    for i, item in enumerate(results['items']):
        track = item['track']
        spotifyID.append(track["id"])
    

    # Forms a DataFrame with the features of each song
    features = []
    features.append(sp.audio_features(spotifyID))
    df = pd.DataFrame(features)
    df.to_csv('recentSongsDataset.csv',index=False)

    # Finds the average valence of the past 50 songs
    valence = []
    for j in range(50):
        valence.append(features[0][j]['valence'])
    avValence = sum(valence)/len(valence)
    return avValence
  


def alterMood(avValence):

    # Writes the average valence to a text file
    MusicMood = str(int(avValence * 100)) 
    x = open("Mood.txt", "a")
    x.truncate(0)
    x.write(MusicMood)
    x.close()


# I will need the song ids of songs that have a valence above a certain value. This should be taken in context with other songs. I will create a csv file with happy songs in it. max playlist length will be 50. If the playlist is longer than 50 then I will start nocking off music that has been in the playlist longest. 
# the items refers to each value in results the i in necassery to allow for the for loop to loop through the list.
# this seems to be a good measure for how happy a song should be 
# need to identify if a playlist already exists
# need this for working passing to other api requests 
# checks to see if the playlist already exists
# replaces the old songs with some newer happy ones.
# if the playlist does not exist it creates one, important that its public so we can see it in the next api call   
# need to be public for this to be different from previous call
# cycles through items in the dictionary


def createHappyPlaylist(results):

    # Seperates track IDs and finds features of last 50 songs
    spotifyID = []
    for i, item in enumerate(results['items']): 
        track = item['track']
        spotifyID.append(track["id"])
    features = []
    features.append(sp.audio_features(spotifyID))
    happySongsID = []
    for j in range(50):
        valence = (features[0][j]['valence'])

        # If the song is happy add ID to list
        if valence > 0.75: 
            happySongsID.append(features[0][j]['id'])
    
    # Checks to see if "Happy Vibes" exists
    playlists = sp.current_user_playlists()
    playlistNames = []
    playlistIDs = []
    for i, item in enumerate(playlists['items']):
        playlistNames.append(item["name"])
        playlistIDs.append(item["id"]) 

    # Replace the songs in "Happy Vibes"    
    if "Happy Vibes" in playlistNames: 
        positionIndex = playlistNames.index("Happy Vibes")   
        sp.playlist_replace_items(playlist_id = playlistIDs[positionIndex], items = happySongsID) 
    
    # Create a playlist with called Happy Vibes
    else: 
        sp.user_playlist_create(user = "d23zzt1cy4l04283ewvgktqoy", name = "Happy Vibes", description= "A happy playlist for you to listen to when things aren't going so great.", public= True )
        playlists = sp.current_user_playlists() 
        for i, item in enumerate(playlists['items']): 
            playlistNames.append(item["name"])
            playlistIDs.append(item["id"])
        positionIndex = playlistNames.index("Happy Vibes")
        sp.playlist_add_items(playlist_id = playlistIDs[positionIndex], items = happySongsID)
    return happySongsID



def spotifyReadFull():

    # Finds Average Valence
    results = getRecentTracks()
    avValence = getFeatures(results)
    alterMood(avValence)
    return avValence

def HappyPlayslistFull():

    # Creates a Happy Playlist
    results = getRecentTracks()
    createHappyPlaylist(results)

def main():
    results = getRecentTracks()
    createHappyPlaylist(results)
    """printRecentTracks(results)
    avValence = getFeatures(results)
    alterMood(avValence)"""


if __name__ == '__main__':
    print("Running Programn")
    main()
    
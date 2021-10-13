import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope = "user-read-recently-played,playlist-modify-private,playlist-modify-public",client_id='3b17a2138f654ee2af635167b3a14e3a', client_secret='26309b0980754c04992edc602e9ac31e', redirect_uri = "http://localhost:8080"))

def getRecentTracks():
    results = sp.current_user_recently_played(limit = 50) # this is how many songs the average person listens to per day and thus should be a good numbner for this
    return results

    
   
def printRecentTracks(results):
     for i, item in enumerate(results['items']):
        track = item['track']
        print(i + 1, track['artists'][0]['name'], " – ", track['name'])
    
        
          
def getFeatures(results):
    spotifyID = []
    for i, item in enumerate(results['items']):
        track = item['track']
        spotifyID.append(track["id"])
    features = []
    features.append(sp.audio_features(spotifyID))
    df = pd.DataFrame(features)
    df.to_csv('recentSongsDataset.csv',index=False)
    valence = []
    for j in range(50):
        valence.append(features[0][j]['valence'])
    avValence = sum(valence)/len(valence)
    return avValence
  


def alterMood(avValence):
    MusicMood = str(int(avValence * 100)) 
    x = open("Mood.txt", "a")
    x.truncate(0)
    x.write(MusicMood)
    x.close()



def createHappyPlaylist(results): # I will need the song ids of songs that have a valence above a certain value. This should be taken in context with other songs. I will create a csv file with happy songs in it. max playlist length will be 50. If the playlist is longer than 50 then I will start nocking off music that has been in the playlist longest. 
    spotifyID = []
    for i, item in enumerate(results['items']): # the items refers to each value in results the i in necassery to allow for the for loop to loop through the list.
        track = item['track']
        spotifyID.append(track["id"])
    features = []
    features.append(sp.audio_features(spotifyID))
    happySondsID = []
    for j in range(50):
        valence = (features[0][j]['valence'])
        if valence > 0.75: # this seems to be a good measure for how happy a song should be 
            happySondsID.append(features[0][j]['id'])
    print(happySondsID)
    #need to identify if a playlist already exists
    if 
    sp.user_playlist_create(user = "d23zzt1cy4l04283ewvgktqoy", name = "Happy Vibes", description= "A happy playlist for you to listen to when things aren't going so great.", public= False )
    return happySondsID



def spotifyReadFull():
    results = getRecentTracks()
    avValence = getFeatures(results)
    alterMood(avValence)
    return avValence



def main():
    results = getRecentTracks()
    createHappyPlaylist(results)
    """printRecentTracks(results)
    avValence = getFeatures(results)
    alterMood(avValence)"""


if __name__ == '__main__':
    print("Running Programn")
    main()
    
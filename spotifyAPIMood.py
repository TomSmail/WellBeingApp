import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope = "user-read-recently-played",client_id='3b17a2138f654ee2af635167b3a14e3a', client_secret='26309b0980754c04992edc602e9ac31e', redirect_uri = "http://localhost:8080"))

def getRecentTracks():
    results = sp.current_user_recently_played(limit = 10)
    return results
   
def printRecentTracks(results):
     for i, item in enumerate(results['items']):
        track = item['track']
        print(i, track['artists'][0]['name'], " – ", track['name'])
    
def convertToDataFrame(features):
    df = pd.DataFrame(features)
    return df

def recentTracksCSV(df):
    df.to_csv('recentSongsDataset.csv',index=False)
    print (df)

def getSpotifyId(results):
    spotifyID = []
    for i, item in enumerate(results['items']):
        track = item['track']
        spotifyID.append(track["id"])
        i +=1
    return spotifyID
        
def getFeatures(spotifyID):
    features = []
    features.append(sp.audio_features(spotifyID))
    return features
    
def getValence(features):
    valence = []
    for i in range(10):
        valence.append(features[0][i]['valence'])
    return valence

def averageValence(valence):
    avValence = sum(valence)/len(valence)
    return avValence

def alterMood(avValence):
    MusicMood = str(int(avValence * 100)-50) 
    x = open("Mood.txt", "a")
    x.truncate(0)
    x.write(MusicMood)
    x.close()
    
    

def main():
    getRecentTracks()
    results = getRecentTracks()
    spotifyID = getSpotifyId(results)
    features = getFeatures(spotifyID)
    df = convertToDataFrame(features)
    valence = getValence(features)
    avValence = averageValence(valence)
    printRecentTracks(results)
    recentTracksCSV(df)
    averageValence(valence)
    alterMood(avValence)

if __name__ == '__main__':
    print("Running Programn")
    main()
    







# set SPOTIPY_CLIENT_ID= 3b17a2138f654ee2af635167b3a14e3a
# set SPOTIPY_CLIENT_SECRET= 26309b0980754c04992edc602e9ac31e
# set SPOTIPY_REDIRECT_URI= http://localhost:8080  <- using a port auto redirects the link to the python file so it does not have to be input by the user. 


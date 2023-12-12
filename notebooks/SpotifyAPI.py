import requests
import json
import time
from base64 import b64encode

try:
    secret_key_file  = open("../keys/secret_key.json")
    secret_key_json = json.load(secret_key_file)
    secret_key = secret_key_json.get("secret")
    client_id = secret_key_json.get("client_id")
    secret_key_file.close()
except:
    try:
        with open('../keys/secret_key.json') as secret_key_file:
            secret_key_json = json.load(secret_key_file)
            secret_key = secret_key_json.get('secret')
    except: 
        print('something went wrong looking for secret key')

def get_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": 'Basic ' + b64encode((client_id + ':' + secret_key).encode()).decode('utf-8')
}
       # "Content-Type" : "application/x-www-form-urlencoded"
    
    data = {
        "grant_type" : "client_credentials"
      #  "client_id" : "90a88a757a04438597a61e53c3a681ff"
    }
    response = requests.post(url, data = data, headers = headers)
    
    return response.json()

def test_getkey():
    secret_key_file = open('../keys/secret_key.json')
    secret_key_json = json.load(secret_key_file)
    secret_key = secret_key_json.get('secret')
    secret_key_file.close()
    print(f'secret key = {secret_key}')



def get_available_genre_seeds():
    #define base url
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"

    #get token to put in headers
    access_token = get_token().get("access_token")
    
    #define headers
    headers = {
        "Authorization" : f"Bearer {access_token}" ,
        "Content-Type" : "application/json"
    }

    #ask spotify for data
    response = requests.get(url, headers = headers)

    #return data
    return response.json()
    


def recommendations(track_id = "4nFAL2TKUOoAPQJ5DGGoTd"):
    url = f"https://api.spotify.com/v1/recommendations?seed_tracks={track_id}"

    access_token = get_token().get('access_token')

    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token}"
    }

    response = requests.get(url, headers = headers)

    return response.json()

def search(search_term = "song", music_type = "track,album", limit = 5):
    #sleep to not go over api request limit
    time.sleep(1.5)
    #turn spaces into %20
    if search_term.find("Funkytown") != -1:
        search_term = search_term.replace(' ', '%20')
    if search_term.find('&') != -1:
        search_term = search_term.replace('&', '%26')
    print(search_term)
        
    url = f"https://api.spotify.com/v1/search?q={music_type}:{search_term}&type={music_type}&limit={limit}"
    print(url)

    access_token = get_token().get('access_token')
    
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)

    return response.json()

def get_recs(**kwargs):
    if kwargs.get('mode') == "search":
        search_response = search(search_term = kwargs.get('name'), music_type = 'track')
        rec_id = search_response.get('tracks').get('items')[0].get('id')

        recs = recommendations(track_id=rec_id)
        return recs




def get_new_releases(country = "US", limit = 20, offset = 0):
    url = f"https://api.spotify.com/v1/browse/new-releases?country={country}&limit={limit}&offset={offset}"

    access_token = get_token().get('access_token')

    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    return response.json().get('albums').get('items')

def get_album(id = '2T1qRB6zSSGdNgcTD3Dg8H', market = 'US'):
    time.sleep(3)
    url = f"https://api.spotify.com/v1/albums/{id}"

    access_token = get_token().get('access_token')

    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    return response.json().get('tracks').get('items')



def audio_features(track_id = "4nFAL2TKUOoAPQJ5DGGoTd"):
    time.sleep(3)
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    
    access_token = get_token().get('access_token')

    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : f'Bearer {access_token}'
    }
    
    response = requests.get(url, headers=headers)

    return response.json()

def get_several_albums(ids, market = "US"):
    url = f"https://api.spotify.com/v1/albums?ids={ids}"

    access_token = get_token().get('access_token')

    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    return response.json().get('albums')

def get_several_tracks(ids = "7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ"):
    url = f"https://api.spotify.com/v1/tracks?ids={ids}"

    access_token = get_token().get('access_token')

    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    return response.json()

    




def new_release_features(limit = 20, offset = 0, country = "US"):

    new_release_albums = get_new_releases(country = "US",
                                          limit = limit,
                                          offset = offset)
    album_ids = [alb.get('id') for alb in new_release_albums]
    album_request_string = ""
    for index, id in enumerate(album_ids):
        if index != (len(album_ids) - 1):
          album_request_string += (id + ',')
        else:
            album_request_string += id
    albums = get_several_albums(ids = album_request_string)

    data  =[]
    for alb in albums:
        alb_tracks = alb.get('tracks').get('items')
        for track in alb_tracks:
            track_ids = [track.get('id') for track in alb_tracks]
            for id in track_ids:
                features = audio_features(track_id=id)
                data.append(features)
    return data
        
def get_playlist_tracks(playlist_id,offset):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}"
    access_token = get_token().get('access_token')

    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : f'Bearer {access_token}'
    }
    
    response = requests.get(url, headers=headers)

    return response.json()

def find_average_song(
    seed_tracks="7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ", 
    limit = 1,
    market="US",
    acousticness=.5,
    danceability=.5,
    energy=.5,
    instrumentalness=.5,
    liveness = .5,
    speechiness = .5,
    valence=.4,
):

    url = f"""
    https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks}&limit={limit}&market={market}&target_acousticness={acousticness}
    """
    access_token = get_token().get('access_token')
    
    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    
    return response.json()













        
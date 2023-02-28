from dotenv import load_dotenv
import os
import base64
import json
from requests import post,get

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    grant_type = 'client_credentials'
    body_params = {'grant_type': grant_type}
    auth_headers = {'Authorization': f'Basic {client_creds_b64.decode()}'}
    response = post(auth_url, data=body_params, headers=auth_headers)
    access_token = response.json()['access_token']
    return access_token

def get_auth_header(token):
    return {'Authorization': 'Bearer '+ token}

def search_for_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print('Artist not exist')
        return None
    return json_result[0]

def get_songs_by_artist(token,artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_header(token)
    result = get(url,headers = headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

token = get_token()
result = search_for_artist(token,'ACDC')
artist_id = result['id']
songs = get_songs_by_artist(token,artist_id)

def get_track_markets(track_name):
    query = f'track:{track_name}'
    response = get(f'https://api.spotify.com/v1/search?q={query}&type=track&limit=1', headers=get_auth_header(token))
    search_results = response.json()
    if search_results['tracks']['total'] == 0:
        return None
    else:
        track_id = search_results['tracks']['items'][0]['id']
        response = get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=get_auth_header(token))
        track_info = response.json()
        return track_info['available_markets']


name = input('Eter name of artist: ')
if len(search_for_artist(get_token(),name)['name']) !=0:
    while True:
        params = ['name','the most popular song','artist id','available markets of the most popular song','exit']
        param = input('''What information do you need?
(name,the most popular song,artist id,available markets of the most popular song)
Print 'exit' to end
''')
        if param == 'name':
            print(search_for_artist(get_token(),name)['name'])
        if param == 'the most popular song':
            print([song['name'] for song in songs][0])
        if param == 'artist id':
            print(artist_id)
        if param == 'available markets of the most popular song':
            print(get_track_markets([song['name'] for song in songs][0]))
        if param not in params:
            print('Wrong argument')
        if param == 'exit':
            break



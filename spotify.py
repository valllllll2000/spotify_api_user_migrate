import requests
import json
import os
from dotenv import load_dotenv

#Get bearer tokens for both users from the https://github.com/valllllll2000/web-api-examples app

load_dotenv()
auth_token1 = os.getenv("auth_token1")
auth_token2 = os.getenv("auth_token2")

def get_playlist_item_ids(bearer_token):
    """
    Fetches playlist data from Spotify API andreturns a list of item IDs.

    Args:
        bearer_token: The Spotify API bearer token.

    Returns:
        A list of playlist item IDs.
    """

    url = 'https://api.spotify.com/v1/me/playlists?limit=50&offset=0'
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Items found: " + str(data['total']))
        print("Next found: " + str(data['next']))
        item_ids = [item['id'] for item in data['items']]
        return item_ids
    else:
        print("Error fetching playlist data:", response.status_code)
        print("Reason:", response.reason)
        return []


def follow_playlist(bearer_token, id):
    """
    Follows a playlist from Spotify API.

    Args:
        bearer_token: The Spotify API bearer token.
        id: the id of the playlist to follow

    Returns:
       empty response
    """

    url = f"https://api.spotify.com/v1/playlists/{id}/followers"
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.put(url, headers=headers)

    if response.status_code == 200:
        print("List followed: " + id)
    else:
        print("Error following list", response.status_code)
        print("Reason:", response.reason)
        print("List: " + id)

def get_followed_artists_ids(bearer_token):
    """
    Fetches artist data from Spotify API andreturns a list of item IDs.

    Args:
        bearer_token: The Spotify API bearer token.

    Returns:
        A list of artists item IDs.
    """

    url = 'https://api.spotify.com/v1/me/following?type=artist&limit=50'
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()['artists']
        print("Items found: " + str(data['total']))
        item_ids = [item['id'] for item in data['items']]
        return item_ids
    else:
        print("Error fetching artist data:", response.status_code)
        print("Reason:", response.reason)
        return []

def follow_artists(bearer_token, item_ids):
    """
    Follows multiple artists onSpotify.

    Args:
        bearer_token: The Spotify API bearer token.
        item_ids: A list of artist IDs to follow.
    """

    url = 'https://api.spotify.com/v1/me/following?type=artist'
    headers = {'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    data = json.dumps({"ids": item_ids})

    response = requests.put(url, headers=headers, data=data)

    if response.status_code == 204:
        print("Artists followed successfully!")
    else:
        print("Error following artists:", response.status_code)


playlists_ids = get_playlist_item_ids(auth_token1)
artist_ids = get_followed_artists_ids(auth_token1)


if playlists_ids:
    for item_id in playlists_ids:
        follow_playlist(auth_token2, item_id)
if (artist_ids):
    follow_artists(auth_token2, artist_ids)
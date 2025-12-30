import csv
import io
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

def get_channel_id(youtube, video_id):
    """Retrieves the channel ID for a given video ID."""
    try:
        response = youtube.videos().list(part='snippet', id=video_id).execute()
        if not response['items']:
            return None
        channel_id = response['items'][0]['snippet']['channelId']
        return channel_id
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def save_video_comments_to_csv(youtube, video_id, output_dir='data'):
    """
    Retrieves comments for a video and saves them to a CSV file in the specified directory.
    Returns the full path to the saved file.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Retrieve comments for the specified video
    comments = []
    try:
        results = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText'
        ).execute()

        while results:
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                username = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comments.append([username, comment])
            
            if 'nextPageToken' in results:
                nextPage = results['nextPageToken']
                results = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    pageToken=nextPage
                ).execute()
            else:
                break
    except HttpError as error:
        print(f'An error occurred while fetching comments: {error}')
        return None

    # Save the comments to a CSV file
    filename = f"{video_id}.csv"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username', 'Comment'])
        for comment in comments:
            writer.writerow([comment[0], comment[1]])
            
    return filepath

def get_video_stats(youtube, video_id):
    """Retrieves statistics for a given video ID."""
    try:
        response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        if not response['items']:
            return None
            
        return response['items'][0]['statistics']
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def get_channel_info(youtube, channel_id):
    """Retrieves information for a given channel ID."""
    try:
        response = youtube.channels().list(
            part='snippet,statistics,brandingSettings',
            id=channel_id
        ).execute()

        if not response['items']:
            return None

        snippet = response['items'][0]['snippet']
        statistics = response['items'][0]['statistics']
        
        channel_info = {
            'channel_title': snippet.get('title'),
            'video_count': statistics.get('videoCount'),
            'channel_logo_url': snippet.get('thumbnails', {}).get('high', {}).get('url'),
            'channel_created_date': snippet.get('publishedAt'),
            'subscriber_count': statistics.get('subscriberCount'),
            'channel_description': snippet.get('description')
        }

        return channel_info

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

    


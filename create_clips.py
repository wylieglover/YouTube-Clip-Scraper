from scrape_html import get_most_replayed_data
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import re

def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', text)

def download_original_video(video_url, video_id):
    yt = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
    video_title = yt.title
    video_stream = yt.streams.filter(file_extension='mp4').first()
    video_stream.download(filename='original_video.mp4')
    
    print(f"Video downloadeded: {video_title}\n")
    return video_title

def create_video_clips(data, video_title):
    
    if 'mostReplayed' in data:
        timed_marker_decorations = data['mostReplayed'].get('timedMarkerDecorations', [])
        
        if timed_marker_decorations:
            for idx, decoration in enumerate(timed_marker_decorations):
                start_time = decoration.get('visibleTimeRangeStartMillis') / 1000
                end_time = decoration.get('visibleTimeRangeEndMillis') / 1000
                
                print(f"Initiating Moviepy Processes...\n")
                clip = VideoFileClip('original_video.mp4').subclip(start_time, end_time)
                clean_video_title = remove_emojis(video_title)
                output_file = f'clips/{clean_video_title}_clip_{idx + 1}.mp4'
                clip.write_videofile(output_file, codec='libx264', verbose=False)
                clip.close()
            
            os.remove('original_video.mp4')
            print(f"\nClips created for video {idx + 1}\nDeleting original video...\n")
    else:
        print("Failed to fetch video duration. Please check the API key or video ID.")

def main():
    # add video ids to video_ids.txt
    video_ids_file_path = 'video_ids.txt'
    with open(video_ids_file_path, 'r') as file:
        video_ids = file.read().splitlines()
    
    for video_id in video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_title = download_original_video(video_url, video_id)
        data = get_most_replayed_data(video_id)
        create_video_clips(data, video_title)
    
    print("\nAll clips created.")

if __name__ == "__main__":
    main()
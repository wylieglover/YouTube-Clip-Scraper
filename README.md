# YouTube-Clip-Scraper
Clips the most replayed segment(s) of a Youtube video
# Local Development Setup
Before starting, make sure you have at least these components installed on your computer:
- Python
- pytube3
- moviepy
- requests

Start by cloning this repository into a local folder/directory:
```sh
git clone https://github.com/wylieglover/dataliteracy
```
Now for each Youtube video you want clipped, add Youtube video ids (```Example: dQw4w9WgXcQ from https://www.youtube.com/watch?v=dQw4w9WgXcQ```) on seperate lines inside the ```video_ids.txt``` file.


You can now run ```create_clips.py``` which will clip the most replayed segment(s) of each video!

# Youtube Transcripts to Video Editing Time Codes

This takes in a Youtube ID, and generates time codes for easy clip making and markers

Usage:
```commandline
python main.py YOUTUBEID normal | Tee-Object -FilePath "./youtube_dialog.txt"

# If you just want the raw json
python main.py YOUTUBEID raw | Tee-Object -FilePath "./youtube_dialog.json"

```

Format of Output:
```commandline
Sentence [Start Time Code - End Time Code] - (Duration Time Code)
 I'm I'm liking I'm liking it [00:01:49:50 - 00:01:53:16] - (00:00:03:25)
```
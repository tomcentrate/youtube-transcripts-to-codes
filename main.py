from youtube_transcript_api import YouTubeTranscriptApi
import sys
import time
import math
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def convert_time_to_60fps_time(startTime):
    startTimeString = time.strftime("%H:%M:%S", time.gmtime(startTime))
    startTimeInBase100 = math.floor(math.floor(math.modf(startTime)[0] * 100) * (60 / 100))
    return f'{startTimeString}:{startTimeInBase100:0>2}'

def download_transcript(videoId, style):
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(videoId)
    raw_data = fetched_transcript.to_raw_data()
    full_transcript = ""
    split_delimiter = '.'
    endTime = 0
    startTime = 0
    if style == 'raw':
        print(raw_data)
        exit(0)
    for snippet in fetched_transcript:
        current_text = snippet.text
        if split_delimiter in current_text:
            endTime = snippet.start + snippet.duration
            current_text = current_text.split(split_delimiter)
            addPeriod = True
            for word in current_text:
                if addPeriod:
                    addPeriod = False
                    startTimeString = convert_time_to_60fps_time(startTime)
                    endTimeString = convert_time_to_60fps_time(endTime)
                    duration = endTime - startTime
                    duration = convert_time_to_60fps_time(duration)
                    full_transcript = full_transcript + " " + word + " [" + startTimeString + ' - ' + endTimeString + "] - (" + duration +  ")\n"
                    startTime = snippet.start + snippet.duration
                    endTime = snippet.start + snippet.duration
                else :
                    full_transcript = full_transcript + " " + word
        else:
            full_transcript += " " + snippet.text

    return full_transcript


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(download_transcript(sys.argv[1], sys.argv[2]))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

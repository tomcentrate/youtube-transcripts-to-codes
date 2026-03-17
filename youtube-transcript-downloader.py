import tkinter as tk
from tkinter import filedialog, messagebox
from urllib.parse import urlparse, parse_qs
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



def extract_video_id_from_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if not parsed.netloc:
        # Assume the user pasted a bare video ID
        return url.strip()

    # Handle standard YouTube URLs
    if "youtube.com" in parsed.netloc:
        query = parse_qs(parsed.query)
        vid = query.get("v", [""])[0]
        return vid

    # Handle short youtu.be URLs
    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")

    # Fallback to path segment
    return parsed.path.lstrip("/")


def browse_output_file(entry_widget: tk.Entry) -> None:
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Select output file"
    )
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)


def run_download(url_entry: tk.Entry, path_entry: tk.Entry) -> None:
    url = url_entry.get().strip()
    output_path = path_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL or video ID.")
        return

    if not output_path:
        messagebox.showerror("Error", "Please select an output file path.")
        return

    try:
        video_id = extract_video_id_from_url(url)
        if not video_id:
            raise ValueError("Could not determine video ID from URL.")

        # Use the existing function; keep style as 'default' (timestamped lines)
        transcript_text = download_transcript(video_id, "default")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        messagebox.showinfo("Success", f"Transcript saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download transcript:\n{e}")


def create_gui() -> None:
    root = tk.Tk()
    root.title("YouTube Transcript Downloader")

    # URL label + entry
    url_label = tk.Label(root, text="YouTube URL or Video ID:")
    url_label.grid(row=0, column=0, padx=8, pady=8, sticky="e")

    url_entry = tk.Entry(root, width=60)
    url_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

    # Output file label + entry + browse button
    path_label = tk.Label(root, text="Output File Path:")
    path_label.grid(row=1, column=0, padx=8, pady=8, sticky="e")

    path_entry = tk.Entry(root, width=60)
    path_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

    browse_button = tk.Button(
        root,
        text="Browse...",
        command=lambda: browse_output_file(path_entry)
    )
    browse_button.grid(row=1, column=2, padx=8, pady=8)

    # Run button
    run_button = tk.Button(
        root,
        text="Download Transcript",
        command=lambda: run_download(url_entry, path_entry)
    )
    run_button.grid(row=2, column=0, columnspan=3, padx=8, pady=12)

    # Make columns resize nicely
    root.columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    create_gui()


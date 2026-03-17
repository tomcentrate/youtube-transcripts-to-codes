import tkinter as tk
from tkinter import filedialog, messagebox
from urllib.parse import urlparse, parse_qs

from main import download_transcript


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


import requests
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from queue import Queue
from colorama import init
import webbrowser


init(autoreset=True)


STATUS_COLORS = {
    200: "green",
    301: "orange",
    302: "orange",
    400: "red",
    403: "purple",
    404: "red",
    500: "red",
}

# Global variables
stop_scan = False
valid_paths_count = 0
lock = threading.Lock()
output_cache = []  # Store output for filtering


def worker(queue, base_url):
    """Worker thread to process URL requests"""
    global valid_paths_count, stop_scan
    while not queue.empty() and not stop_scan:
        path = queue.get()
        full_url = f"{base_url.rstrip('/')}/{path}"
        try:
            response = requests.get(full_url, timeout=5)
            status_code = response.status_code

            if status_code in STATUS_COLORS:
                color = STATUS_COLORS[status_code]
                log_output(f"{full_url} -> {status_code}", color)

                if status_code == 200:
                    with lock:
                        valid_paths_count += 1

        except requests.exceptions.RequestException:
            pass
        queue.task_done()


def log_output(text, tag="info"):
    """Log output to GUI and store in cache"""
    output_cache.append((text, tag))  # Store in cache for filtering
    output_box.insert(tk.END, text + "\n", tag)
    output_box.yview(tk.END)  # Auto-scroll


def start_scan():
    """Starts scanning URLs from the wordlist"""
    global stop_scan, valid_paths_count, output_cache
    stop_scan = False
    valid_paths_count = 0
    output_cache = []  # Reset cache on new scan

    base_url = url_entry.get().strip()
    wordlist_file = wordlist_path.get()
    num_threads = int(threads_entry.get().strip())

    if not base_url or not wordlist_file:
        messagebox.showerror("Error", "Please enter a valid URL and select a wordlist file.")
        return

    output_box.delete(1.0, tk.END)
    log_output(f"🔍 Scanning {base_url}...", "info")
    log_output(f"⏳ Scanning in progress...", "info")
    log_output(f"🧵 Using {num_threads} threads...\n", "info")

    try:
        with open(wordlist_file, "r") as file:
            paths = file.read().splitlines()
    except FileNotFoundError:
        messagebox.showerror("Error", "Wordlist file not found.")
        return

    queue = Queue()
    for path in paths:
        queue.put(path)

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(queue, base_url))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    def check_completion():
        if queue.empty():
            log_output(f"\n✅ Scan Complete! 🎯 Found {valid_paths_count} valid paths (200 status code).", "info")
        else:
            root.after(1000, check_completion)

    check_completion()


def stop_scan_function():
    """Stops scanning"""
    global stop_scan
    stop_scan = True
    log_output("\n❌ Scan stopped by user.", "error")


def select_wordlist():
    """Selects wordlist file"""
    filename = filedialog.askopenfilename(title="Select Wordlist File", filetypes=[("Text Files", "*.txt")])
    wordlist_path.set(filename)


def filter_results(status_code):
    """Filters output based on status code"""
    output_box.delete(1.0, tk.END)  # Clear output box
    for line, tag in output_cache:
        if f"-> {status_code}" in line or status_code is None:
            output_box.insert(tk.END, line + "\n", tag)


def open_url(event):
    """Opens the clicked URL in the web browser"""
    index = output_box.index(tk.CURRENT)
    line_text = output_box.get(index + " linestart", index + " lineend")
    url = line_text.split(" -> ")[0]  # Extract the URL part

    if url.startswith("http"):
        webbrowser.open(url)


# GUI Setup
root = tk.Tk()
root.title("Path Finder GUI - Ayush Kumar")
root.geometry("850x600")  # Increased window size
root.resizable(False, False)

# Banner
banner_label = tk.Label(root, text="🔍 Path Finder", font=("Arial", 16, "bold"), fg="blue")
banner_label.pack(pady=5)

# URL Entry
frame_url = tk.Frame(root)
frame_url.pack(pady=5)
tk.Label(frame_url, text="🔗 URL: ").pack(side=tk.LEFT)
url_entry = tk.Entry(frame_url, width=50)
url_entry.pack(side=tk.LEFT)

# Wordlist Selection
frame_wordlist = tk.Frame(root)
frame_wordlist.pack(pady=5)
wordlist_path = tk.StringVar()
tk.Label(frame_wordlist, text="📄 Wordlist: ").pack(side=tk.LEFT)
wordlist_entry = tk.Entry(frame_wordlist, textvariable=wordlist_path, width=40, state="readonly")
wordlist_entry.pack(side=tk.LEFT)
tk.Button(frame_wordlist, text="Browse", command=select_wordlist).pack(side=tk.LEFT)

# Threads Entry
frame_threads = tk.Frame(root)
frame_threads.pack(pady=5)
tk.Label(frame_threads, text="🧵 Threads: ").pack(side=tk.LEFT)
threads_entry = tk.Entry(frame_threads, width=5)
threads_entry.insert(0, "20")  # Default 20 threads
threads_entry.pack(side=tk.LEFT)

# Start & Stop Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)
tk.Button(frame_buttons, text="🚀 Start Scan", command=start_scan, bg="green", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(frame_buttons, text="❌ Stop Scan", command=stop_scan_function, bg="red", fg="white").pack(side=tk.LEFT, padx=10)

# Status Code Filter Buttons
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)
tk.Label(filter_frame, text="📊 Filter by Status Code: ").pack(side=tk.LEFT)

for code, color in STATUS_COLORS.items():
    tk.Button(filter_frame, text=str(code), bg=color, fg="white",
              command=lambda c=code: filter_results(c)).pack(side=tk.LEFT, padx=2)

tk.Button(filter_frame, text="🔄 Show All", command=lambda: filter_results(None)).pack(side=tk.LEFT, padx=5)

# Output Box
output_box = scrolledtext.ScrolledText(root, width=100, height=25, cursor="hand2")  # Increased size
output_box.pack(pady=10)
output_box.tag_config("info", foreground="blue")
output_box.tag_config("error", foreground="red")
output_box.tag_config("green", foreground="green")
output_box.tag_config("orange", foreground="orange")
output_box.tag_config("red", foreground="red")
output_box.tag_config("purple", foreground="purple")

# Bind Click Event for URLs
output_box.bind("<Button-1>", open_url)

# Run GUI
root.mainloop()

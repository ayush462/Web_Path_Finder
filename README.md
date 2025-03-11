# Web_Path_Finder
# Path Finder GUI

## Description
Path Finder GUI is a simple tool that scans URLs from a wordlist and checks their HTTP response status. It provides a graphical interface using Tkinter and color-coded results based on status codes.

## Features
- GUI-based URL scanning
- Multi-threading for faster scans
- Status code filtering
- Clickable URLs for quick access
- Start and Stop scanning functionality

## Installation Guide

### Prerequisites
Ensure you have Python installed. This script requires Python 3.

#### Check Python Version:
```sh
python --version
```
It should be **Python 3.x**.

### Install Required Modules
The script requires the following Python modules:
- `requests`
- `tkinter` (comes pre-installed with Python)
- `colorama`

Install dependencies using pip:
```sh
pip install requests colorama
```

### Installation on Linux
1. Clone the repository (or download the script):
   ```sh
   git clone https://github.com/yourusername/path-finder-gui.git
   cd path-finder-gui
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the script:
   ```sh
   python path_finder.py
   ```

### Installation on Windows
1. Download the script or clone the repository:
   ```sh
   git clone https://github.com/yourusername/path-finder-gui.git
   cd path-finder-gui
   ```
2. Open a command prompt in the project folder and install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the script:
   ```sh
   python path_finder.py
   ```

## Usage Guide
1. Enter the **Base URL** in the input field.
2. Select a **wordlist** file (must be a `.txt` file with paths listed line by line).
3. Set the **number of threads** (default is 20).
4. Click **Start Scan** to begin scanning.
5. Click **Stop Scan** to halt scanning at any time.
6. Filter results by status code using the filter buttons.
7. Click on any found URL in the output box to open it in a browser.

## Status Code Colors
- **200 (OK)** - Green
- **301, 302 (Redirects)** - Orange
- **400, 404 (Client Errors)** - Red
- **403 (Forbidden)** - Purple
- **500 (Server Error)** - Red

## License
This project is licensed under the MIT License.

## Author
Developed by Ayush Kumar.

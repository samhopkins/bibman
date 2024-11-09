#!/usr/bin/env python3

import sys
import curses
import requests
from bs4 import BeautifulSoup
import os
import subprocess

def find_bibfile():
    """Finds a .bib file in the current directory and returns its filename, or None if no .bib file is found."""
    for filename in os.listdir():
        if filename.endswith(".bib"):
            return filename
    return None


def search_google_scholar(query):
    """Search Google Scholar for the provided query and return a list of results."""
    search_url = f"https://scholar.google.com/scholar?q={requests.utils.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception("Error fetching results from Google Scholar.")
    
    # Parsing results
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.select(".gs_ri"):
        title = item.select_one(".gs_rt").text
        link = item.select_one(".gs_rt a")["href"] if item.select_one(".gs_rt a") else ""
        authors = item.select_one(".gs_a").text.split("-")[0]
        results.append({
            "title": title,
            "authors": authors,
            "link": link,
        })
    
    return results

def interactive_chooser(query):
    """Interactive chooser function for Google Scholar search results."""
    results = search_google_scholar(query)

    def display_menu(stdscr):
        curses.curs_set(0)  # Hide cursor
        curses.start_color()  # Enable color mode
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default color
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Color for authors
        selected_idx = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Search results for '{query}':\n", curses.A_BOLD)
            for idx, result in enumerate(results):
                # Highlight selected item
                if idx == selected_idx:
                    stdscr.addstr(idx * 2 + 1, 0, f"> {result['title']}", curses.A_REVERSE)
                    stdscr.addstr(idx * 2 + 2, 2, f"{result['authors']}", curses.color_pair(2) | curses.A_REVERSE)
                else:
                    stdscr.addstr(idx * 2 + 1, 0, f"  {result['title']}", curses.color_pair(1))
                    stdscr.addstr(idx * 2 + 2, 2, f"{result['authors']}", curses.color_pair(2))

            key = stdscr.getch()

            if key == ord('j') and selected_idx < len(results) - 1:
                selected_idx += 1
            elif key == ord('k') and selected_idx > 0:
                selected_idx -= 1
            elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
                return results[selected_idx]["title"]

    return curses.wrapper(display_menu)


def main():
    if len(sys.argv) < 2:
        print("Usage: bibman \"search query\"")
        sys.exit(1)
    
    query = sys.argv[1]
    chosen_title = interactive_chooser(query)
    bibfile = find_bibfile()
    subprocess.run("import_dblp --query \"" + chosen_title + "\" --bib " + bibfile, shell=True)
    
if __name__ == "__main__":
    main()
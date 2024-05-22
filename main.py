import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
 
 
def classify_link(base_url, link):
   parsed_link = urlparse(link)
   if parsed_link.scheme and parsed_link.netloc:
       if parsed_link.netloc == urlparse(base_url).netloc:
           return "Internal"
       else:
           return "External"
   else:
       return "Internal"
 
 
def extract_links():
   url = url_entry.get()
   try:
       response = requests.get(url)
       soup = BeautifulSoup(response.text, 'html.parser')
       base_url = response.url
       links = [link.get('href') for link in soup.find_all('a')]
       external_links = []
       internal_links = []
       total_links = 0
       output_text.delete(1.0, tk.END)  # Clear previous output
       for link in links:
           total_links += 1
           classification = classify_link(base_url, link)
           if classification == "External":
               external_links.append(link)
           else:
               internal_links.append(link)
       output_text.insert(tk.END, "Internal Links:\n")
       for link in internal_links:
           output_text.insert(tk.END, f"{link} [Internal]\n")
       output_text.insert(tk.END, "\nExternal Links:\n")
       for link in external_links:
           output_text.insert(tk.END, f"{link} [External]\n")
       output_text.insert(tk.END, f"\nTotal URLs: {total_links}\n")
       output_text.insert(tk.END, f"External Links: {len(external_links)}\n")
       output_text.insert(tk.END, f"Internal Links: {len(internal_links)}\n")
   except Exception as e:
       output_text.delete(1.0, tk.END)  # Clear previous output
       output_text.insert(tk.END, f"Error: {e}")
 
 
# Create main window
window = tk.Tk()
window.title("Website Links Extractor - The Pycodes")
window.geometry("700x500")
 
 
# URL entry
url_label = tk.Label(window, text="Enter URL:")
url_label.pack()
url_entry = tk.Entry(window, width=80)
url_entry.pack()
 
 
# Button to extract links
extract_button = tk.Button(window, text="Extract Links", command=extract_links)
extract_button.pack()
 
 
# Output area
output_label = tk.Label(window, text="Extracted Links:")
output_label.pack()
output_text = scrolledtext.ScrolledText(window, width=100, height=30)
output_text.pack(padx=10)
 
 
# Run the main loop
window.mainloop()

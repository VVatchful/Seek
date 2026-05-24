import os
import json

from urllib.parse import urlparse

def print_json(node, indent=0):
    print(" " * indent + node["name"])
    if node["type"] == "folder":
        for child in node["children"]:
            print_json(child, indent + 1)

def gather_domain(url):
    url = urlparse(url)
    domain = url.netloc.removeprefix("www.")

    if url.scheme in ['chrome', 'about', 'file']:
        return "other"
    return domain

def display_categories(categories):
    for domain, bookmarks in categories.items():
        print(f"{domain} ({len(bookmarks)})")
        for bookmark in bookmarks:
            print(f"  └─ {bookmark['name']}")

# finds how many of the same bookmarks have the same domain and appends them to a dict
def categorize_domain(node, result={}):
    if node["type"] == "url":
        # we can have another domain because its within the functions scope though we can change it to prevent mismatch and confusion
        domain = gather_domain(node["url"])
        result.setdefault(domain, []).append(node)
    elif node["type"] == "folder":
        for child in node["children"]:
            # we call the function on itself
            categorize_domain(child, result)
    #return the results
    return result

local_app_data = os.environ['LOCALAPPDATA']
bookmarks_path = os.path.join(local_app_data, "Google", "Chrome", "User Data", "Default", "Bookmarks")

try:
    with open(bookmarks_path, "r", encoding="utf-8") as f:
        bookmarks = json.load(f)
        print(bookmarks)
        categories = categorize_domain(bookmarks["roots"]["bookmark_bar"])
        print(categories)
        display_categories(categories)
except FileNotFoundError:
    print("Bookmarks file not found at: {}".format(bookmarks_path))

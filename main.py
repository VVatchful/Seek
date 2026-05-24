import os
import json
import shutil
import uuid
from urllib.parse import urlparse

def print_json(node, indent=0):
    print(" " * indent + node["name"])
    if node["type"] == "folder":
        for child in node["children"]:
            print_json(child, indent + 1)

def flatten_collect(node):
    flattened = []
    if node["type"] == "url":
        flattened.append(node)
    elif node["type"] == "folder":
        for child in node["children"]:
            flattened.extend(flatten_collect(child))
    return flattened


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
def categorize_domain(flat_list, result=None):
    if result is None:
        result = {}
    for bookmark in flat_list:
        domain = gather_domain(bookmark["url"])
        result.setdefault(domain, []).append(bookmark)
    return result

import uuid

def structure(categories):
    new_children = []
    for domain, bookmarks in categories.items():
        if len(bookmarks) == 1:
            new_children.append(bookmarks[0])
        else:
            new_children.append({
                "type": "folder",
                "name": domain,
                "children": bookmarks,
                "date_added": bookmarks[0]["date_added"],
                "date_modified": bookmarks[0]["date_added"],
                "guid": str(uuid.uuid4()),
                "id": str(hash(domain) & 0xFFFFFF)
            })
    return new_children

local_app_data = os.environ['LOCALAPPDATA']
bookmarks_path = os.path.join(local_app_data, "Google", "Chrome", "User Data", "Default", "Bookmarks")

def main():
    with open(bookmarks_path, "r", encoding="utf-8") as f:
        bookmarks = json.load(f)

    flat = flatten_collect(bookmarks["roots"]["bookmark_bar"])
    categories = categorize_domain(flat)

    while True:
        print("\nWhat would you like to do?")
        print("1. Display bookmarks by domain")
        print("2. Preview a reorganized structure of bookmarks")
        print("3. Save to Chrome")
        print("4. Exit")
        print("5. restore from .bak")

        choice = input("> ")
        if choice == "1":
            display_categories(categories)


        elif choice == "2":
            new_children = structure(categories)
            for item in new_children:
                if item["type"] == "folder":
                    print(f"::{item['name']} ({len(item['children'])})")
                    for child in item["children"]:
                        print(f"   └─ {child['name']}")
                else:
                    print(f":{item['name']}")


        elif choice == "3":
            print("Make sure Chrome is closed! Proceed? (y/n)")
            confirm = input("> ")
            if confirm == "y":
                new_children = structure(categories)
                bookmarks["roots"]["bookmark_bar"]["children"] = new_children
                shutil.copy(bookmarks_path, bookmarks_path + ".bak")
                with open(bookmarks_path, "w", encoding="utf-8") as f:
                    json.dump(bookmarks, f, indent=4)


        elif choice == "4":
            break
        elif choice == "5":
            shutil.copy(bookmarks_path + ".bak", bookmarks_path)
            print("Restored! Restart Chrome to see changes.")
        else:
            print("Please enter a valid option")

if __name__ == "__main__":
    main()
# Seek

Seek aims to clear up those messy leftover bookmarks everyone forgets about 
in Chrome. Those days are now gone. Seek is a lightweight CLI that 
auto-categorizes your bookmarks by domain, lets you preview the new structure, 
and exports a clean HTML file you can import directly into Chrome — no manual 
sorting required.

## Features
- Display all bookmarks grouped by domain
- Preview the reorganized folder structure before committing
- Export as an importable HTML file for Chrome
- Restore from backup if anything goes wrong
- Safe to re-run — flattens and re-categorizes every time

## Usage

```bash
git clone https://github.com/VVatchful/Seek.git
cd Seek
python main.py
```

Requires Python 3.14.0+

No external dependencies — uses only Python standard library.

## Struggles

The biggest challenge was working with recursion when parsing Chrome's nested 
JSON bookmark structure. Chrome stores bookmarks as a tree where folders contain 
children that can themselves be folders, which required careful recursive 
traversal. Flattening that tree before re-categorizing was a key breakthrough 
that made the logic much cleaner. Getting the HTML export format exactly right 
for Chrome's importer was also trickier than expected — small formatting details 
like quote style broke the import silently.

## Future Plans
- JSON export to make the process seamless without needing to manually import
- Support for other browsers such as Firefox, which uses a similar format
- A config file for defining custom categorization rules
- Automatic scheduling so bookmarks stay organized over time
- User-defined folder renaming (e.g. reddit.com to Reddit)
- A --dry-run flag that always previews changes before applying them

## Why Seek?

As someone who games a lot, I was constantly hunting through a cluttered 
bookmark bar trying to track down build guides, wikis, and tools buried under 
dozens of unrelated tabs. I built Seek to solve my own problem — and named it 
after that exact feeling of always having to seek out what I was looking for.
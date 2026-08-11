import urllib.request
import json
import re
import os

WIKIS = [
    {
        "name": "DeadSpace14",
        "url": "https://wiki.deadspace14.net/api.php?action=query&list=users&ususers=WikiHampter&usprop=editcount&format=json",
        "color": "3B82F6"
    },
    {
        "name": "Sunrise14",
        "url": "https://wiki.sunrise14.top/w/api.php?action=query&list=users&ususers=WikiHampter&usprop=editcount&format=json",
        "color": "F59E0B"
    },
    {
        "name": "Station14",
        "url": "https://station14.ru/api.php?action=query&list=users&ususers=KirillGolub&usprop=editcount&format=json",
        "color": "10B981"
    }
]

def fetch_edits(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 GitHubActions/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data['query']['users'][0]['editcount']
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return 0

def main():
    badges = []
    for wiki in WIKIS:
        edits = fetch_edits(wiki['url'])
        print(f"{wiki['name']}: {edits} edits")
        if edits > 0:
            badge_url = f"https://img.shields.io/badge/{wiki['name']}-{edits}_edits-{wiki['color']}?style=for-the-badge&logo=wikipedia&logoColor=white"
            badges.append(f"<img src=\"{badge_url}\" alt=\"{wiki['name']} Stats\" />")
    
    badge_html = "\n  ".join(badges)
    
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
    
    pattern = r"(<!-- WIKI_STATS_START -->).*?(<!-- WIKI_STATS_END -->)"
    replacement = f"\\1\n  {badge_html}\n  \\2"
    
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    main()

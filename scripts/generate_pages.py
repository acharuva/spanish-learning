#!/usr/bin/env python3
"""Generate HTML pages from Spanish vocabulary CSV."""

import csv
import os
from pathlib import Path

# Configuration
WORDS_PER_PAGE = 50
INPUT_CSV = "data/spanish_100_words.csv"  # Change to spanish_3000_words.csv for full run
OUTPUT_DIR = "pages"

# CSS styles (inline for portability)
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    background: #f5f5f5;
}
header { text-align: center; margin-bottom: 20px; }
h1 { color: #c41e3a; margin-bottom: 5px; }
.subtitle { color: #666; }
nav { margin: 15px 0; text-align: center; }
nav a {
    color: #c41e3a;
    text-decoration: none;
    padding: 8px 16px;
    border: 1px solid #c41e3a;
    border-radius: 4px;
    margin: 0 5px;
    display: inline-block;
}
nav a:hover { background: #c41e3a; color: white; }
nav a.disabled { color: #ccc; border-color: #ccc; pointer-events: none; }
table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-radius: 8px;
    overflow: hidden;
}
th {
    background: #c41e3a;
    color: white;
    padding: 12px;
    text-align: left;
}
td { padding: 12px; border-bottom: 1px solid #eee; }
tr:nth-child(even) { background: #fafafa; }
tr:hover { background: #fff3cd; }
.rank { font-weight: bold; color: #666; width: 60px; }
.spanish { font-weight: bold; font-size: 1.1em; }
.infinitive {
    font-weight: normal;
    font-size: 0.85em;
    color: #888;
    font-style: italic;
}
.form {
    font-size: 0.85em;
    padding: 2px 8px;
    border-radius: 12px;
    display: inline-block;
}
.form-verb { background: #e3f2fd; color: #1565c0; }
.form-noun { background: #e8f5e9; color: #2e7d32; }
.form-adjective { background: #fff3e0; color: #e65100; }
.form-adverb { background: #fce4ec; color: #c2185b; }
.form-other { background: #f3e5f5; color: #7b1fa2; }
footer { margin-top: 20px; text-align: center; color: #666; font-size: 0.9em; }
"""

def get_form_class(form):
    """Get CSS class for word form."""
    form_lower = form.lower()
    if form_lower == "verb":
        return "form-verb"
    elif form_lower == "noun":
        return "form-noun"
    elif form_lower == "adjective":
        return "form-adjective"
    elif form_lower == "adverb":
        return "form-adverb"
    else:
        return "form-other"

def generate_page(words, page_num, total_pages, total_words):
    """Generate HTML for a vocabulary page."""
    start = (page_num - 1) * WORDS_PER_PAGE + 1
    end = min(page_num * WORDS_PER_PAGE, total_words)

    # Navigation links
    prev_link = f'<a href="words-{(page_num-2)*WORDS_PER_PAGE+1:03d}-{(page_num-1)*WORDS_PER_PAGE:03d}.html">← Previous</a>' if page_num > 1 else '<a class="disabled">← Previous</a>'
    next_link = f'<a href="words-{page_num*WORDS_PER_PAGE+1:03d}-{min((page_num+1)*WORDS_PER_PAGE, total_words):03d}.html">Next →</a>' if page_num < total_pages else '<a class="disabled">Next →</a>'

    # Build table rows
    rows = []
    for word in words:
        rank = word['rank']
        spanish = word['spanish']
        english = word['english']
        form = word['form']
        infinitive = word.get('infinitive', '').strip()

        # Add infinitive for verbs (if different from the word itself)
        spanish_display = spanish
        if infinitive and infinitive != spanish:
            spanish_display = f'{spanish} <span class="infinitive">({infinitive})</span>'

        form_class = get_form_class(form)
        form_abbrev = form[:4] if len(form) > 4 else form  # Abbreviate long forms

        rows.append(f'''            <tr>
                <td class="rank">{rank}</td>
                <td class="spanish">{spanish_display}</td>
                <td>{english}</td>
                <td><span class="form {form_class}">{form_abbrev}</span></td>
            </tr>''')

    table_rows = '\n'.join(rows)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spanish Vocabulary: Words {start}-{end}</title>
    <style>{CSS}</style>
</head>
<body>
    <header>
        <h1>Spanish Vocabulary</h1>
        <p class="subtitle">Words {start}-{end} of {total_words}</p>
    </header>

    <nav>
        <a href="index.html">Index</a>
        {prev_link}
        {next_link}
    </nav>

    <table>
        <thead>
            <tr>
                <th>Rank</th>
                <th>Spanish</th>
                <th>English</th>
                <th>Form</th>
            </tr>
        </thead>
        <tbody>
{table_rows}
        </tbody>
    </table>

    <footer>
        <nav>
            <a href="index.html">Index</a>
            {prev_link}
            {next_link}
        </nav>
        <p style="margin-top: 15px;">Data source: Real Academia Española (RAE)</p>
    </footer>
</body>
</html>'''

    return html

def generate_index(total_pages, total_words):
    """Generate the index page."""
    # Group pages by level
    links = []
    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * WORDS_PER_PAGE + 1
        end = min(page_num * WORDS_PER_PAGE, total_words)
        filename = f"words-{start:03d}-{end:03d}.html"
        links.append(f'<a href="{filename}">Words {start}-{end}</a>')

    links_html = '\n            '.join(links)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spanish Vocabulary - Top {total_words} Words</title>
    <style>
{CSS}
.index-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
    margin: 20px 0;
}}
.index-grid a {{
    display: block;
    padding: 15px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    text-decoration: none;
    color: #333;
    text-align: center;
    transition: all 0.2s;
}}
.index-grid a:hover {{
    border-color: #c41e3a;
    background: #fff3cd;
}}
.level-section {{
    margin: 30px 0;
}}
.level-title {{
    color: #c41e3a;
    border-bottom: 2px solid #c41e3a;
    padding-bottom: 5px;
    margin-bottom: 15px;
}}
    </style>
</head>
<body>
    <header>
        <h1>Spanish Vocabulary</h1>
        <p class="subtitle">Top {total_words} Most Frequent Words</p>
    </header>

    <div class="level-section">
        <h2 class="level-title">All Pages</h2>
        <div class="index-grid">
            {links_html}
        </div>
    </div>

    <footer>
        <p>Data source: Real Academia Española (RAE)</p>
    </footer>
</body>
</html>'''

    return html

def main():
    # Read CSV
    words = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words.append(row)

    total_words = len(words)
    total_pages = (total_words + WORDS_PER_PAGE - 1) // WORDS_PER_PAGE

    print(f"Processing {total_words} words into {total_pages} pages...")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate vocabulary pages
    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * WORDS_PER_PAGE
        end_idx = min(page_num * WORDS_PER_PAGE, total_words)
        page_words = words[start_idx:end_idx]

        start = start_idx + 1
        end = end_idx
        filename = f"words-{start:03d}-{end:03d}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)

        html = generate_page(page_words, page_num, total_pages, total_words)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Generated {filename}")

    # Generate index page
    index_html = generate_index(total_pages, total_words)
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"  Generated index.html")

    print(f"\nDone! {total_pages + 1} files generated in {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()

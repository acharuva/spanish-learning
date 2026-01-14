# Spanish Vocabulary Learning Tool - Implementation Plan

## Project Overview

**Goal**: Create a web-based Spanish vocabulary learning tool with the top 3000 most frequent Spanish words.

**Key Requirements**:
- 3000 Spanish words with English translations and word forms (noun/verb/adjective/etc.)
- Split into 60 HTML pages (50 words per page)
- Beautiful CSS-styled tables displaying: rank, Spanish word, English translation, word form
- Index page with navigation to all 60 pages
- Static HTML only (no JavaScript)

**Target User**: Spanish beginner building vocabulary

---

## Data Source

### Primary Source: RAE Corpus Frequency List
- **File**: `data/10000_formas.TXT`
- **URL**: https://corpus.rae.es/frec/10000_formas.TXT
- **Source**: Real Academia Española (RAE) - the official authority on the Spanish language
- **Contains**: Top 10,000 most frequent Spanish word forms

### File Format
```
Orden    Frec.absoluta    Frec.normalizada
1.       de               9,999,518    65545.55
2.       la               6,277,560    41148.59
3.       que              4,681,839    30688.85
```

**Columns** (tab-separated):
1. Rank (with period, e.g., "1.")
2. Spanish word
3. Absolute frequency
4. Normalized frequency

**Encoding**: Latin-1 (ISO-8859-1) - needs conversion to UTF-8

### Data Processing Required
The RAE file provides frequency-ranked Spanish words but **does not include**:
- English translations
- Word forms (noun/verb/adjective/etc.)

**Solution**: Use Claude (LLM) to translate words and identify word forms - no external APIs needed.

---

## Technology Stack

### Recommended: Python
**Why Python?**
- Simple data manipulation with pandas
- Easy HTML templating with Jinja2
- Great for data processing and file generation

**Key Libraries**:
- `pandas` - Data manipulation and CSV handling
- `jinja2` - HTML templating

### Translation Approach: LLM-Based
Instead of external translation APIs, we use Claude (the LLM) to:
- Translate Spanish words to English
- Identify part of speech (verb, noun, adjective, etc.)
- Handle context-dependent meanings

**Advantages**:
- No API keys or rate limits
- High-quality translations with nuance
- Can batch process words efficiently
- Understands word forms and conjugations

---

## Data Schema

### Final Output Format: CSV
```csv
rank,spanish,english,form,infinitive
1,de,of/from,preposition,
2,la,the,article,
3,que,that/which,conjunction,
19,es,he/she is,verb,ser
39,ser,to be,verb,ser
43,fue,he/she was / went,verb,ser/ir
57,hay,there is/are,verb,haber
```

**Fields:**
- `rank`: Frequency rank (1-3000)
- `spanish`: The Spanish word as it appears in the corpus
- `english`: English translation with pronoun for verbs (e.g., "I am", "he/she was")
- `form`: Part of speech (verb, noun, adjective, etc.)
- `infinitive`: Base verb form (only for verbs, empty for other forms)

**Verb Display Rules:**
- Conjugated verbs show infinitive inline: "fue *(ser/ir)*"
- Infinitive verbs show as-is: "ser"
- Multiple infinitives separated by slash: "ser/ir"
- Impersonal verbs use "there": "there is/are", "there was"
- All verb translations include the pronoun: "I am", "he/she goes", "we have"

### Processing Pipeline
1. Read `data/10000_formas.TXT` (Latin-1 encoding)
2. Parse and extract first 3000 words
3. Clean data (remove rank periods, handle encoding)
4. Add English translations (with pronouns for verbs)
5. Add word forms (part of speech)
6. Add infinitive forms (for verbs only)
7. Save as `data/spanish_3000_words.csv` (UTF-8)

---

## File Structure

```
spanish/
├── docs/
│   └── implementation-plan.md
├── data/
│   ├── 10000_formas.TXT          # Original RAE data (Latin-1)
│   └── spanish_3000_words.csv    # Processed data with translations
├── pages/
│   ├── index.html                # Main navigation page
│   ├── words-001-050.html        # Page 1: words 1-50
│   ├── words-051-100.html        # Page 2: words 51-100
│   ├── words-101-150.html        # Page 3: words 101-150
│   └── ...                       # 60 pages total
├── scripts/
│   ├── process_data.py           # Parse RAE file, add translations
│   └── generate_pages.py         # HTML generation script
└── requirements.txt              # Python dependencies
```

---

## HTML/CSS Design

### Page Structure

Each vocabulary page will have:
- Header with page title and navigation
- Table with 50 words
- Footer with navigation to previous/next pages and index

### CSS Styling Approach

**Approach**: Inline CSS in each HTML file for portability

**Table Design Features**:
- Responsive layout
- Alternating row colors (zebra striping)
- Header with bold styling
- Hover effects on rows
- Clean, readable typography
- Mobile-friendly design
- Color-coded word forms (verb=blue, noun=green, etc.)

### Sample HTML Structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spanish Vocabulary: Words 1-50</title>
    <style>
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
        nav { margin: 15px 0; }
        nav a {
            color: #c41e3a;
            text-decoration: none;
            padding: 8px 16px;
            border: 1px solid #c41e3a;
            border-radius: 4px;
            margin: 0 5px;
        }
        nav a:hover { background: #c41e3a; color: white; }
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
        .form-adj { background: #fff3e0; color: #e65100; }
        .form-other { background: #f3e5f5; color: #7b1fa2; }
        footer { margin-top: 20px; text-align: center; }
    </style>
</head>
<body>
    <header>
        <h1>Spanish Vocabulary</h1>
        <p>Words 1-50 of 3000</p>
    </header>

    <nav>
        <a href="index.html">← Index</a>
        <a href="words-051-100.html">Next →</a>
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
            <!-- Non-verb example -->
            <tr>
                <td class="rank">1</td>
                <td class="spanish">de</td>
                <td>of, from</td>
                <td><span class="form form-other">prep</span></td>
            </tr>
            <!-- Verb example with inline infinitive -->
            <tr>
                <td class="rank">43</td>
                <td class="spanish">fue <span class="infinitive">(ser/ir)</span></td>
                <td>he/she was / went</td>
                <td><span class="form form-verb">verb</span></td>
            </tr>
            <!-- Impersonal verb example -->
            <tr>
                <td class="rank">57</td>
                <td class="spanish">hay <span class="infinitive">(haber)</span></td>
                <td>there is/are</td>
                <td><span class="form form-verb">verb</span></td>
            </tr>
        </tbody>
    </table>

    <footer>
        <nav>
            <a href="index.html">← Index</a>
            <a href="words-051-100.html">Next →</a>
        </nav>
    </footer>
</body>
</html>
```

### Index Page Design:
- Grid layout with links to all 60 pages
- Show word range for each page (e.g., "Words 1-50")
- Visual grouping by difficulty (words 1-1000, 1001-2000, 2001-3000)

---

## Implementation Steps

### Phase 1: Data Processing

1. **Create data processing script** (`scripts/process_data.py`)
   - Read RAE file with Latin-1 encoding
   - Parse tab-separated data
   - Extract first 3000 words
   - Clean rank numbers (remove periods)
   - Handle special characters

2. **Add English translations and word forms using LLM**
   - Use Claude sub-agent to process words in batches (e.g., 100 words at a time)
   - For each word, get: English translation(s) and part of speech
   - Categories: verb, noun, adjective, adverb, preposition, article, pronoun, conjunction, other
   - Handle conjugated verb forms (e.g., "fue" → "was/went", verb)
   - Output as structured data (CSV format)

3. **Save processed data**
   - Output to `data/spanish_3000_words.csv`
   - UTF-8 encoding
   - Validate completeness

### Phase 2: HTML Generation

5. **Create HTML generation script** (`scripts/generate_pages.py`)
   - Read processed CSV data
   - Split into 60 groups of 50 words
   - Generate HTML with inline CSS
   - Add navigation links (previous/next/index)
   - Save to `pages/` directory

6. **Create index page**
   - Generate `pages/index.html`
   - Grid layout with links to all 60 pages
   - Group by difficulty level

### Phase 3: Testing

7. **Local testing**
   - Open pages in browser
   - Check table formatting
   - Verify navigation links work
   - Test on mobile devices
   - Verify special characters display correctly (á, é, í, ó, ú, ñ, ü)

8. **Deployment options**
   - GitHub Pages (free, easy setup)
   - Netlify (drag-and-drop hosting)
   - Any static web hosting service

---

## Challenges and Solutions

### Challenge 1: Encoding Issues
**Problem**: RAE file uses Latin-1 encoding, causing characters like "más" to appear as "m�s"
**Solution**: Read file with `encoding='latin-1'` and save output as UTF-8

### Challenge 2: Adding Translations and Word Forms
**Problem**: RAE file doesn't include English translations or parts of speech
**Solution**: Use Claude (LLM) sub-agents to translate and classify words
- Process in batches of ~100 words for efficiency
- LLM has comprehensive Spanish vocabulary knowledge
- Can handle conjugated forms and context-dependent meanings
- No external API dependencies

### Challenge 3: Verb Conjugations
**Problem**: Frequency list includes conjugated forms (fue, era, había) not infinitives
**Note**: This is actually useful for learners - they learn actual word forms used in Spanish

---

## Next Steps

1. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install pandas jinja2
   ```

2. **Create `requirements.txt`**
   ```
   pandas
   jinja2
   ```

3. **Parse RAE data file**
   - Extract first 3000 words from `data/10000_formas.TXT`
   - Handle Latin-1 encoding

4. **Translate words using LLM sub-agents**
   - Process words in batches (~100 at a time)
   - Get English translations and parts of speech
   - Save to `data/spanish_3000_words.csv`

5. **Create HTML generation script**

6. **Generate pages and test**

---

## Success Criteria

- [ ] RAE data parsed correctly (3000 words)
- [ ] All words have English translations
- [ ] All words have form classification
- [ ] 60 HTML pages generated (50 words each)
- [ ] Index page with working navigation
- [ ] Beautiful, responsive CSS tables
- [ ] All navigation links functional
- [ ] Special characters display correctly (á, é, í, ó, ú, ñ)
- [ ] Mobile-friendly design

---

**Version**: 2.2
**Date**: 2026-01-13
**Data Source**: Real Academia Española (RAE) Corpus
**Translation**: LLM-based (Claude sub-agents)

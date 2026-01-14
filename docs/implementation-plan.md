# Spanish Vocabulary Learning Tool - Implementation Plan

## Project Overview

**Goal**: Create a static website with the top 3000 most frequent Spanish words for vocabulary learning.

**Features**:
- 3000 Spanish words with English translations and word forms
- 60 HTML pages (50 words per page)
- Tables showing: rank, Spanish word, English translation, word form
- Index page with navigation to all pages
- Hosted on AWS S3

**Target User**: Spanish beginner building vocabulary

---

## Data Source

**File**: `data/10000_formas.TXT`
**Source**: Real Academia Española (RAE) - https://corpus.rae.es/frec/10000_formas.TXT

**Format** (tab-separated, Latin-1 encoding):
```
Orden    Frec.absoluta    Frec.normalizada
1.       de               9,999,518    65545.55
2.       la               6,277,560    41148.59
```

---

## Data Schema

**Output**: `data/spanish_3000_words.csv` (UTF-8)

```csv
rank,spanish,english,form,infinitive
1,de,of/from,preposition,
2,la,the,article,
19,es,he/she is,verb,ser
43,fue,he/she was / went,verb,ser/ir
57,hay,there is/are,verb,haber
```

**Fields**:
- `rank`: Frequency rank (1-3000)
- `spanish`: Spanish word as it appears in corpus
- `english`: English translation (with pronoun for verbs)
- `form`: Part of speech (verb, noun, adjective, adverb, preposition, article, pronoun, conjunction, other)
- `infinitive`: Base verb form (only for verbs)

**Verb Rules**:
- Conjugated verbs show infinitive inline: `fue (ser/ir)`
- Translations include pronoun: "I am", "he/she was", "we have"
- Impersonal verbs: "there is/are", "there was"

---

## File Structure

```
spanish/
├── docs/
│   └── implementation-plan.md
├── data/
│   ├── 10000_formas.TXT          # Original RAE data
│   └── spanish_3000_words.csv    # Processed data with translations
├── pages/
│   ├── index.html
│   ├── words-001-050.html
│   ├── words-051-100.html
│   └── ...                       # 60 pages total
├── scripts/
│   └── generate_pages.py         # HTML generation script
└── requirements.txt
```

---

## HTML/CSS Design

**Approach**: Inline CSS for portability (self-contained pages)

**Features**:
- Responsive layout
- Zebra-striped rows
- Hover effects
- Color-coded word forms (verb=blue, noun=green, adjective=orange, other=purple)
- Mobile-friendly

**Sample Table Row**:
```html
<!-- Non-verb -->
<tr>
    <td class="rank">1</td>
    <td class="spanish">de</td>
    <td>of, from</td>
    <td><span class="form form-other">prep</span></td>
</tr>

<!-- Verb with infinitive -->
<tr>
    <td class="rank">43</td>
    <td class="spanish">fue <span class="infinitive">(ser/ir)</span></td>
    <td>he/she was / went</td>
    <td><span class="form form-verb">verb</span></td>
</tr>
```

---

## Implementation Steps

### Phase 1: Data Processing

1. **Parse RAE file**
   - Read with Latin-1 encoding
   - Extract first 3000 words
   - Clean rank numbers (remove periods)

2. **Translate using LLM**
   - Use Claude sub-agents to process in batches (~100 words)
   - Get: English translation, part of speech, infinitive (for verbs)
   - Save to `data/spanish_3000_words.csv`

### Phase 2: HTML Generation

3. **Generate vocabulary pages**
   - Create `scripts/generate_pages.py`
   - Split data into 60 groups of 50 words
   - Generate HTML with inline CSS
   - Add prev/next navigation

4. **Generate index page**
   - Grid layout linking to all 60 pages
   - Group by level (1-1000, 1001-2000, 2001-3000)

### Phase 3: Deploy

5. **Test locally**
   - Verify table formatting
   - Check navigation links
   - Test special characters (á, é, í, ó, ú, ñ)

6. **Deploy to S3**
   ```bash
   aws s3 sync pages/ s3://your-bucket-name --delete
   ```

---

## Success Criteria

- [ ] 3000 words parsed from RAE data
- [ ] All words have English translations
- [ ] All words have form classification
- [ ] Verbs have infinitive forms
- [ ] 60 HTML pages generated
- [ ] Index page with working navigation
- [ ] Special characters display correctly
- [ ] Deployed to S3

---

**Version**: 3.0
**Date**: 2026-01-13

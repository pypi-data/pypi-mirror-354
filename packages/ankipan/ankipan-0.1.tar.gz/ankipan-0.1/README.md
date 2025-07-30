# Ankipan

Ankipan is a language learning utility which systematically tracks the words you already know, and allows you to parse any source you are personally interested in (text, subtitles, websites, lyrics etc.) for new words to learn.

New words are internally stored and converted to Anki Flashcards, which contain customizable content such as scraped dictionary definitions and example sentences from different sources.

Currently supported languages are japanese, german, french and english.

## Getting started

### 1. Prerequisites

- Download and install anki from https://apps.ankiweb.net/
- Create an account on their website
- Install the ankiconnect plugin from https://ankiweb.net/shared/info/2055492159
- Open the app and login, keep anki open when syncing databases (in anki, open Tools -> Add Ons -> Get Add-Ons -> paste code 2055492159)

### 2. Installation

```bash
# Clone the repository
git clone git@gitlab.com:ankipan/ankipan_db.git
cd ankipan_db

# Install dependencies:
python -m pip install -r requirements.txt

```

### 3. (Optional) Install lemmatizers to parse your own texts

- Download pytorch from https://pytorch.org/get-started/locally/ (for stanza lemma parsing)
- install dependencies:

```bash
 pip install stanza hanta
```
-  Select language, currently supported are 'jp, 'de', 'fr', 'en', see https://stanfordnlp.github.io/stanza/performance.html

```bash
 python -c "import stanza; stanza.download('jp')"
```

## Usage

See interactive notebook in `/examples`

```python
# Create a new collection with your name, learning language and native language
from ankipan import Collection
collection = Collection('testcollection', source_lang='jp', native_lang='en')

# Specify content to be downloaded for flashcards (see collection.get_available_sources() for example sentences and scraper.py module)
collection.section_names = ['sentences_anime', 'sentences_lyrics', 'sentences_youtube', 'jisho', 'wadoku', 'wikitionary_en', 'wikitionary_jp']

# Specify a source the words of which you would like to add to your collection, either from db or path textfile or folder with textfiles
# Alternatively, specify source name from db or string or wordcounts directly (see help(Collection.collect))
words = collection.collect('example_text_jp.txt')

# Select the words you already know and the words you would like to learn from the table overview
words.select_new_words()

# Add words to collection
collection.add_deck(words, 'example_source')

# Optional: Persist collection state to harddrive (see /'.data' folder)
collection.save()

# Download content for new cards (also autosaves collection to drive)
collection.fetch('example_source')

# Sync current collection with anki to upload them to currently open anki instance
collection.sync_with_anki('testsource')

```

## Notes

- Current lemmatization is done via the `stanza` library in the reader.py module. While this works mostly fine, the library still just uses a statistical model to estimate the likely word roots (lemmas) of the different pieces of sentences. It sometimes makes mistakes, which requires the users to manually filter them in the `select_new_words` overview, or suspend the card later on in anki.

- The translation engine running on the server has a limited quota. Once it has been exceeded for the day, users will have to specify their own API key which is then locally used for translations. (TODO)

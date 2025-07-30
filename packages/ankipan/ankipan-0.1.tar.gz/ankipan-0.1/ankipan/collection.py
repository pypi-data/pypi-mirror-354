from pathlib import Path
from collections import OrderedDict, Counter
from copy import deepcopy
import requests
import logging
import shutil
import fnmatch
import json

from typing import Union, Dict, Iterable, List, Any

from . import PROJECT_ROOT, DATA_DIR, ANKIPAN_DB_ADDR
from . import Scraper
from . import AnkiManager
from . import Reader, File
from . import Card
from . import Deck
from . import util
from . import CardSection
from . import load_json, save_json

logger = logging.getLogger(__name__)

# TODO: generate automatically from scraper module
VALID_SECTION_NAMES = ['sentences_*', 'jisho', 'wadoku', 'sprachnudel', 'tatoeba', 'urban', 'wikitionary_*']

class Collection:
    def __init__(self,
                 name: str,
                 *,
                 source_lang: str = None,
                 native_lang: str = None,
                 section_names: List[str] = None,
                 data_dir = DATA_DIR):
        """
        Load new or existing collection

        Parameters
        ----------
        name : Name of collection.
            Creates new collection for new names, loads existing collection for existing names.
        source_lang : Name of language the user wants to learn.
            Currently available: ['jp', 'de', 'en', 'fr']
        native_lang : Native language of the user for translations and explanations.
            Currently available: ['en', 'de']
        section_names (optional): Names of the sections to be scraped/downloaded when calling collection.fetch()
            Select from fetch_* functions in Scraper module.
            Order of list is currently used to determine how to print card backsides (e.g. first dict translation and then examples)
            Currently available: ['jisho', 'dict', 'tatoeba']

        """
        self.name = name
        self.data_dir = data_dir
        self.metadata_path = data_dir / name / 'metadata.json'
        self.card_sections_dir = data_dir / name / 'card_sections'
        metadata = load_json(self.metadata_path)
        if metadata:
            if source_lang or native_lang or section_names:
                raise RuntimeError(f'Initializing existing database "{name}", specified kwargs would be ignored')
            self.source_lang = metadata.get('source_lang', source_lang)
            self.native_lang = metadata.get('native_lang', native_lang)
            self.source_names = metadata.get('source_names', [])
            self.section_names = metadata.get('section_names', [])
            self.known_sources = metadata.get('known_sources', {})
            self.cards = {}
            for word in metadata.get('card_words', []):
                self.cards[word] = Card.from_dict(word, self.card_sections_dir / f'{word}.json')
            self.known_words = {}
            for known_word in metadata.get('known_words', []):
                self.known_words[known_word] = Card.from_dict(word, self.card_sections_dir / f'{word}.json')
        else:
            if not (source_lang and native_lang):
                raise RuntimeError('source_lang and native_lang kwargs required when initializing new collection')
            self.source_lang = source_lang
            self.native_lang = native_lang
            self.source_names = []
            self.section_names = section_names if section_names else []
            self._known_sources = {}
            self.cards = {}
            self.known_words = {}

        self.anki_manager = AnkiManager()
        self.reader = Reader(self.source_lang)
        self.scraper = Scraper(self.source_lang, self.native_lang)
        self._available_sources = None

    @property
    def known_sources(self):
        """
        Tracks categories of sources and concrete sources that the user is familiar with.

        Examples
        --------
        collection = Collection('testcollection', source_lang='jp', native_lang='en')
        collection.get_available_sources()
            --> {'anime': ['One Piece', 'Bleach', ...], 'lyrics': {'Eve': [...], ...}, ...}
        collection.known_sources = {'anime': ['One Piece']}
        # Get Word percentile information in word overview and display example sentences from categories on flashcards
        # Prioritize and highlight familiar sources in particular (Always try to include One piece example sentences if possible)
        # Also include other sources if not enough example sentences are available

        OR

        collection.get_available_sources().keys()
            --> dict_keys(['Netflix', 'anime', 'jpsubbers', 'lyrics', 'misc', 'youtube'])
        collection.known_sources = ['anime', 'lyrics', 'youtube']
            --> {'anime': [], 'lyrics': [], 'youtube': [], }
        # Still generates percentile information and displays generic example sentences from categories

        """
        return self._known_sources

    @known_sources.setter
    def known_sources(self, value):
        sources = {}
        if isinstance(value, list):
            for item in value:
                assert item in self.get_available_sources().keys()
                sources[item] = []
        elif isinstance(value, dict):
            for key, vals in value.items():
                assert key in self.get_available_sources().keys()
                for val in vals:
                    assert val in self.get_available_sources()[key]
                sources[key] = vals
        self._known_sources = sources

    @property
    def all_words(self):
        return self.cards | self.known_words

    @property
    def sorted_learning_words(self):
        return [word for word, card in sorted(self.cards.items(), key=lambda kv: kv[1].frequency, reverse=True)]

    @property
    def word_frequencies(self):
        return OrderedDict({word: card.frequency for word, card in sorted(self.cards.items(), key=lambda kv: kv[1].frequency, reverse=True)})

    @property
    def words_with_content(self):
        return [word for word in self.sorted_learning_words
                if all([section_name in self.cards[word].keys() for section_name in self.section_names])]

    def collect(self,
                paths: Union[Union[str, Path], Iterable[Union[str, Path]]] = None,
                *,
                source_name: str = None,
                string: str = None,
                word_counts: Dict[str, int] = None) -> Deck:
        """
        Collect words from specified source.

        Parameters
        ----------
        path: Path to a file or directory with textfiles to be added to the collection
            Uses stanza lemma parsing from reader.py to parse source files into wordcount dictionary

        kwargs (only consiered if path is not provided):
            source_name: Name of source in db to fetch lemmas from (does not require stanza)
            string: String to be parsed directly without reading a file
            word_counts: Dict of words and word_counts, directly adopted as Deck object

        """
        if not (isinstance(paths, list) or isinstance(paths, set)):
            if isinstance(paths, str) or isinstance(paths, Path):
                paths = [paths]
            elif not paths == None:
                raise RuntimeError(f'Unknown type passed as path: {paths}')
        deck = Deck(self.source_lang, self.native_lang,
                                         section_names = self.section_names,
                                         learning_collection_words = set(self.cards.keys()),
                                         known_collection_words = set(self.known_words.keys()),
                                         known_collection_sources = self.known_sources.keys())
        if paths:
            for path in paths:
                deck.add(path=path)
        elif string:
            deck.add(string=string)
        elif word_counts:
            deck.add(word_counts=word_counts)
        elif source_name:
            data = {'lang': self.source_lang, 'source_name': source_name}
            res = requests.post(f'{ANKIPAN_DB_ADDR}/api/source_lemmas', json=data)
            if res.status_code == 404:
                raise RuntimeError(f'Ankipan DB 404 Error: {res.json()}')
            lemmas_and_count = res.json()
            deck.source_words.update(lemmas_and_count)
        return deck

    def add_deck(self,
            deck: Deck,
            source_name: str):
        """
        Add new deck from new words in Deck to current collection.
        Changes made to the new words and known words in the Deck object are adopted into the collection.

        Parameters
        ----------
        words: Words from Deck
        source_name: Name of source you are adding, e.g. movie or series title

        """

        if not source_name:
            raise RuntimeError('source_name is a mandatory field')
        if source_name in self.source_names:
            raise RuntimeError('source with same name already in collection')
        self.source_names.append(source_name)
        for word, freq in deck.known_words.items():
            if word in self.cards.keys(): #TODO: not needed?
                self.known_words[word] = self.cards.pop(word)
            elif word not in self.known_words:
                self.known_words[word] = Card(word, source_references = {source_name: freq})
            self.known_words[word].source_references[source_name] = freq
        for word, freq in deck.learning_words.items():
            self.cards[word].source_references[source_name] = freq
        for i, word in enumerate(deck.new_words):
            # TODO: Look into if this is too convoluted, we pass the available sources to the wordcollection, then get this info back? Maybe recalculate or store in db?
            self.cards[word] = Card(word, source_references = {source_name: deck.source_words[word]}, index = i)

    def remove(self,
               source_name: str):
        """
        Remove source added with specific name
                    file_paths = set()
        """
        # TODO: consider caching mechanism so downloaded info isn't destroyed
        if source_name not in self.source_names: raise RuntimeError(f'source name "{source_name}" not present in list of collection source names')
        self.source_names.remove(source_name)
        for stack in [self.cards, self.known_words]:
            superfluous_cards = []
            for word, card in stack.items():
                if source_name in card.source_references.keys():
                    if len(card.source_references) == 1:
                        superfluous_cards.append(word)
                    else:
                        stack[word].source_references.pop(source_name)
            [stack.pop(word) for word in superfluous_cards]

    # TODO: solve more elegantly with setter override or custom class
    def validate_section_names(self):
        bad = [n for n in self.section_names
            if not any(fnmatch.fnmatch(n, p) for p in VALID_SECTION_NAMES)]
        if bad:
            raise RuntimeError(f"Invalid section names: {', '.join(bad)}")

    # TODO: ignores existing sources and overwrites everything for some reason
    def fetch(self,
              source_name: str,
              section_names: Iterable[str] = None,
              words: Iterable[str] = None,
              force_update = False):
        """
        Scrape/download data for new cards from sources

        Parameters
        ----------
        source_name: Name of source to download data for
        section_names (optional): restrict sections to download data for
        words (optional): restrict words to download data for
        force_update: overwrite existing data

        """
        self.validate_section_names()
        if not words:
            words = self.cards.keys()
        missing_sections = {}
        source_cards = [card for card in self.cards.values() if card.source_references and list(card.source_references.keys())[0] == source_name and card.word in words]
        logger.debug(f'Fetching sources for "{source_name}"')

        for card in source_cards:
            missing_sections_for_word = [section_name for section_name in (section_names if section_names else self.section_names) if not section_name in card.keys() or force_update]
            logger.debug(f'missing sections for "{card.word}": {missing_sections_for_word}')
            for section in missing_sections_for_word:
                if section not in missing_sections:
                    missing_sections[section] = [card.word]
                else:
                    missing_sections[section].append(card.word)
        if missing_sections:
            print(f'Fetching content for "{source_name}", {list(missing_sections.keys())}:')
            for section_name, words in missing_sections.items():
                print(f' - {section_name}: {words}')

            for i, (section_name, results) in enumerate(self.scraper.fetch_card_sections(missing_sections, known_sources_by_subdomain = self.known_sources).items()):
                for word in missing_sections[section_name]:
                    if word in results.keys():
                        self.cards[word][section_name] = results[word]
                    else:
                        self.cards[word][section_name] = CardSection('empty', 'black', '')
            self.save()

    def sync_with_anki(self, source_name: str, overwrite = False):
        """
        Sync collection data with anki database.
        Uses AnkiConnect to interface with anki app functionalities via localhost.
        Requires anki to be installed, open and logged in during execution. (see README.md)
        https://apps.ankiweb.net/

        TODO: Currently slow at adding new cards, improve (windows issue)
        """

        # TODO: add "full_overwrite" kwarg, which bulk-removes and readds card instead of updating one by one (faster)
        source_cards = [card for card in self.cards.values() if source_name in card.source_references.keys()]
        # TODO: sometimes not sorted? See Card.index creation
        source_cards.sort(key=lambda card: (card.index is None, card.index))
        incomplete_cards = {}
        for card in source_cards:
            for section_name in self.section_names:
                if section_name not in card.keys():
                    if card.word not in incomplete_cards:
                        incomplete_cards[card.word] = [section_name]
                    else:
                        incomplete_cards[card.word].append(section_name)
        if incomplete_cards:
            raise RuntimeError(f'Some words are missing sections defined in the collection, run collection.fetch(<source_name>) first: {incomplete_cards}')
        if source_cards:
            print('Syncing anki for words', [card.word for card in source_cards])
            self.anki_manager.sync_collection(source_name, source_cards, self.section_names, overwrite=overwrite)
            self.anki_manager.sync()

    def save(self, name = None):
        """
        Write all collection data to MongoDB database.

        """
        self.validate_section_names()
        if not name:
            name = self.name
        if not self.card_sections_dir.exists():
            self.card_sections_dir.mkdir(parents=True, exist_ok=True)
        print(f'saving collection "{name}"')
        metadata = {
            'source_lang': self.source_lang,
            'native_lang': self.native_lang,
            'section_names': self.section_names,
            'source_names': self.source_names,
            'card_words': list(self.cards.keys()),
            'known_words': list(self.known_words.keys()),
            'known_sources': self.known_sources
        }
        save_json(self.metadata_path, metadata)

        for word, card in {**self.cards, **self.known_words}.items():
            if card.was_modified:
                json_path = self.card_sections_dir / f'{word}.json'
                save_json(json_path, card.as_dict())
                if not card.json_path:
                    card.json_path = json_path

    def estimate_known_words_for_domain(self, subdomain, level = None):
        word_counts = requests.post(f'{ANKIPAN_DB_ADDR}/api/corpus_wordcounts', json={'lang': self.source_lang, 'subdomains': [subdomain]}).json()
        proficiency_level = level*0.01*len(word_counts[subdomain]) if level else util.estimate_proficiency(word_counts[subdomain])
        items = Counter(word_counts[subdomain]).most_common()[:int(proficiency_level)]
        return self.collect(word_counts = dict(items), is_known = True)

    def get_available_sources(self, domain_names: List[str] = None) -> Dict[str, Dict[str, List[str]]]:
        if self._available_sources is None:
            data = {'domain_names': domain_names, 'lang': self.source_lang}
            try:
                self._available_sources = requests.post(f'{ANKIPAN_DB_ADDR}/api/available_sources', json=data).json()
            except (json.JSONDecodeError, ConnectionRefusedError) as e:
                logger.error(f'Server to fetch sources not available: {e}')
        return self._available_sources

    def add_custom(self, custom_explanations: Dict[str, CardSection]):
        """
        User method to add arbitrary card sections to collection cards.

        Parameters
        ----------
        custom_explanations: dict
            Map of words to CardSection object
            Can also be simple string or html wrapped inside, see classes in scraper module

        """

        unknown_items = [key for key in custom_explanations if key not in self.all_words]
        if unknown_items:
            raise RuntimeError(f'Unknown items {unknown_items}')
        for word, explanation in custom_explanations.items():
            if word in self.all_words:
                self.all_words[word]['custom'] = explanation
            else:
                self.cards[word] = Card(word)
                self.cards[word]['custom'] = explanation

    @classmethod
    def load_from_dict(cls, name, dict: Union[str, Union[str, Iterable, Dict[str, Dict[str, Union[int, dict]]]]]) -> 'Collection':
        """
        Initialize collection from dictionary.

        Mostly used for testing.

        """
        dict_ = deepcopy(dict)
        card_words = dict_.pop('card_words')  if 'cards' in dict_.keys() else {}
        known_words = dict_.pop('known_words')  if 'known_words' in dict_.keys() else []
        source_names = dict_.pop('source_names') if 'source_names' in dict_.keys() else []

        instance = cls(name, **dict_)
        instance.cards = {word: Card.from_dict(word, PROJECT_ROOT / name / 'card_sections' / f'{name}.json') for word in card_words}
        instance.known_words = {word: Card.from_dict(word, PROJECT_ROOT / name / 'card_sections' / f'{name}.json') for word in known_words}
        instance.source_names = source_names

        return instance

    # TODO: Implement safety mechanism to not accidentally lose massive amounts of data
    # TODO: Implement function to recreate database based on current anki database state in case of loss
    def delete_collection(self, name):
        """
        Delete collection from database
        Currently ignores whether collection is present in database or not

        """
        if input('Are you sure? type "yes"') == 'yes':
            shutil.rmtree(self.data_dir / name)

    def as_dict(self):
        return {
            'source_lang': self.source_lang,
            'native_lang': self.native_lang,
            'section_names': self.section_names,
            'source_names': self.source_names,
            'card_words': [word for word in self.cards.keys()],
            'known_words': [word for word in self.cards.keys()],
            'known_sources': self.known_sources
        }

    def __repr__(self):
        return '\n'.join([
        f'name (collection name): {self.name}',
        f'source_lang: {self.source_lang}',
        f'native_lang: {self.native_lang}',
        f'source_names: {self.source_names}',
        f'section_names: {self.section_names}',
        f'n cards: {len(self.cards)}',
        f'n known_words: {len(self.known_words)}',
        f'n words_with_content: {len(self.words_with_content)}'])

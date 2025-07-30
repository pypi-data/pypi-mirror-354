from pathlib import Path
from collections import OrderedDict, Counter
from copy import deepcopy
import requests
import logging
import shutil
from collections.abc import Iterable
import json
import fnmatch
from urllib3.exceptions import MaxRetryError

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

class Collection:
    def __init__(self,
                 name: str,
                 *,
                 source_lang: str = None,
                 native_lang: str = None,
                 data_dir = DATA_DIR):
        """
        Load new or existing collection.
        A collection can hold 0 to n decks.
        A deck can hold 1 to n flashcards.
        Flashcards have 1 to n fields, which refers to information on the backside (dictionary definitions, example sentences etc.)

        Parameters
        ----------
        name : Name of collection.
            Creates new collection for new names, loads existing collection for existing names.
        source_lang : Name of language the user wants to learn.
            Currently available: ['jp', 'de', 'en', 'fr']
        native_lang : Native language of the user for translations and explanations.
            Currently available: ['en', 'de']

        """
        self.name = name
        self.data_dir = data_dir
        self.metadata_path = data_dir / name / 'metadata.json'
        self.flashcard_fields_dir = data_dir / name / 'flashcard_fields'
        metadata = load_json(self.metadata_path)
        if metadata:
            if source_lang or native_lang:
                raise RuntimeError(f'Initializing existing database "{name}", specified kwargs would be ignored')
            self.source_lang = metadata.get('source_lang', source_lang)
            self.native_lang = metadata.get('native_lang', native_lang)
            self.source_names = metadata.get('source_names', [])
            self.flashcard_fields = metadata.get('flashcard_fields', {})
            self.known_sources = metadata.get('known_sources', {})
            self.cards = {}
            for word in metadata.get('card_words', []):
                self.cards[word] = Card.from_dict(word, self.flashcard_fields_dir / f'{word}.json')
            self.known_words = {}
            for known_word in metadata.get('known_words', []):
                self.known_words[known_word] = Card.from_dict(word, self.flashcard_fields_dir / f'{word}.json')
        else:
            if not (source_lang and native_lang):
                raise RuntimeError('source_lang and native_lang kwargs required when initializing new collection')
            self.source_lang = source_lang
            self.native_lang = native_lang
            self.source_names = []
            self.flashcard_fields = {}
            self.known_sources = {}
            self.cards = {}
            self.known_words = {}

        self.anki_manager = AnkiManager()
        self.reader = Reader(self.source_lang)
        self.scraper = Scraper(self.source_lang, self.native_lang)
        self._available_sources = None
        self.database_unavailable = False
        self.valid_definition_fields = [func.removeprefix('fetch_') for func in
                                fnmatch.filter([func for func in dir(Scraper)
                                                if callable(getattr(Scraper, func))], 'fetch_*')]


    def set_flashcard_fields(self,
                             definitions: List[str] = None,
                             sentence_sources: List[str] = None):
        """
        Tracks categories of sources and
        concrete sources that the user is familiar with.

        Examples
        --------
        collection = Collection('testcollection', source_lang='jp', native_lang='en')
        collection.get_available_sources()
            --> {'anime': ['One Piece', 'Bleach', ...], 'lyrics': {'Eve': [...], ...}, ...}
        # Get Word percentile information in word overview and display example sentences from categories on flashcards
        # Prioritize and highlight familiar sources in particular (Always try to include One piece example sentences if possible)
        # Also include other sources if not enough example sentences are available

        OR

        collection.get_available_sources().keys()
            --> dict_keys(['Netflix', 'anime', 'jpsubbers', 'lyrics', 'misc', 'youtube'])
            --> {'anime': [], 'lyrics': [], 'youtube': [], }
        # Still generates percentile information and displays generic example sentences from categories

        """
        invalid_fields = []
        assert isinstance(definitions, Iterable)
        assert isinstance(sentence_sources, Iterable)
        if definitions:
            for definition in definitions:
                if definition not in self.valid_definition_fields:
                    invalid_fields.append(definition)
        if sentence_sources:
            available_sources = self.get_available_sources()
            if available_sources is None:
                raise RuntimeError('Server currently unavailable, setting sentence sources not possible')
            for sentence_source in sentence_sources:
                if sentence_source not in available_sources.keys():
                    invalid_fields.append(sentence_source)
        if invalid_fields:
            raise RuntimeError(
                f"Some of the specified fields are invalid: {invalid_fields}\n\n"
                f"Valid definition field names (collection.valid_definition_fields):\n"
                f"{self.valid_definition_fields}\n\n"
                f"Valid sentence_source names (collection.get_available_sources()):\n"
                f"{list(available_sources.keys())}"
            )
        self.flashcard_fields['definitions'] = list(definitions) if definitions is not None else []
        self.flashcard_fields['sentence_sources'] = list(sentence_sources) if sentence_sources is not None else []

    @property
    def flashcard_fields_flattened(self):
        fields_flattened = []
        fields_flattened.extend([field for field in self.flashcard_fields['definitions']])
        fields_flattened.extend([f'sentences_{field}' for field in self.flashcard_fields['sentence_sources']])
        return fields_flattened

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
                if all([field in self.cards[word].keys() for field in self.flashcard_fields_flattened])]

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
                    learning_collection_words = set(self.cards.keys()),
                    known_collection_words = set(self.known_words.keys()),
                    sentence_sources = self.flashcard_fields.get('sentence_sources', []))
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

    # TODO: ignores existing sources and overwrites everything for some reason
    def fetch(self,
              deck_name: str,
              flashcard_fields: Iterable[str] = None,
              words: Iterable[str] = None,
              force_update = False):
        """
        Scrape/download data for new cards from sources

        Parameters
        ----------
        deck_name: Name of source to download data for
        flashcard_fields (optional): restrict fields to download data for
        words (optional): restrict words to download data for
        force_update: overwrite existing data

        """
        if not words:
            words = self.cards.keys()
        missing_fields = {}
        source_cards = [card for card in self.cards.values() if card.source_references and list(card.source_references.keys())[0] == deck_name and card.word in words]
        logger.debug(f'Fetching flashcard fields for "{deck_name}"')

        for card in source_cards:
            missing_fields_for_word = [field for field in (flashcard_fields if flashcard_fields else self.flashcard_fields_flattened)
                                         if not field in card.keys() or force_update]
            logger.debug(f'Missing fields for "{card.word}": {missing_fields_for_word}')
            for field in missing_fields_for_word:
                missing_fields.setdefault(field, []).append(card.word)
        if missing_fields:
            print(f'Fetching content for "{field}", {list(missing_fields.keys())}:')
            for field, words in missing_fields.items():
                print(f' - {field}: {words}')

            for i, (field, results) in enumerate(
                self.scraper.download_flashcard_fields(missing_fields,
                                                       known_sources_by_subdomain = self.known_sources).items()):
                for word in missing_fields[field]:
                    if word in results.keys():
                        self.cards[word][field] = results[word]
                    else:
                        self.cards[word][field] = CardSection('empty', 'black', '')
            self.save()

    def sync_with_anki(self, deck_name: str, overwrite = False):
        """
        Sync collection data with anki database.
        Uses AnkiConnect to interface with anki app functionalities via localhost.
        Requires anki to be installed, open and logged in during execution. (see README.md)
        https://apps.ankiweb.net/

        TODO: Currently slow at adding new cards, improve (windows issue)
        """

        # TODO: add "full_overwrite" kwarg, which bulk-removes and readds card instead of updating one by one (faster)
        source_cards = [card for card in self.cards.values() if deck_name in card.source_references.keys()]
        # TODO: sometimes not sorted? See Card.index creation
        source_cards.sort(key=lambda card: (card.index is None, card.index))
        incomplete_cards = {}
        for card in source_cards:
            for field in self.flashcard_fields_flattened:
                if field not in card.keys():
                    incomplete_cards.setdefault(card.word, []).append(field)
        if incomplete_cards:
            raise RuntimeError(f'Some cards are missing data for fields defined in Collection.flashcard_fields, run collection.fetch(<deck_name>) first: {incomplete_cards}')
        if source_cards:
            print('Syncing anki for words', [card.word for card in source_cards])
            self.anki_manager.sync_deck(deck_name, source_cards, self.flashcard_fields_flattened, overwrite=overwrite)
            self.anki_manager.sync()

    def save(self, name = None):
        """
        Write all collection data to local database.

        """
        if not name:
            name = self.name
        if not self.flashcard_fields_dir.exists():
            self.flashcard_fields_dir.mkdir(parents=True, exist_ok=True)
        print(f'saving collection "{name}"')
        metadata = {
            'source_lang': self.source_lang,
            'native_lang': self.native_lang,
            'flashcard_fields': self.flashcard_fields,
            'source_names': self.source_names,
            'card_words': list(self.cards.keys()),
            'known_words': list(self.known_words.keys()),
            'known_sources': self.known_sources
        }
        save_json(self.metadata_path, metadata)

        for word, card in {**self.cards, **self.known_words}.items():
            if card.was_modified:
                json_path = self.flashcard_fields_dir / f'{word}.json'
                save_json(json_path, card.as_dict())
                if not card.json_path:
                    card.json_path = json_path

    def estimate_known_words_for_domain(self, subdomain, level = None):
        word_counts = requests.post(f'{ANKIPAN_DB_ADDR}/api/corpus_wordcounts', json={'lang': self.source_lang, 'subdomains': [subdomain]}).json()
        proficiency_level = level*0.01*len(word_counts[subdomain]) if level else util.estimate_proficiency(word_counts[subdomain])
        items = Counter(word_counts[subdomain]).most_common()[:int(proficiency_level)]
        return self.collect(word_counts = dict(items), is_known = True)

    def get_available_sources(self) -> Dict[str, Dict[str, List[str]]]:
        if self.database_unavailable:
            logger.warning('Previous database connection attempt was unsuccessful, not reconnecting until Collection.database_unavailable is set to False again')
            return
        if self._available_sources is None:
            data = {'lang': self.source_lang}
            try:
                response = requests.post(f'{ANKIPAN_DB_ADDR}/api/available_sources', json=data)
                response.raise_for_status()  # Optional: ensure it's a 200-level response
                self._available_sources = response.json()
            except (requests.exceptions.JSONDecodeError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.HTTPError,
                    requests.exceptions.RequestException) as e:
                logger.error(f'Server to fetch sources not available: {e}')
                self.database_unavailable = True
        return self._available_sources

    def add_custom(self, custom_explanations: Dict[str, CardSection]):
        """
        User method to add arbitrary flashcard fields to collection cards.

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
        instance.cards = {word: Card.from_dict(word, PROJECT_ROOT / name / 'flashcard_fields' / f'{name}.json') for word in card_words}
        instance.known_words = {word: Card.from_dict(word, PROJECT_ROOT / name / 'flashcard_fields' / f'{name}.json') for word in known_words}
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
            'flashcard_fields': self.flashcard_fields,
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
        f'flashcard_fields: {self.flashcard_fields}',
        f'known_sources: {self.known_sources}',
        f'n cards: {len(self.cards)}',
        f'n known_words: {len(self.known_words)}',
        f'n words_with_content: {len(self.words_with_content)}'])

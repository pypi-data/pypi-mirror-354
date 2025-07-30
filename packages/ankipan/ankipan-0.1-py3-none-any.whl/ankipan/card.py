import functools
from jinja2 import Template

from ankipan.scraper import CardSection
from ankipan import HTML_TEMPLATE_DIR, load_json

from typing import Dict, OrderedDict

class Card(OrderedDict):
    def __init__(self,
                 word: str,
                 json_path = None,
                 *,
                 index: int = None,
                 anki_id: int = None,
                 source_references: Dict[str, int] = None):
        """
        Flashcard object.
        Exposes content by inheriting from OrderedDict.
            Key is name of the card section. (e.g. wikitionary or sentences_anime)
            Value is actual content, a CardSection object which contains the downloaded information.
            Values are lazy-loaded from json to prevent a collection with many cards from cluttering memory.

        Parameters
        ----------
        word: Word of the flashcard
        json_path: path to local json path with all sections (saves compute for many cards)
        sources: added sources where this word occurs
        anki_id: optional, filled when card is synced with anki
        source_references: optional, maps source name to number of references
        """
        self.word = word
        self._source_references = source_references if source_references else OrderedDict()
        self._anki_id = anki_id
        self.index = index if index else None
        self.was_modified = False
        self.is_initialized = False
        self.json_path = json_path
        super().__init__({})

    def ensure_initialized(method):
        """
        Lazy loading of card content from json file.

        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.json_path and not self.is_initialized:
                self.is_initialized = True
                card_dict = load_json(self.json_path)
                self._anki_id = card_dict.get('anki_id')
                self._source_references = card_dict.get('source_references', {})
                self.index = card_dict.get('index')

                for name, section in card_dict.get('sections', {}).items():
                    super(Card, self).__setitem__(name,
                                                CardSection.from_dict(section))
            return method(self, *args, **kwargs)
        return wrapper

    @ensure_initialized
    def items(self):
        return super().items()

    @ensure_initialized
    def values(self):
        return super().values()

    @ensure_initialized
    def __getitem__(self, key):
        return super().__getitem__(key)

    @ensure_initialized
    def __setitem__(self, key, value):
        if not self.was_modified:
            self.was_modified = True
        return super().__setitem__(key, value)

    @property
    @ensure_initialized
    def source_references(self):
        return self._source_references

    @source_references.setter
    def source_references(self, value):
        print(f'Modifying sources from {self._source_references} to {value}')
        self._source_references = value
        if not self.was_modified:
            self.was_modified = True

    @property
    @ensure_initialized
    def anki_id(self):
        return self._anki_id

    @anki_id.setter
    def anki_id(self, value):
        print(f'Modifying anki_id from {self._anki_id} to {value}')
        self._anki_id = value
        if not self.was_modified:
            self.was_modified = True

    @property
    @ensure_initialized
    def frequency(self):
        """
        total frequency of word aggregated over all sources
        """
        return sum([freq for freq in self.source_references.values()])

    def generate_front(self):
        return f'<p style="font-size: 30px;">{self.word}</p>'

    @ensure_initialized
    def generate_back(self, section_names):
        """
        Generate flashcard html from downloaded card content sections
        """
        with open(HTML_TEMPLATE_DIR / 'static.html', 'r') as f:
            static = f.read()
        css_files = HTML_TEMPLATE_DIR.glob('*.css')
        css = '\n'.join(css_file.read_text(encoding='utf-8') for css_file in css_files)
        js_files = HTML_TEMPLATE_DIR.glob('*.js')
        js = '\n'.join(js_files.read_text(encoding='utf-8') for js_files in js_files)
        with open(HTML_TEMPLATE_DIR / 'card.html', 'r') as f:
            template = Template(f.read())
        back = template.render(
            static_content=static,
            css_content=css,
            js_content=js,
            card_content='<br>'.join([str(self[section_name]) for section_name in section_names])
        )
        return back

    @staticmethod
    def from_dict(word, json_path):
        """
        Create card object from dict
        Relevant when loading cards from nosql database or for testing
        """
        card = Card(word, json_path)
        return card

    @ensure_initialized
    def as_dict(self):
        """
        Dump card info as dict
        Relevant when storing nosql database and for printing
        """
        return {
            'source_references': self.source_references,
            'sections': {section_name: section.as_dict() for section_name, section in self.items()},
            'anki_id': self.anki_id,
            'index': self.index
        }

    @ensure_initialized
    def __repr__(self):
        return f'word: {self.word}\n' + \
               'frequencies:\n' + \
               '\n'.join([f'    {source_name}: {freq}' for source_name, freq in self.source_references.items()]) + '\n' + \
               'sections: \n' + \
               '\n'.join([f'    {section}' for section in self.keys()]) + '\n' + \
               f'anki_id: {self.anki_id}'

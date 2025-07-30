# Disclaimer: The current scraping methods are only implemented for sources where scraping is not explicitly prohibited.
# The downloaded data is used strictly for educational purposes, and is only stored locally for each individual user who is creating their own flashcards.
# If you are the owner of any of those sources and would like your scraping code removed, please message me and I will do so right away. (daniel.mentock@gmail.com)

import requests
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.notebook import tqdm
import time
import random
import re
import pykakasi
import markdown
import logging

from typing import List, Dict, Union, Iterable, get_args

from ankipan import HTML_TEMPLATE_DIR, ANKIPAN_DB_ADDR

logger = logging.getLogger(__name__)

deeptrans_lang_map = {
    'jp': 'japanese',
    'en': 'english',
    'fr': 'french',
    'de': 'german'
}

google_dict_lang_map = {
    'jp': 'ja',
}

wikitionary_lang_map = {
    'jp': 'ja',
}

ContentNode = Union['HeaderAndContent','Collapsible', 'DictEntries', 'RawHtml']
EnumNode = Union['Enumeration', 'BulletEnumeration', 'BracketedList', 'ConcatenatedSections', 'SpanEnumeration']
ScalarNode = Union['Sentence','Placeholder', 'YoutubeEmbed', 'Wikitionary']
AnyNode = Union[EnumNode, ContentNode, ScalarNode, str]

env = Environment(
    loader=FileSystemLoader(HTML_TEMPLATE_DIR),
    autoescape=select_autoescape(['html']),
)
env.filters['render'] = lambda value: str(value)

# color codes: https://htmlcolorcodes.com/color-names/
class CardSection:
    def __init__(self,
                 display_name: str,
                 color: str,
                 content: AnyNode,
                 url: str = None,
                 is_open = False):
        self.display_name = display_name
        self.color = color
        self.content = content
        self.url = url
        self.is_open = is_open

    def as_dict(self):
        def generate_dict(section_element):
            class_name = section_element.__class__.__name__
            if items:= section_element.items() if isinstance(section_element, dict) else \
                       section_element.__dict__.items() if hasattr(section_element, '__dict__') else None:
                result = OrderedDict()
                for attr, value in items:
                    result[attr] = generate_dict(value)
            elif isinstance(section_element, list) or isinstance(section_element, set):
                result = [generate_dict(item) for item in section_element]
            else:
                result = section_element
            return (class_name, result)
        return generate_dict(self)

    @staticmethod
    def from_dict(data, is_type_description_node = True):
        if is_type_description_node:
            if data[0] in [CardSection.__name__] + \
                          [ref.__forward_arg__ for ref in get_args(EnumNode)] + \
                          [ref.__forward_arg__ for ref in get_args(ContentNode)]+ \
                          [ref.__forward_arg__ for ref in get_args(ScalarNode)]:
                ClassRef = globals()[data[0]]
                return ClassRef(**CardSection.from_dict(data[1], is_type_description_node = False))
            else:
                return CardSection.from_dict(data[1], is_type_description_node = False)
        elif isinstance(data, dict):
            return OrderedDict({key: CardSection.from_dict(val) for key, val in data.items()})
        elif isinstance(data, list):
            return [CardSection.from_dict(item) for item in data]
        else:
            return data

    def __str__(self):
        if str(self.content):
            template = env.get_template('card_section.html')
            return template.render(card_section=self)
        else:
            return ''

    def __bool__(self):
        return bool(self.content)

class HeaderAndContent:
    def __init__(self, header: str,
                 content: AnyNode,
                 header_level: int = None,
                 header_color: str = 'white'):
        self.header = header
        self.content = content
        self.header_level = header_level if header_level else 4
        self.header_color = header_color

    def __str__(self):
        template = env.get_template('header_and_content.html')
        return template.render(header_and_content=self)

    def __bool__(self):
        return bool(self.content)

class Collapsible(HeaderAndContent):
    def __init__(self, header: str,
                 content: AnyNode,
                 header_level: int = None,
                 is_open: bool = False,
                 header_color: str = 'white',
                 summary_size: int = None,
                 summary_as_header = False,
                 summary_color = None,
                 light: bool = False):
        super().__init__(header, content, header_level, header_color)
        self.is_open = is_open
        self.summary_size = summary_size
        self.light = light

    def __str__(self):
        template = env.get_template('collapsible.html')
        return template.render(collapsible=self)

    def __bool__(self):
        return bool(self.content)

class DictEntries:
    def __init__(self,
                 definitions: Dict[str, AnyNode]):
        self.definitions = definitions

    def __str__(self):
        template = env.get_template('dict_entries.html')
        return template.render(dict_entries=self)

    def __bool__(self):
        return bool(self.definitions)

class Enumeration:
    def __init__(self, entries: Iterable[AnyNode]):
        self.entries = entries

    def __str__(self):
        return '\n'.join([f'{str(item)}' for item in self.entries if item])

    def __bool__(self):
        return bool(self.entries)

class SpanEnumeration(Enumeration):
    def __str__(self):
        return '\n'.join([f'<span style="padding: 0; margin: 0;"> {str(item)}</span><br>' for item in self.entries if item])

class BracketedList(Enumeration):
    def __str__(self):
        if self.entries:
            return '(' + ', '.join([f'{str(item)}' for item in self.entries if item]) + ')'
        else:
            return ''

class ConcatenatedSections(Enumeration):
    def __str__(self):
        return ' '.join([f'{str(item)}' for item in self.entries if item])

class CommaSeparatedSections(Enumeration):
    def __str__(self):
        return '; '.join([f'{str(item)}' for item in self.entries if item])

class BulletEnumeration(Enumeration):
    def __str__(self):
        template = env.get_template('bullet_enumeration.html')
        return template.render(bullet_enumeration=self)

class RawHtml():
    def __init__(self, html):
        self.html = html

    def __str__(self):
        return f'<div style="text-align: center !important;">\n{self.html}\n</div>'

    def __bool__(self):
        return True if self.html else False

class Sentence():
    def __init__(self, sentence, word, youtube_hash = None):
        self.sentence = sentence
        self.word = word

    def __str__(self):
        return re.sub(
            rf'(\s*){re.escape(self.word.strip())}(\s*)',
            lambda m: f'{m.group(1)}&#8239;<div style="color:red !important; display:inline;">{html.escape(self.word.strip())}</div>&#8239;{m.group(2)}',
            html.escape(str(self.sentence)))

    def __bool__(self):
        return True if self.sentence and self.word else False

class YoutubeEmbed():
    def __init__(self, youtube_hash, start_s, end_s):
        self.youtube_hash = youtube_hash
        self.start_s = start_s
        self.end_s = end_s

    def __str__(self):
        template = env.get_template('youtube_embed.html')
        return template.render(youtube_embed=self)

    def __bool__(self):
        return True if self.youtube_hash else False

class Wikitionary():
    def __init__(self, content):
        self.content = content

    def __str__(self):
        template = env.get_template('wikitionary.html')
        return template.render(wikitionary=self)

    def __bool__(self):
        return True if self.content else False

class Scraper:
    def __init__(self, source_lang, native_lang):
        self.source_lang = source_lang
        self.native_lang = native_lang
        self.timeout = 25
        self.unsplash_access_key = "6EwImfEiXvVj0QxjzVV16R3hY13ar20I5HPRWg79kgU"
        self.kks = pykakasi.kakasi()

    def fetch_card_sections(self,
                            missing_sections: Dict[str, List[str]],
                            known_sources_by_subdomain: Dict[str, List[str]] = None,
                            save_func=None):
        """
        Called by Collection.fetch to trigger download of contents for this word

        TODO: print available sections

        missing_sections: dict, section_name -> list of lemmas
        scraper: Scraper module passed from collection
            Only one instance is required instead of one for each card
            Especially since it only contains static methods

        """
        logger.debug(f'fetch_card_sections: {missing_sections.keys()}')
        downloaded_sections = {}
        if has_sentences:= any([section_name for section_name in missing_sections.keys() if section_name.startswith('sentences_')]):
            task_id = self.trigger_sentences(
                {'_'.join(section_name.split('_')[1:]): words for section_name, words in missing_sections.items()
                    if section_name.startswith("sentences_")}, known_sources_by_subdomain = known_sources_by_subdomain)

        tasks = []
        for section_name, words in {section_name: words for section_name, words in missing_sections.items()
                                    if not section_name.startswith("sentences_")}.items():
            try:
                func = getattr(self, f'fetch_{section_name}')
            except AttributeError as e:
                raise RuntimeError(f'Section name "{section_name}" not specified in scraper.py module.')

            for word in words:
                tasks.append((section_name, word, func))
        random.shuffle(tasks)
        word_to_future = {}
        downloaded_sections = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            for section_name, word, func in tasks:
                future = executor.submit(func, word)
                word_to_future[(section_name, word)] = future

            for i, ((section_name, word), future) in enumerate(word_to_future.items()):
                for attempt in range(5):
                    try:
                        result = future.result()
                        continue
                    except Exception as e:
                        logger.error(f'Fail to collect section {section_name} for word "{word}": {e}. Waiting before retry...')
                        time.sleep(150)
                if section_name not in downloaded_sections:
                    downloaded_sections[section_name] = {}
                downloaded_sections[section_name][word] = result
                print("finished", section_name, word)
                if not i+1%5 and save_func:
                    print(f"saving ({save_func})")
                    save_func()

        if has_sentences:
            sentences_by_subdomains = self.download_sentences(task_id)
            for subdomain, sentences in sentences_by_subdomains.items():
                downloaded_sections[f'sentences_{subdomain}'] = sentences
        return downloaded_sections

    def trigger_sentences(self,
                          lemmas_by_subdomain: Dict[str, List[str]],
                          known_sources_by_subdomain: Dict[str, List[str]]) -> List[int]:
        available_sources = self.get_available_sources()
        unknown_sources = []
        for subdomain, source_names in known_sources_by_subdomain.items():
            for source_name in source_names:
                if source_name not in available_sources.get(subdomain, {}):
                    unknown_sources.append((subdomain, source_name))
        if unknown_sources:
            raise RuntimeError(f'Invalid known sources in collection: "{unknown_sources}"')
        chunk_size = 5
        task_ids = []
        lemma_chunks = [list(lemmas_by_subdomain.items())[i:i + chunk_size] for i in range(0, len(lemmas_by_subdomain), chunk_size)]
        for lemma_chunk in lemma_chunks:
            data = {'lemmas_by_subdomain': dict(lemma_chunk), 'known_sources_by_subdomain': known_sources_by_subdomain, 'source_lang': self.source_lang, 'native_lang': self.native_lang}
            response = requests.post(f'{ANKIPAN_DB_ADDR}/api/sentences', json=data).json()
            task_ids.append(response['task_id'])
        return task_ids

    def download_sentences(self, task_ids: List[int]):
        def generate_sentences_overview(sentence_overview_by_lemmas):
            results = {}
            for lemma, sentence_overview_sections in sentence_overview_by_lemmas.items():
                sections = []
                for section, overview in sentence_overview_sections.items():
                    sections.append(Collapsible(section, RawHtml(markdown.markdown(overview))))
                results[lemma] =  CardSection(f'Overview', 'Crimson', SpanEnumeration(sections), is_open = True)
            return results
        i = 0
        sentences_by_subdomain = {}
        while task_ids:
            for idx in range(len(task_ids) - 1, -1, -1):
                task_id = task_ids[idx]
                status_url = f'{ANKIPAN_DB_ADDR}/api/sentences/status/{task_id}'
                try:
                    response = requests.get(status_url).json()
                except requests.RequestException as e:
                    raise RuntimeError(f"HTTP request failed: {e}")
                if response['status'] == 'SUCCESS':
                    task_ids.pop(idx)
                    examples_results = {k: v for k, v in response['result'].items() if k!='_overview'}
                    sentences_by_subdomain.update(self.generate_sentences(examples_results))
                    if (sentence_overview_by_lemmas:=response['result'].get('_overview')):
                        sentences_overview = {}
                        for lemma, sentence_overview_sections in sentence_overview_by_lemmas.items():
                            sections = []
                            for section, overview in sentence_overview_sections.items():
                                sections.append(Collapsible(section, RawHtml(markdown.markdown(overview))))
                            sentences_overview[lemma] =  CardSection(f'Overview', 'Crimson', SpanEnumeration(sections), is_open = True)
                        sentences_by_subdomain.setdefault('_overview', {}).update(sentences_overview)

                elif response['status'] == 'FAILURE':
                    raise RuntimeError(f"Task failed: {response['result']}")
            i += 1
            print(f"Waiting for db sentences query to finish, iteration {i}")
            time.sleep(5)
        logger.debug(f'finish download_sentences')
        return sentences_by_subdomain

    def generate_sentences(self, db_result):
        logger.debug(f'generate_sentences: {db_result}')
        sentences_by_subdomain = {}
        for subdomain, sentences_by_lemmas in db_result.items():
            words_and_sentences = {}
            for lemma, known_and_unknown_sentences_by_source in sentences_by_lemmas.items():
                def process_sentences(entries_and_sentences_by_source: Dict[str, Dict[str, List[str]]], subdomain, color='white'):
                    if not entries_and_sentences_by_source: return []
                    rendered_sentences = []
                    for source_name, sentences_by_source_entry in entries_and_sentences_by_source.items():
                        source_sentences = []
                        for source_entry_name, source_entry_sentences in sentences_by_source_entry.items():
                            entry_sentences = []
                            for i, source_entry_sentence in enumerate(source_entry_sentences):
                                sentence_components = []
                                word = source_entry_sentence['word']
                                entries = source_entry_sentence['entries']
                                entries_section = []
                                if subdomain == 'youtube':
                                    try:
                                        start_s = source_entry_sentence['start_s']
                                        end_s = source_entry_sentence['end_s']
                                        entry_title = ' '.join(source_entry_name.split('_')[1:]).replace('-', ' ')
                                        youtube_hash = source_entry_name.split('_')[0]
                                        entries_section.append(YoutubeEmbed(youtube_hash, start_s, end_s))
                                    except:
                                        pass
                                else:
                                    entry_title = source_entry_name.replace('_', ' ').replace('-', ' ')
                                for j, entry in enumerate(entries):
                                    translation = '<To be translated>' if source_entry_sentence['translations'][j] == None else source_entry_sentence['translations'][j]
                                    if self.source_lang=='jp':
                                        translation+='<br>'+self.add_furigana(entry)
                                    logger.debug(f'entry: {entry}')
                                    logger.debug(f'translation: {translation}')
                                    entries_section.append(Collapsible(
                                        Sentence(entry, word), translation, summary_size='14px', light=True))
                                    logger.debug(f'entries_section: {entries_section}')

                                sentence_components.append(Enumeration(entries_section))
                                entry_sentences.append(Collapsible(entry_title, Enumeration(sentence_components), header_level=6, is_open=True, header_color = 'Silver'))
                            source_sentences.append(Enumeration(entry_sentences))
                        rendered_sentences.append(Collapsible(source_name, Enumeration(source_sentences), header_color=color))
                    return rendered_sentences
                parsed_sentences = []
                if known_sources := known_and_unknown_sentences_by_source.get('entries_from_known_sources'):
                    known_sentences = process_sentences(known_sources, subdomain, color = '31EC81')
                    logger.debug(f"known_sources: {known_sources}, {len(known_sentences)}")
                    parsed_sentences.extend(known_sentences)
                if unknown_sources := known_and_unknown_sentences_by_source.get('entries_from_unknown_sources'):
                    extra_sentences = process_sentences(unknown_sources, subdomain)
                    logger.debug(f"unknown_sources: {unknown_sources}, {len(extra_sentences)}")
                    parsed_sentences.extend(extra_sentences)
                words_and_sentences[lemma] = CardSection(subdomain.title(), 'DarkOrange', Enumeration(parsed_sentences),
                                                        is_open = True)
            sentences_by_subdomain[subdomain] = words_and_sentences
        logger.debug(f'finish generate_sentences')
        return sentences_by_subdomain

    def fetch_jisho(self, word: str) -> Dict[str, Dict[str, str]]:
        url="https://jisho.org/search/{}".format(word)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        vstr=requests.get(url, headers=headers, timeout=self.timeout).content
        soup = BeautifulSoup(vstr,features="html.parser",from_encoding='utf8')
        rows = soup.findAll('div', {"class":"concept_light clearfix"})
        jisho = OrderedDict()
        for row in rows:
            furigana = [span.get_text() for span in row.find_all('span', class_='kanji')]
            text_jp_ = row.findAll('span', {"class":"text"})
            text_jp = str(text_jp_).replace('<span class="text">',"").replace("<span>","").replace("</span>","").replace(" ","").replace("[","").replace("]","").replace("\n","").strip()
            text_target_ = row.findAll('span', {"class":"meaning-meaning"})
            text_target = str(text_target_).replace('<span class="meaning-meaning">',"").replace("<span>","").replace("</span>","").replace("[","").replace("]","").replace("\n","").strip()
            if "<span" in text_target:
                text_target = text_target.split("<span")[0]
            if "\n" in text_target:
                text_target = text_target.split("\n")[0]
            if text_jp not in jisho.keys() and furigana and text_jp and text_target:
                jisho[text_jp] = ConcatenatedSections([text_target, BracketedList(furigana)])
        return CardSection('Jisho.org', 'Violet', DictEntries(jisho), url = url)

    def fetch_tatoeba(self, word: str) -> Dict[str, List[str]]:
        lang_mapping = {
            'jp': 'jpn',
            'en': 'eng',
            'de': 'deu',
            'fr': 'fra'
        }
        def fetch(source_lang, native_lang):
            max_pages = 3
            tatoeba=OrderedDict()
            url= f"https://tatoeba.org/eng/sentences/search?from={lang_mapping[self.source_lang]}&query={word}&to={lang_mapping[self.native_lang]}"
            vstr=requests.get(url, timeout=self.timeout).content
            soup = BeautifulSoup(vstr,features="html.parser",from_encoding='utf8')
            paging = soup.find('ul', class_='paging')
            if paging:
                li_tags = paging.find_all('li', {'class': lambda x: x != 'next' and x != 'ellipsis'})
                # Get the text of the last li tag (which will be the last page number)
                last_page = min(int(li_tags[-1].a.get_text()), max_pages)
                # last_page = 2
            else:
                last_page = 1
            for page in range(1, last_page+1):
                if page>1:
                    url= f"https://tatoeba.org/eng/sentences/search?from={lang_mapping[self.source_lang]}&query={word}&to={lang_mapping[self.native_lang]}&page={page}"
                    vstr=requests.get(url, timeout=self.timeout).content
                    soup = BeautifulSoup(vstr,features="html.parser",from_encoding='utf8')
                rows = soup.findAll('div', {"class":"sentence-and-translations"})
                for row in rows:
                    if row:
                        ng_init = row['ng-init']
                        comma_pos = ng_init.find(',')
                        end_bracket_pos = ng_init.rfind(']')
                        json_str = f'[{ng_init[comma_pos+1:end_bracket_pos].strip()}]]'
                        data = json.loads(json_str)
                        example = data[0]['text']
                        translations = []
                        for translation in data[0]['translations']:
                            if translation:
                                translations.append(translation[0]['text'])
                        tatoeba[example] = Enumeration(translations)
            return tatoeba
        examples = fetch(self.source_lang, self.native_lang) if self.native_lang!='en' else OrderedDict()
        examples.update(fetch(self.source_lang, 'en'))


        return CardSection('Tatoeba.org', 'Tomato', DictEntries(examples),
            url = f"https://tatoeba.org/eng/sentences/search?from={lang_mapping[self.source_lang]}&query={word}&to={lang_mapping[self.native_lang]}")

    def fetch_urban(self, word: str) -> List[str]:
        logger.debug(f'fetch_urban: {word}')

        url = f"http://api.urbandictionary.com/v0/define?term={word}"
        response = requests.get(url)
        dictionary = json.loads(response.text)['list']
        definitions = {}
        for definition in dictionary:
            definitions[definition['word']] = {'thumbs': definition['thumbs_up'], 'definition': definition['definition']}

        return CardSection(
            'Urban Dictionary',
            'Violet',
            DictEntries(
                OrderedDict({
                    word: info["definition"] for word, info in sorted(definitions.items(), key=lambda item: item[1]['thumbs'], reverse=True)
            })),
            url = url)

    def fetch_sprachnudel(self, word: str) -> Dict[str, Union[List[str], str]]:
        logger.debug(f'fetch_sprachnudel: {word}')

        url = f'https://www.sprachnudel.de/woerterbuch/{word}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        html_content = requests.get(url, headers=headers, timeout=self.timeout).content
        if 'Hast du dich verirrt?' in str(html_content):
            content = ''
        else:
            soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf8')
            main_meaning = secondary_meaning = examples = ''
            for div in soup.find_all('div'):
                text = div.get_text()
                if 'Hauptbedeutung' in text:
                    main_meaning = text.split('Hauptbedeutung')[1].split('Nebenbedeutung')[0].strip()
                elif 'Bedeutung (Definition)' in text and not main_meaning:
                    main_meaning = text.split('Bedeutung (Definition)')[-1].split('Deine Bedeutung')[0].strip()
                if 'Nebenbedeutung' in text:
                    secondary_meaning = text.split('Nebenbedeutung')[1].split('Assoziative Bedeutungen')[0].strip()
                if 'Beispielsätze' in text:
                    examples = [example.strip() for example in text.split('Beispielsätze')[1].split('Dein Beispielsatz')[0].strip().split('\n') if example.strip()]

            def extract_associative_meanings(soup):
                associative_headings = soup.find_all('h3', text='Assoziative Bedeutungen')
                for heading in associative_headings:
                    next_ul = heading.find_next_sibling('ul')
                    if next_ul:
                        associative_meanings = [li.get_text(strip=True) for li in next_ul.find_all('li')]
                        return associative_meanings
                return []
            content = Enumeration([
                HeaderAndContent('Main Meaning', main_meaning),
                HeaderAndContent('Secondary Meaning', secondary_meaning),
                HeaderAndContent('Examples', BulletEnumeration(examples)),
                HeaderAndContent('Associative Meanings', BulletEnumeration(extract_associative_meanings(soup)))
            ])
        return CardSection('Sprachnudel.de', 'Bisque', content, url = url)

    def fetch_wadoku(self, word):
        url = f'https://www.wadoku.de/search/{word}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        html_content = requests.get(url, headers=headers).content
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', id='resulttable')
        dict_entries = {}
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    japanese_parts = cells[1].find_all('span', class_='orth')
                    japanese_word = ''.join(part.get_text(strip=True) for part in japanese_parts)
                    furigana_parts = cells[1].find_all('span', class_='reading')
                    furigana = ''.join(part.get_text(strip=True) for part in furigana_parts)
                    japanese_formatted = f'{japanese_word} ({furigana})' if furigana else japanese_word
                    german_translation = ''
                    german_translation_section = cells[2].find('div', class_='d')
                    if german_translation_section:
                        german_translation = RawHtml(str(german_translation_section))
                    else:
                        german_translation = RawHtml(str(cells[2]))
                    dict_entries[japanese_formatted] = german_translation
        return CardSection('Wadoku.de', 'Lavender', DictEntries(dict_entries), url=url)

    def fetch_leo(self, word):
        """
        Don't scrape, strict copyright laws here.
        """
        return CardSection('Leo.org', 'Yellow', "Scraping not allowed", url = f'dict.leo.org/german-english/{word}')

    def _fetch_wikitionary(self, lang, word):
        logger.debug(f'fetch_wikitionary: {word}')

        url = f'https://{lang}.m.wiktionary.org/wiki/{word}'
        content = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        html_content = requests.get(url, headers=headers).content
        soup = BeautifulSoup(html_content, 'html.parser')
        if ("Wiktionary does not yet have an entry for mektoub." in soup.text and lang == 'en') or \
           ("ウィクショナリーには現在この名前の項目はありません" in soup.text and lang == 'ja') or \
           ("ne possède pas de page dédiée à cette suite de lettres." in soup.text and lang == 'fr') or \
           ("Dieser Eintrag existiert noch nicht!" in soup.text and lang == 'de'):
            content = ''
        else:
            rows = soup.findAll('div', {"id":"mw-content-text"})
            content = Wikitionary(RawHtml('\n'.join([str(row) for row in rows]).replace('href="/wiki', 'href="https://en.wiktionary.org/wiki')))
        return CardSection(f'{lang}.Wikitionary.org', 'Gray', content, url = url)

    def fetch_wikitionary_en(self, word):
        return self._fetch_wikitionary('en', word)

    def fetch_wikitionary_jp(self, word):
        return self._fetch_wikitionary('ja', word)

    def fetch_wikitionary_fr(self, word):
        return self._fetch_wikitionary('fr', word)

    def fetch_wikitionary_de(self, word):
        return self._fetch_wikitionary('de', word)

    def add_furigana(self, sentence):
        result = []
        for word in self.kks.convert(sentence):
            if word['orig'] != word['hira']:
                result.append(f"{word['orig']} ({word['hira']})")
            else:
                result.append(word['orig'])
        return ''.join(result)

    def translate_google(self, sentences):
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source=google_dict_lang_map.get(self.source_lang, self.source_lang),
                                    target=google_dict_lang_map.get(self.native_lang, self.native_lang))
        translations = translator.translate_batch(sentences)
        return translations

    def translate_mymemory(self, sentences):
        from deep_translator import MyMemoryTranslator
        translator = MyMemoryTranslator(source=deeptrans_lang_map[self.source_lang],
                                        target=deeptrans_lang_map[self.native_lang])
        return translator.translate_batch(sentences)

    def translate_pons(self, word) -> List[str]:
        from deep_translator import PonsTranslator
        translator = PonsTranslator(source=deeptrans_lang_map[self.source_lang],
                                        target=deeptrans_lang_map[self.native_lang])
        return translator.translate(word, return_all=True)

    def translate_linguee(self, word) -> List[str]:
        from deep_translator import LingueeTranslator
        translator = LingueeTranslator(source=deeptrans_lang_map[self.source_lang],
                                        target=deeptrans_lang_map[self.native_lang])
        return translator.translate(word, return_all=True)

    def get_available_sources(self, domain_names: List[str] = None) -> Dict[str, Dict[str, List[str]]]:
        data = {'domain_names': domain_names, 'lang': self.source_lang}
        return requests.post(f'{ANKIPAN_DB_ADDR}/api/available_sources', json=data).json()

    # TODO
    # def _fetch_unsplash(self, english_synonyms, count: int = 10) -> List[str]:
    #     unsplash_image_dir = self.project_dir / 'unsplash'
    #     existing_image_ids = [image.split('.')[0] for image in os.listdir(unsplash_image_dir)]
    #     image_ids = []
    #     if not unsplash_image_dir.exists():
    #         unsplash_image_dir.mkdir(parents=True)
    #     url = "https://api.unsplash.com/search/photos"
    #     #todo: print url of all fetched images/number of opened links etc
    #     for word in english_synonyms:
    #         query = {
    #             "query": word,
    #             "client_id": self.unsplash_access_key,
    #             "per_page": count
    #         }
    #         response = requests.get(url, params=query)
    #         if response.status_code == 200:
    #             results = response.json()['results']
    #             for result in results:
    #                 image_url = result['urls']['regular']
    #                 image_id = f'{word}_{result["id"]}'  # Get the image ID from Unsplash
    #                 if image_id not in existing_image_ids:
    #                     print(f'Downloading image {image_id}')
    #                     image_data = requests.get(image_url).content
    #                     image_path = unsplash_image_dir / f"{image_id}.jpg"
    #                     with open(image_path, 'wb') as file:
    #                         file.write(image_data)
    #                 else:
    #                     print(f'Image {image_id} already dowloaded')
    #                 image_ids.append(image_id)
    #             print(f'Downloaded {len(results)} images for "{word}"')
    #         else:
    #             print(f'Error: {response.status_code} when downloading images to {image_path}')
    #     return image_ids


import re
import pysubs2
import os
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.notebook import tqdm
from pathlib import Path
from typing import Union, Dict, Any, Iterable, List, Optional, Tuple
import pickle
import logging
import chardet
from intervaltree import Interval, IntervalTree
import re
from bs4 import BeautifulSoup
import unicodedata
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from ankipan import PROJECT_ROOT

logger = logging.getLogger(__name__)

hanta_map = {
    'de': 'morphmodel_ger.pgz'
}
_nlp_hanta = None

stanza_map = {
    'jp': 'ja'
}

pattern = re.compile(
    r'[^'
    r'\s'
    r'\u3040-\u309F'  # Hiragana
    r'\u30A0-\u30FF'  # Katakana
    r'\u4E00-\u9FFF'  # Kanji
    r'\u3000-\u303F'  # Japanese punctuation
    r'\uFF10-\uFF19'  # Full-width digits
    r'\uFF21-\uFF3A'  # Full-width uppercase letters
    r'\uFF41-\uFF5A'  # Full-width lowercase letters
    r'a-zA-Z0-9'      # ASCII alphanumerics
    r'.,!?。、！？'    # Common punctuation marks
    r'\u00C0-\u00FF'  # Latin-1 Supplement (e.g., ä, ö, ü, ß, ç, é)
    r'\u0100-\u017F'  # Latin Extended-A (e.g., Œ, œ, Ā, Ă, Ą)
    r']',
)

class Reader():
    def __init__(self, source_lang):
        self.source_lang = source_lang
        self._nlp_stanza = None
        self.corpus_occurrences_ = None
        self.torch_ = None
    @property
    def torch(self):
        if not self.torch_:
            import torch
            self.torch_ = torch
        return self.torch_

    @property
    def nlp_stanza(self):
        if self._nlp_stanza is None:
            import stanza
            stanza_lang_name = stanza_map.get(self.source_lang, self.source_lang)
            try:
                self._nlp_stanza = stanza.Pipeline(stanza_lang_name, download_method=None, processors='tokenize,pos,lemma', use_gpu=True, tokenize_mode='A')
            except (stanza.pipeline.core.LanguageNotDownloadedError, stanza.resources.common.ResourcesFileNotFoundError, FileNotFoundError):
                print(f'Downloading stanza model for {stanza_lang_name}...')
                stanza.download(stanza_lang_name)
                print(f'Stanza model for {stanza_lang_name} downloaded')
                self._nlp_stanza = stanza.Pipeline(stanza_lang_name, download_method=None, processors='tokenize,pos,lemma', use_gpu=True,  **{'tokenize': {'mode': 'A'}})
        return self._nlp_stanza

    @property
    def corpus_occurrences(self):
        if self.corpus_occurrences_ is None:
            try:
                # TODO: Dependency to parent folder not good
                with open(f'{PROJECT_ROOT}/corpus_resources/{self.source_lang}.pkl', "rb") as f:
                    self.corpus_occurrences_ = pickle.load(f)
            except:
                self.corpus_occurrences_ = Counter()
        return self.corpus_occurrences_

    def collect_file_paths(self, path, excluded_files = None, file_match_pattern = None, dir_match_pattern = None):
        compiled_file_pattern = re.compile(file_match_pattern) if file_match_pattern else None
        compiled_dir_pattern = re.compile(dir_match_pattern) if dir_match_pattern else None
        file_paths = set()
        path = Path(path)
        if path.is_file():
            if not excluded_files or Path(path).stem not in excluded_files and compiled_file_pattern.match(Path(path).name):
                file_paths.add(path)
        elif path.is_dir():
            for root, dirs, files in os.walk(path):
                if compiled_dir_pattern:
                    dirs[:] = [d for d in dirs if compiled_dir_pattern.match(d)]
                for filename in files:
                    if not compiled_file_pattern or compiled_file_pattern.match(Path(filename).name):
                        if not excluded_files or Path(filename).stem not in excluded_files:
                            file_paths.add(Path(root, filename))
        else:
            raise RuntimeError(f'Path does not exist: "{path}"')
        return file_paths

    def detect_languages(self, file_contents):
        """
        Currently used to assert integrity of files (only one language used)

        """
        part_length = len(file_contents) // 4
        parts = [file_contents[i * part_length:(i + 1) * part_length] for i in range(4)]

        detected_languages = set()
        for part in parts:
            try:
                lang = detect(part)
                detected_languages.add(lang)
            except LangDetectException:
                continue
        return detected_languages

    def clean_string(self, string, chars_to_filter):
        string = ''.join(
            c for c in string if unicodedata.category(c) not in {'Cc', 'Cf', 'Cs', 'Co', 'Cn', 'Zl', 'Zp'} or c in {'\n'}
        )
        if chars_to_filter:
            for char_to_filter in chars_to_filter:
                replacement = " "
                if isinstance(char_to_filter, tuple):
                    char_to_filter, replacement = char_to_filter
                string = re.sub(char_to_filter, replacement, string)
        string = pattern.sub('', string)
        return string.strip()

    def open_files(self,
                   file_paths: List[Union[str, Path]],
                   replace_chars: List[str] = None,
                   subdomain_name: str = None,
                   assert_coherence: bool = False,
                   index_separators: Iterable[str] = None):

        """
        Extract raw text from list of files.

        Valid formats:
        - Any raw text (.txt etc.)
        - Subtitles (.ass, .srt)
        - Websites (.html)

        Parameters:
        -----------

        file_paths: list of files to process
        replace_chars: List of characters to be removed when processing
        subdomain_name: Allows for special parcing of content on specific websites in parse_html
            Currently only have rule for ['wikipedia']
        assert_coherence: check if files have sentences in more than one language, skip if that is the case.
        index_separators: Custom delimiter to text into small segments.
            Only relevant if we want to create example sentences from this in the db.
            Subtitles are already segmented in small chunks by default.
            If left empty, stanza sentence segementation will be used.

        """
        files = []
        text_indices = None
        sub_indices = None
        processed_words = {} # storing past results
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            encoding_result = chardet.detect(raw_data)
            encoding = encoding_result['encoding']
            if not encoding:
                encoding = 'utf-8'
            try:
                raw_file_contents = raw_data.decode(encoding, errors='replace')
            except LookupError as e:
                logger.error(f'Decode error: {e}')
                continue
            file_contents = None
            if file_path.suffix in ['.ass', '.srt']:
                if index_separators:
                    raise RuntimeError('index_separators not used when parsing subs')
                try:
                    file_contents, text_indices, sub_indices = self.parse_subs(raw_file_contents, replace_chars=replace_chars)
                except Exception as e:
                    print(f'Error: "{file_path}": {type(e).__name__} - {e}')
            else:
                if file_path.suffix in ['.html']:
                    raw_file_contents = self.parse_html(raw_file_contents, subdomain_name = subdomain_name)
                file_contents = self.clean_string(raw_file_contents, replace_chars)

            if file_contents:
                if assert_coherence:
                    langs = self.detect_languages(file_contents)
                    if len(langs)>1:
                        logger.error(f"Skipping file {file_path}, Multiple languages detected: {langs}")
                        continue
                logger.debug(f'appending file {file_path}')
                logger.debug(f'file_contents1: {len(file_contents)}, {file_contents}')
                logger.debug(f'text_indices: {text_indices}')
                logger.debug(f'sub_indices: {sub_indices}')
                files.append(File(self.source_lang,
                                file_contents,
                                processed_words=processed_words,
                                path=file_path,
                                text_indices=text_indices,
                                sub_indices=sub_indices,
                                index_separators=index_separators))
        return sorted(files, key=lambda x: x.path.name)

    def process_files(self, files: List['File'], get_indices=False, n_threads=None, max_retries=3):
        """
        Concurrently extract lemmas from files

        """
        def process_file(file):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    file.analyze_lemmas(self.nlp_stanza, get_indices=get_indices)
                    break
                except self.torch.cuda.OutOfMemoryError as e:
                    logger.error(f"CUDA out of memory error: {e}. Attempt {retry_count + 1} of {max_retries}.")
                    logger.error("file", file.content)
                    self.torch.cuda.empty_cache()
                    break

        with ThreadPoolExecutor(max_workers=n_threads if n_threads else 5) as executor:
            futures = [executor.submit(process_file, file) for file in files]
            progress = tqdm(as_completed(futures), total=len(futures), desc="Extracting lemmas")
            for future in progress:
                future.result()

    def parse_html(self, file_contents: str, subdomain_name = None) -> str:
        """
        Clean html files to extract text (relevant for scraped pages)

        """
        soup = BeautifulSoup(file_contents, 'lxml')
        if subdomain_name == 'wikipedia':
            if soup.find('meta', attrs={'http-equiv': 'Refresh'}):
                return ""
            body_content_div = soup.find('div', id='bodyContent')
            text = ""
            if body_content_div:
                paragraphs = body_content_div.find_all('p')
                for paragraph in paragraphs:
                    text += paragraph.get_text() + "\n"
            clean_text = re.sub(r'\[.*?\]', '', text)
            clean_text = re.sub(r'[^\x00-\x7F]+', '', clean_text)
        else:
            clean_text = soup.get_text()
        return clean_text.strip()

    def parse_subs(self, file_contents: str, replace_chars: List[str] = None) -> str:
        """
        Extract and clean text from sub files

        """
        logger.debug(f'parse_subs: {file_contents}')
        try:
            subs = pysubs2.SSAFile.from_string(file_contents)
        except Exception as e:
            subs = pysubs2.SSAFile.from_string(file_contents, format="srt")
        text_list = []

        # TODO: Currently manually assembled from trial and error with different files, is there an automated way to solve this?
        filter_expressions = {
            'jp': [r'《', r'》',r'（.*?）', r'\[.*\]', r'\{.*?\}', r'\(.*?\)', '\u3000', '\n', '“','”','「', '」', r'\\N', r'\n', r'\n' '…', '→','〉', '〈', '‥', '⁉', r'[\u2460-\u2473]', '‪', '‬', r'\r', r'  '],
            'de': [r'\{.*?\}', '\.', ',', '\!', ';', '\"', "\'", '\?', ('\n', ' '), ':', r'\\N', '%']
        }
        def is_jp_dialogue(text):
            non_dialogue_patterns = [r'---', r'翻译:', r'www.', '字幕組', '翻译', '校对', '后期', '广告', '制作成员']
            if any(re.search(pattern, text) for pattern in non_dialogue_patterns):
                return False
            if re.search(r'[\u3000\u3040-\u30ff\u4e00-\u9fff]+', text):
                return True
            return True
        text_indices = []
        sub_indices = []
        current_index = 0
        for line in subs:
            logger.debug(f'Cleaning line {[line.text]}')
            text = self.clean_string(line.text, filter_expressions.get(self.source_lang, []) + (replace_chars if replace_chars else []))
            logger.debug(f'Cleaned  line: {[text]}')
            if (not self.source_lang=='jp' or is_jp_dialogue(text)) and text:
                start_time = round(line.start / 1000)
                end_time = round(line.end / 1000)
                start_index = current_index
                text_list.append(text)
                end_index = start_index+len(text)
                current_index += len(text) + 1
                text_indices.append((start_index, end_index))
                sub_indices.append((start_time, end_time))
        final_text = ' '.join(text_list).strip()
        logger.debug(f'text_indices: {text_indices}')
        logger.debug(f'sub_indices: {sub_indices}')
        return final_text, text_indices, sub_indices

class File:
    def __init__(self,
                 source_lang,
                 content: List[str],
                 processed_words: Dict[str, str] = None,
                 path = None,
                 text_indices: List[Tuple[int, int]] = None,
                 sub_indices: List[Tuple[int, int]] = None,
                 index_separators: str = None):
        self.source_lang = source_lang
        self.path = path
        self.content = content
        self.processed_words = processed_words if processed_words else {}
        self.text_indices = text_indices
        self.sub_indices = sub_indices # text indices -> time on screen
        self.index_separators = index_separators

        # Variables to be written to when we are adding this source to the main db (TODO: move this from ankipan to ankipan_db)
        self.text_segment_components = OrderedDict() #This has the same keys as sub_indices, but points to a list of (lemma, word)
        self.word_count = Counter()
        self.stanza_segments_by_indices = None

    @property
    def nlp_hanta(self):
        global _nlp_hanta
        if not _nlp_hanta:
            from HanTa import HanoverTagger as ht
            _nlp_hanta = ht.HanoverTagger(hanta_map[self.source_lang]) if self.source_lang in hanta_map.keys() else None
        return _nlp_hanta

    def parse_stanza_segments_by_indices(self, nlp_stanza):
        """
        In-place parsing of self.content into stanza_segments_by_indices

        """

        if self.text_indices and self.index_separators:
            raise RuntimeError(f'index_separators "{self.index_separators}" would override text_indices {self.text_indices}')
        try:
            doc = nlp_stanza(self.content)
            stanza_sentences = doc.sentences
        except Exception as e:
            if len(self.content) > 10000:
                self.content = self.content[:10000]
                print("content", self.content)
            raise e
        if not self.text_indices and self.index_separators:
            indices = []
            separators = '|'.join(map(re.escape, self.index_separators))
            pattern = f"({separators})"
            for sentence in stanza_sentences:
                sentence_start = sentence.tokens[0].start_char
                sentence_end = sentence.tokens[-1].end_char
                sentence_text = self.content[sentence_start:sentence_end]
                segments = re.split(pattern, sentence_text)
                start = sentence_start

                for i in range(len(segments)):
                    trimmed_segment = segments[i].strip()
                    if trimmed_segment:
                        segment_start = self.content.find(trimmed_segment, start)
                        segment_end = segment_start + len(trimmed_segment)
                        indices.append([segment_start, segment_end])
                        start = segment_end
            if indices:
                indices = sorted(indices)
                merged_indices = []
                current_start, current_end = indices[0]
                for start, end in indices[1:]:
                    if start <= current_end:
                        current_end = max(current_end, end)
                    else:
                        merged_indices.append([current_start, current_end])
                        current_start, current_end = start, end
                merged_indices.append([current_start, current_end])
                self.text_indices = merged_indices
        if self.text_indices:
            current_index = 0
            index_tree = IntervalTree(Interval(start, end, []) for start, end in self.text_indices)
            for sentence in stanza_sentences:
                for word in sentence.words:
                    if word.start_char: current_index = word.start_char
                    overlapping_intervals = index_tree[current_index]
                    if overlapping_intervals:
                        first_interval = next(iter(overlapping_intervals))
                        first_interval.data.append(word)
            sorted_intervals = sorted(index_tree, key=lambda interval: interval.begin)
            stanza_segments = OrderedDict(((interval.begin, interval.end), interval.data) for interval in sorted_intervals)
        else:
            stanza_segments = {
                (sentence.tokens[0].start_char, sentence.tokens[-1].end_char):
                [word for word in sentence.words if word.lemma] for sentence in stanza_sentences
            }
        return stanza_segments

    def analyze_lemmas(self, nlp_stanza, get_indices = False):
        """
        In-place parsing of lemmas in self.stanza_segments_by_indices into self.text_segment_components

        """

        self.stanza_segments_by_indices = self.parse_stanza_segments_by_indices(nlp_stanza)
        for text_char_indices, stanza_segment in self.stanza_segments_by_indices.items():
            metadata = []
            # TODO: collect words in list first, then fetch available lemmas from db
            for i, stanza_token in enumerate(stanza_segment):
                word = stanza_token.text
                if word in self.processed_words:
                    self.word_count[self.processed_words[word]] = self.word_count.get(self.processed_words[word], 0) + 1
                    if get_indices:
                        metadata.append({
                            'word': word,
                            'lemma': self.processed_words[word]})
                else:
                    lemma = None

                    if self.source_lang=='jp':
                        if stanza_token.lemma and re.search(r'[\u4E00-\u9FD0]+', stanza_token.lemma) and re.search(r'[\u4E00-\u9FD0]+', stanza_token.text):
                            lemma = stanza_token.lemma
                    elif stanza_token.pos in ["NOUN", "VERB", "ADJ", "ADV", "AUX", "PROPN"] and stanza_token.xpos != 'NE' and stanza_token.lemma and stanza_token.lemma.isalpha():
                        if self.source_lang=='de':
                            try:
                                hanta_lemmas = self.nlp_hanta.tag_sent([token.text for token in stanza_segment])
                                hanta_lemma = hanta_lemmas[i] if i < len(hanta_lemmas)-1 and hanta_lemmas[i][0] == stanza_token.text else \
                                            self.nlp_hanta.tag_sent([stanza_token.text])[0]
                                lemma = hanta_lemma[1] if len(hanta_lemma)>=3 else stanza_token.lemma
                            except IndexError as e:
                                print(f"Hanta Error: {e}")
                                lemma = stanza_token.lemma
                        else:
                            lemma = stanza_token.lemma
                    if lemma:
                        self.word_count[lemma] = self.word_count.get(lemma, 0) + 1
                        if get_indices:
                            metadata.append({
                                'word': word,
                                'lemma': lemma,
                                })
                        if stanza_token.text not in self.processed_words:
                            self.processed_words[stanza_token.text] = lemma
                # print("====================================================")
                # print("stanza_token.lemma",stanza_token.lemma)
                # print("stanza_token.text",stanza_token.text)
                # print("stanza_token.pos",stanza_token.pos)
                # print("stanza_token.xpos",stanza_token.xpos)
                # print("hanta_lemma",hanta_lemma)
            if get_indices:
                self.text_segment_components[text_char_indices] = metadata

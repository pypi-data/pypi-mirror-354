from collections import OrderedDict, Counter
from pathlib import Path
import time
import requests
from typing import Iterable, Dict, Union
import logging

from ankipan import Reader, Scraper, File, ANKIPAN_DB_ADDR

logger = logging.getLogger(__name__)

class Deck:
    def __init__(self,
                 source_lang: str,
                 native_lang: str,
                 section_names = None,
                 source_words = None,
                 learning_collection_words: set = None,
                 known_collection_words: set = None,
                 known_collection_sources: set = None):
        self.source_lang = source_lang
        self.section_names = section_names if section_names else ['dict']
        self.reader = Reader(source_lang)
        self.scraper = Scraper(source_lang, native_lang)
        self.source_words = source_words if source_words else Counter()
        self.ignored_words = set()
        self.learning_collection_words = learning_collection_words if learning_collection_words else set()
        self.known_collection_words = known_collection_words if known_collection_words else set()
        self.skip_words = set()
        self.percentiles = {}
        self.scraped_definitions = {}
        self.known_collection_sources = list(known_collection_sources) if known_collection_sources else []
        self._word_percentiles = None
        self._sorted_words = None
        self._domain_occurrences = None

    @property
    def all_words(self):
        return {word for word in self.source_words}

    @property
    def new_words(self):
        return Counter({word: count for word, count in self.source_words.items() if word not in self.learning_collection_words and word not in self.known_collection_words and word not in self.ignored_words and word not in self.skip_words})

    @property
    def learning_words(self):
        """Get words that are already being learned in collection"""
        return Counter({word: count for word, count in self.source_words.items() if word in self.learning_collection_words})

    @property
    def known_words(self):
        """Get words that are already specified as known word in collection"""
        return Counter({word: count for word, count in self.source_words.items() if word in self.known_collection_words})

    @property
    def domain_occurrences(self):
        if self._domain_occurrences is None:
            try:
                self._domain_occurrences = requests.post(f'{ANKIPAN_DB_ADDR}/api/corpus_wordcounts',
                                                         json={'lang': self.source_lang,
                                                               'words': list(self.source_words.keys()),
                                                               'subdomains': self.known_collection_sources}).json()
            except:
                logger.error('Unable to reach remote server, not fetching domain occurrences')
                return {}
        return self._domain_occurrences

    @property
    def word_percentiles(self):
        if not self._word_percentiles:
            domains = {'source': self.source_words} | self.domain_occurrences
            self._word_percentiles = self.calculate_percentiles(self.new_words.keys(), domains)
        return self._word_percentiles

    @property
    def sorted_words(self):
        # TODO: does not yet account for when words are literally added or removed
        if not self._sorted_words:
            min_percentiles = {
                word: self.word_percentiles[word].get('source', 1) for word in self.word_percentiles
            }
            self._sorted_words = sorted(min_percentiles.keys(), key=lambda w: min_percentiles[w])
        return self._sorted_words

    def select_new_words(self, n_words=None):
        """
        Displays words in an ipysheet 'spreadsheet'. Each row has 'Skip', 'Known',
        'Word', and dynamically generated percentile columns.
        """
        import ipysheet
        from ipysheet import sheet, column, cell
        from ipywidgets import Button, VBox, Layout
        from IPython.display import display
        from IPython import get_ipython
        from functools import partial
        import ipywidgets as widgets

        if not get_ipython():
            raise NotImplementedError("Spreadsheet UI only available in Jupyter.")
        words_to_show = self.sorted_words if n_words is None else self.sorted_words[:n_words]
        all_domains   = sorted({d for v in self.word_percentiles.values() for d in v})

        n_rows = len(words_to_show)
        s      = sheet(rows=n_rows, columns=3 + len(all_domains))
        s.column_headers = ["Skip", "Known", "Word"] + all_domains

        col_sel   = column(0, [False]*n_rows, type="checkbox", label="Skip",  sheet=s)
        col_known = column(1, [False]*n_rows, type="checkbox", label="Known", sheet=s)
        col_word  = column(2, words_to_show,  type="text",     label="Word",  sheet=s)

        def bg(val: float | None) -> str:
            if val is None:
                return "#ffffff"
            if val < 0.10:
                return "#c6f7c6"
            if val < 0.25:
                return "#fff7b5"
            return "#f7c6c6"
        for col_idx, domain in enumerate(all_domains, start=3):
            for row_idx, word in enumerate(words_to_show):
                val = self.word_percentiles.get(word, {}).get(domain)
                txt = "" if val is None else f"{val:.4f}"
                ipysheet.cell(
                    row=row_idx,
                    column=col_idx,
                    value=txt,
                    sheet=s,
                    type="text",
                    background_color=bg(val),
                    layout=Layout(width="70px")
                )

        btn  = widgets.Button(description="Set unknown words")
        out  = widgets.Output()
        def on_click(b):
            with out:
                out.clear_output()
                err_mask   = col_sel.value
                known_mask = col_known.value
                words      = col_word.value
                skip_words  = [w for w, m in zip(words, err_mask)   if m]
                known      = [w for w, m in zip(words, known_mask) if m]
                unknown = set(self.source_words) - set(skip_words) - set(known)
                self.set_new_words(unknown, skip_words)
                print("✅ Skip Words:", skip_words[:10], "...")
                print("✅ Known    :", known[:10], "...")
                print("➡️ New  :", sorted(unknown)[:10], "...")
        btn.on_click(on_click)
        display(widgets.VBox([s, btn, out]))

    def set_new_words(self, new_words: Iterable, skip_words, ignore_unknown=False):
        for word in self.source_words.keys():
            if word in new_words:
                self.known_collection_words.discard(word)
                self.learning_collection_words.discard(word)
            elif word in skip_words:
                self.skip_words.add(word)
            elif word not in self.known_collection_words and word not in self.learning_collection_words:
                self.known_collection_words.add(word)
        for word in new_words:
            if word not in self.all_words:
                print(f'Warning: word {word} not in source words, ' +
                      f'{"ignoring" if ignore_unknown else "adding with occurrence 1"}')
                if not ignore_unknown:
                    self.source_words[word] = 1

    def set_ignored_words(self, ignored_words: Iterable):
        for word in ignored_words:
            self.ignored_words.add(word)
            if word in self.known_collection_words:
                self.known_collection_words.remove(word)
            if word in self.learning_collection_words:
                self.learning_collection_words.remove(word)

    def calculate_percentiles(self, words: Iterable[str], domains: OrderedDict[str, Counter]) -> Dict[str, Dict[str, float]]:
        if not hasattr(self, 'percentiles'):
            self.percentiles = {}
        percentiles = {word: {} for word in words}
        for word in words:
            if word not in self.percentiles:
                for domain_name, word_count_dict in domains.items():
                    counter = Counter(word_count_dict)
                    if word in counter:
                        common = [word for word, count in counter.most_common()]
                        percentile = common.index(word) / len(counter) if counter[word] != 1 else 1.0
                        percentiles[word][domain_name] = percentile
                    else:
                        percentiles[word][domain_name] = None
                self.percentiles[word] = percentiles[word]
            else:
                percentiles[word] = self.percentiles[word]
        return percentiles

    def __repr__(self):
        return str(self)

    def __str__(self):
        if not any([self.new_words, self.learning_words, self.known_words]):
            return 'No words in collection'
        categories = [f'New Words ({len(self.new_words)})',
                      f'Learning Words ({len(self.learning_words)})',
                      f'Known Words ({len(self.known_words)})']
        domains = {'source': self.source_words} | self.domain_occurrences
        lines = []
        col_widths = [max(len(domain_name) + 8, 10) for domain_name in domains]  # Adjust width for "source" and "global"
        word_width = max(14, max(len(word) for category in [self.new_words, self.learning_words, self.known_words] for word in category.keys()) + 2)
        header_line = ' '.join(['word'.ljust(word_width)] + [f"{header}".ljust(width) for header, width in zip(domains.keys(), col_widths)])
        lines.append(' | '.join([f'{category:<{sum(col_widths) + word_width + 2}}' for category in categories]))
        lines.append("_" * (sum(col_widths) + word_width + 3 * len(categories) + 2 * (len(categories)-1)))
        lines.append(' | '.join([f'{header_line:<{sum(col_widths) + word_width + 2}}' for _ in categories]))
        lines.append('')
        data = {}
        for category, counter in zip(categories, [self.new_words, self.learning_words, self.known_words]):
            # TODO replace with properties
            categorypercentiles = self.calculate_percentiles(counter.keys(), domains)
            sorted_words = sorted(categorypercentiles.keys(), key=lambda word: categorypercentiles[word].get('source', float('inf')))
            data[category] = {word: categorypercentiles[word] for word in sorted_words}
        max_length = max(len(data[category]) for category in data)
        for i in range(max_length):
            row_parts = []
            for category in categories:
                words = list(data[category].keys())
                if i < len(words):
                    word = words[i]
                    row = word.ljust(word_width)
                    for domain_name in domains:
                        percentile = data[category][word].get(domain_name)
                        if percentile is None:
                            text = "N/A"
                        elif percentile == 1.0:
                            text = "100.00%"
                        else:
                            text = "{:.2%}".format(percentile)
                        row += text.ljust(col_widths[list(domains.keys()).index(domain_name)])
                else:
                    row = " " * word_width
                row_parts.append(f'{row:<{sum(col_widths) + word_width + 2}}')
            lines.append(" | ".join(row_parts))
        return "\n".join(lines)

    def add(self,
            path: Union[str, Path] = None,
            *,
            string: str = None,
            word_counts: Union[Dict[str, int], Counter] = None):
        """
        Add words from file(s) to word collection

        Parameters
        ----------
        path: path to file(s)
        string (optional): parse string instead of file, only valid if no file is specified

        """
        if path and string:
            raise RuntimeError('Please only supply either a path or a string.')
        elif word_counts is not None:
            if not (isinstance(word_counts, dict) or isinstance(words, Counter)):
                raise RuntimeError(f'Deck requires Dict- or Counter like datastructure to update, received {type(word_counts)}:\n  {word_counts}')
        else:
            if string is not None:
                files = [File(self.source_lang, string,)]
            else:
                file_paths = self.reader.collect_file_paths(path)
                files = self.reader.open_files(file_paths)
            self.reader.process_files(files)
            word_counts = Counter()
            for file in files:
                word_counts.update(file.word_count)
        self.source_words.update(word_counts)

    def remove(self, words: Union[str, Iterable]):
        """
        Remove words from word collection

        Parameters
        ----------
        words: words to remove

        """
        if isinstance(words, str):
            words = [words]
        elif not (isinstance(words, list) or isinstance(words, set)):
            raise RuntimeError('Only string or list allowed in collection.remove command')
        for word in words:
            if word not in self.source_words: raise RuntimeError(f'Word "{word}" is not part of this wordcollection, abort.')
        [self.source_words.pop(word) for word in words]

    def remove_range(self, lower: int, upper: int):
        self.remove([word for word, count in self.source_words.items() if count >= lower and count < upper])

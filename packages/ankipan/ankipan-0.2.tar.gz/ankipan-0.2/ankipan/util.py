import numpy as np
from collections import Counter
import pickle
from ankipan import PROJECT_ROOT
from pathlib import Path
from collections import Counter
import json

from typing import Any

def load_json(path: Path) -> dict[str, Any]:
    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    else:
        return {}

def save_json(path: Path, obj: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)

def estimate_proficiency(word_counter: Counter, simulated_responses=None):
    """
    Very minimal method to estimate a user's initial proficiency level:
    Pick large corpus, sort by frequency, assume that less frequent words are less likely to be known.
    Query for words of different frequency, estimate ballpark interval of proficiency level.

    Returns
    -------

    A list of words that the use is likely to already know, alongside the percentile value

    """
    # TODO: Currently, we just create a zipf curve from our corpus, and estimating where a reasonable cut off index could be.
    # A more sophisticated method would detect areas the user is knowledgeable at, and areas where he/she is lacking.

    words = list(word_counter.keys())
    frequencies = list(word_counter.values())

    # Sort words by frequency (most frequent to least frequent)
    sorted_indices = np.argsort(frequencies)[::-1]
    sorted_words = [words[i] for i in sorted_indices]

    # Create a dictionary for fast index lookup
    word_to_index = {word: idx for idx, word in enumerate(words)}

    def initialize_probabilities(words):
        probabilities = np.ones(len(words)) / len(words)
        return probabilities

    def update_probabilities(words, probabilities, group, response):
        indices = [word_to_index[word] for word in group]
        known = np.array(response)

        for i, word in enumerate(group):
            index = indices[i]
            if known[i]:
                probabilities[index] *= 1.5
            else:
                probabilities[index] *= 0.7

        probabilities /= np.sum(probabilities)
        return probabilities

    def estimate_level(probabilities):
        cumulative = np.cumsum(probabilities)
        level = np.argmax(cumulative >= 0.5)
        return level

    def select_words(percentiles, words, words_per_question):
        selected_words = []
        for percentile in percentiles:
            start_idx = max(0, int(percentile * len(words) / 100))
            end_idx = min(len(words), start_idx + max(1, len(words) // 100))
            if end_idx > start_idx:
                selected_words.extend(np.random.choice(words[start_idx:end_idx], 1, replace=False))
        return selected_words[:words_per_question]

    initial_percentiles = [20, 40, 60, 80]
    probabilities = initialize_probabilities(words)
    num_questions = 5
    words_per_question = 5

    for question_num in range(num_questions):
        group = select_words(initial_percentiles, sorted_words, words_per_question)
        group.sort()
        percentiles = [
            (sorted_words.index(word) / len(words)) * 100
            for word in group
        ]
        if simulated_responses:
            response = simulated_responses[question_num]
        else:
            response = input(f"{list(zip(group, percentiles))} Do you know these words? Enter 'y' or 'n' for each, separated by space: ").split()
            if len(response) != words_per_question or any(r not in ['y', 'n'] for r in response):
                print(f"Please enter exactly {words_per_question} y/n responses.")
                continue

        response = [r.lower() == 'y' for r in response]
        probabilities = update_probabilities(words, probabilities, group, response)

        if all(response):
            initial_percentiles = [min(p + 10, 100) for p in initial_percentiles]  # Move to harder words
        elif not any(response):
            initial_percentiles = [max(p - 10, 0) for p in initial_percentiles]  # Move to easier words
        else:
            lower_bound = min(p for p, r in zip(percentiles, response) if r)
            upper_bound = max(p for p, r in zip(percentiles, response) if r)
            mid_point = (lower_bound + upper_bound) / 2
            initial_percentiles = [max(mid_point - 10, 0), mid_point, min(mid_point + 10, 100)]

    estimated_level = estimate_level(probabilities) / 3
    percentile = estimated_level / len(words) * 100
    return estimated_level, percentile

if __name__ == "__main__":
    with open(f'{PROJECT_ROOT}/corpus_resources/de.pkl', "rb") as f:
        corpus_occurrences_ = pickle.load(f)
    estimate_proficiency(corpus_occurrences_)

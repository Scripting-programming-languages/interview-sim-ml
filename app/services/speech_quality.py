import re
from collections import Counter

def filler_score(num_fillers, total_words):
    if total_words == 0:
        return 0

    ratio = num_fillers / total_words

    if ratio < 0.02:
        return 1
    elif ratio < 0.1:
        return 0.8
    elif ratio < 0.2:
        return 0.6
    else:
        return 0.3


def pause_score(num_pauses, total_words):
    if total_words == 0:
        return 0

    ratio = num_pauses / total_words

    if ratio < 0.05:
        return 1
    elif ratio < 0.1:
        return 0.8
    elif ratio < 0.2:
        return 0.6
    else:
        return 0.3


def speed_score(total_words, duration):
    if duration == 0:
        return 0

    wpm = total_words / duration * 60

    if 120 <= wpm <= 160:
        return 1
    elif 100 <= wpm < 120 or 160 < wpm <= 180:
        return 0.8
    elif 80 <= wpm < 100 or 180 < wpm <= 200:
        return 0.6
    else:
        return 0.4


def vocabulary_score(words):
    if not words:
        return 0

    unique_words = len(set(words))
    ratio = unique_words / len(words)

    if ratio > 0.8:
        return 1
    elif ratio > 0.7:
        return 0.8
    elif ratio > 0.5:
        return 0.6
    else:
        return 0.4


def repetition_score(words):
    if not words:
        return 0

    counts = Counter(words)
    most_common = counts.most_common(1)[0][1]

    ratio = most_common / len(words)

    if ratio < 0.1:
        return 1
    elif ratio < 0.2:
        return 0.8
    elif ratio < 0.3:
        return 0.6
    else:
        return 0.4


def speech_quality_score(words, fillers, pauses, duration):

    total_words = len(words)

    f_score = filler_score(len(fillers), total_words)
    p_score = pause_score(len(pauses), total_words)
    s_score = speed_score(total_words, duration)
    v_score = vocabulary_score(words)
    r_score = repetition_score(words)

    final = (
        0.30 * f_score +
        0.25 * p_score +
        0.20 * s_score +
        0.15 * v_score +
        0.10 * r_score
    )

    percent = round(final * 100, 0)

    return percent
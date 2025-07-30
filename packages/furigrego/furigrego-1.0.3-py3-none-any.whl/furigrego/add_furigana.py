from typing import Tuple, Generator
from os.path import commonprefix

from fugashi import Tagger  # Morphological analyzer using MeCab
from furigrego.converter import kata2hira  # Convert katakana to hiragana
from furigrego.checking import (
    is_unknown,
    is_kana_only,
    is_kanji_only,
    is_latin_only,
    is_hira,
    is_kanji,
)

# Initialisation du tagger MeCab pour l’analyse morphologique du texte
tagger = Tagger()  # type: ignore


def add_furigana(sentence: str) -> Generator[str, None, None]:
    """
    Traite une phrase complète, en conservant les espaces.
    Divise d'abord par espace, traite chaque fragment individuellement avec furigana.
    """
    sub_sentences = sentence.split(" ")  # Découper par espaces
    last_index = len(sub_sentences) - 1

    for i, sub_sentence in enumerate(sub_sentences):
        yield from add_furigana_text(sub_sentence)  # Ajoute les furigana au fragment
        if i < last_index:
            yield " "  # Réinsère les espaces


def add_furigana_text(text: str) -> Generator[str, None, None]:
    """
    Analyse morphologiquement un fragment de texte.
    Pour chaque mot identifié par MeCab, applique add_furigana_word.
    """
    for morpheme in tagger(text):  # type: ignore
        yield add_furigana_word(morpheme.surface, morpheme.feature.kana)  # type: ignore


def add_furigana_word(surface: str, kata: str | None) -> str:
    if kata is None:
        return surface  # Pas de lecture : retourne le mot original

    hira = kata2hira(kata)

    if is_unknown(surface, kata):
        return surface  # Ne traite pas les mots inconnus

    if is_kana_only(surface):
        return surface  # Pas besoin de furigana pour les mots uniquement en kana

    if is_kanji_only(surface):
        return ruby_wrap(surface, hira)  # Furigana complet pour les kanji seuls

    if is_latin_only(surface):
        return surface  # Ne traite pas l'alphabet latin

    # Traitement des mots mélangés (kanji + kana)
    (prefix, (mid_text, mid_hira), suffix) = cut_by_hira(surface, hira)

    if is_kanji_only(mid_text):
        return f"{prefix}{ruby_wrap(mid_text, mid_hira)}{suffix}"

    try:
        # Essaye de découper les composés complexes
        return f"{prefix}{add_furigana_compound(mid_text, mid_hira)}{suffix}"
    except:
        # Cas spéciaux, anciens mots ou irréguliers
        return ruby_wrap(surface, hira)


def add_furigana_compound(surface: str, hira: str) -> str:
    """
    Applique les furigana à un mot composé complexe en identifiant les parties déjà en hiragana.
    Exemple : 思い出した → 思<rt>おも</rt>い出<rt>だ</rt>した
    """
    hira_in_surface_reversed = ""

    # Recherche des hiragana dans la fin du mot pour faire la séparation
    for char in surface[::-1]:
        if is_hira(char):
            hira_in_surface_reversed += char
        if is_kanji(char) and hira_in_surface_reversed:
            break

    if not hira_in_surface_reversed:
        return ruby_wrap(surface, hira)

    # Trouve la position du segment hiragana
    hira_in_surface = hira_in_surface_reversed[::-1]
    hira_index_in_surface, hira_index_in_hira = (
        surface.rindex(hira_in_surface),
        hira.rindex(hira_in_surface),
    )

    # Découpe à gauche et à droite du segment hiragana
    left_surface, left_hira = surface[:hira_index_in_surface], hira[:hira_index_in_hira]
    right_surface, right_hira = (
        surface[hira_index_in_surface + len(hira_in_surface):],
        hira[hira_index_in_hira + len(hira_in_surface):],
    )

    # Appel récursif sur chaque partie
    return (
        add_furigana_compound(left_surface, left_hira)
        + hira_in_surface
        + ruby_wrap(right_surface, right_hira)
    )


def ruby_wrap(kanji: str, hira: str) -> str:
    """
    Enveloppe le kanji avec la balise HTML <ruby> pour ajouter les furigana.
    """
    return f"<ruby>{kanji}<rt>{hira}</rt></ruby>"


def cut_by_hira(surface: str, hira: str) -> Tuple[str, Tuple[str, str], str]:
    """
    Identifie les préfixes et suffixes communs entre la forme du mot et sa lecture,
    pour isoler la partie centrale à traiter.
    """
    prefix = find_common_prefix(surface, hira)
    suffix = find_common_suffix(surface, hira)

    middle = (
        surface.removeprefix(prefix).removesuffix(suffix),
        hira.removeprefix(prefix).removesuffix(suffix),
    )

    return (prefix, middle, suffix)


def find_common_prefix(str1: str, str2: str) -> str:
    """
    Retourne le préfixe commun entre deux chaînes.
    """
    return commonprefix((str1, str2))


def find_common_suffix(str1: str, str2: str) -> str:
    """
    Retourne le suffixe commun entre deux chaînes (en comparant les chaînes inversées).
    """
    return commonprefix((str1[::-1], str2[::-1]))[::-1]

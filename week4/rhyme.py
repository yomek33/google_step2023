import pykakasi

kks = pykakasi.kakasi()

def is_rhyme(word1, word2):
    if not is_japanese(word1) or not is_japanese(word2):
        return False
    if abs(len(word1) - len(word2)) > 2:
        return False
    word1 = kks.convert(word1)[0]['hira']
    word2 = kks.convert(word2)[0]['hira']
    
    word1_vowels = hiragana_to_vowels(remove_characters(word1))
    word2_vowels = hiragana_to_vowels(remove_characters(word2))
    if len(word1_vowels) < len(word2_vowels):
        word1_vowels, word2_vowels = word2_vowels, word1_vowels

    return word1_vowels == word2_vowels

def is_japanese(s):
    return all(ord(c) > 123 or ord(c) < 65 for c in s)

def hiragana_to_vowels(word):
    hiragana_vowels = {
        'あ': 'あ', 'い': 'い', 'う': 'う', 'え': 'え', 'お': 'お',
        'か': 'あ', 'き': 'い', 'く': 'う', 'け': 'え', 'こ': 'お',
        'さ': 'あ', 'し': 'い', 'す': 'う', 'せ': 'え', 'そ': 'お',
        'た': 'あ', 'ち': 'い', 'つ': 'う', 'て': 'え', 'と': 'お',
        'な': 'あ', 'に': 'い', 'ぬ': 'う', 'ね': 'え', 'の': 'お',
        'は': 'あ', 'ひ': 'い', 'ふ': 'う', 'へ': 'え', 'ほ': 'お',
        'ま': 'あ', 'み': 'い', 'む': 'う', 'め': 'え', 'も': 'お',
        'や': 'あ', 'ゆ': 'う', 'よ': 'お',
        'ら': 'あ', 'り': 'い', 'る': 'う', 'れ': 'え', 'ろ': 'お',
        'わ': 'あ', 'を': 'お',
        'が': 'あ', 'ぎ': 'い', 'ぐ': 'う', 'げ': 'え', 'ご': 'お',
        'ざ': 'あ', 'じ': 'い', 'ず': 'う', 'ぜ': 'え', 'ぞ': 'お',
        'だ': 'あ', 'ぢ': 'い', 'づ': 'う', 'で': 'え', 'ど': 'お',
        'ば': 'あ', 'び': 'い', 'ぶ': 'う', 'べ': 'え', 'ぼ': 'お',
        'ぱ': 'あ', 'ぴ': 'い', 'ぷ': 'う', 'ぺ': 'え', 'ぽ': 'お',
    }

    small_hiragana_vowels = {
        'ゃ': 'あ', 'ゅ': 'う', 'ょ': 'お'
    }

    result = ""
    for i, char in enumerate(word):
        if char in small_hiragana_vowels:
            result = result[:-1] + small_hiragana_vowels[char]
        elif char in hiragana_vowels:
            result += hiragana_vowels[char]

    return result





def remove_characters(word):
    word = word.replace('ん', '')
    word = word.replace('っ', '')
    word = word.replace('ー', '')
    word = word.replace('ゎ', '')
    return word




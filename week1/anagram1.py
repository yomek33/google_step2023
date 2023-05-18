import collections

def find_anagram_upgraded(S):
    with open('anagram/words.txt') as f:
        dictionary = [s.strip().lower() for s in f.readlines()]

    S_count = collections.Counter(S.lower())
    anagram_list = []

    for word in dictionary:
        word_count = collections.Counter(word)
        if all(word_count[k] <= S_count[k] for k in word_count) and all(S_count[k] <= word_count[k] for k in S_count):
            anagram_list.append(word)

    return anagram_list

if __name__ == '__main__':
    S = input().lower()
    ans_list = find_anagram_upgraded(S)

    if len(ans_list) == 0:
        print('There is no anagram')
    else:
        for word in ans_list:
            print(word)

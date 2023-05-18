import sys
import collections

def find_anagram(random_words, dictionary):
    sorted_random_words = [collections.Counter(x) for x in random_words]
    new_dictionary = [[collections.Counter(word), word] for word in dictionary]
    new_dictionary.sort(key=lambda x: score_counter(x[1]))
    anagram = [get_anagram(x, new_dictionary) for x in sorted_random_words]
    
    return anagram

def binary_search(sorted_random_word, new_dictionary):
    left = 0
    right = len(new_dictionary) - 1
    answer = []

    while right >= left:
        middle = (right + left) // 2
        if sorted_random_word < new_dictionary[middle][0]:
            right = middle - 1
        elif sorted_random_word > new_dictionary[middle][0]:
            left = middle + 1
        else:
            for i in range(middle, -1, -1):
                if sorted_random_word == new_dictionary[i][0]:
                    answer.append(new_dictionary[i][1])
                else:
                    break
            for i in range(middle + 1, len(new_dictionary)):
                if sorted_random_word == new_dictionary[i][0]:
                    answer.append(new_dictionary[i][1])
                else:
                    break
            break
    return answer

def get_anagram(word, dictionary):
    for i in range(len(dictionary) - 1, 0, -1):
        if word == dictionary[i][0]:
            return dictionary[i][1]
    return ""

def score_counter(word):
    points = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    return sum(points[ord(x) - ord('a')] for x in word)

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as a_file:
        return [line.strip().split()[0] for line in a_file]

def write_anagram(list_of_anagram):
    if not list_of_anagram:
        print('no anagrams')
    else:
        with open('output.txt', 'w', encoding='utf-8') as a_file:
            a_file.write('\n'.join(str(anagram) for anagram in list_of_anagram))

def main(dict_file, data_file):
    dictionary = read_file(dict_file)
    random_words = read_file(data_file)
    answer = find_anagram(random_words, dictionary)
    write_anagram(answer)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: %s dict_file data_file" % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

import sys
import collections
from collections import deque
from rhyme import is_rhyme
class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        

        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        #スタートノードをキューに追加し、キューが空になるまでのwhileループ
        title_to_id = {v: k for k, v in self.titles.items()}
        start_id = title_to_id.get(start)
        goal_id = title_to_id.get(goal)

        if start_id is None or goal_id is None:
            print("Start or goal page not found.")
            return None
        queue = deque([(start_id, [start_id])]) 
        visited = set() 
        
        while queue:
            (node, path) = queue.popleft()
            if node not in visited:
                visited.add(node)
                
                if node == goal_id:
                    path_titles = [self.titles[p_id] for p_id in path]
                    print(path_titles)
                    return [self.titles[p_id] for p_id in path]
                
        #現在のノードから直接リンクされている全てのノードに対し、各ノードに至るパスがキューに保持される
                for adjacent in self.links.get(node, []): ##現在のノードから直接リンクされているノードを繰り返し処理
                    new_path = list(path) 
                    new_path.append(adjacent)
                    queue.append((adjacent, new_path))
                    #全部のノードではなく一つ前のノードが分かれば一つ前のノードもわかるはずなので前だけでおk。。。。
        print("No path found from {} to {}.".format(start, goal))
        return None


    # Calculate the page ranks and print the most popular pages.
    def calculate_page_rank(self, page_ranks, damping_factor, iterations):
        # 初期化
        num_pages = len(self.titles)
        page_ranks = {page: 1/num_pages for page in self.titles.keys()} 
        
        for _ in range(iterations):
            new_page_ranks = {}
            for page in self.titles.keys(): #各ページについて、新しいページランクスコアが計算
                total = 0
                for outgoing_link in self.links[page]: 
                    if self.links[outgoing_link]:
                        total += page_ranks[outgoing_link] / len(self.links[outgoing_link])
                    else:
                        total += 0
                rank = (1.0 - damping_factor) + (damping_factor * total)
                new_page_ranks[page] = rank
            page_ranks = new_page_ranks
        return new_page_ranks

    def find_most_popular_pages(self):
        damping_factor = 0.85  
        iterations = 10 

        page_ranks = {}
        page_ranks = self.calculate_page_rank(page_ranks, damping_factor, iterations)

        sorted_page_ranks = sorted(page_ranks.items(), key=lambda x: x[1], reverse=True)

        print("The most popular pages are:")
        for page, rank in sorted_page_ranks[:10]:  
            print(self.titles[page], rank)
        print()

    # Do something more interesting!!

    def rhyme_path(self, start_word):
        def check_words(word1, word2):
            if word1 in word2 or word2 in word1:
                return False
            return True
 
        title_to_id = {v: k for k, v in self.titles.items()}
        start_id = title_to_id.get(start_word)
        if start_id is None:
            print("Start page not found.")
            return None


        queue = deque([(start_id, [start_word])])
        visited = set()

        while queue:
            (node, path) = queue.popleft()
            if node not in visited:
                visited.add(node)

                for linked_id in self.links[node]:
                    linked_word = self.titles[linked_id]
                    if is_rhyme(start_word, linked_word) and check_words(start_word, linked_word):
                        new_path = list(path)
                        new_path.append(linked_word)
                        queue.append((linked_id, new_path))
                        print(new_path)




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # wikipedia.find_most_popular_pages()
    #wikipedia.rhyme_path("雨")
    wikipedia.rhyme_path("エミネム") #なし
    wikipedia.rhyme_path("幽体離脱") #なし

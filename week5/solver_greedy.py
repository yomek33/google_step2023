#!/usr/bin/env python3


import sys
import math


from common import print_tour, read_input




def distance(city1, city2):
   return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)




# sample code　貪欲法
def greedy(cities):
   N = len(cities)


   dist = [[0] * N for i in range(N)]
   for i in range(N):
       for j in range(i, N):
           dist[i][j] = dist[j][i] = distance(cities[i], cities[j])


   current_city = 0
   unvisited_cities = set(range(1, N))
   tour = [current_city]


   while unvisited_cities:
       next_city = min(unvisited_cities,
                       key=lambda city: dist[current_city][city])
       unvisited_cities.remove(next_city)
       tour.append(next_city)
       current_city = next_city
   return tour


# 2-opt法　　
# 2つの都市間の道順を入れ替えると、全体のルートが短くなるかも
# N=5 3862.2m, N=8 6101.57m, N=16 13479.25 m、greedyと変わらない
def two_opt(cities, tour):
   N = len(tour)
   while True:
       count = 0
       for i in range(N - 2):
           for j in range(i + 2, N if i > 0 else N - 1):
               l1 = distance(cities[tour[i]], cities[tour[i+1]]) + distance(cities[tour[j]], cities[tour[(j+1)%N]])
               l2 = distance(cities[tour[i]], cities[tour[j]]) + distance(cities[tour[i+1]], cities[tour[(j+1)%N]])
               if l2 < l1:
                   tour[i+1:j+1] = reversed(tour[i+1:j+1]) #i+1からj+1を逆順に並び替える
                   count += 1
       if count == 0:
           break
   return tour


#k-minus
#各要素の値からその行と列の距離の平均値を減算する
#N=5 3862.2m, N=8 6101.57m, N=16 13479.25 m、greedyと変わらない
def minus_k_mean_distance(dist, N, k):
   ave_dist = np.mean(np.sort(dist, axis=1)[:, 1:min(N, k + 1)], axis=1) #二次元の距離行列から、各行に対してその最も近いk個の要素（ただし最大Nまで）の平均を計算
   dist = [[dist[i][j] - (ave_dist[i] + ave_dist[j])
           for i in range(N)] for j in range(N)]
   return dist


def greedy_with_k_mean(cities, k=5):
   N = len(cities)


   dist = [[0] * N for i in range(N)]
   for i in range(N):
       for j in range(i, N):
           dist[i][j] = dist[j][i] = distance(cities[i], cities[j])


   dist = minus_k_mean_distance(dist, N, k)


   current_city = 0
   unvisited_cities = set(range(1, N))
   tour = [current_city]


   while unvisited_cities:
       next_city = min(unvisited_cities,
                       key=lambda city: dist[current_city][city])
       unvisited_cities.remove(next_city)
       tour.append(next_city)
       current_city = next_city
   return tour


if __name__ == '__main__':
   assert len(sys.argv) > 1
   cities = read_input(sys.argv[1])
   greedy_tour = greedy(read_input(sys.argv[1]))
   improved_tour = two_opt(cities, greedy_tour)
   k_mean_tour = greedy_with_k_mean(read_input(sys.argv[1]))
   print_tour(improved_tour)

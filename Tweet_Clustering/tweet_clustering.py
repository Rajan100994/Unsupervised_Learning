import json,random,sys

#with open('/Users/rajan/Desktop/Tweets.json','r') as data_file:
 #   data = json.loads(data_file.read())

seeds =[]
seed_ids = []

if len(sys.argv) > 4:
    k=int(sys.argv[1])
    pathtoseeds = sys.argv[2]
    pathtotweets = sys.argv[3]
    outputpath = sys.argv[4]
else:
    k=25
    pathtoseeds = sys.argv[1]
    pathtotweets = sys.argv[2]
    outputpath = sys.argv[3]


line = open(pathtoseeds, 'r')
seeds.append(line.readlines())

for i in range((len(seeds[0]))):
    data_set = []
    x = seeds[0][i].split(',')
    #data_set.append(x[0])
    seed_ids.append(x[0])

tweets = []
for line in open(pathtotweets, 'r'):
    tweets.append(json.loads(line))

if k != 25:
    if k>25:
        k=25
    seed_ids = random.sample(seed_ids,k)
    #print seed_ids
    k = len(seed_ids)




def JaccardDist(s1,s2):

    str1 = set(s1.split())
    str2 = set(s2.split())

    sim = float(len(str1 & str2)) / len(str1 | str2)
    dist = 1 - sim
    return dist

#initialize clusters
def init_clust():

    clusters = []
    for i in range(k):
        add_cl = []
        add_cl.append(i)
        clusters.append(add_cl)
    return clusters
#cluster initialization ends

#find index of seeds i/p - tweets and seed_ids(id of each seed)
def get_seed_ind(tweets,b):
    seed_index = []
    for j in range(len(tweets)):

        a=tweets[j]['id']

    #    print type(a),type(b)
    #    print a,b
        if a in b:
            seed_index.append(j)

    print seed_index
    return seed_index
#end of index of seeds

#dist between tweets and seeds
def dist_tweets_seeds(seed_index):
    total_dist=[]
    for j in seed_index :

        s1 = tweets[j]['text']
        distance = []

        for i in range(len(tweets)):
            s2=tweets[i]['text']
            distance.append(JaccardDist(s1,s2))
        total_dist.append(distance)
    return total_dist
#end of dist between tweets and seeds

#assign clusters
def assign_clusters(clusters,total_dist):
    for i in range(len(tweets)):
        min_dist = []
        for j in range(len(seed_ids)):
            min_dist.append(total_dist[j][i])
        #print len(min_dist)
        if len(min_dist) > 0 :
            cluster = min_dist.index(min(min_dist))
            clusters[cluster].append(i)

    print clusters
    return clusters
#end of cluster assignment

#find all intracluster distances and new seeds
def update_seeds(clusters):
    intr_dist =[]
    new_seed=[]
    for k in range(len(clusters)):
        dist_sum=[]
        for i in clusters[k]:
            in_dist=[]
            for j in clusters[k]:
                in_dist.append(JaccardDist(tweets[i]['text'],tweets[j]['text']))
            dist_sum.append(sum(in_dist))
        if len(dist_sum) > 0:
            new_seed.append(clusters[k][dist_sum.index(min(dist_sum))])

    print new_seed
    return new_seed
#end of finding new seeds

clusters = init_clust()
b = map(int, seed_ids)

seed_index = get_seed_ind(tweets,b)

total_dist = dist_tweets_seeds(seed_index)

clusters = assign_clusters(clusters,total_dist)

for row in clusters:
    del row[0]



for i in range(2):
    up_seeds = update_seeds(clusters)
    clusters = init_clust()
    new_dist = dist_tweets_seeds(up_seeds)
    clusters = assign_clusters(clusters,new_dist)
    for row in clusters:
        del row[0]

def findSSE(tweets, clusters,up_seeds):
    sse=0
    for i in range(len(clusters)):
        a = tweets[up_seeds[i]]['text']
        for j in range(len(clusters[i])):
            b=tweets[clusters[i][j]]['text']
            distance = JaccardDist(a,b)
            sse += distance**2
    return sse

file1 = open(outputpath, "w")
for i in range(len(clusters)):
    line = '' + str(i + 1)
    line += "\t"

    for idx in range(len(clusters[i])):
            line += str(tweets[clusters[i][idx]]['id'])
            line += ", "
    line = line[:-2]
    line += "\n\n"
    file1.write(line)
print "Output File Generated "
sse = findSSE(tweets, clusters,up_seeds)
print sse
file1.write("\nSSE : "+ str(sse))
file1.close()


import urllib2,cookielib,random,sys

link = "http://www.utdallas.edu/~axn112530/cs6375/unsupervised/test_data.txt"
hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(link,headers = hdr)
page = urllib2.urlopen(req)

content = page.read()

'''
file = open('/Users/rajan/Desktop/cl_data', 'r')
content = file.readlines()

'''
#print content
data =[]
seeds =[]
final = []
k = int(sys.argv[1])
print 'k :',k

#Generate random seeds
def seed_gen():
    for j in range(k):
        seed=[]
        seed.append(round(random.random(),3))
        seed.append(round(random.random(),3))
        seeds.append(seed)
    #print seeds
    return seeds
#Seeds Generated

#Read content from website and store it in required format and req datatype
def get_content() :
    for line in content.split('\r'):
        data.append(line)

    for i in range((len(data))):
        data_set = []
        for x in data[i].split('\t'):
            #print x
            data_set.append(x)
        final.append(data_set)
    for row in final:
        del row[0]
    final.remove(final[0])
#    print final
    final1 = []
    for i in range(len(final)):
        final1.append([float(x) for x in final[i]])
    return final1
#Reading of data finished

#Main
final = get_content()
seeds = random.sample(final,k)
#seeds = seed_gen()
#Generating cluster categories
cnt =0

while(cnt < 25):
#    print seeds
    updated_seeds = []
    clusters = []
    for i in range(k):
        add_cl = []
        add_cl.append(i)
        clusters.append(add_cl)

    #Determine category for each
    for j in range(1,100) :
        min_dist = []
        for i in range(len(seeds)):
            dist = pow((seeds[i][0] - final[j][0]),2) + pow((seeds[i][1] - final[j][1]),2)
            #print dist
            min_dist.append(dist)
        cluster_category = min_dist.index(min(min_dist))
            #print "Category is"
            #print cluster_category

        clusters[cluster_category].append(j)

    for i in range(k):
        us =[]
        x=0
        y=0
        for j in range(1,len(clusters[i])):
            x+=final[clusters[i][j]][0]
            y+=final[clusters[i][j]][1]
        us.append((float)(x/j))
        us.append((float)(y/j))
        #print us
        updated_seeds.append(us)
    seeds = updated_seeds
#    print updated_seeds
    print clusters
    cnt+=1

def findSSE(final, clusters,seeds):
    sse = 0
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):

            x = (final[clusters[i][j]][0])
            y = (final[clusters[i][j]][1])
            x1 = x - seeds[i][0]
            y1 = y - seeds[i][1]
            sse += ((x1 ** 2) + (y1 ** 2))
        return sse

file1 = open(sys.argv[2], "w")
for i in range(len(clusters)):
    line = '' + str(i + 1)
    line += "\t"

    for idx in range(len(clusters[i])):
            line += str(clusters[i][idx] + 1)
            line += ", "
    line = line[:-2]
    line += "\n\n"
    file1.write(line)
print "Output File Generated "
sse = findSSE(final, clusters,seeds)
print sse
file1.write("\nSSE : "+ str(sse))
file1.close()
#print updated_seeds

#print clusters
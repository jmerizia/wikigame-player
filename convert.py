import time

id_to_title = {}  # THESE JUST BARELY FIT IN 4G !! WHOOO
title_to_id = {}
title_to_redirect = {}
c = 0

# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

start_time = time.time()

print("collecting data from articles.csv...")

with open('articles_save.csv', 'r') as f:
    next(f)
    for line in f:

        line = line.lower().strip('"')

        c += 1
        if c % 100000 == 0:
            print("{:,}".format(c))
            elapsed_time = time.time() - start_time
            print("Elapsed time: {}".format(hms_string(elapsed_time)))

        arr = line.split('$')
        id_to_title[int(arr[0])] = arr[1]
        title_to_id[arr[1]] = int(arr[0])

print("done collecting data from articles.csv")
c = 0

print("collecting data from articles_redirect.csv...")

with open('articles_redirect_save.csv', 'r') as f:
    next(f)
    for line in f:

        line = line.lower().strip('"')

        c += 1
        if c % 100000 == 0:
            print("{:,}".format(c))
            elapsed_time = time.time() - start_time
            print("Elapsed time: {}".format(hms_string(elapsed_time)))

        arr = line.split('$')
        title_to_redirect[arr[1]] = arr[2];

print("done collecting data from articles_redirect.csv...")
c = 0

num_in = 0
num_not_in = 0

with open('articles_save.csv', 'r') as articles_file, \
     open('wikipedia.in', 'w') as graph_file, \
     open('lookup.in', 'w') as lookup_file:
    next(articles_file)
    for line in articles_file:

        line = line.lower().strip('"')

        c += 1
        if c % 100000 == 0:
            print("{:,}".format(c))
            print("ratio: ", float(num_in) / (num_not_in + num_in))
            elapsed_time = time.time() - start_time
            print("Elapsed time: {}".format(hms_string(elapsed_time)))


        arr = line.split('$')
        u_id = int(arr[0])
        lookup_file.write('%d %s\n' % (u_id, arr[1]))

        for i in range(2, len(arr)):   # skip id, title

            first = arr[i].split('|')[0]

            v_id = -1
            
            hashtag = first.find('#')
            if hashtag != -1:
                first = first[0:hashtag] # remove hashtag

            if first in title_to_id:

                v_id = title_to_id[first];

                num_in += 1
                #print("is :", first)

            elif first in title_to_redirect:
                redirect = title_to_redirect[first];
                if redirect in title_to_id:

                    v_id = title_to_id[redirect]

                    num_in += 1
                    #print("is :", first)

            else:
                num_not_in += 1
                #print("not:", first)

            if v_id != -1:
                graph_file.write('%d %d %d\n' % (u_id, v_id, i - 1)) # u, v, rank


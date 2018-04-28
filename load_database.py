# NOTE: Do not use this script! It runs WAY too slow. Use these SQL scripts instead:

# load data local infile './wikipedia.in' into table graph fields terminated by ' ';
# load data local infile './lookup.in' into table lookup fields terminated by '$';

# Make sure you split up the wikipedia.in file first though!


import _mysql

password = ""
with open('cred.txt', 'r') as cred_file:
    password = cred_file.read()[:-1]

db = _mysql.connect(
        host='localhost',
        user='root',
        passwd=password,
        db='wikipedia'
        )


# Load the graph into database
# A buffered approach is used that uses more memory and a cursor
def load_graph():
    count = 0
    buff_size = 1e4
    buff = []
    with open('wikipedia.in', 'r') as wikipedia_file:
        for line in wikipedia_file:

            (u, v, r) = map(int, line.split()) # ignore rank
            buff.append((u, v))

            if len(buff) == buff_size:
                for k in buff:
                    db.query("insert into graph (u, v) values (%d, %d)" % k)
                del buff[:] # clear buff
                buff = []

            count += 1
            if count % 1e5 == 0:
                print("Edges loaded: {:,}".format(count))
                print("Buff size: {:,}".format(len(buff)))

            if count == 4e6:
                break

# load the lookup table into database
def load_lookup():
    count = 0
    with open('lookup.in', 'r') as lookup_file:
        for line in lookup_file:

            first_space = line.find(' ')     # because I was too lazy to use a better delimiter
            id = int(line[ : first_space])  
            title = line[first_space + 1 : ]
            db.query("insert into lookup (id, title) values (%d, %s)" % (id, title))

            count += 1
            if count % 1e6 == 0:
                print("Pages loaded: {:,}".format(count))


print("Loading graph...")
load_graph()

quit()

print("Loading lookup table...")
load_lookup()

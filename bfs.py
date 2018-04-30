from collections import deque
import _mysql
import time

password = ""
with open('cred.txt', 'r') as cred_file:
    password = cred_file.read()[:-1]

db = _mysql.connect(
        host='localhost',
        user='root',
        passwd=password,
        db='wikipedia'
        )

# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

def lookup_id(title):
    db.query("select id from lookup where title = \"%s\"" % title)
    result = db.use_result()
    row = result.fetch_row()
    if len(row) != 0:
        return int(row[0][0])
    return -1

def lookup_title(id):
    db.query("select title from lookup where id = %d" % id)
    result = db.use_result()
    row = result.fetch_row()
    if len(row) != 0:
        return row[0][0].decode('UTF-8')
    return -1

def back_trace(u, tree):
    path = []
    while tree[u] != u:
        path.append(lookup_title(u))
        u = tree[u]
    path.append(lookup_title(u))
    path.reverse()
    return path

def bfs(A, B):
    Q = deque()
    tree = {A: A}
    Q.append(A)
    mx = -1
    count = 0
    while len(Q) != 0:

        count += 1
        if count % 1000 == 0:
            print("max queue size:", mx)

        u = Q.popleft()
        db.query("select v from graph where u = %d" % u)  # Isn't SQL beautiful?
        result = db.use_result()
        row = result.fetch_row()
        while len(row) != 0:
            v = int(row[0][0])
            if v == B:
                tree[v] = u
                result.fetch_row(0) # fetches all rows to end the select query
                return mx, back_trace(B, tree)
            if v not in tree:
                Q.append(v)
                tree[v] = u
            row = result.fetch_row()
            mx = max(mx, len(Q))

A = lookup_id(input("Start page: "))
if A == -1:
    print("A not found")
    quit()
else:
    print("Found it!")

B = lookup_id(input("End page: "))
if B == -1:
    print("B not found")
    quit()
else:
    print("Found it!")

start_time = time.time()
print("Searching...")
print(bfs(A, B))
elapsed_time = time.time() - start_time
print("Elapsed time: {}".format(hms_string(elapsed_time)))

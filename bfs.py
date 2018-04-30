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
    return list(db.store_result().fetch_row(0))

def lookup_title(id):
    db.query("select title from lookup where id = %d" % id)
    result = db.use_result()
    row = result.fetch_row()
    if len(row) != 0:
        return row[0][0].decode('UTF-8')
    return -1

def back_trace(shared, treeA, treeB):

    pathA = []
    u = shared
    while treeA[u] != u:
        pathA.append(lookup_title(u))
        u = treeA[u]
    pathA.append(lookup_title(u))
    pathA.reverse()

    pathB = []
    v = shared
    while treeB[v] != v:
        # the following two lines are swapped to skip the shared node
        v = treeB[v]
        pathB.append(lookup_title(v))

    return pathA + pathB

def bfs(A, B):
    QA = deque()
    QB = deque()
    treeA = {A: A}
    treeB = {B: B}
    QA.append(A)
    QB.append(B)
    mxA = -1
    mxB = -1
    count = 0
    # these conditions will *almost* never be met (unless no path from A to B i.e. dog -> frog)
    while len(QA) != 0 and len(QB) != 0:  

        count += 1
        if count % 1000 == 0:
            print("max/current queue size (A): %d/%d" % (mxA, len(QA)))
            print("max/current queue size (B): %d/%d" % (mxB, len(QB)))

        # start on A
        u = QA.popleft()
        db.query("select v from graph where u = %d" % u)  # Isn't SQL beautiful?
        result = db.use_result()
        row = result.fetch_row()
        while len(row) != 0:     # for every row
            v = int(row[0][0])
            if v in treeB: # if this node is shared
                treeA[v] = u
                result.fetch_row(0) # fetches all rows to end the select query
                return mxA, mxB, back_trace(v, treeA, treeB)
            if v not in treeA:
                QA.append(v)
                treeA[v] = u
            row = result.fetch_row()
            mxA = max(mxA, len(QA))

        # start on B
        v = QB.popleft()
        db.query("select u from graph where v = %d" % v)
        result = db.use_result()
        row = result.fetch_row()
        while len(row) != 0:
            u = int(row[0][0])
            if u in treeA:
                treeB[u] = v
                result.fetch_row(0)
                return mxA, mxB, back_trace(u, treeA, treeB)
            if u not in treeB:
                QB.append(u)
                treeB[u] = v
            row = result.fetch_row()
            mxB = max(mxB, len(QB))

    return "disconnected"

poss = lookup_id(input("Start page: "))
if len(poss) == 0:
    print("Not found :[")
    quit()
else:
    print("Hit!")
idx = 0
if len(poss) > 1:
    print(poss)
    idx = int(input("Which one? ")) - 1
A = int(poss[idx][0])

poss = lookup_id(input("End page: "))
if len(poss) == 0:
    print("Not found :[")
    quit()
else:
    print("Hit!")
idx = 0
if len(poss) > 1:
    print(poss)
    idx = int(input("Which one? ")) - 1
B = int(poss[idx][0])
print(A, B)

start_time = time.time()
print("Searching...")
print(bfs(A, B))
elapsed_time = time.time() - start_time
print("Elapsed time: {}".format(hms_string(elapsed_time)))

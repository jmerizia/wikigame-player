import queue
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


def bfs(A, B):
    Q = queue.Queue()
    vis = {}
    tree = {}
    Q.put(A)
    count = 0
    while not Q.empty():
        count += 1
        if count >= 30:
            return -1
        u = Q.get()
        db.query("select v from graph where u = %d" % u)
        result = db.use_result()
        row = result.fetch_row()[0]
        while len(row) != 0:
            u = int(row[0])
            if u == B:
                return u
            if not vis[u]:
                Q.put(u)
                tree[u] = v
                vis[u] = True
            row = result.fetch_row()[0]

bfs(12, 0)

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
    tree = {}
    Q.put(A)
    count = 0
    while not Q.empty():
        count += 1
        if count >= 30:
            return -1
        u = Q.get()
        db.query("select v from graph where u = %d" % u)  # Isn't SQL beautiful?
        result = db.use_result()
        row = result.fetch_row()[0]
        while len(row) != 0:
            v = int(row[0])
            if v == B:
                return v
            if v not in tree:
                Q.put(v)
                tree[v] = u
            row = result.fetch_row()[0]

print(bfs(12, 6243762))

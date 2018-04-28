with open('wikipedia.in', 'r') as wikipedia_file, \
     open('wikipedia2.in', 'w') as output_file:
    count = 0
    last_id = -1
    cur_id = -1
    for line in wikipedia_file:

        count += 1
        if count % 1e6 == 0:
            print("Count: {:,}".format(count))

        if count <= 100000001:
            continue

        #if count >= 1e8:
        #    last_id = cur_id
        #    cur_id = int(line.split()[0])
        #    if last_id != -1 and last_id != cur_id:
        #        break

        output_file.write(line)

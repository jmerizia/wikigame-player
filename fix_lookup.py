# just to fix my mistake of using a bad delimiter

count = 0
with open('lookup.in', 'r') as lookup_file, \
     open('lookup_fixed.in', 'w') as fixed_file:
    for line in lookup_file:

        first_space = line.find(' ')     # because I was too lazy to use a better delimiter
        id = line[ : first_space]
        title = line[first_space + 1 : ]

        fixed_file.write("%s$%s" % (id, title))

        count += 1
        if count % 1e6 == 0:
            print("Pages loaded: {:,}".format(count))

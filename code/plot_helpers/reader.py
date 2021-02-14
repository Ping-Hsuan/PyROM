def reader(fname):
    with open(fname, 'r') as f:
        k = f.read()
    list_of_lines = k.split('\n')
    list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
    data = [x[-1] for x in list_of_words]
    return data

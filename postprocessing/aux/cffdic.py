def cffdic(filenames, pt, idx):
    import re
    dic = {}
    for fname in filenames:
        match = re.match(pt, fname)
        if match:
            if match.groups()[idx] not in dic:
                dic[match.groups()[idx]] = []
            dic[match.groups()[idx]].append(fname)

    return dic

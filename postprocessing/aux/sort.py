def sort(ROMs, key1, key2):
    import numpy as np
    data1 = []
    data2 = []
    for rom in ROMs:
        data1.append(rom.info[key1])
        data2.append(rom.outputs[key2])

    data = np.column_stack((data1, data2))
    data = data[data[:, 0].argsort()]
    return data

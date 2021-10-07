def rom_checker(fname, pattern):
    import re
    match_rom = re.match(pattern, fname)
    assert match_rom is not None

    if match_rom.groups()[0] == 'g':
        solver = 'G-ROM'
    elif match_rom.groups()[0] == 'c':
        solver = 'C-ROM'
    elif match_rom.groups()[0] == 'l':
        solver = 'L-ROM'
    elif match_rom.groups()[0] == 'p':
        solver = 'P-ROM'
    elif match_rom.groups()[0] == '':
        solver = 'G-ROM'

    return solver


def angle_checker(fname, solver):
    fsplit = fname.split('_')

    if solver == 'L-ROM':
        angle = int(fsplit[-4])+90
    else:
        angle = int(fsplit[-3])+90

    return angle

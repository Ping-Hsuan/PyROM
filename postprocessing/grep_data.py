import re
import os
import sys


def create_dir(fname):
    # get the absolute error in ROM
    isExist = os.path.exists(os.getcwd()+fname)
    if isExist:
        print("The target directory "+fname+" exist")
        pass
    else:
        os.mkdir(os.getcwd()+fname)
        print("Create the target "+fname+" directory successfully")
    print("---------------------------------------------")


print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print(os.getcwd())
os.chdir(str(sys.argv[1]))
print(os.getcwd())
print("---------------------------------------------")

rom_dir = str(sys.argv[2])
for root, dirs, files in os.walk("./"+rom_dir+"/", topdown=False):
    for name in files:
        if re.match('^.*_(.*)rom_.*$', name):
            pass
    for name in dirs:
        pass


if len(sys.argv) >= 4:
    N = str(sys.argv[3])
    filenames = [name for name in files if
                 re.match('^.*_(.*)rom_'+N+'nb_.*$', name)]
else:
    filenames = [name for name in files if re.match('^.*_(.*)rom_.*$', name)]

print(filenames)
create_dir('/'+rom_dir+'_info/')

labels = ['rom_abserr', 'nu', 'romu', 'romt', 'proj_relerr', 'dual_norm',
          'fom_norm', 'rom_norm']

data_mkdir = ['/'+element+'/' for element in labels]
data_fname = ['_'+element for element in labels]
data_pattern = [r'^\sh1\serror:', r'\snus', r'\sromu', r'\sromt',
                r'\srelative\sh1\serror:',
                r'(residual in h1 norm:\s\s+)(\d\.\d+E?-?\d+)',
                r'^\sFOM*', r'^\sROM*']


for (mkdir, label, pattern) in zip(data_mkdir, data_fname, data_pattern):
    create_dir('/'+rom_dir+'_info'+mkdir)
    print("---------------------------------------------")
    print('Getting '+label+' info')
    for fname in filenames:
        forleg = fname.split('_')

        match_rom = re.match('^.*_(.*)rom_.*$', fname)
        assert match_rom is not None

        # write out absolute error in ROM
        ft = open('./'+rom_dir+'_info'+mkdir+fname+label, 'w')
        with open(root+fname, 'r') as f:
            for line in f:
                if re.search(pattern, line):
                    ft.write(line)
        ft.close()

    print("---------------------------------------------")

import re
import os
import sys
import yaml


def create_dir(fname):
    # get the absolute error in ROM
    path = os.path.join(os.getcwd(), fname)
    print(path)
    isExist = os.path.exists(path)
    if isExist:
        print("The target directory "+fname+" exist")
        pass
    else:
        os.mkdir(path)
        print("Create the target "+fname+" directory successfully")


print("---------------------------------------------")
print("This is the name of the program:", sys.argv[0])
print("Argument List:", str(sys.argv))
print(os.getcwd())
os.chdir(str(sys.argv[1]))
src_dir = str(sys.argv[2])
rom_dir = src_dir+'_info'
cur_path = os.getcwd()
top_dir = os.path.dirname(cur_path)
print("---------------------------------------------")

for root, dirs, files in os.walk(os.path.join(cur_path, src_dir), topdown=False):
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
create_dir(rom_dir)

# Create a dictionary for supproted features
labels = ['mabserr', 'nu', 'romu', 'romt', 'mrelerr', 'dual_norm',
          'fom_norm', 'rom_norm']
data_pattern = [r'^\sh1\serror:', r'\snus', r'\sromu', r'\sromt',
                r'\srelative\sh1\serror:',
                r'(residual in h1 norm:\s\s+)(\d+\.\d+E?-?\d+)',
                r'^\sFOM*', r'^\sROM*']
sprt_features = dict(zip(labels, data_pattern))

# Extract user specify features
with open(src_dir+'/features.yaml') as f:
    features = yaml.load(f, Loader=yaml.FullLoader)

for feature in features.keys():
    print("---------------------------------------------")
    feature_dir = os.path.join(rom_dir, feature)
    create_dir(feature_dir)
    print('Getting '+feature+' info')
    for fname in filenames:
        forleg = fname.split('_')

        match_rom = re.match('^.*_(.*)rom_.*$', fname)
        assert match_rom is not None

        target_dir = os.path.join(feature_dir, fname+'_'+feature)
        ft = open(target_dir, 'w')
        with open(os.path.join(root, fname), 'r') as f:
            for line in f:
                if re.search(sprt_features[feature], line):
                    ft.write(line)
        ft.close()

    print("---------------------------------------------")


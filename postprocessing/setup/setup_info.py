import sys


def setup_info(src_dir, N):
    """setup info directory
    argv[1]: source directory
    argv[2]: N
    """
    from aux.create_dir import create_dir
    from setup.cfpdic import cfpdic
    from setup.load_features import load_features
    from setup.grep_files import grep_files
    from setup.grep_feature import grep_feature

    rom_dir = src_dir+'_info'
    create_dir(rom_dir)

    root, filenames = grep_files(src_dir, N)

    sprt_features = cfpdic()
    features = load_features()

    for feature in features.keys():
        print("---------------------------------------------")
        grep_feature(filenames, feature, sprt_features[feature], src_dir,
                     rom_dir)
        print("---------------------------------------------")


if __name__ == '__main__':
    setup_info(*sys.argv[1:])

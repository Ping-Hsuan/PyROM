import sys


def setup_info(argv):
    """setup info directory
    argv[1]: source directory
    argv[2]: N
    """
    from aux.create_dir import create_dir
    from setup.create_dic import create_dic
    from setup.load_features import load_features
    from setup.grep_files import grep_files
    from setup.grep_feature import grep_feature

    src_dir = str(argv[1])
    rom_dir = src_dir+'_info'
    create_dir(rom_dir)

    if len(argv) >= 3:
        # argv[2] = N and grep files match this N
        root, filenames = grep_files(src_dir, argv[2])
    else:
        root, filenames = grep_files(src_dir)

    sprt_features = create_dic()
    features = load_features()

    for feature in features.keys():
        print("---------------------------------------------")
        grep_feature(filenames, feature, sprt_features[feature], src_dir,
                     rom_dir)
        print("---------------------------------------------")


if __name__ == '__main__':
    setup_info(sys.argv)

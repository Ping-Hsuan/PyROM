def load_features():
    import yaml
    # Extract user specify features
    with open('./features.yaml') as f:
        features = yaml.load(f, Loader=yaml.FullLoader)

    print('Features that will be extracted are:')
    print(*[i for i in features.keys()], sep='\n')
    return features

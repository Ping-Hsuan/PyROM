def cfpdic():
    '''Create a feature-pattern dictionary'''

    labels = ['mabserr', 'nu', 'romu', 'romt', 'mrelerr', 'dual_norm',
              'fom_norm', 'rom_norm', 'tke', 'temp_dual_norm', 'vel_dual_norm',
              'vel_mrelerr', 'temp_mrelerr', 'vel_mabserr', 'temp_mabserr']

    data_pattern = [r'\sabsolute\sh1\s\serror:', r'\snus', r'\sromu',
                    r'\sromt', r'\srelative\sh1\s\serror:',
                    r'(residual in h1 norm:\s\s+)(\d+\.\d+E?-?\d+)',
                    r'^\sFOM*', r'^\sROM*', r'^(?!.*?(?:MOR)s?).*tke$',
                    r'(temp residual in h1 norm\s\s+)(\d+\.\d+E?-?\d+)',
                    r'(vel residual in h1 norm\s\s+)(\d+\.\d+E?-?\d+)',
                    r'\srelative\sh1\serror\sfor\su:',
                    r'\srelative\sh1\serror\sfor\st:',
                    r'\sabsolute\sh1\serror\sfor\su:',
                    r'\sabsolute\sh1\serror\sfor\st:']
    sprt_features = dict(zip(labels, data_pattern))
    return sprt_features

def cfpdic():
    '''Create a feature-pattern dictionary'''

    labels = ['nu_1st2nd', 'nu', 'romu', 'romt', 'fom_norm',
              'rom_norm', 'tke', 'dual_norm', 'temp_dual_norm',
              'vel_dual_norm','mabserr', 'mrelerr',
              'mabserr_h1', 'mrelerr_h1',
              'mabserr_h10', 'mrelerr_h10', 'mabserr_l2',
              'mrelerr_l2', 'vel_mrelerr_h1', 'temp_mrelerr_h1',
              'vel_mabserr_h1', 'temp_mabserr_h1',
              'vel_mrelerr_h10', 'temp_mrelerr_h10',
              'vel_mabserr_h10', 'temp_mabserr_h10',
              'vel_mrelerr_l2', 'temp_mrelerr_l2',
              'vel_mabserr_l2', 'temp_mabserr_l2',
              'mtke']

    data_pattern = [r'\snus', r'\snus', r'\sromu', r'\sromt',
                    r'^\sFOM*', r'^\sROM*', r'^(?!.*?(?:MOR)s?).*tke$',
                    r'(residual in h1 norm:\s\s+)(\d+\.\d+E?-?\d+)',
                    r'(temp residual in h1 norm\s\s+)(\d+\.\d+E?-?\d+)',
                    r'(vel residual in h1 norm\s\s+)(\d+\.\d+E?-?\d+)',
                    r'\sabsolute\sh1\s\serror:',
                    r'\srelative\sh1\s\serror:',
                    r'\sabsolute\sh1\s\serror:',
                    r'\srelative\sh1\s\serror:',
                    r'\sabsolute\sh10\serror:',
                    r'\srelative\sh10\serror:',
                    r'\sabsolute\sl2\s\serror:',
                    r'\srelative\sl2\s\serror:',
                    r'\srelative\sh1\s\serror\sfor\su:',
                    r'\srelative\sh1\s\serror\sfor\st:',
                    r'\sabsolute\sh1\s\serror\sfor\su:',
                    r'\sabsolute\sh1\s\serror\sfor\st:',
                    r'\srelative\sh10\serror\sfor\su:',
                    r'\srelative\sh10\serror\sfor\st:',
                    r'\sabsolute\sh10\serror\sfor\su:',
                    r'\sabsolute\sh10\serror\sfor\st:',
                    r'\srelative\sl2\s\serror\sfor\su:',
                    r'\srelative\sl2\s\serror\sfor\st:',
                    r'\sabsolute\sl2\s\serror\sfor\su:',
                    r'\sabsolute\sl2\s\serror\sfor\st:',
                    r'mean\stke',
                    ]

    sprt_features = dict(zip(labels, data_pattern))
    return sprt_features

import numpy as np
import sys
import re
import os
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/post_pro/')
import aux1
sys.path.append('/Users/bigticket0501/Developer/PyMOR/code/plot_helpers/')
import mypostpro


class ROM:

    def __init__(self, info_dict):
        self.info = {}
        self.fnames = {}
        self.outputs = {}
        # Assign ROM info based on info_dict specifed by user
        for key, value in info_dict.items():
            self.info[key] = value

    def get_data(self):
        for feature in self.info['features'].keys():
            search_dir = self.info['method']+'_info'
            if list(self.info['anchors'])[0] == 'theta':
                self.fnames[feature] = aux1.gtfpath(search_dir, '^.*_'+self.info['POD_norm']+'_'+str(self.info['anchors']['theta']-90)+'_'+feature)
            else:
                self.fnames[feature] = aux1.gtfpath(search_dir, '^.*_'+self.info['POD_norm']+'_.*'+str(self.info['anchors']['Ra'])+'.*_'+feature)
        return

    def get_coef(self, nb, rank=None):
        field = self.field
        # Get the only file
        if rank is None:
            ptr = r"^.*_(\d+)nb_.*"
        else:
            ptr = r"^.*_(\d+)nb_.*_r"+str(rank)+'_rom.*$'
        for element in self.fnames['rom'+field.lower()]:
            z = re.match(ptr, element)
            if z is not None:
                if int(z.groups()[0]) == nb:
                    fname = element
        coef = []
        t = []
        print(fname)
        with open(fname, 'r') as f:
            for line in f:
                info = line.split()
                coef.append(info[2])
                t.append(info[1])

        self.outputs['t'] = np.reshape(np.array(t).astype(np.float64),
                                       (nb,-1), order='F')
        self.outputs[field] = np.reshape(np.array(coef).astype(np.float64),
                                         (nb, -1), order='F')
        return

    def coef_mean(self, T0):
        field = self.field

        num_sample = len(self.outputs[field][0, T0:])

        avg_coef = np.sum(self.outputs[field][:, T0:], axis=1) / num_sample

        self.outputs[field+'a'] = avg_coef
        return

    def coef_variance(self, T0):
        field = self.field

        num_sample = len(self.outputs[field][0, T0:])

        var_coef = np.sum((self.outputs[field][:, T0:]
                           - self.outputs[field+'a'][:, None])**2, axis=1) \
                           / (num_sample-1)

        self.outputs[field+'v'] = var_coef
        return

    def DTAR(self):
        with open(self.fpath, 'r') as f:
            k = f.read()
        list_of_lines = k.split('\n')
        list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
        dtar = [x[-1] for x in list_of_words]
        self.outputs['dtar'] = np.array(dtar).astype(np.float64)
        return

    def anchor(self, parameter):
        # Might need to change according to the parameter
        # Currently using theta
        root = os.getcwd()
        sp1 = (root.split('/'))
        for element in sp1:
            z = re.match(parameter+r"_(\d+)", element)
            if z:
                self.info['anchor'] = float(((z.groups())[0]))
        return

    def compute_momentum(self):
        if self.info['init'] == 'zero':
            self.info['J0'] = mypostpro.find_nearest(self.outputs['t'][0, :], 501)
            self.coef_mean(self.info['J0'])
            self.coef_variance(self.info['J0'])
        elif self.info['init'] == 'ic':
            self.info['J0'] = 0
            print(self.info['J0'])
            self.outputs['t'] += int(self.info['T0'])-1
            self.coef_mean(self.info['J0'])
            self.coef_variance(self.info['J0'])

        return

    def cdict(self, feature):
        if self.info['method'] == 'l-rom':
            files_dict = aux1.create_dict(self.fnames[feature], '^.*_([0-9]*)nb_.*_'+self.info['perc']+'_'+feature)
        else:
            files_dict = aux1.create_dict(self.fnames[feature], '^.*_([0-9]*)nb_.*_\d+_'+feature)
        return files_dict

    def get_dual_wN(self):
        # Should make the regular expression more specific
        # Rightnow it will grep other files
        files_dict = self.cdict('dual_norm')
        data = []
        nbs = []
        for nb, fnames in files_dict.items():
            for fname in fnames:
                with open(fname, 'r') as f:
                    k = f.read()
                list_of_lines = k.split('\n')
                list_of_words = [[k for k in line.split(' ') if k] for line in list_of_lines][:-1]
                data.append([float(x[-1]) for x in list_of_words])
                nbs.append(int(nb))
        self.nbs, self.erris = [list(tuple) for tuple in zip(*sorted(zip(nbs, data)))]
        return

    def get_mrelerr(self):
        # For now, grep proj and rom relerr at the same time
        files_dict = self.cdict('mrelerr')
        nbs = []
        rom = []
        proj = []
        for nb, fnames in files_dict.items():
            for fname in fnames:
                data = aux1.reader(fname)
                rom.append(float(data[0]))
                proj.append(float(data[1]))
                nbs.append(int(nb))
        self.nbs, self.rom_relerr, self.proj_relerr = [list(tuple) for tuple in zip(*sorted(zip(nbs, rom, proj)))]
        return

    def get_mabserr(self):
        # For now, grep proj and rom abserr at the same time
        files_dict = self.cdict('mabserr')
        nbs = []
        rom = []
        proj = []
        for nb, fnames in files_dict.items():
            for fname in fnames:
                data = aux1.reader(fname)
                rom.append(float(data[0]))
                proj.append(float(data[1]))
                nbs.append(int(nb))
        self.nbs, self.rom_abserr, self.proj_abserr= [list(tuple) for tuple in zip(*sorted(zip(nbs, rom, proj)))]
        return

    def get_rom_norm(self):
        files_dict = aux1.create_dict(self.fnames['rom_norm'], '^.*_([0-9]*)nb_.*$')
        nbs = []
        rom_norm = []
        for nb, fnames in files_dict.items():
            for fname in fnames:
                data = aux1.reader(fname)
                data = np.array(data).astype(np.float64)
                rom_norm.append((data))
                nbs.append(int(nb))
        self.nbs, self.rom_norm = [list(tuple) for tuple in zip(*sorted(zip(nbs, rom_norm), key= lambda t: t[0]))]
        return

    def get_tke(self):
        files_dict = aux1.create_dict(self.fnames['tke'], '^.*_([0-9]*)nb_.*$')
        self.tke = {}
        for nb, fnames in files_dict.items():
            t = []
            tke = []
            self.tke[nb] = {}
            for fname in fnames:
                with open(fname, 'r') as f:
                    for line in f:
                        info = line.split()
                        t.append(info[0])
                        tke.append(info[1])
            self.tke[nb]['t'] = (np.array(t).astype(np.float64))
            self.tke[nb]['tke'] = (np.array(tke).astype(np.float64))
#       for element in self.fnames['rom'+field.lower()]:
#           z = re.match(r"^.*_(\d+)nb_.*", element)
#           if int(z.groups()[0]) == self.info['tke']:
#               fname = element
        return


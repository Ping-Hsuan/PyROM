import numpy as np
import os

# Initialize Output
data = []
etag = []
lr1  = []
elmap = []
time  = []
istep = []
fields = []
wdsz = []
header = []


# OPEN THE FILE


fname = 'basht0.f00001'

# READ HEADER into a string
header = (np.fromfile(fname, dtype='c', count=132))
a_string = ''.join([str(item)[2] for item in header])
print(a_string)

emode = 'le'
f = open(fname, "rb")
f.seek(132, os.SEEK_SET)
etag = int((np.fromfile(f, dtype=np.float32, count=1)[0])*1e5)

# If using big endian, then do it again
if etag != 654321:
    print('Big endian')
    f.close()

    emode = 'be'
    f = open(fname, "rb")
    f.seek(132, os.SEEK_SET)
    etag = int((np.fromfile(f, dtype=np.float32, count=1)[0])*1e5)
    f.close()

etag = etag*1e-5
f.close()

# READ HEADER from a string

# word size
wdsz = int(a_string[5])
if (wdsz == 4):
    realtype = 'float32'
elif (wdsz == 8):
    realtype = 'float64'
else:
    raise ValueError("ERROR: could not interpret real type", wdsz)

# element size
lr1 = [int(a_string[6:9]), int(a_string[9:12]), int(a_string[12:15])]

# total number of points per element
npel = (np.prod(lr1))

# compute the total number of active dimensions
ndim = 2 + (lr1[2] > 1)

# number of elements
nel = int(a_string[16:27])

# number of elements in the file
nelf = int(a_string[27:38])
print(nelf)

# time
time = format(float(a_string[38:59]), '16.15E')
print(time)

# istep 
istep = int(a_string[59:69])
print(istep)

# get file id
fid = int(a_string[69:76])
print(fid)

# get total number of files
nf = int(a_string[76:83])
print(nf)

# get fields [XUPTS]
fields = a_string[83:87]
fields = a_string[83:]

var = np.zeros((5,)).astype(np.int)
if "X" in fields:
    print('Coordinate')
    var[0] = ndim
if "U" in fields:
    print('Velocity')
    var[1] = ndim
if "P" in fields:
    print('Pressure')
    var[2] = 1
if "T" in fields:
    print('Temperature')
    var[3] = 1

nfields = (sum(var))
print(nfields)

# read element map
f = open(fname, "rb")
f.seek(136, os.SEEK_SET)
elmap = ((np.fromfile(f, dtype=np.int32, count=nelf)))
print(elmap)
f.close()

# READ DATA
f = open(fname, "rb")
f.seek(136+nelf*4, os.SEEK_SET)
data = np.zeros((nelf, npel, nfields))
for ivar in range(0,len(var)):
    idim0 = sum(var[:ivar+1])-2
    for iel in elmap:
        for idim in range(0, var[ivar]):
            data[iel-1,:,idim+idim0] = np.fromfile(f, dtype=realtype, count=npel)

# Check with Paul whether there is a metadata?
#if ndim == 3:
#    if var[0] != 0:
#        metax = []
#    else:
#        metax = []
#    if var[1] != 0:
#        metax = []
#    else:
#        metau = []
#    if var[2] != 0:
#        metax = []
#    else:
#        metap = []
#    if var[3] != 0:
#        metax = []
#    else:
#        metat = []
#
# CLOSE FILE
f.close()


##### Chunk Parsers #####

def matrix(fobj):
    mtx = struct.unpack('<16f', fobj.read(64))
    MMatrix = om.MMatrix((
        mtx[0] , mtx[1] , mtx[2] , mtx[3] ,
        mtx[4] , mtx[5] , mtx[6] , mtx[7] ,
        mtx[8] , mtx[9] , mtx[10], mtx[11],
        mtx[12], mtx[13], mtx[14], mtx[15]
    ))

    objects[-1][mat].append(MMatrix)
 
def positions(fobj):
    MPositions = om.MPointArray()
    positions = struct.unpack("<I", fobj.read(4))[0]

    for i in range(positions):
        x , y , z = struct.unpack("<3f", fobj.read(12))
        MPositions.append((x , y , z))

    if(positions):
        objects[-1][obj].append("msh")
        objects[-1][pos].append(MPositions)
    else:
        objects[-1][obj].append("jnt")
    
def normals(fobj):
    MNormals = om.MVectorArray()
    normals = struct.unpack("<I", fobj.read(4))[0]
    
    for i in range(normals):
        nx , ny , nz = struct.unpack("<3f", fobj.read(12))
        MNormals.append(( nx , ny , nz ))

    objects[-1][nor].append(MNormals)

def textcoords(fobj):
    UValues = om.MFloatArray()
    VValues = om.MFloatArray()
    textcoords = struct.unpack("<I", fobj.read(4))[0]
   
    for i in range(textcoords):
        u = struct.unpack("f", fobj.read(4))[0]
        UValues.append(u)
        v = struct.unpack("f", fobj.read(4))[0]
        VValues.append(1.0 - v)
        seek(4, elu)

    objects[-1][utx].append(UValues)
    objects[-1][vtx].append(VValues)

def faces(fobj):
    MFaces = om.MUintArray()
    MConnects = om.MUintArray()
    MFacestextcoords = om.MUintArray()

    faces = struct.unpack("<I", fobj.read(4))[0]

    if(faces):
        seek(8, fobj)

        for i in range(faces):
            faces_idx = struct.unpack("<I", fobj.read(4))[0]
            MFaces.append(faces_idx)

            for j in range(faces_idx):
                faces_ord, textcoords = struct.unpack("<2H", fobj.read(4))
                MConnects.append(faces_ord)
                MFacestextcoords.append(textcoords)
                seek(8, fobj)
            seek(2, fobj)
    
    objects[-1][fac].append(MFaces)
    objects[-1][con].append(MConnects)
    objects[-1][ftxt].append(MFacestextcoords)

def faces14(fobj):
    MFaces = om.MUintArray()
    MConnects = om.MUintArray()
    MFacestextcoords = om.MUintArray()

    faces = struct.unpack("<I", fobj.read(4))[0]

    if(faces):
        seek(8, fobj)

        for i in range(faces):
            faces_idx = struct.unpack("<I", fobj.read(4))[0]
            MFaces.append(faces_idx)

            for j in range(faces_idx):
                faces_ord, textcoords = struct.unpack("<2H", fobj.read(4))
                MConnects.append(faces_ord)
                MFacestextcoords.append(textcoords)
                seek(10, fobj)
            seek(2, fobj)
    
    objects[-1][fac].append(MFaces)
    objects[-1][con].append(MConnects)
    objects[-1][ftxt].append(MFacestextcoords)


def binds(fobj):
    binds = []
    binds = struct.unpack("<I", fobj.read(4))[0]
    
    for i in range(binds):
        influences = struct.unpack("<I", fobj.read(4))[0] # numbers of bones which affects this vertex
        for j in range(influences):
            seek(2, fobj)
            bone = struct.unpack("<H", fobj.read(2))[0] # bone idx
            weight = struct.unpack("f", fobj.read(4))   # bone to vtx weight

        

def vertex(fobj):
    vertex = []
    vertex = struct.unpack("<I", fobj.read(4))[0]

    for i in range(vertex):
        vtx_idx = 0
        nrm_idx = 0
        txt_idx = 0
        vtx_idx, nrm_idx, txt_idx = struct.unpack('<3H', fobj.read(6))
        seek(6, fobj)

def vertex14(fobj):
    vertex = []
    vertex = struct.unpack("<I", fobj.read(4))[0]

    for i in range(vertex):
        vtx_idx = 0
        nrm_idx = 0
        txt_idx = 0
        vtx_idx, nrm_idx, txt_idx = struct.unpack('<3H', fobj.read(6))
        seek(8, fobj)

def face(fobj):
    face = []
    face = struct.unpack("<I", fobj.read(4))[0]

    for i in range(face):
        seek(2, fobj)    

def header(fobj):
    magic = struct.unpack("<I", fobj.read(4))[0]
    if(magic != 17297504):
        print(exterr)
        sys.exit()
    version = hex(struct.unpack("<I", fobj.read(4))[0])
    print(eluversion % (version))
    fobj.seek(4, os.SEEK_CUR)
    objcount = struct.unpack("<I", fobj.read(4))[0]

    return version, objcount

def meta0(fobj):
    namelen = struct.unpack("<I", fobj.read(4))[0]
    tmp = fobj.read(namelen)
    name = strbytes(tmp)
    print(objectstr % (name))
    parentlen = struct.unpack("<I", fobj.read(4))[0]
    tmp = fobj.read(parentlen)
    parent = strbytes(tmp)
    parentidx = struct.unpack("<I", fobj.read(4))[0]
    objects[-1][nam].append(name)
    objects[-1][par].append(parent)
    objects[-1][pidx].append(parentidx)

def meta1(fobj):
    namelen = struct.unpack("<I", fobj.read(4))[0]
    tmp = fobj.read(namelen)
    name = strbytes(tmp)
    print(objectstr % (name))
    parentidx = struct.unpack("<I", fobj.read(4))[0]
    parentlen = struct.unpack("<I", fobj.read(4))[0]
    tmp = fobj.read(parentlen)
    parent = strbytes(tmp)
    objects[-1][nam].append(name)
    objects[-1][par].append(parent)
    objects[-1][pidx].append(parentidx)

def strbytes(strs):
    tmp0 = bytes.decode(strs)
    tmp1 = tmp0.replace('\x00','')
    strs = tmp1.replace(" ","_")

    if(strs.isdigit()):
        stuple = ("Object",strs)
        strs = "".join(stuple)
    return strs

##### Parsing Jumps #####

def seek(size, fobj):
    fobj.seek(size, os.SEEK_CUR)

def ukn12(fobj):
    ukn_cnt = struct.unpack("<I", fobj.read(4))[0]
    for i in range(ukn_cnt):
        seek(12, fobj)

def ukn16(fobj):
    ukn_cnt = struct.unpack("<I", fobj.read(4))[0]
    for i in range(ukn_cnt):
        seek(16, fobj)

def ukn64(fobj):
    ukn_cnt = struct.unpack("<I", fobj.read(4))[0]
    for i in range(ukn_cnt):
        seek(64, fobj)
    for i in range(ukn_cnt):
        seek(2, fobj)

##### Objects Parsers #####

def import_5011(fobj):
    seek(8, fobj)
    matrix(fobj)
    seek(4, fobj)
    positions(fobj)
    normals(fobj)
    ukn16(fobj)
    ukn12(fobj)
    textcoords(fobj)
    ukn12(fobj)
    faces(fobj)
    ukn12(fobj)
    seek(4, fobj)
    binds(fobj)
    ukn64(fobj)
    vertex(fobj)
    seek(4, fobj)
    face(fobj)
    ukn12(fobj)
    seek(24, fobj)

def import_5012(fobj):
    seek(8, fobj)
    matrix(fobj)
    seek(8, fobj)
    positions(fobj)
    normals(fobj)
    ukn16(fobj)
    ukn12(fobj)
    textcoords(fobj)
    ukn12(fobj)
    faces(fobj)
    ukn12(fobj)
    seek(4, fobj)
    binds(fobj)
    ukn64(fobj)
    vertex(fobj)
    seek(4, fobj)
    face(fobj)
    ukn12(fobj)
    seek(24, fobj)

def import_5013(fobj):
    matrix(fobj)
    seek(16, fobj)
    positions(fobj)
    textcoords(fobj)
    ukn12(fobj)
    normals(fobj)
    ukn16(fobj)
    ukn12(fobj)
    faces(fobj)
    ukn12(fobj)
    seek(4, fobj)
    binds(fobj)
    seek(4, fobj)
    vertex(fobj)
    ukn64(fobj)
    ukn12(fobj)
    face(fobj)
    seek(24, fobj) 

def import_5014(fobj):
    matrix(fobj)
    seek(16, fobj)
    positions(fobj)
    seek(2, fobj)
    textcoords(fobj)
    ukn12(fobj)
    ukn12(fobj)
    normals(fobj)
    ukn16(fobj)
    ukn12(fobj)
    faces14(fobj)
    ukn12(fobj)
    seek(4, fobj)
    binds(fobj)
    seek(4, fobj)
    vertex14(fobj)
    ukn64(fobj)
    ukn12(fobj)
    face(fobj)
    seek(24, fobj)

#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################



#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################

###### Standards modules #####

import io
import os
import sys
import struct
from enum import IntEnum

##### Autodesk Maya's API Modules #####

import maya.cmds as cmds
import maya.api.OpenMaya as om

# Strings

ffilters = "RS3 Models Files (*.elu) ;; All Files (*.*)"
title = "\n\t\t\t\t\t\t##### GaZoiL #####\n"
exterr = "Incorrect or corrupted file format ! Please select a correct .elu file \nProgram will stop !"
err = "Internal error ! Contact admin"
eluversion = "Elu Version : %s"
objectstr = "Object : %s"
curpos = 'Done ! file curpos at %x' # debug string
comperr = "no support for this version of elu format yet !"

# Arrays

objects = []

# Objects definitions

meshFn = om.MFnMesh()

##### Classes #####

class Array:

    def extend(self):
        self.append([])
        for j in range(len(Index)):
            self[-1].append([])

    def log(self):
        print("logging array")
        for j in range(len(self)):
            print(self[j])

# Enums

class Index(IntEnum):

    objtype = 0
    name = 1
    parent = 2
    parentidx = 3
    matrix = 4
    positions = 5
    normals = 6
    tangents = 7
    utextcoords = 8
    vtextcoords = 9
    faces = 10
    connects = 11
    vertexindices = 12
    facesindices = 13
    blendvertices = 14
    dagpath = 15
    facetextcoords = 16
    
# Aliases

obj  = Index.objtype
nam  = Index.name
par  = Index.parent
pidx = Index.parentidx
mat  = Index.matrix
pos  = Index.positions
nor  = Index.normals
tan  = Index.tangents
utx  = Index.utextcoords
vtx  = Index.vtextcoords
fac  = Index.faces
con  = Index.connects
vind = Index.vertexindices
find = Index.facesindices
bvtx = Index.blendvertices
dag  = Index.dagpath
ftxt = Index.facetextcoords

# Functions definitions

def new(): # Debug reset UI
    cmds.file(new=True, force=True)

def openfile():
    fullpath = cmds.fileDialog2(fileMode=1, ff=ffilters)
    fullpath = str(fullpath[0])
    cnt = fullpath.count("/")
    splitpath = fullpath.split("/")
    filename = splitpath[cnt]
    realpath = fullpath.replace(filename,"")
    os.chdir(realpath)
    file_object = io.open(filename,'r+b')
    print ("Opening file : %s \nFrom : %s " % (filename, realpath))
    return file_object

def objgen():

    for j in range(len(objects)):
        
        if(objects[j][obj][0] == "jnt"):
            cmds.select(all=True, deselect=True)
            cmds.joint(name=objects[j][nam][0])
            selection = om.MSelectionList()
            selection.add(objects[j][nam][0])
            dagpath = selection.getDagPath(0)
            tnode = om.MFnTransform(dagpath)
            tmtx = om.MTransformationMatrix(objects[j][mat][0])
            tnode.setTransformation(tmtx)

        elif(objects[j][obj][0] == "msh"):
            print(objects[j][nam][0])
            cmds.select(all=True, deselect=True)
            mesh = meshFn.create(objects[j][pos][0],objects[j][fac][0],objects[j][con][0])
            if(len(objects[j][utx][0]) & len(objects[j][vtx][0])):
                meshFn.renameUVSet('map1',objects[j][nam][0])
                meshFn.setUVs(objects[j][utx][0],objects[j][vtx][0],uvSet=objects[j][nam][0])
                meshFn.assignUVs(objects[j][fac][0],objects[j][ftxt][0],uvSet=objects[j][nam][0])
            dpnode = om.MFnDependencyNode(mesh)
            dpnode.setName(objects[j][nam][0])
            selection = om.MSelectionList()
            selection.add(objects[j][nam][0])
            dagpath = selection.getDagPath(0)
            tnode = om.MFnTransform(dagpath)
            tmtx = om.MTransformationMatrix(objects[j][mat][0])
            tnode.setTransformation(tmtx)

        else:
            print(err)

        objects[j][dag].append(dagpath)

def parent():

    for j in range(len(objects)):

        if(objects[j][pidx][0] != 0xFFFFFFFF):
            cmds.parent(objects[j][nam][0], objects[objects[j][pidx][0]][nam][0], relative=True)
"""
def skin():
    
    for j in range(len(objects)):
        if(objects[nam]):
"""


########################################################################
##### code instructions #####

print(title)
elu = openfile()
headerargs = header(elu)

for i in range(headerargs[1]):
    if(headerargs[0] == "0x5011"):
        Array.extend(objects)
        meta0(elu)
        import_5011(elu)
    elif(headerargs[0] == "0x5012"):
        Array.extend(objects)
        meta0(elu)
        import_5012(elu)
    elif(headerargs[0] == "0x5013"):
        Array.extend(objects)
        meta1(elu)
        import_5013(elu)
    elif(headerargs[0] == "0x5014"):
        Array.extend(objects)
        meta1(elu)
        import_5014(elu)
    else:
        print(err)

print("EOF")

objgen()
parent()
elu.close()
skincluster0 = ("Crt_UPbody_Ff%s" % ("_SC"))
skincluster1 = ("Crt_Hand_Ff%s" % ("_SC"))
skincluster2 = ("Object002%s" % ("_SC"))
cmds.skinCluster("Bip01","Crt_UPbody_Ff",n=skincluster0)
cmds.skinCluster("Bip01","Crt_Hand_Ff",n=skincluster1)
cmds.skinCluster("Bip01","Object002",n=skincluster2)
print(skincluster0)
print(skincluster1)
print(skincluster2) 
print("EOS")

########################################################################
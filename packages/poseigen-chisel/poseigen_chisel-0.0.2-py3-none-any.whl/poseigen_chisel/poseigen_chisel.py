import numpy as np
import pandas as pd

from Bio.Seq import reverse_complement
import pyBigWig
import pysam

import poseigen_seaside.basics as se



def BinCurrentInverter(BinCurrent): return [1-b for b in BinCurrent] 

def Bed2Markers(fileloc, sep = '\t', header = None, skiprows = None, strandcol = None, addcols = None, addcols_names = None, centered = False): 
    
    Markercols = ['subseq', 'loc', 'strand', 'size']
    if addcols is not None: 
        Markercols = Markercols + ['add' + str(x) for x in addcols] if addcols_names is None else Markercols + addcols_names
    px = pd.read_csv(fileloc, sep=sep, header = header,skiprows = skiprows)
    
    Markers = []
    for i in range(len(px)): 
        p = px.iloc[i]
        st = p[strandcol] if strandcol is not None else 0
        k = (p[q] for q in addcols) if addcols is not None else []
        if centered: M = [p[0], p[1], st, 0, *k]
        else: 
            si = p[2] - p[1]
            M = [p[0], (p[1] + p[2]) // 2, st, si, *k]
        Markers.append(M)
    
    Markers = pd.DataFrame(Markers, columns = Markercols).sort_values(by=['subseq', 'loc', 'strand']).reset_index(drop = True) 
    
    return Markers


def CurrentModifier(SigCurrent, modifier, mode = np.multiply, dtype = None, single = False): 
    #modifier is a list, should match len of SigCurrent. Could be a single value ex. [-1] 
    
    if single: modifier = np.repeat(modifier, len(SigCurrent))
    
    mos = []
    for z,m in zip(SigCurrent, modifier):
        mo = mode(z, m)
        if dtype is not None: mo = mo.astype(dtype)
        mos.append(mo)
    
    return mos

def CurrentsZeroEnds(Currents, reso, zeroends = 3000):

    tozero = zeroends // reso
    
    zerod = []
    for Z in Currents:
        zer = Z.copy()
        zer[:tozero] = 0
        zer[-tozero:] = 0
        zerod.append(zer)

    return zerod


def CurrentZeroExpander(SigCurrent, reso, exp_size): 
    exp_size = (exp_size // reso) // 2
    
    nT = []
    for Z in SigCurrent: 
        zers = np.where(np.max(Z, axis = 1) == 0)[0]
        newT = np.ones(len(Z))
        for ze in zers: 
            newT[ze - exp_size: ze + exp_size ] = 0
        
        nT.append(newT.reshape(-1, 1))
        
    return nT

def CurrentFlagger(SigCurrent, reso = 5, window = 1000, stride = 50, flagmode = np.argmax): 
    
    # EDITED 22.11.06
    #flagmode can be either np.argmax, np.argmin or any index searcher 

    #FLAG NEED TO BE A SINGLE TYPE SHAPE (-1, 1)
    
    window, stride = (0 if x is None else x//reso for x in [window,stride])
    window, stride = (1 if x == 0 else x for x in [window,stride])
    
    j = SigCurrent[0].shape[1]
    ms = []
    for z in SigCurrent:

        y = z.copy()
        lz = len(z)

        for i in range(lz - window + 1)[::stride]: 
            newwin = np.zeros((window, j))
            win1 = y[i: i + window]
            if np.sum(win1) != 0: 
                fa = flagmode(y[i: i + window])
                newwin[fa] = y[fa + i]
                y[i: i + window] = newwin 
        
        ms.append(y) 
    
    return ms


def CurrentDtype(Current, dtype): 
    return [z.astype(dtype) for z in Current]
    
def LowerResCurrent(SigCurrent, reso, newreso, resomode = np.mean, dtype = None): 
    
    resoratio = newreso // reso
    AT = [] 
    for t in range(SigCurrent[0].shape[1]): 
        T = [z[:,t] for z in SigCurrent]
        nT = []
        for z in T: 
            newlength = resoratio * (len(z)//resoratio)
            nT.append(resomode(z[:newlength].reshape(-1, resoratio), axis = 1).reshape(-1,1))
        
        if dtype is not None: nt = CurrentDtype(nT, dtype) 
        AT.append(nT)
    
    return Currents2Current(AT)


def CurrentScaler(MergedSigCurrent, rounds = 1, dtype = np.float64): 
    # gets the mean of each sigcurrent then scales it to make the all equal.

    # I thought that roudns would do something for loawer res but they dont. leave it tho. 

    for r in np.arange(rounds): 

        print(f'round: {r}')
        
        msg = MergedSigCurrent if r == 0 else msg_scaled

        if dtype is not None: msg = [m.astype(dtype) for m in msg]

        msg_stacked_sums = np.vstack(msg).sum(0)
        print(f'unscaled total reads: {msg_stacked_sums}')

        msg_stacked_sums_mean = np.mean(msg_stacked_sums)
        print(f'average total reads: {msg_stacked_sums_mean}')

        msg_stacked_rel2mom = (msg_stacked_sums/msg_stacked_sums_mean).reshape(1, -1)
        print(f'relative to average: {msg_stacked_rel2mom, np.std(msg_stacked_rel2mom)}')

        print

        msg_scaled = [(m.astype(np.float64) / msg_stacked_rel2mom) for m in MergedSigCurrent]
        print(f'scaled total reads: {np.vstack(msg_scaled).sum(0)}')

    return msg_scaled




def SigCurrent2Slice(SigCurrent, Marker, BS_ids, select_BS_ids = None, Vsize = 1000, reso = 5, 
                     newreso = None, resomode = np.mean, 
                     exact = False, Vpad = 2, stranded = False, dtype = None): 
    
    #MAY 18 2023 MODIFICATION: SLICES ARE NOW OF SHAPE (LENGTH, SIGS) NOT (SIGS, LENGTH) 

    if reso == 1: exact = False
    
    if select_BS_ids is None: select_BS_ids = BS_ids
    ind = select_BS_ids.index(Marker.iloc[0])

    Vsize_curr = Vsize // reso

    r = Marker.iloc[1]
    j = se.Rounder(r,reso)
    c = j // reso #cent

    VP = Vpad if exact else 0
    VS = Vsize_curr + 2*VP
    VR = Vpad*reso

    dep = SigCurrent[0].shape[-1]

    ST = np.lib.stride_tricks.sliding_window_view
    current_win = ST(SigCurrent[ind], (VS, dep))

    newspot = c - (Vsize_curr // 2) - VP
    
    V = current_win[newspot][0]

    if exact: 
        g = VR + (r-j)
        V = np.stack([np.interp(np.arange(g, g+(Vsize_curr * reso), reso), 
                                np.arange(0, VS*reso, reso), 
                                b) for b in V.T], axis = 0).T

    if stranded == True: 
        if Marker.iloc[2] > 0: V = np.flip(V, axis = -1)
    
    if newreso is not None: 
        resoratio = 1 if newreso is None else newreso // reso
        newlength = resoratio * ((V.shape[0])//resoratio)
        V = resomode(V[:newlength].reshape(-1, resoratio, V.shape[-1]), axis = 1)
    
    if dtype is not None: V = V.astype(dtype)

    return V

def Profile2AreaPack(Pack, reso = None, areas = [], mode = np.trapz):
    
    areas = [a//2 for a in areas]
    if reso is not None: areas = [a//reso for a in areas]
   
    c = Pack.shape[1] // 2
    
    areas = [a for a in areas if c-a >= 0] #returns only those areas within 
    
    return np.stack([mode(Pack[:, c-a:c+a, :], axis = 1) for a in areas], axis = 1)

def LowerResProfilePack(ProfilePack, reso, newreso, resomode = np.mean, dtype = None): 
    
    shape = ProfilePack.shape
    
    resoratio = newreso // reso
    newlength = resoratio * ((shape[1])//resoratio)

    ProfilePack = resomode(ProfilePack[:, :newlength, :].reshape(-1, newlength // resoratio, resoratio, shape[-1]), axis = -2)
    
    if dtype is not None: ProfilePack = ProfilePack.astype(dtype)
    
    return ProfilePack


def SigCurrent2Pack(SigCurrent, Markers, BS_ids, select_BS_ids = None, Vsize = 1000, reso = 5, newreso = None, resomode = np.mean, 
                    areas = None, exact = False, stranded = False, dtype = None): 
    #newreso needs to be divisiable by reso
    #areas is a list of areas to output instead of profile/single area
    
    if select_BS_ids is None: select_BS_ids = BS_ids
    
    Pack = []
    for ir in range(len(Markers.index)):
        Pack.append(SigCurrent2Slice(SigCurrent, Markers.iloc[ir], BS_ids = BS_ids, select_BS_ids = select_BS_ids, 
                                     Vsize = Vsize, reso = reso, newreso = None, 
                                     resomode = np.mean, exact = exact, Vpad = 2, stranded = stranded))

    Pack = np.stack(Pack, axis = 0)
    
    if newreso is not None: 
        Pack = LowerResProfilePack(Pack, reso, newreso, resomode, dtype)
        reso = newreso
    
    if areas is not None: Pack = Profile2AreaPack(Pack, reso, areas)
    
    if dtype is not None: Pack = Pack.astype(dtype)
    
    return Pack


def IdxFlat2Current(SigCurrent, flatidx): 
    
    lz = [0] + [len(z) for z in SigCurrent]
    rs = np.cumsum(lz)
    Currentidx = [flatidx[np.where((flatidx >= rs[i]) & (flatidx < rs[i+1]))[0]] - rs[i] for i in range(len(SigCurrent))]
    
    return Currentidx

def SigCurrent2Markers(SigCurrent, select_BS_ids = None, reso = 1, select = None, select_mode = None): 
    
    if select is not None: 
        
        allvals = np.concatenate(SigCurrent, axis = 0).reshape(-1)
        nz_idx = np.where(allvals != 0)[0]
        nz_vals = allvals[nz_idx] 
        
        if select_mode is not None: 
            mode_idx = select_mode[0](nz_vals, select, **select_mode[1])
            sel_idx = nz_idx[mode_idx]
        
        else: sel_idx = np.random.choice(nz_idx, replace = False, size = select)
        
        pdx = IdxFlat2Current(SigCurrent, sel_idx)
    
    else: pdx = [np.where(z != 0)[0] for z in SigCurrent]
    
    Markers = []
    for ip, p in enumerate(pdx): 
        lp = len(p)
        vals = (SigCurrent[ip][p]).reshape(-1)
        subseqs, strand, size = [np.repeat(x, lp) for x in [select_BS_ids[ip], 0, 1]]
        Markers.append(np.stack([subseqs, p*reso, strand, size, vals], axis = 1))
    Markers = np.vstack(Markers)
    
    d = pd.DataFrame(Markers, columns = ['subseq', 'loc', 'strand', 'size', 'val'])
    d[['loc', 'strand', 'size']] = d[['loc', 'strand', 'size']].astype(int)
    d[['val']] = d[['val']].astype(float)
    
    d = d.sort_values(by=['subseq', 'loc', 'strand']).reset_index(drop = True)
    
    return d    




def MarkersFilter(Markers, SigCurrent, BS_ids, select_BS_ids = None, reso = 1, exact = False, 
                  Msizes = None, threshold = None, threshmode = np.sum, threshsign = np.greater): 
    
    #Msizes could be Markers[:, 3]
    
    select_BS_ids = BS_ids if select_BS_ids is None else select_BS_ids
    
    MarkersFilt = Markers[Markers.iloc[:, 0].isin(select_BS_ids)].reset_index(drop = True)
    
    si = np.repeat(1, len(Markers)) if Msizes is None else Msizes
    if len(Msizes) == 1: si = np.repeat(Msizes[0], len(Markers))
    
    pp = []
    for ir in MarkersFilt.index: 
        V = SigCurrent2Slice(SigCurrent, MarkersFilt.iloc[ir] , BS_ids, select_BS_ids, Vsize = si[ir], 
                             reso = reso, newreso = None, resomode = np.mean, exact = exact, Vpad = 2)
        if threshsign(threshmode(V), threshold) == True: pp.append(ir) #took away threshmode(V, axis = 1 #Sept 13
            
    MarkersFilt = MarkersFilt.iloc[pp].reset_index(drop = True) 
    
    return MarkersFilt


def Markers4Packs(Markers, select_BS_ids = None, opposite = False, ends = None, BS_sizes = None, BS_ids = None): 
    
    if select_BS_ids is not None: Markers = Markers[Markers['subseq'].isin(select_BS_ids)].reset_index(drop = True)
    
    if ends is not None: 
        ss = Markers['subseq'].unique()
        goodidx = []
        for u in ss: 
            ind = BS_ids.index(u)
            le = BS_sizes[ind] - ends
            g = Markers[Markers['subseq'] == u]
            goodidx.append(g[(g['loc'] - g['size'] > ends) & (g['loc'] + g['size'] < le)].index)
        goodidx = np.concatenate(goodidx)
        Markers = Markers.iloc[goodidx]
        
    if opposite == True: 
        MarkersOpp = Markers.copy() 
        MarkersOpp['strand'] = 1 - MarkersOpp['strand']
        Markers = pd.concat([Markers, MarkersOpp]).sort_values(by=['subseq', 'loc', 'strand'])
        Markers = Markers.drop_duplicates().reset_index(drop = True)
    
    return Markers



def SortMarkers(Markers, ids):
    #sorts by ids order
    Markers.subseq =pd.Categorical(Markers.subseq,categories=ids)
    Markers=Markers.sort_values(['subseq', 'loc'] ).reset_index(drop = True)

    return Markers





OHEdict = {'A': [1,0,0,0],
           'C': [0,1,0,0],
           'G': [0,0,1,0],
           'T': [0,0,0,1],
           'N': [0.25,0.25,0.25,0.25],
           'R': [0.5,0,0.5,0], 
           'Y': [0,0.5,0,0.5],
           'S': [0,0.5,0.5,0], 
           'W': [0.5,0,0,0.5], 
           'K': [0,0,0.5,0.5], 
           'M': [0.5,0.5,0,0], 
           'B': [0,0.33,0.33,0.33], 
           'D': [0.33,0,0.33,0.33], 
           'H': [0.33,0.33,0,0.33], 
           'V': [0.33,0.33,0.33,0]}

Intdict = {k: ik for ik, k in enumerate(OHEdict.keys())}

OHEdict_int = {ik: OHEdict[k] for ik, k in enumerate(Intdict.keys())}

def Str2Arr(inp): 
    return np.fromiter(inp, (np.str_,1))

def Seq2Int(seq, nuc_dict = Intdict): 
    #takes a seq (string), converts into an array and converts each value by lookup 
    ss = Str2Arr(seq.upper())
    for k in nuc_dict.keys(): 
        ss[ss == k] = nuc_dict[k]
    return ss.astype(np.int8)

def Seqs2SigCurrent(seqs, nuc_dict = Intdict): 
    return [Seq2Int(seq, nuc_dict = nuc_dict).reshape(-1,1) for seq in seqs] 

def Seqs2OHE(seqs, expand_dim = None, nuc_dict = OHEdict):
    
    #This is v4 from SLICEandDICE in P5 
    
    #all the seqs have to be the same size for this one
    
    # seqs are either a list or an array 
    # if they are a list, each element is a string or a list of numbers that wants to be converted into OHE. Then it is stacked with expand_dim option 
    # if it is an array, it is shape of (number of seqs, length of seq) OR (number of seqs, length of seq, 1) OR (number of seqs, 1, length of seq, 1)
    #^ each element is a single thing 
    
    #Elements of array can be strngs or numbers. if stirng, gotta do uppers

    #if isinstance(seqs, str): seqs = [seqs]
    
    if isinstance(seqs, list):
        if isinstance(seqs[0], str): 
            seqs_array = np.stack([Str2Arr(seq.upper()) for seq in seqs], axis = 0)
        else: seqs_array = np.stack(seqs)
    else: seqs_array = seqs
    
    ss_shape = seqs_array.shape
    lss = len(ss_shape)
    
    if lss == 4: 
        seqs_array = np.squeeze(seqs_array, axis = (1, 3))
        expand_dim = 1
    elif lss == 3: seqs_array = np.squeeze(seqs_array, axis = -1)

    zeros = np.zeros((*seqs_array.shape, len(list(nuc_dict.values())[0])))
    
    for k in nuc_dict.keys():
        zeros[np.where(seqs_array == k)] = nuc_dict[k]
        
    if expand_dim is not None: zeros = np.expand_dims(zeros, axis = expand_dim)
    
    return zeros


def SeqCurrent2Slice(SeqCurrent, Marker, BS_ids, select_BS_ids, Vsize = 1000, stranded = False, seqmode = None): 
    #seqmode is either None or Seqs2OHE or Seqs2OHERC 
    
    select_BS_ids = BS_ids if select_BS_ids is None else select_BS_ids
    
    ind = select_BS_ids.index(Marker.iloc[0])
    ud = Vsize // 2
    ado = Vsize % 2
    r = Marker.iloc[1]
    V = SeqCurrent[ind][r-ud:r+ud+ado]
    if stranded == True: 
        if Marker.iloc[2] > 0: V = reverse_complement(V)
    
    return seqmode[0]([V], **seqmode[1]) if seqmode is not None else V 

def SeqCurrent2Pack(SeqCurrent, Markers, BS_ids, select_BS_ids = None, Vsize = 1000, seqmode = None, stranded = False): 
    #mode is either Seqs2OHE or Seqs2OHERC 
    #if RC is true, it will add the reverse complement of the pack at the end 

    print('WARNING: SOMETHING IS WRONG WITH THE SELECBS_IDS')
    
    select_BS_ids = BS_ids if select_BS_ids is None else select_BS_ids
    
    seqs = [] 
    markers_nogood = []
    for ir in range(len(Markers.index)): 
        seco = SeqCurrent2Slice(SeqCurrent, Markers.iloc[ir], BS_ids, select_BS_ids, 
                                     Vsize = Vsize, stranded = stranded, seqmode = None)

        if len(seco) == Vsize: seqs.append(seco)
        else: markers_nogood.append( Markers.iloc[ir])
        

    print(markers_nogood)
    
    if seqmode is not None: seqs = seqmode[0](seqs, **seqmode[1])
    
    return seqs





def PackShaper(Pack, expand_dim = None, squeeze = False, twoD = False, flatten = False): 
    
    if expand_dim is not None: Pack = np.expand_dims(Pack, axis = expand_dim)
    if squeeze == True: Pack = np.squeeze(Pack) 
    if twoD == True: Pack = np.reshape(Pack, (len(Pack), -1))
    if flatten == True: Pack = np.reshape(Pack, (-1)) 
    
    return Pack

def Packs2Pack(Packs): 
    return np.hstack(Packs)


################################################


def CentTransPack(transpack, window, reso): 

    #transpack shape: (obs, len, diff) 

    #

    tp_shape = transpack.shape
    
    win = window // reso 

    numwins = tp_shape[1] - win + 1
    centwin = numwins // 2

    ST = np.lib.stride_tricks.sliding_window_view
    tp_win = ST(transpack, (1, win, tp_shape[-1]))

    return tp_win[:, centwin, 0, 0, :, :]


def MakeTransAugs(packs,
                  resos = 1, slice_size = 1, slice_mode = None,
                  num_trans = 2):
    
    #MakeTransAugs_2 from trainers 

    #length dimension needs to always be the 3rd (index 2) dim. 
    

    ##########################################

    step_size = np.lcm.reduce(resos)

    LC, LM = len(packs), len(packs[0])
    
    ################################################################

    if isinstance(resos, int): resos = np.repeat(resos, LC)
    if isinstance(slice_size, int): slice_size = np.repeat(slice_size, LC)
    
    if slice_mode is None: slice_mode = [None] * LC
    elif isinstance(slice_mode, list) is False: slice_mode = [slice_mode for _ in range(LC)]
    elif len(slice_mode) != LC: slice_mode = slice_mode + [None] * (LC - len(slice_mode)) #Adds Nones at the end if its a list already 

    ################################################################

    ST = np.lib.stride_tricks.sliding_window_view

    Vsize_curr = [(sl // re) for sl,re in zip(slice_size, resos)]

    max_trans = packs[0].shape[2] - Vsize_curr[0] + 1 #The packs dimension index 2 is always length
    step_max = max_trans // step_size

    steps = (np.linspace(0, max_trans, num_trans) * step_size).astype(int)


    packs_shapes = [pa.shape for pa in packs]

    newjs = []

    for P,S,V,re,sm in zip(packs, packs_shapes, Vsize_curr, resos, slice_mode):

        tranz = steps // re
        tranz[-1] = tranz[-1] - 1

        if len(S) == 4: 
            packs_win = ST(P, (1, S[1], V, S[-1]))
            newj = np.vstack([packs_win[:, 0, z, 0, 0] for z in tranz])
        elif len(S) == 3: 
            packs_win = ST(P, (1, S[1], V))
            print(packs_win.shape)
            newj = np.vstack([packs_win[:, 0, z, 0] for z in tranz])

        if sm is not None: newj = sm[0](newj, **sm[1])

        newjs.append(newj)
    
    return newjs






def Bw2Current(fileloc, BS_sizes, BS_ids, select_BS_ids = None, newreso = 20, resomode = np.sum, window = None, dtype = None):
    
    select_BS_ids = BS_ids if select_BS_ids is None else select_BS_ids 
    
    bw =  pyBigWig.open(fileloc)
    
    T = []
    for z in select_BS_ids: 
        ind = BS_ids.index(z)
        m = np.zeros(BS_sizes[ind])
        if dtype is not None: m = m.astype(dtype) 
        
        if window is not None: 
            for x in bw.intervals(z):
                if x[1]-x[0] < window: m[x[0]:x[1]] = x[2]
        else: 
            for x in bw.intervals(z): m[x[0]:x[1]] = x[2]
        if newreso > 1: 
            newlength = newreso * (BS_sizes[ind] // newreso)
            m = resomode(m[:newlength].reshape(-1, newreso), axis=1)
        
        if dtype is not None: m = m.astype(dtype) 
        T.append(m.reshape(-1,1))
    
    return T



def Currents2Current(SigCurrents): 
    return [np.hstack([SigCurrents[T][z] for T in range(len(SigCurrents))]) for z in range(len(SigCurrents[0]))]


def CurrentMerger(SigCurrent, mode = np.mean, dtype = None):
    
    ms = []
    for z in SigCurrent: 
        m = mode(z, axis = 1).reshape(-1,1)
        if dtype is not None: m = m.astype(dtype)
        ms.append(m) 
    
    return ms

def CurrentEqualizer(current, prints = False):
    sums = [np.sum(D) for D in np.vstack(current).T]
    refto1 = np.array([sums[0] / s for s in sums])
    equalized = [C * refto1 for C in current]
    if prints: print(f'Before: {sums}, After: {[np.sum(D) for D in np.vstack(equalized).T]}')
    return equalized


def CurrentWindower(SigCurrent, reso = 1, mode = np.mean, window = None, center = None, extend = None, dtype = None, indiv = False): 

    inds = SigCurrent[0].shape[1] if indiv else 1
    
    window = 0 if window is None else window//reso 
    window = 1 if window == 0 else window
    
    TM = []
    for z in SigCurrent: 
        
        lz = len(z) 
        r = np.squeeze(np.lib.stride_tricks.sliding_window_view(z, (window, z.shape[1])), axis = 1)

        t = mode(r, 1)
        if indiv is False: t = mode(t, -1).reshape(-1, 1)

        if dtype is not None: t = t.astype(dtype)
        dy = t.dtype.type
        
        if center is not None: t = np.vstack([np.full((window // 2, inds), center, dtype = dy), t])
        if extend is not None and lz - len(t) > 0: t = np.vstack([t, np.full((lz - len(t), inds), extend, dtype = dy)])

        TM.append(t)
    
    return TM 




def BwChrs(fileloc):
    return list(pyBigWig.open(fileloc).chroms().keys())


def CurrentSelect(Current, BS_ids, select_BS_ids): 
    idx = [BS_ids.index(z) for z in select_BS_ids if z in BS_ids] 
    return [Current[i] for i in idx]

def CurrentChooser(current, idxs): 
    if isinstance(idxs, int): idxs = [idxs]
    return [C[:, idxs] for C in current]



def CurrentThresholder(SigCurrent, threshold = 0, threshsign = np.greater, binary = False): 
    
    TT = [(threshsign(z, threshold)*1).astype(np.int8) for z in SigCurrent]
    if binary is not True: TT = [z*t for z,t in zip(SigCurrent, TT)]
    
    return TT

def CurrentFilter(current, filter):
    curs = []
    for z,f in zip(current, filter):
        y = z.copy()
        y[f == 0] = 0
        curs.append(y)
    return curs 


def CurrentStd(Current, ddof = 0): 
    return [np.std(z, ddof = ddof, axis = 1).reshape(-1, 1) for z in Current]


def Array2Markers(inp, center = True): 
    
    if center: centos = (inp[:, 1].astype(int) + inp[:, 2].astype(int)) // 2
    else: centos = inp[:, 1].astype(int)
    
    tomarkrs = pd.DataFrame(np.stack([inp[:, 0], centos], axis = 1), columns = ['subseq', 'loc'])
    tomarkrs['loc'] = tomarkrs['loc'].astype(int)
    tomarkrs = tomarkrs.sort_values(by=['subseq', 'loc']).reset_index(drop = True)
    tomarkrs['strand'] = 0
    
    return tomarkrs



def Slicer(Current, Markers, BS_ids, select_BS_ids = None, Vsize = 1000, reso = 5): 
    
    if select_BS_ids is None: select_BS_ids = BS_ids
    inds = [select_BS_ids.index(u) for u in Markers.iloc[:, 0]]
    Markers_2 = np.stack([inds, se.Rounder(Markers.iloc[:, 1].to_numpy(), reso)], axis = -1)

    Vsize_curr = Vsize // reso
    
    Markers_A = Markers_2
    cent = Markers_A[:, 1] // reso 
    Markers_3 = np.stack([Markers_A[:, 0], cent - (Vsize_curr // 2)], axis = 1)

    ST = np.lib.stride_tricks.sliding_window_view
    currents_win = [ST(c, (Vsize_curr, c.shape[-1])) for c in Current]

    div = np.stack([currents_win[m[0]][m[1]] for m in Markers_3], axis = 0)

    return div





def BamReadCounts(bamname, select_chrs = None): 
    #returns total aligned reads
    stats = pysam.idxstats(bamname).split('\n')
    stats_sep = [stat.split('\t') for stat in stats][:-2]

    aligned = [int(stat[2]) for stat in stats_sep]
    if select_chrs is not None: 
        chrs = [stat[0] for stat in stats_sep]
        chrs_idx = [chrs.index(z) for z in select_chrs]
        aligned = [aligned[ci] for ci in chrs_idx]

    return np.sum(aligned)

def BamMakeIndex(fileloc):
    pysam.index(fileloc)
    return 

def Bam2Current(fileloc, BS_sizes, BS_ids, select_BS_ids = None, 
                center = None,
                newreso = 20, resomode = np.sum, stranded = True, 
                read_length = None, paired = False, 
                dtype = None): 
    
    #From 22.08.29.Bam2Current
    #When paired is True, the mates are mapped only by the first mate. Reads with unmapped mates are mapped as single end reads. 
    
    #22.09.14. added dtype for memory. could be np.int or np.float with 8/16/32. 

    #25.03.30. Added center option. Removed make index, made a seperate function for that
    
    select_BS_ids = BS_ids if select_BS_ids is None else select_BS_ids 
    
    samfile = pysam.AlignmentFile(fileloc, 'rb')

    centx = center // 2 if center is not None else None
    
    T = []
    for z in select_BS_ids: 

        ind = BS_ids.index(z)
        ls = BS_sizes[ind]
        m = np.zeros((ls, 2), dtype = int)

        for read in samfile.fetch(z): 
            rp, rl, rt = read.pos, read.rlen, read.tlen
            
            rx = read_length if read_length is not None else rl 
            
            if paired == True and rt != 0: 
                if '{0:012b}'.format(read.flag)[::-1][6] == '1': rx = abs(read.tlen)
                else: continue 
                
            rp, st, e1, e2 = (rp + rl + 1, 1, rx, 0) if '{0:012b}'.format(read.flag)[::-1][4] == '1' else (rp, 0, 0, rx)

            j,k = rp-e1, rp+e2

            if centx is not None: 
                jk_cent = j + ((k-j) // 2)
                j, k = (jk_cent - centx, jk_cent + centx + 1)

            if j < 0: j = 0

            m[j:k, st] += 1
        
        if stranded == False: m = np.sum(m, axis = 1).reshape(-1,1)
    
        if newreso is not None:
            newlength = newreso * (BS_sizes[ind] // newreso)
            m = resomode(m[:newlength].reshape(newlength//newreso, newreso, -1), axis = 1)
        
        print(np.max(m))
            
        if dtype is not None: m = m.astype(dtype) 
        
        T.append(m) 
        
    return T





def TransAugPacker(pack, winsize = 1, reso = 1, everyother = 1):

    #pack shape is num, len, type

    # Gets all possible windows then skips everyother // reso 

    wino = winsize // reso
    eoy = everyother // reso
    print(eoy)

    ST = np.lib.stride_tricks.sliding_window_view
    tp_win = ST(pack, (1, wino, pack.shape[-1]))[:, ::eoy, 0, 0]

    print(tp_win.shape)

    tp_win2 = tp_win.reshape(-1, *tp_win.shape[-2:])
    print(tp_win2.shape)

    return tp_win2







    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  MOTIF TOOLS 

    

def MEME2Motifs(meme_path, name_idx = 1): 
    #Jan 17 2024

    parsed = [line.split() for line in open(meme_path)]

    names, matrixes = [], []
    for ip, p in enumerate(parsed): 

        if len(p) > 0 and p[0] == 'MOTIF':
            try: 
                names.append(p[name_idx])
            except: 
                names.append(p[name_idx-1])
            mat = []
            for pa in parsed[ip+3:]:
                if len(pa) == 4: mat.append(pa)
                else: 
                    mat = np.array(mat, dtype = np.float64)
                    matrixes.append(mat)
                    break

    return names, matrixes  


def PWMScorer(inp1, inp2, 
                 revcomp = False, 
                 sepwindows = False, extendbig = False,
                 score_mode = 'dot'):

    #inps can be 2 dim (length, width) or 3 dim (num, length, width)
    #its the smallest comparing to the largest one 

    #sep windows is that you dont do any summary on the window set

    #PWM score is the SUM of the product of the kmer and the OHE 

    #extendbig extends the bigger one by random (0.25)


    if len(inp1.shape) < 3: inp1 = np.expand_dims(inp1, axis = 0)
    if len(inp2.shape) < 3: inp2 = np.expand_dims(inp2, axis = 0)

    if extendbig: 
        exto = np.full((1, inp1.shape[1], 4), 0.25)
        inp2 = np.concatenate([exto, inp2, exto], axis = 1)

    lens = [x.shape[1] for x in [inp1, inp2]]

    if lens[0] < lens[1]:
        inp2s = [inp2[:, b:b+lens[0]] for b in range(lens[1]-lens[0]+1)]
    else: inp2s = [inp2]

    sha = inp2s[0].shape
    
    ST = np.lib.stride_tricks.sliding_window_view

    scos = []

    inpx = [inp1, np.flip(inp1, axis = (-1, -2))] if revcomp else [inp1]

    for inpj in inpx:

        for p2 in inp2s:

            w = ST(inpj, sha)[:, :, 0, 0] #You get shape of [num inp1, windows, lenwindow, widwindow]

            px = np.expand_dims(p2, 0) #now its shape [1, 1, lenwindow, widwindow]

            if score_mode == 'recipeuc':
                d1 = 1 / (np.sum(np.abs(w-px)**2, axis = (-1, -2))**(1/2))
            elif score_mode == 'euc':
                d1 = np.sum(np.abs(w-px)**2, axis = (-1, -2))**(1/2)
            else: #automatically goes to 'dot'
                d1 = np.sum(w * px, axis = (-1, -2))
           
            d2 = d1 if sepwindows else np.max(d1, axis = -1).reshape(-1, 1)

            scos.append(d2)
    
    if sepwindows:
        fin = np.hstack(scos) if lens[0] < lens[1] else np.vstack(scos)

    else:
        scos = np.stack(scos)
        ff = np.max
        fin = ff(scos, axis = 0)

    return fin



def CM2PFM(CM): 
    sums = np.sum(CM, axis = 1).reshape(-1, 1)
    return CM / sums


def kPPMFromPPM(ppm, k, name = None):
    #for ppms 

    lm = len(ppm)

    if lm == k:
        shifs = [ppm]
        if name is not None: nam = [name + '_0']
    
    else: 
        if lm > k:
            diff = lm - k
            shifs = [ppm[x:x+k] for x in np.arange(diff + 1)]
    
        else:
            shifs = []
            diff = k - lm
            base = np.empty((k,4))
            base.fill(0.25)

            for d in np.arange(diff + 1): 
                bas2 = base.copy()
                bas2[d:d+lm] = ppm
                shifs.append(bas2)

        if name is not None: nam = [name + '_' + str(x) for x in np.arange(diff + 1)]

    out = (shifs, nam) if name is not None else shifs
    return out 



def kmersFromPPM(ppm, num = 10000, unique = False):

    # Generates k-mers from PPM. 

    lets = [np.random.choice(['A', 'C', 'G', 'T'], 
                                     size = num, replace = True, 
                                     p = px) for px in ppm]
    
    kmers = [''.join(row) for row in np.stack(lets, axis = 1)]

    if unique: kmers = list(np.unique(kmers))
    
    return kmers
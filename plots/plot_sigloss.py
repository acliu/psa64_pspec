#! /usr/bin/env python
import numpy as n, pylab as p
from matplotlib import gridspec
import glob

fig = p.figure(1, figsize=(7,7))
gs = gridspec.GridSpec(2,2, width_ratios=[1,.4], height_ratios=[.4,1])
fig.subplots_adjust(left=.15, top=.95, bottom=.15, wspace=.15, hspace=.15, right=0.95)

#fig2 = p.figure(2)
pCs,pIs = [],[]
pCs_err,pIs_err = [],[]
for inject in glob.glob('data/sigloss/inject_*'):
    pspecs = glob.glob(inject + '/pspec_boot*.npz')
    inject = float(inject.split('_')[-1])
    pC_avg, pI_avg = [], []
    pC_spec, pI_spec = [], []
    for pspec in pspecs:
        npz = n.load(pspec)
        pC,pI = npz['pC'], npz['pI']
        pC_avg.append(n.average(pC.real))
        pI_avg.append(n.average(pI.real))
        #pC_spec.append(n.average(pC.real, axis=1))
        #pI_spec.append(n.average(pI.real, axis=1))
        #pC_spec.append(pC.real)
        #pI_spec.append(pI.real)
    pCs.append(n.average(pC_avg))
    pCs_err.append(n.std(pC_avg)/n.sqrt(len(pspecs)))
    pIs.append(n.average(pI_avg))
    pIs_err.append(n.std(pI_avg)/n.sqrt(len(pspecs)))
    #pC_spec = n.average(pC_spec, axis=0)
    #pI_spec = n.average(pI_spec, axis=0)
    #p.figure(2); p.plot(pI_spec/pC_spec)
    #print inject, pspec, pC_avg, pI_avg
    #p.figure(1)
    #p.subplot(211); p.loglog([pI_avg], [pC_avg], 'k.')
    #p.subplot(212); p.loglog([pC_avg], [pI_avg/pC_avg], 'k.')
#p.show()
pIs,pCs = n.array(pIs), n.array(pCs)
pIs_err,pCs_err = n.array(pIs_err), n.array(pCs_err)
p.figure(1)

pklo,pkhi = 1e4,1e13
p.subplot(gs[2])
#p.loglog(pIs, pCs, 'k.')
p.errorbar(pIs, pCs, xerr=2*pIs_err, yerr=2*pCs_err, capsize=0, fmt='k.')
p.loglog([pklo,pkhi],[pklo,pkhi], 'k-')
p.xlim(pklo, pkhi)
p.ylim(pklo, pkhi)
p.xlabel(r'$P_{\rm in}(k)\ [{\rm mK}^2\ (h^{-1}\ {\rm Mpc})^3]$', fontsize=14)
p.ylabel(r'$P_{\rm out}(k)\ [{\rm mK}^2\ (h^{-1}\ {\rm Mpc})^3]$', fontsize=14)
p.grid()

npz = n.load('data/final_pspecs/v032/pspec.npz')
print npz.files
kpls,pks,errs = npz['kpl'], npz['pk'], npz['err']
for kpl,pk,err in zip(kpls,pks,errs):
    #p.([pklo,pkhi], [pk,pk], 'r')
    pkup = max(pk+err,1e-6)
    pkdn = max(pk-err,1e-6)
    p.subplot(gs[2])
    p.fill_between([pklo,pkhi], [pkdn,pkdn], [pkup,pkup], facecolor='gray', edgecolor='gray')
    p.subplot(gs[3])
    p.fill_between([1e-3,20], [pkdn,pkdn], [pkup,pkup], facecolor='gray', edgecolor='gray')

ax3 = p.subplot(gs[3])
p.setp(ax3.get_yticklabels(), visible=False)
#p.loglog(n.clip(pIs/pCs - 1, 1e-3,n.Inf), pCs, 'k.')
#p.loglog(n.abs(pIs/pCs - 1), pCs, 'k.')
p.errorbar(pIs/pCs - 1, pCs, xerr=2*pIs_err/pCs, yerr=2*pCs_err, fmt='k.', capsize=0)
print pIs/pCs - 1
print pCs
ax3.set_xscale('log')
ax3.set_yscale('log')
p.ylim(pklo, pkhi)
p.xlim(1e-3,20)
#p.xlim(1,10)
p.grid()
p.xlabel(r'$P_{\rm in}/P_{\rm out}-1$', fontsize=14)

ax0 = p.subplot(gs[0])
p.setp(ax0.get_xticklabels(), visible=False)
p.errorbar(pIs, pCs/pIs, xerr=2*pIs_err, yerr=2*pCs_err/pIs, fmt='k.', capsize=0)
ax0.set_xscale('log')
p.xlim(pklo, pkhi)
#p.ylim(3e-2,3)
p.ylim(0,1.1)
p.grid()
p.ylabel(r'$P_{\rm out}/P_{\rm in}$', fontsize=14)

p.show()

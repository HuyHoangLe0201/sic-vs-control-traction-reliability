import numpy as np, tonhao as th, dao_dong as dd, hanhtrinh as h
th.use_sink('tannhiet_step.npz')
for cfg in ('SiC-ANPC','Si-NPC'):
  for I,m,fe in ((138.6,0.3,40.0),(138.6,0.5,80.0),(138.6,0.9,200.0),(462,0.3,30.0),(462,0.9,150.0)):
    r=th.analyse_point(cfg,I,m,0.95,1500,fe=fe); tp=r['tp']
    LT=th.at_temp(r['L'],r['Tb']); G=dd.ripple_map(tp,LT,fe)
    Aeq,beq,_=dd.eq_constraints(tp,r['inpb'],r['g'])
    rs,x,rr,st,dual=dd.ripple_lp(tp,G,Aeq,beq,npc=r['npc'])
    w=x.reshape(th.NBIN,th.NOFF,len(tp['otypes']))
    for nh in (12,60):
        h.NHARM=nh
        tab,H=h.policy_tables(r['L'],w,r['Tb'])
        rp=h.ripple_p2p(H,tp['rth'],tp['foster'],fe)
        print(cfg,I,m,fe,'NHARM',nh,'max ripple sim',round(rp.max(),3),'LP',round(rr.max(),3))
    h.NHARM=12

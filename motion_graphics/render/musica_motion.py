import numpy as np, wave, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_motion as M
SR=48000; DUR=M.TOTAL; N=int(SR*DUR); BPM=125; B=60/BPM
rng=np.random.default_rng(5); L=np.zeros(N); R=np.zeros(N)
def t_(d): return np.arange(int(SR*d))/SR
def add(s,at,g=1,pan=0):
    i=int(at*SR); s=s[:max(0,N-i)]*g
    if len(s)==0: return
    L[i:i+len(s)]+=s*(1-max(0,pan)); R[i:i+len(s)]+=s*(1+min(0,pan))
from scipy.signal import lfilter
def lp(x,a): return lfilter([a],[1,a-1],x)
def hp(x,a): return x-lp(x,a)
def note(n): return 440*2**((n-69)/12)
def kick():
    t=t_(.3); f=50+120*np.exp(-t*40); return np.tanh(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*2)*.8
def hat(o=False):
    d=.18 if o else .04; t=t_(d); return hp(rng.standard_normal(len(t)),.6)*np.exp(-t*(16 if o else 90))*.18
def clap():
    t=t_(.22); return hp(lp(rng.standard_normal(len(t)),.4),.1)*np.exp(-t*30)*.35
def pluck(n,d=.22):
    t=t_(d); f=note(n); s=sum(np.sign(np.sin(2*np.pi*f*h*t))/h for h in (1,2))*.5
    return lp(s,.25)*np.exp(-t*12)*.16
def bass(n,d):
    t=t_(d); s=np.sin(2*np.pi*note(n)*t)+.3*np.sign(np.sin(2*np.pi*note(n)*t)); return lp(s,.05)*np.minimum(1,t/.01)*np.exp(-t*2)*.35
def pad(ch,d):
    t=t_(d); s=sum(2*((t*note(n)*(1+dt)+rng.random())%1)-1 for n in ch for dt in (-.003,.003))
    return lp(s/(len(ch)*2),.03)*np.minimum(1,t/.3)*np.minimum(1,(d-t)/.3)*.25
CH=[[60,64,67],[57,60,64],[53,57,60],[55,59,62]]; RT=[36,33,29,31]
bar=4*B; nb=int(DUR/bar)+1
for b in range(nb):
    t0=b*bar; c=CH[b%4]
    add(pad(c,bar+.05),t0,.8)
    for k in range(4):
        tb=t0+k*B
        if t0>=1.8: add(kick(),tb,.9)
        add(hat(True),tb+B/2,.8,.2)
        if k in (1,3) and t0>=1.8: add(clap(),tb,.8)
        add(bass(RT[b%4],B*.9),tb+B/2,1 if t0>=1.8 else .4)
    for k in range(8):
        add(pluck(c[k%3]+12+(12 if k==7 else 0)),t0+k*B/2,.9,-.2 if k%2 else .2)
m=np.stack([L,R],1); fade=np.ones(N); fs=int((DUR-1.2)*SR); fade[fs:]=np.linspace(1,0,N-fs); m*=fade[:,None]
m=np.tanh(m*1.2); m/=np.abs(m).max()+1e-9; m*=.85
w=wave.open(os.path.join(M.MO,'musica.wav'),'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m*32767).astype(np.int16).tobytes()); w.close()
# voz y efectos en sus tiempos
A='/tmp/claude-0/-home-user-finanzas/400f996d-bb64-5a86-b968-aadbbec0de6b/scratchpad/audio/'
def rd(p):
    w=wave.open(p); return np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(np.float32)/32768
vox=np.zeros((N,2),np.float32)
for i,s in enumerate(M.LS):
    v=rd(os.path.join(M.MO,'voz',f'l{i:02d}.wav')); j=int(s*SR); n=min(len(v),N-j); vox[j:j+n]+=v[:n]
fx=np.zeros((N,2),np.float32); S={k:rd(A+k+'.48.wav') for k in ['whoosh','pop','punch','impact','shimmer','typing','clink']}
ev=[('pop',.1,.5)]+[('whoosh',c-.2,.5) for c in M.CUT[1:]]
ev+=[('pop',M.CUT[1]+.05,.4),('pop',M.CUT[2]+.05,.5),('punch',M.CUT[3]+.75,.6),('punch',M.CUT[3]+.85,.5),('pop',M.CUT[4]+.3,.4),
     ('typing',M.LS[4]+.75,.25),('pop',M.CUT[5]+.05,.5),('pop',M.CUT[6]+.6,.4),('shimmer',M.CUT[7]+.3,.4),('clink',M.CUT[8]+.75,.4),
     ('shimmer',M.CUT[8]+.8,.5),('punch',M.CUT[9]+.6,.6),('impact',M.CUT[10]+.1,.6),('shimmer',M.LS[10]+.3,.4)]
for k,t,g in ev:
    s=S[k]; j=max(0,int(t*SR)); n=min(len(s),N-j)
    if n>0: fx[j:j+n]+=s[:n]*g
w=wave.open(os.path.join(M.MO,'voz_total.wav'),'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(vox,-1,1)*32767).astype(np.int16).tobytes()); w.close()
w=wave.open(os.path.join(M.MO,'sfx.wav'),'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(fx*.6,-1,1)*32767).astype(np.int16).tobytes()); w.close()
print('ok',round(DUR,2))

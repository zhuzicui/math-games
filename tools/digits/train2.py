import numpy as np, time, pickle
from gen import make
from scipy.ndimage import gaussian_filter, map_coordinates
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_digits
from PIL import Image
rs=np.random.default_rng(5)
def elastic(x, a=3.0, s=4.0):
    im=x.reshape(28,28); dx=gaussian_filter(rs.uniform(-1,1,(28,28)),s)*a*6; dy=gaussian_filter(rs.uniform(-1,1,(28,28)),s)*a*6
    yy,xx=np.mgrid[0:28,0:28]; return map_coordinates(im,[yy+dy,xx+dx],order=1).ravel()
def reframe(img):  # bbox -> 20px box -> centre, same as app
    a=np.asarray(img,np.float32); ys,xs=np.nonzero(a>0.15)
    if len(xs)==0: return np.zeros(784,np.float32)
    a=a[ys.min():ys.max()+1, xs.min():xs.max()+1]; h,w=a.shape; sc=20/max(h,w)
    p=Image.fromarray((a*255).astype('uint8')).resize((max(1,round(w*sc)),max(1,round(h*sc))),Image.BILINEAR)
    c=Image.new('L',(28,28)); c.paste(p,((28-p.size[0])//2,(28-p.size[1])//2)); return np.asarray(c,np.float32).ravel()/255
dg=load_digits(); R=np.array([reframe(Image.fromarray((im/16*255).astype('uint8')).resize((24,24),Image.BILINEAR)) for im in dg.images]); RY=dg.target
idx=rs.permutation(len(R)); tr,te=idx[:900],idx[900:]
t=time.time()
X,Y=make(6000,seed=21)
Xe=np.array([elastic(x) if rs.random()<.6 else x for x in X])
Xr=np.repeat(R[tr],4,0); Xr=np.array([elastic(x,2,4) for x in Xr]); Yr=np.repeat(RY[tr],4)
XX=np.concatenate([Xe,Xr]); YY=np.concatenate([Y,Yr])
Xt,Yt=make(400,seed=99)
print('data',XX.shape,round(time.time()-t))
for hs in [(192,)]:
    m=MLPClassifier(hidden_layer_sizes=hs,alpha=5e-4,batch_size=256,learning_rate_init=2e-3,max_iter=35,random_state=0)
    m.fit(XX,YY)
    print(hs,'synthetic test',m.score(Xt,Yt),'real held-out',round(m.score(R[te],RY[te]),3),round(time.time()-t))
pickle.dump(m,open('m.pkl','wb'))

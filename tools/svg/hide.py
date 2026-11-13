import json,sys
for sh in sys.argv[1:]:
    W,H,items=json.load(open(f'bb/{sh}.json'))
    hide=[k for k,b,fill,st,sw,tag in items if (b[2]-b[0])*(b[3]-b[1])>0.2*W*H or b[2]<=b[0] or b[3]<=b[1]]
    json.dump(hide,open(f'samp/{sh}.hide.json','w')); print(sh,'hide',len(hide))

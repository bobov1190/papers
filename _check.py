import re,sys,subprocess
f=sys.argv[1]
t=open(r'C:/Users/bobov/Desktop/papers/'+f,encoding='utf-8').read()
scripts=re.findall(r'<script>(.*?)</script>',t,re.S)
js=scripts[-1]
open(r'C:/Users/bobov/Desktop/papers/_tmp.js','w',encoding='utf-8').write(js)
r=subprocess.run(['node','--check',r'C:/Users/bobov/Desktop/papers/_tmp.js'],capture_output=True,text=True)
print('node rc',r.returncode,r.stderr[:600])
for tag in ['div','section','svg','table','details','figure','dl','ul','ol','pre']:
    a=len(re.findall('<'+tag+r'[\s>]',t));b=len(re.findall('</'+tag+'>',t))
    if a!=b: print('MISMATCH',tag,a,b)
ids=set(re.findall(r'id="(w[a-z0-9]+)-svg"',t)); print('widgets',ids)

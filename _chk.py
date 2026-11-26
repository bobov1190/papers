t=open(r'C:/Users/bobov/Desktop/papers/linlesson1.html',encoding='utf-8').read()
i=t.index('<details'); j=t.index('</details>',i)+10
print(t[i-300:j+20])
print('=====')
k=t.index('const NS'); print(t[k-200:k+700])

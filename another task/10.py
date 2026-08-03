n = int(input())
answ = 0

if n>0:
    answ = (1+n)/2*n
    print(int(answ))
elif n<0:
    answ = (1+n)/2*(2-n)
    print(int(answ))
else: print(1)
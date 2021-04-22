import random

cnt = 0
for _ in range(100):
    minuend = random.randint(1, 10)
    subtrahend = random.randint(1, 9)
    if minuend - subtrahend < 0:
        minuend += 10
    else:
        continue
        pass
    diff = minuend - subtrahend
    print(f'{minuend:>2} - {subtrahend} = {diff}')

    enhance = input(f'{minuend:>2} - {subtrahend} = ')
    if diff == enhance:
        cnt += 1

print(f'There are {cnt} correct answer with in 100.')

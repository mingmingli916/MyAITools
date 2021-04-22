import random

cnt = 0
for _ in range(100):
    augend = random.randint(1, 9)
    addend = random.randint(1, 9)

    sum_ = augend + addend
    print(f'{augend:>2} + {addend} = {sum_}')

    enhance = input(f'{augend} + {addend} = ')
    if sum_ == enhance:
        cnt += 1

print(f'There are {cnt} correct answer with in 100.')

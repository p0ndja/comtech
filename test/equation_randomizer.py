import random
import time

LEVEL_FACTOR = 3
RANDOM_SEED = 1234
RANDOM_SEED_FACTOR = 0

def set_seed(sd:int):
    global RANDOM_SEED
    RANDOM_SEED = sd

def set_level(lv:int):
    global LEVEL_FACTOR
    LEVEL_FACTOR = lv

def gen_equation():
    global LEVEL_FACTOR, RANDOM_SEED, RANDOM_SEED_FACTOR
    random.seed(RANDOM_SEED + RANDOM_SEED_FACTOR)
    RANDOM_SEED_FACTOR += 1
    if LEVEL_FACTOR == 1:
        eqa = [random.randint(1,20), ["+","+","+","+","+","-","-","-","-","-","*","/"][random.randint(0,11)], random.randint(1,10)]
        if eqa[0] < eqa[2]:
                eqa = [eqa[2],eqa[1],eqa[0]]
        if not check_hard_lv(eqa, 1):
            return gen_equation()
        return eqa
    elif LEVEL_FACTOR == 2:
        eqa = [random.randint(1,50), ["+","+","+","-","-","-","*","/"][random.randint(0,7)], random.randint(1,50)]
        if eqa[0] < eqa[2]:
                eqa = [eqa[2],eqa[1],eqa[0]]
        if not check_hard_lv(eqa, 2):
            return gen_equation()
        return eqa
    else:
        eqa = [random.randint(1,99), ["+","+","-","-","*","/"][random.randint(0,5)], random.randint(1,99)]
        if eqa[0] < eqa[2]:
                eqa = [eqa[2],eqa[1],eqa[0]]
        if not check_hard_lv(eqa, 3):
            return gen_equation()
        return eqa

def check_hard_lv(eqa,lv):
    x,o,y = eqa
    if o == "/" and y % x != 0:
        return False

    sum = 0
    if o == "+":
        sum = x+y
    elif o == "-":
        sum = x-y
    elif o == "*":
        sum = x*y
    elif o == "/":
        sum = x/y
    else:
        return False

    if (lv == 1 and sum <= 50) or (lv == 2 and (sum <= 200 and sum >= 20)) or (lv == 3 and (sum <= 999 and sum >= 50)):
        return True
    return False

def answer(eqa):
    x,o,y = eqa
    if o == "+":
        return x+y
    elif o == "-":
        return x-y
    elif o == "*":
        return x*y
    elif o == "/":
        return x/y
    else:
        return None

if __name__ == '__main__':
    set_seed(1234)
    set_level(1)
    while True:
        equation = gen_equation()
        print(f"LV: {LEVEL_FACTOR}, SEED: {RANDOM_SEED}, {equation[0]} {equation[1]} {equation[2]} = {answer(equation)}")
        time.sleep(1)

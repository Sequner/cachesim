from configs import *
import random

PATTERNS = ['InOrder', 'Random', 'LimitedRandom']

def isAttacked(attacked, row):
    for i in range(row-2, row+3):
        if i in attacked:
            return True

def generateAttack(rows = W // T_RH, num_req = W, output_dir = 'output.txt', pattern = 'InOrder'):
    assert rows <= W // T_RH
    assert pattern in PATTERNS

    victims = set()
    aggressors = []
    for _ in range(rows):
        row = random.randint(0, MAX_ADDR-1)
        while isAttacked(victims, row):
            row = random.randint(0, MAX_ADDR-1)
        victims.add(row)
        aggressors.append(row-1)
        aggressors.append(row+1)

    victims = list(victims)
    with open(output_dir, 'w') as f:
        requests = 0
        # attacked = [0 for _ in aggressors] # counter for random addrs
        while requests < num_req:
            if pattern == 'InOrder':     # can generate more than num_req requests because of the for loop
                for row in aggressors:      
                    f.write(str(row)+'\n')
                    requests += 1
            elif pattern == 'Random':
                i = random.randint(0, len(aggressors)-1)
                f.write(str(aggressors[i]) + '\n')
                requests += 1
                # attacked[i] += 1
            elif pattern == 'LimitedRandom':
                temp = [i for i in aggressors]
                while temp:
                    i = random.randint(0, len(temp)-1)
                    f.write(str(temp.pop(i)) + '\n')
                    requests += 1
    return victims
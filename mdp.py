LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3
nA = 4  #max no. of actions

s = []
fhand = open('input0.txt')
for line in fhand:
    line = line.rstrip()
    s.append(line)
n = int(s[0])               # grid size
nS = int(n*n)               # space size
s.pop(0)

space = [[0 for i in range(n)] for i in range(n)]   # initializing the grid
m = int(s[0])               # no. of walls
s.pop(0)
w = None

for i in range(m):
    x,y = s[0].split(',')
    space[int(x)-1][int(y)-1] = w       # wall coordinates
    s.pop(0)
t = int(s[0])                           # no. of terminal states
s.pop(0)

for i in range(t):
    x,y,rew = s[0].split(',')
    space[int(x)-1][int(y)-1] = float(rew)      #termianl states' coordinates
    s.pop(0)

p1 = float(s[0])                        # P
p2 = (1-p1)/2                           # (1-P)/2
r = int(s[1])
gamma = float(s[2])                     # gamma
epsilon = 0.001                          # epsilon
theta = epsilon*(1-gamma)/gamma

for i in range(n):                      # filling each cell with repective rewards
    for k in range(n):
        if space[i][k] == 0:
            space[i][k] = r

P = {s : {a : [] for a in range(nA)} for s in range(nS)} # initializing Probability matrix i.e Transition model

def to_s(row, col):             # converts the addreses into state number
    return row*n + col

def shift(row, col, a):         # shifting in a particular direction
    if a == LEFT:
        return (row, col-1)
    elif a == DOWN:
        return (row+1, col)
    elif a == RIGHT:
        return (row, col+1)
    elif a == UP:
        return (row-1, col)

def check(x,y):                 # to check if a particular address/state is in the limits of grid
    if x>=0 and y>=0 and x<n and y<n:
        return True
    else:
        return False

def get_prob(row,col,move,yes):     #returns the (prob, new_state) for a particular action
    if move == LEFT:                # in each direction checking the other two 45 degree cells
        dir1 = UP
        dir2 = DOWN
    if move == DOWN:
        dir1 = LEFT
        dir2 = RIGHT
    if move == RIGHT:
        dir1 = UP
        dir2 = DOWN
    if move == UP:
        dir1 = LEFT
        dir2 = RIGHT
    temp = []                         #contains (probability, new state)
    x,y = shift(row,col,move)
    if check(x,y):                    #check if move is valid
        p,q = shift(x,y,dir1)         #either UP or LEFT
        r,s = shift(x,y,dir2)         #either DOWN or RIGHT
        if yes[x][y] != w :
            temp.append((p1,to_s(x,y),yes[x][y]))       # append(probability, new_state, reward)
        if check(p,q) == True and yes[p][q] != w:
            temp.append((p2,to_s(p,q),yes[p][q]))
        if check(r,s) == True and yes[r][s] != w:
            temp.append((p2,to_s(r,s),yes[r][s]))
        sum = 0
        for i,k,j in temp:
            sum += i
        if float(sum) != 1.0:          #in case of existence of Wall or Invalid cell in any direction staying in same cell
            temp.append((1-sum,to_s(row,col),yes[row][col]))
    else:
        temp.append((1,to_s(row,col),yes[row][col]))
    return temp                       #returns a list of (probabilities, new state)

w_list = []
exit_list = []
for row in range(n):                  # filling the Transition model P
    for col in range(n):
        if space[row][col] != w and space[row][col] != r:
            exit_list.append(to_s(row,col))
        if space[row][col] == w:
            w_list.append(to_s(row,col))
            continue
        else:
            s = to_s(row,col)
            for a in range(4):
                li = P[s][a]
                temp = get_prob(row,col,a,space)
                for prob, new_state, rew in temp:
                    li.append((prob,new_state,rew))

def look_ahead(state, V):                       # for extracting optimal action
    A = [0 for i in range(nA)]
    for a in range(nA):
        for prob, next_state, reward in P[state][a]:
            A[a] += prob * (reward + gamma * V[next_state])
    return A

V = [0 for i in range(nS)]                      #Value iteration
while True:
    delta = 0
    for s in range(nS):
        A = look_ahead(s, V)
        best_action_value = max(A)
        delta = max(delta, abs(best_action_value - V[s]))
        V[s] = best_action_value
    if delta < theta:
        break

policy = [[0 for k in range(nA)]for i in range(nS)]         #extracting optimal policy
for s in range(nS):
    A = look_ahead(s, V)
    best_action = A.index(max(A))
    policy[s][best_action] = 1

d = {0:'L',1:'D',2:'R',3:'U'}                               # filling optimal moves for each state/cell
final = []
for i in policy:
    final.append(d[i.index(1)])

temp = []
pos = 0
while pos<len(final):
    z = []
    start = pos
    for i in range(start,start+n):
        if i in exit_list:
            final[i] = 'E'
        if i in w_list:
            final[i] = 'N'
        z.append(final[i])
        pos += 1
    temp.append(','.join(z))

for i in temp:
    print(i)

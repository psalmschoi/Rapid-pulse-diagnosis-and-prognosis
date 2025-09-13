
def get_path(num) :
    n = num - 1
    
    path = ''
    for i in range(4) :
        n, mod = divmod(n, 3)
        
        if mod == 0 :
            path = path + 'M'
        elif mod == 1 :
            path = path + 'D'
        else :
            path = path + 'H'
            
    path = (path + 'D')[::-1]
    
    return path

def get_num(path):
    path = path[1:][::-1]
    num = 1
    for i, p in enumerate(path):
        if p == 'M':
            pass
        elif p == 'D':
            num += 3**i
        elif p == 'H':
            num += 2 * 3**i
    return num

if __name__ == '__main__':
    for n in range(1, 82, 1):
        path = get_path(n)
        _n = get_num(path)
        if n != _n:
            print(n, _n)
    print("Run Main Finished")
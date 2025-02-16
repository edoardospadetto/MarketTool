
def go_down(obj,leafPath):
    a=obj
    for p in leafPath:
        if(a):
            if(isinstance(p, int) and len(a)>p):
                a = a[p]
            elif(isinstance(p, str) and p in a.keys()):
                a = a[p]
            else:
                return(None)
    return(a)

def find_path(json,mystring):
    a=json
    leafPath1=[]
    keys=[]
    again = True
    while(again):
        again = False
        if isinstance(a, dict):
            keys=list(a.keys())
        else:
            keys=[i for i in range(len(a))]
        #print(keys)
        for key in keys:
            if(mystring in str(a[key])):
                leafPath1.append(key)
                a = a[key]
                again = True
                break
    return(leafPath1)

from speedsense.tc_estimator import compute_complexity
import inspect
def findprimes(x):
    primecount=0
    for i in range(2,x):
        factors=0
        for j in range(2,i):
            if i%j==0:
                factors+=1
        if factors==2:
            primecount+=1
    return primecount


test_code = inspect.getsource(findprimes)
compute_complexity(test_code)

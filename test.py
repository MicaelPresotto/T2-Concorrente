
def divide_jobs(jobs, number):
    division = []
    number_jobs = len(jobs)
    q = number_jobs // number
    r = number_jobs % number
    start = 0
    for _ in range(number):
        k = q
        if r:
            r -= 1
            k += 1
        division.append(jobs[start:start+k])
        start += k
    return division[:]

print(divide_jobs([1,2,3,4,5,4,2], 3))
import random
import math

# scale down ms values to number of slots
SCALE_FACTOR = 51.2

# 1e+5 simulations run when calculation contention interval
N_SIMULATIONS = 100000


# When computing minimum, test all values of lambda that are integers from 30-200 inclusive.
#
# Change these to (100, 0.1, 120) for a more accurate reading of the best lambda value, because 
# it is known that the best lambda value is usually in the range [108, 115].
#
# Leave this as is if you only want the minimum contention interval, the 
# large range of values maintains the integrity of the test, but does not test 
# values that are too small (< 30) to keep running time low. Also good to see the trend
# by uncommenting line 33, and seeing the contention interval at all these lambda values.
MIN_LAMBDA = 100
LAMBDA_INCREMENT = 0.1
MAX_LAMBDA = 120


# gets the contention intervals of a range of lambda values to find 
# the minimum contention interval and the lambda value that invoked it.
def getMinimumContentionInterval():
    min = float(sys.maxsize)
    min_lam = MAX_LAMBDA + 1

    lam = MIN_LAMBDA
    while(lam <= MAX_LAMBDA):
        curr = getContentionInterval(lam)
        # print("Lambda = " + str(lam) + "\t:: " + str(curr))
        if curr < min:
            min = curr
            min_lam = lam
        lam += LAMBDA_INCREMENT

    return min, min_lam


# runs 1e+5 simulations for a given value of lambda and averages the intervals 
# to return the contention interval.
def getContentionInterval(lam):
    avg = 0
    for i in range(N_SIMULATIONS):
        avg = avg * (i/(i+1)) + simulate(lam)/(i+1)
    return avg


# attempts randomly timed transmissions until a successful transmission is confirmed,
# returns the number of time slots until the successful transmission.
def simulate(lam):
    # initialize time (code units)
    time = 0

    while(1):
        # attempt ith transmission
        time, success = transmit(lam, time)

        # check next transmission on success
        if success:
            # save a copy of ith transmissions time
            time_i = time

            # attempt i+1th transmission
            time, success = transmit(lam, time)

            # check that the ith transmission is indeed a success
            if success:
                return time_i


# calculates x and new time given lambda, returns new time 
# and whether it collides the previous transmission
def transmit(lam, time):
    # compute x
    u = random.uniform(0, 1)
    x = -1 * lam * math.log(u)

    # t is the time of this transmission in code units
    t = time + x/SCALE_FACTOR

    # return time of this transmission, and whether it collides
    return t, t - 1 > time


if __name__ == "__main__":
    import os, sys

    # input validation
    if (len(sys.argv) != 2):
        print("Usage:	" + os.path.basename(__file__) + " lambda")
        sys.exit(2)
    try:
        lam = float(sys.argv[1])
    except ValueError:
        print("Please enter a real number.")
        sys.exit(2)
    if lam <= 0:
        print("Please enter a positive number.")
        sys.exit(2)

    # start simulation
    print("\nWith lambda = " + str(lam) + " :")
    print("Contention Interval =\t" + "{:.5f}".format(getContentionInterval(lam)) + " slot times")
    min, min_lam = getMinimumContentionInterval()
    print("Minimum Contention Interval =\t" + "{:.5f}".format(min) + " slot times\tat lambda = " + str(min_lam) + "\n")
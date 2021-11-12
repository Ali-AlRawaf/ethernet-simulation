# Run it! #

1. Navigate to the directory containing simulate.py
2. `python simulate.py 100.23`

# Implementation #
*Note: time is maintained in this program as the accumulation of random transmission waiting times. The unit is slot time, where each slot time is equivalent to 51.2 ms*

`transmit(lam, time)`

- expects a float value for `lam` and `time`
- gets a random value `u` between 0 and 1 using math.random, which uses Mersenne Twister as its RNG
- calculates a random amount of milliseconds using formula `x = -lam * log(u)`, and scales `x` down to slot times
- returns the new time value `t = time + x`, and whether a transmission at `t` would collide with the last transmission, which occured at `time`

`simulate(lam)`
    
- expects a float value for `lam`
- attempts transmissions until a transmission was made that doesn't collide the transmission before and after it
- the assignment guidelines says that we want to find a transmission that occured at time `t` where there are no other transmissions in time interval [t-1, t+1]
- this is equivalent to finding a transmission `trans_i` that doesn't collide the one before it, and checking that the transmission after `trans_i` doesn't collide `trans_i`, because this means that there are no other transmissions within 1 slot time from `trans_i` since we checked the immediate neighbors of `trans_i`
- this function behaves exactly as described above, and maintains the accumulating time of the simulation
- returns the time of the successful transmission

`getContentionInterval(lam)`

- expects a float value for `lam`
- calculates the average time-until-success of 100000 simulations with lambda = `lam`
- returns this average, which is indeed the contention interval

`getMinimumContentionInterval()`

- calculates the contention interval of many different values of lambda
- more specifically, tests every value of lambda that is an integer in [30, 200]
- returns the minimum contention interval computed, and which value of lambda invoked this minimum
- see comments above the constants `MIN_LAMBDA`, `LAMBDA_INCREMENT`, `MAX_LAMBDA` defined in simulate.py for insight on how to modify these values and the rationale behind the selection

# Question #

The Ethernet alternates between contention intervals and successful transmissions. Suppose the average transmission lasts 8 slot times (512 bytes). Using the minimum length of the contention interval determined before, calculate what fraction of the theoretical 10-Mbps bandwidth is available for transmissions?

The minimum contention interval that I consistently observed is about 5.7 slot times. Every 8 + 5.7 = 13.7 slot times, we have 5.7 slot times available for transmission. The fraction available is 5.7/13.7 = 0.416. 41.6% of the bandwidth is available for transmission.
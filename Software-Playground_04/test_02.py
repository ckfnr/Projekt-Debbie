# Decorators
from env.decr.decorators import cached

@cached
def slow_function(x: int) -> int:
    print(f"Computing for {x}...")  # Will only print when computation happens
    return x * 2

# Call with 50 different values (fills cache)
for i in range(50):
    slow_function(i)

# Call a cached value (should NOT print "Computing for X...")
slow_function(10)  

# Call a new value (triggers eviction of an old one)
slow_function(51)  

# Call an old value that was likely evicted (should compute again)
slow_function(0)  
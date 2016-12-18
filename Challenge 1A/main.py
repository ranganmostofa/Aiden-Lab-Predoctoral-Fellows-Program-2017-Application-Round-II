import argparse


def main():
    """
    Driver function that sets up a command line argument parser to receive inputs
    specific to Challenge 1A and outputs the result from the solution to this challenge
    using these inputs from the argument parser
    """
    # initialize a command line argument parser and store a description of what this python file accomplishes
    parser = argparse.ArgumentParser(description='Given a target value (integer) and a list of bucket sizes '
                                                 '(list of integers), returns true if the bucket sizes can be used to '
                                                 'reach the target value and returns false otherwise')

    # all inputs except the last are handled by a list, i.e. the list of bucket sizes
    parser.add_argument('bucket_sizes', nargs='+', type=int, help='A list of integers representing the bucket sizes')
    # last input is handled by an integer, i.e. the target value
    parser.add_argument('target_value', type=int, help='An integer representing the target value')

    args = parser.parse_args()  # parse the arguments passed into the command line

    print is_reachable(args.target_value, args.bucket_sizes)  # solve challenge using arguments provided at command line


def is_reachable(target_value, bucket_sizes):
    """
    Given a target value (integer) and a list of bucket sizes (list of integers),
    returns true if the bucket sizes can be used to reach the target value and
    returns false otherwise
    """
    if len(bucket_sizes) == 0:  # if there are no bucket sizes are provided
        return "No bucket sizes have been provided."
    elif len(bucket_sizes) == 1:  # if there is only one bucket size available
        return not target_value % bucket_sizes[0]  # return true if the target size is divisible by the bucket size
    else:  # otherwise
        if is_divisible(target_value, bucket_sizes):  # if the target size os divisible by any of the bucket sizes
            return True  # return True
        sorted_bucket_sizes = list(bucket_sizes)  # create a different list of bucket sizes
        sorted_bucket_sizes.sort()  # sort the new list of bucket sizes in ascending order
        divisor = sorted_bucket_sizes[0]  # get the smallest bucket size
        remainder = target_value  # store the target value in the remainder
        remaining_bucket_sizes = list(bucket_sizes)
        remaining_bucket_sizes.remove(divisor)  # create a new list of bucket sizes not containing the smallest one
        while divisor < remainder:  # as long as the remainder is greater than the divisor
            remainder -= divisor  # take away the divisor from the remainder one at a time
            # use the remainder as the new target size and remaining list of bucket sizes as the parameters to a
            # simplified problem, the solution of which, is the solution to the original problem
            # (check attached files for a more thorough explanation)
            if is_reachable(remainder, remaining_bucket_sizes):
                return True  # return True if the answer to the simplified problem above is True
    return False  # if all cases have failed return False


def is_divisible(target_value, bucket_sizes):
    """
    Given a target value (integer) and a list of bucket sizes (list of integers),
    returns true if the target value is divisible by at least one of the bucket sizes
    and returns false otherwise
    """
    for bucket_size in bucket_sizes:  # for every bucket size
        if not target_value % bucket_size:  # if target value is divisible
            return True  # return True
    return False  # return False otherwise


main()  # call main


# UNCOMMENT TEST SUITE BELOW TO TEST

"""

# TEST SUITE

# Test 1:

bucket_sizes = [5, 7]
target_value = 5

print "Test 1"
print
print "target_value = " + str(target_value)
print
print "bucket_sizes = " + str(bucket_sizes)
print
print "Implementation Output: " + str(is_reachable(target_value, bucket_sizes))
print
print "Expected Output: " + str(True)
print

# Test 2:

bucket_sizes = [5, 7]
target_value = 33

print "Test 2"
print
print "target_value = " + str(target_value)
print
print "bucket_sizes = " + str(bucket_sizes)
print
print "Implementation Output: " + str(is_reachable(target_value, bucket_sizes))
print
print "Expected Output: " + str(True)
print

# Test 3:

bucket_sizes = [5, 7]
target_value = 9

print "Test 3"
print
print "target_value = " + str(target_value)
print
print "bucket_sizes = " + str(bucket_sizes)
print
print "Implementation Output: " + str(is_reachable(target_value, bucket_sizes))
print
print "Expected Output: " + str(False)
print

# Test 4:

bucket_sizes = [2, 11]
target_value = 9

print "Test 4"
print
print "target_value = " + str(target_value)
print
print "bucket_sizes = " + str(bucket_sizes)
print
print "Implementation Output: " + str(is_reachable(target_value, bucket_sizes))
print
print "Expected Output: " + str(False)
print

# Test 5:

bucket_sizes = [2, 9, 17]
target_value = 19

print "Test 5"
print
print "target_value = " + str(target_value)
print
print "bucket_sizes = " + str(bucket_sizes)
print
print "Implementation Output: " + str(is_reachable(target_value, bucket_sizes))
print
print "Expected Output: " + str(True)
print

# Test 6:

bucket_sizes = []
target_value = 19

print "Test 6"
print
print "target_value = " + str(target_value)
print
print "bucket_sizes = " + str(bucket_sizes)
print
print "Implementation Output: " + str(is_reachable(target_value, bucket_sizes))
print
print "Expected Output: " + "No bucket sizes have been provided."
print

"""



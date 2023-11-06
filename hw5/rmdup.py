# removes duplicates from data.
# This function keeps the last occurence of each element
# and preserves order.
# So rmdup([1,2,3,2,1,4,2]) should return [3,1,4,2]
def rmdup(data):
    # Write me
    last_occur = []

    # reverse the data array
    for element in reversed(data):
        # if this element not record yet, record
        if element not in last_occur:
            last_occur.append(element)

    # return the reverse of the recording array
    last_occur.reverse()
    return last_occur

data = [1,2,3,2,1,4,2]
result = rmdup(data)
print(result)


        

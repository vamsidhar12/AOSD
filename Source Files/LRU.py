# Python3 implementation of FIFO page
# Page replacement in Operating Systems.


# Function to find page faults using FIFO
def pageFaults(pages, n, capacity):
    # To represent set of current pages. We use an unordered_set so that we quickly check if a page is present in set or not.

    S = []
    # To store the pages in LRU manner

    count = 0
    page_faults = 0;
    # Start from initial page
    for i in range(n):
        if pages[i] not in S:
            # Check if the set can hold more pages
            if len(S) == capacity:
                # Insert it into set if not present already which represents page fault
                S.remove(S[0])
                # Pop the first page from the queue
                S.insert(capacity - 1, pages[i])
                # insert the current page
            else:
                S.insert(count, pages[i])
                # Push the current page into the queue
            page_faults += 1
            # increment page fault
            count += 1
        else:
            S.remove(pages[i])
            S.insert(len(S), pages[i])
    return page_faults


# Driver code
if __name__ == '__main__':
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    n = len(pages)
    capacity = 4
    PageFaults = pageFaults(pages, n, capacity)
print("The number of page faults occurred by LRU algorithm are: ", PageFaults)

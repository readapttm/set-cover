import pandas as pd
from queue import PriorityQueue
import os

## Input
# Family F of m sets Si - dictionary with set name as key and items as values

## Output
# Collection of set names which together contain all items a minimal number of times

# Create dictionary to hold sets
set_dict = dict()

# Create saving directory if it doesn't exist already
results_dir = 'results'

if results_dir not in os.listdir():
    os.mkdir(results_dir)

## Load set data
data_dir = 'datasets'
set_data = pd.read_csv(f'{data_dir}/set_data_20_1000.csv', dtype = {'set_id': object, 'member_id': object})
set_data['set_id'].nunique() # 1,000
set_data['member_id'].nunique() # 1,000

# Build set dictionary from dataframe
for i in range(set_data.shape[0]):
    set_id = set_data['set_id'][i]
    member_id = set_data['member_id'][i]

    if set_id in set_dict.keys():
        set_dict[set_id].add(member_id)
    else:
        set_dict[set_id] = set([member_id])

# Remove set_adata (not needed)
del set_data

# Define function to determine minimum collection of sets for full coverage
def set_cover(set_dict: dict) -> list:

    """
    This function finds the smallest set of set_ids containing all member_ids accross all sets

    Args:
        set_dict (dict): dictionary with set_id as keys and member_ids as values.

    Returns:
        list: minimal collection of set_ids

    """

    A = [] # List of sets containing members in the covering set - the target output
    U = set() # member universe, populated below
    covered = set() # Members in universe that are covered
    pqueue = PriorityQueue() # Structure to sort sets by priority to add

    # Build universe of member_ids
    for _, value in set_dict.items():
        U = U.union(value) 

    # Build priority queue
    for key, value in set_dict.items():
        pqueue.put(tuple((-len(U.intersection(value)), key))) # Use negative values as priority queue sorts by minimum (based on a heap)

    # Print queue length (number of sets) and universe size (total members)
    print("queue length: " + str(pqueue.qsize()))
    print("Universe Size: " + str(len(U)))

    # While coverage not full
    while covered != U:
        
        # Deque set that contributes most to coverage
        (mem_id, set_id) = pqueue.get() # mem_id is the number of uncovered members on set with label set_id
        Si = set_dict[set_id] # Get set of members
        Si_rem = Si.difference(covered) # Calculate difference with already covered members

        if Si_rem == Si: # If none of the membets are found in the covered set
            A += [set_id] # Add set to A
            covered = covered.union(Si) # Add members to covered set
        else: # If some of the members are found in the covered set
           set_dict[set_id] = Si_rem # Update the set with only the members outside the covered set
           pqueue.put(tuple((-len(U.intersection(Si_rem)), set_id))) # Recalculate the priority based on members outside covered set
      
    return A

# Determine minimum collection of sets
min_sets = set_cover(set_dict)

# Save as csv
df = pd.DataFrame(min_sets, columns = ['set_id'])
df.to_csv('min cover sets.csv')

# Print number of required sets
print("Required number sets:" + str(len(min_sets))) # approx 10% of the total number of sets 
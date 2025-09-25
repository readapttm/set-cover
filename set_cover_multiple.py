import pandas as pd
import os
from queue import PriorityQueue
import seaborn as sns

## Input
# Family F of m sets Si - dictionary with set name as key and items as values

## Output
# Collection of set names which together contain all items a minimal number of times

#set_data['set_id'].nunique() # 1,000
#set_data['member_id'].nunique() # 1,000


def build_set_dict(set_data: pd.core.frame.DataFrame) -> dict:

    """
    This function convert set data (with each member defined by its member_id and the set_id 
    it belongs to) stored as dataframes to dictionary form

    Args:
        set_data (pandas dataframe): dataframe with two columns specifying set_id and member_id.

    Returns:
        dict: data reorganised as a dictionary with set_id as keys and member_ids as values

    """
    
    # Create dictionary to hold sets
    set_dict = dict()

    # Build set dictionary from dataframe
    for i in range(set_data.shape[0]):
        set_id = set_data['set_id'][i]
        member_id = set_data['member_id'][i]

        if set_id in set_dict.keys():
            set_dict[set_id].add(member_id)
        else:
            set_dict[set_id] = set([member_id])
        
    return set_dict

# Define function to determine minimum set of albums
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

    # Build track universe
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


## Run analysis

# List datasets
data_dir = 'datasets'
set_files = os.listdir(data_dir)

# Create saving directory if it doesn't exist already
results_dir = 'results'

if results_dir not in os.listdir():
    os.mkdir(results_dir)

# Gather results
results_df = pd.DataFrame()

# Loop through each file
for d in set_files:

    ## Load set data
    set_data = pd.read_csv(f'{data_dir}/{d}', dtype = {'set_id': object, 'member_id': object})

    ## Convert to dictionary form
    set_dict =  build_set_dict(set_data) 

    # Remove set_data (not needed)
    del set_data

    # Determine minimum collection of sets
    min_sets = set_cover(set_dict)

    # Store parameters and results
    results_dict = {'set_size': int(d.split('_')[-2]),
                    'unique_members': int(d.split('_')[-1].split('.')[0]),
                    'required_sets': len(min_sets)}

    results_df = pd.concat([results_df, pd.DataFrame(results_dict, index=[0])])

    print(f'Dataset {d} processed.')

# Save results as csv
results_df.sort_values(['set_size', 'unique_members'], inplace=True)
results_df.to_csv(f'{results_dir}/min_sets_by_size_cardinality.csv')

## Create summary chart
p = sns.scatterplot(data = results_df, x = 'unique_members', y = 'required_sets', hue = 'set_size')
p.set_xlabel('Cardinality (over all sets)')
p.set_ylabel('Minimum Required Sets for Complete Coverage')
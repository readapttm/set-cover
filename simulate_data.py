import pandas as pd
import random
import os

# To create a dataset of sets

## Sample the numbers 1 to {unique_members} without replacement in groups of {set_size}, {total_sets} times
## Label each sample with the number 1 to {total_sets}
## Store in data frame
## Repeat for different sets of parameters to explore the effect of set_size and unique_members

## Initialise parameters (this combination generates 2000 rows)
set_size = [1, 2, 5, 10, 20, 50, 100] # 20
unique_members = [10, 20, 50, 100, 200, 500, 1000] # 1000
total_sets = 1000

# Create saving directory if it doesn't exist already
dataset_dir = 'datasets'

if dataset_dir not in os.listdir():
    os.mkdir(dataset_dir)


# Fix the seed for reproducibility
set.seed(1)

## Function to build collections of sets
def build_sets(set_size: int, unique_members: int, total_sets: int) -> pd.core.frame.DataFrame:

    """
    This function builds a collection of sets containing members defined by set_id and member_id

    Args:
        set_size (int): the number of elements to add to each set
        unique_members (int): the total number of unique items in the universe
        total_sets (int): how many sets to generate

    Returns:
        pd.core.frame.DataFrame: contains all sets and members

    """
    
    ## Initialse dataframe
    all_sets = pd.DataFrame()

    ## Check if sampling without replacement is possible given avaiable unique values
    try:
        assert unique_members >= set_size
    
    except AssertionError:
        # Return empty sets
        return all_sets 

    ## Create dataset containing a total of {total_sets} sets
    for i in range(total_sets): 

        # Sample {set_size} members of the list 1 to unique_members
        set_data = {'set_id': [i+1]*set_size, 
                    'member_id': random.sample(range(1, unique_members+1),
                                            set_size)} 
        
        # Concatenate all generated sets
        all_sets = pd.concat([all_sets, pd.DataFrame(set_data)]) 
    
    return all_sets

## Create collections for each combination of parameters
for s in set_size:
    for u in unique_members:
        print(f'Building: set_size {s}, unique members {u}')
        all_sets = build_sets(s, u, total_sets)

        ## Save dataset
        if len(all_sets) > 0:
            all_sets.to_csv(f'{dataset_dir}/set_data_{s}_{u}.csv', index=False)



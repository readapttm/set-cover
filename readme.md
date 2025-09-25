# Solving the set cover problem

The set cover is a classical combinatorial problem with many real world applications. In simple terms, the goal is to take a collection of many assortments (sets) of items and determine which is the smallest subset of assortments that contains all unique items in the 'item universe' at least once. Each assortment usually contains only one copy of each item (although this isn't crucial) but typically contains only a subset of all possible items. Let's illustrate with some real world examples:

- Say in your CD collection (old skool, I know), you have many overlapping music compilation albums. Which is the minimal collection of CDs you should take on holiday (the minimal set that contains all the tracks you want but takes up the least physical space)?
- Logistics: Where should we place delivery depots to cover all addresses?
- Staffing/personnel: Which is the smallest group of people that possess all necessary skills for a task?

# Problem statement
Input: A collection of sets containing unique items. The same item can occur in multiple sets.
Output: The smallest set of sets that contain all unique items.

# Scripts provided

1: simulate_data.py - takes 3 parameters and generates a collection of datasets. Parameter list:

set_size - a list containing a range of values for the size of each assortment.

unique_members - a list containing a range of values for the total number of unique items in the universe.

total_sets - an integer specifying the number of assortments to randomly generate from the universe when building a given dataset. This is kept at a default value of 1000.

The datasets are saved as pandas dataframes.


2: set_cover_example.py - solves the problem for a single dataset and returns the minimal collection of sets for full coverage (i.e. the solution)


3: set_cover_multiple.py - solves the problem for multiple datasets, each specified by the parameters above.

Running this script should produce the following chart:

![](/charts/summary_chart.png)


N.B. This script implements a lazy implementation of the greedy solution to the set cover problem as outlined in algorithm 3 in the following publication: https://people.eng.unimelb.edu.au/ammoffat/abstracts/lmw14acsc.pdf. 


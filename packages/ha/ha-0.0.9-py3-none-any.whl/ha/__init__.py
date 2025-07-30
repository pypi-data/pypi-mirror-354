"""Joke access and generation tools"""
from ha.vendors import *  # what is imported will depend on what tools are installed
from ha.dataset import joke_datasets, all_jokes_store





# Additional utility functions for the 'ha' package to enhance interaction with joke datasets

def search_jokes(keyword, datasets=None):
    """
    Search for jokes containing a specific keyword across specified joke datasets.
    
    Args:
    keyword (str): The keyword to search for within the jokes.
    datasets (list, optional): List of dataset names to search within. If None, searches all available datasets.
    
    Returns:
    dict: A dictionary with keys as dataset names and values as lists of jokes containing the keyword.
    
    Example:
    >>> search_jokes('chicken', ['reddit_jokes'])
    {'reddit_jokes': [{'id': '5tdwk4', 'title': 'Why did the chicken cross the road?', 'body': 'Why did the chicken cross the road? ...', 'score': 1}]}
    """
    if datasets is None:
        datasets = joke_datasets.keys()
    
    result = {}
    for dataset_name in datasets:
        if dataset_name in joke_datasets:
            jokes = joke_datasets[dataset_name]
            filtered_jokes = [joke for joke in jokes if keyword.lower() in joke['body'].lower()]
            if filtered_jokes:
                result[dataset_name] = filtered_jokes
    
    return result

def random_joke_from_dataset(dataset_name):
    """
    Retrieve a random joke from a specified dataset.
    
    Args:
    dataset_name (str): The name of the dataset from which to retrieve a joke.
    
    Returns:
    dict: A random joke from the specified dataset.
    
    Example:
    >>> random_joke_from_dataset('reddit_jokes')
    {'id': '5tdwk4', 'title': 'Why did the chicken cross the road?', 'body': 'Why did the chicken cross the road? ...', 'score': 1}
    """
    import random
    if dataset_name in joke_datasets:
        return random.choice(joke_datasets[dataset_name])
    else:
        raise ValueError(f"No dataset found with the name {dataset_name}")

def top_jokes_from_dataset(dataset_name, top_n=10):
    """
    Retrieve the top N jokes from a specified dataset based on score.
    
    Args:
    dataset_name (str): The name of the dataset.
    top_n (int): Number of top jokes to retrieve based on score.
    
    Returns:
    list: A list of the top N jokes from the specified dataset.
    
    Example:
    >>> top_jokes_from_dataset('reddit_jokes', top_n=5)
    [{'id': '5tdssi', 'title': 'What is Politics?', 'body': 'A little boy goes to his dad and asks, ...', 'score': 123}]
    """
    if dataset_name in joke_datasets:
        jokes = sorted(joke_datasets[dataset_name], key=lambda x: x['score'], reverse=True)
        return jokes[:top_n]
    else:
        raise ValueError(f"No dataset found with the name {dataset_name}")




def joke_count_by_dataset():
    """
    Count the number of jokes available in each dataset.
    
    Returns:
    dict: A dictionary with keys as dataset names and values as the count of jokes in each dataset.
    
    Example:
    >>> joke_count_by_dataset()
    {'reddit_jokes': 194553, 'stupidstuff': 3773, 'wocka': 10019}
    """
    return {dataset_name: len(jokes) for dataset_name, jokes in joke_datasets.items()}

def search_jokes_by_score(keyword, min_score, datasets=None):
    """
    Search for jokes containing a specific keyword across specified joke datasets that have a score above a given threshold.
    
    Args:
    keyword (str): The keyword to search for within the jokes.
    min_score (int): Minimum score that the joke must have to be included in the results.
    datasets (list, optional): List of dataset names to search within. If None, searches all available datasets.
    
    Returns:
    dict: A dictionary with keys as dataset names and values as lists of jokes containing the keyword and having a score above the specified minimum.
    
    Example:
    >>> search_jokes_by_score('chicken', 10, ['reddit_jokes'])
    {'reddit_jokes': [{'id': '5tdwk4', 'title': 'Why did the chicken cross the road?', 'body': 'Why did the chicken cross the road? ...', 'score': 12}]}
    """
    if datasets is None:
        datasets = joke_datasets.keys()
    
    result = {}
    for dataset_name in datasets:
        if dataset_name in joke_datasets:
            jokes = joke_datasets[dataset_name]
            filtered_jokes = [joke for joke in jokes if keyword.lower() in joke['body'].lower() and joke['score'] >= min_score]
            if filtered_jokes:
                result[dataset_name] = filtered_jokes
    
    return result

def all_jokes_sorted_by_score(reverse=True):
    """
    Retrieve all jokes from all datasets sorted by score.
    
    Args:
    reverse (bool): If True, sort in descending order; otherwise, in ascending order.
    
    Returns:
    list: A list of all jokes from all datasets sorted by their score.
    
    Example:
    >>> all_jokes_sorted_by_score()[:3]
    [{'id': '5tdssi', 'title': 'What is Politics?', 'body': 'A little boy goes to his dad and asks, ...', 'score': 123},
     {'id': '5tdsmb', 'title': 'A teacher asked her students...', 'body': 'A teacher asked her 4th grade students a ...', 'score': 40},
     {'id': '5tdwk4', 'title': 'Why did the chicken cross the road?', 'body': 'Why did the chicken cross the road? ...', 'score': 1}]
    """
    all_jokes = []
    for jokes in joke_datasets.values():
        all_jokes.extend(jokes)
    return sorted(all_jokes, key=lambda x: x['score'], reverse=reverse)

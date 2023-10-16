# https://cs50.harvard.edu/ai/2020/projects/2/pagerank/

import os
import random
import re
import sys

DAMPING = 0.85           # decides the amt of prob. to split for the linked pages
SAMPLES = 10000
# corpus : a dict. which maps page_name to the set of all links that points to that page.

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
        
    corpus = crawl(sys.argv[1])      # return a dictionary of those page_ranks

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)       # Samples : cluster of all html pages     || *need to give the same output dict.
    print(f"PageRank Results from Sampling (n = {SAMPLES})")

    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)    #Ctrl + hover
    print(f"PageRank Results from Iteration")

    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")  # *same when given the same corpus//cluster


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each "KEY is a page", and "VALUES are
    a list of all other pages in the corpus that are linked to by the page".
    """
    pages = dict()   # create a dict.

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):     # skip if its not .html
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prop_dist = {}          # which all the 

    # check if page has outgoing links : which links other pages
    dict_len = len(corpus.keys())
    pages_len = len(corpus[page])

    if len(corpus[page]) < 1:
        # no. outgoing pages, choosing randomly from all possible pages
        for key in corpus.keys():
            prop_dist[key] = 1 / dict_len

    else:
        # If there are outgoing pages => calculating distribution//prop.
        random_factor = (1 - damping_factor) / dict_len          # 0.15 / no. of links\\pages
        even_factor = damping_factor / pages_len             # 0.85 / no. of pages

        for key in corpus.keys():
            if key not in corpus[page]:         # if the page is not found
                prop_dist[key] = random_factor    # putting some page in place of that
            else:
                prop_dist[key] = even_factor + random_factor          # this just going to give a prob.(decimal) ???

    return prop_dist

    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # prepare a dict with len equal to sample but values are all zero.
    sample_dict = corpus.copy()
    for i in sample_dict:
        sample_dict[i] == 0

    sample = None        # Cluster of htmls  

    # itearting n times
    for _ in range(n):
        if sample:
            # previous sample is available, choosing using transition model
            dist = transition_model(corpus, sample, damping_factor)           
            dist_lst = list(dist.keys())              # we remove keys(aka pages) from dict 
            dist_weights = [dist[i] for i in dist]       # we remove values(aka links) from dict   
            sample = random.choices(dist_lst, dist_weights, k=1)[0]
            # the prop. of choosing each page and with that link, is also baised(weights)

        else:
            # no previous sample, choosing randomly
            sample = random.choice(list(corpus.keys()))       # its a list of page_name.

        # count each sample   ??
        sample_dict[sample] += 1

    # turn sample count to percentage
    for item in sample_dict:
        sample_dict[item] /= n

    return sample_dict

    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages_number = len(corpus)
    old_dict = {}
    new_dict = {}

    # assigning each page a rank of 1/n, where n is total number of pages in the corpus       
    for page in corpus:              # Just giving intial prob. to pages
        old_dict[page] = 1 / pages_number

    # repeatedly calculating new rank values basing on all of the current rank values
    while True:
        for page in corpus:
            temp = 0
            for linking_page in corpus:#@  @
                # check if page links to our page

                if page in corpus[linking_page]: #@  @
                    temp += (old_dict[linking_page] / len(corpus[linking_page]))  # len(...) : len of the links in that page.
                
                # if page has no links, interpret it as having one link for every other page
                if len(corpus[linking_page]) == 0:
                    temp += (old_dict[linking_page]) / len(corpus) #len(...) : len(all page_name)

            temp *= damping_factor       # assigning each page their prop.
            temp += (1 - damping_factor) / pages_number   # assigning each link their prop. too

            new_dict[page] = temp

        difference = max([abs(new_dict[x] - old_dict[x]) for x in old_dict])    
        if difference < 0.001:         #we gonna stop this prog. only if the diff between the two algo are just 0.001
            break
        else:
            old_dict = new_dict.copy()

    return old_dict

if __name__ == "__main__":
    main()

    #raise NotImplementedError

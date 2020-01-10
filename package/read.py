#!/usr/bin/env python3
from bs4 import BeautifulSoup 

def read_no_tags(path_source,path_target):
    """
    Loads the source and target (no tags)
    
    Parameters: 
        path_source(string): as the name implies
        path_target(string): as the name implies

    Returns:

        source(list): List containing all source setences 
        target(list): List containing all target setences 
    """


    with open(path_source) as source:
        source = [line[:-1] for line in source]        
        with open(path_target) as target:
            target = [line[:-1] for line in target]

    return source , target 


def read_with_tags(path_source_tags):
    """
    Loads the source with tags xml into the program

    Parameters:
        path_source_tags(string): as the name implied

    Returns: 
        soup(soup.object): Soup Object of the xml just read
        contents(soup.result.set(~list)): Splits each source into contents 

    """
    
    with open(path_source_tags) as fp:
        tags = fp.read()
    
    soup = BeautifulSoup(tags,features='lxml')
    soup = soup.find_all('source')
    contents = [n.contents for n in soup ]

    return soup , contents



def read_all(path_source,path_target,path_source_tags):
    """
    Reads both the no tags files and the xml tag file returning everything in a ordered dictionary
    
    Parameters:
        path_source(string): as the name implies
        path_target(string): as the name implies
        path_source_tags(string): as the name implied
    
    Returns: 
        dictionary: part of the data necessary for the tag handling 
    """
    
    source, target = read_no_tags(path_source,path_target)
    soup , contents = read_with_tags(path_source_tags)

    return dict(tag_soup = soup, source = source, target = target, contents = contents)




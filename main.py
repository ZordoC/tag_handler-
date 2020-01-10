#!/usr/bin/env python3
import os 
from bs4 import BeautifulSoup
import argparse
import package.read as read
import package.tags as tags
import package.align_process as al



def render_all_tags(data,original_alignment):
     """

        This is our wrapper function, it will get all the data necessary and write the target with tags on a file called
        "Output.txt"

        Parameters:
            data(dict): dictionary containing source (no tags), target(no_tags), source(tags) and contents

        Returns:
            void

     """
     for i in range(len(data['source'])):
         
        new_alignment = tags.refine_all_alignment(original_alignment[i], limit = 4 )
        dict_to_translate = tags.find_in_alignments_source(new_alignment,data['contents'][i],data['source'][i])
        with open("Output.txt",'a') as f5:
            f5.write(tags.render_response(tags.find_in_alignments_target(new_alignment, dict_to_translate,data['target'][i])) + '\n')


def main(): # path source  source tags and target for inference

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--source', type=str, default='./data/source_no_tags.txt',
                        help='Path to source ')
    parser.add_argument('--target', type=str, default= './data/target_no_tags.txt',
                        help='Path to target')
    parser.add_argument('--tags', type=str, default='./data/source_tags.xml',
                        help='Path to source with tags')
    args = parser.parse_args()
    
    alignments = al.process_every_alignment('aligned.rev')
    #data = read_all('./data/source_no_tags.txt','./data/target_no_tags.txt','./data/source_tags.xml') # use this as input 
    data = read.read_all(args.source,args.target,args.tags) # use this as input 
    render_all_tags(data,alignments)
    
 

if __name__ == '__main__': main()

   
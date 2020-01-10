#!/usr/bin/env python3
import os
from package.align_process import convert_fast_align_process , generate_alignment, process_every_alignment,process_single_alignment

import argparse

def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--source', type=str, default='./data/source_no_tags.txt',
                        help='Path to source ')
    parser.add_argument('--target', type=str, default= './data/target_no_tags.txt',
                        help='Path to target')
    parser.add_argument('--tags', type=str, default='./data/source_tags.xml',
                        help='Path to source with tags')
    
    parser.add_argument('--priors', type=str, default='./data/enru.priors',
                        help='Path to priors')
    

    parser.add_argument('--fast', type=str, default='./data/',
                        help='path to data folder')
    
    
    

    args = parser.parse_args()
    



    convert_fast_align_process(args.source,args.target,args.fast) #  Works :)! 
    generate_alignment(args.fast + 'fast_align_style.txt',args.priors)
    

if __name__ == '__main__': main()

   

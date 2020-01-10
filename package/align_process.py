import os 

def convert_fast_align_process(path_source,path_target,path_output):
    """
    Opens source and target files, and creates a new file with the following format:
        Source sentence (1) ||| Target sentence (1)
        Source sentence (2) ||| Target sentence (2)
                             .
                             .
                             .
    Parameters: 

        path_source(string): path to source file 
        path_target(string): path to target file
        path_output(string): path to output file , leave '' if you want it to stay in the working directory.


    """
    with open(path_target) as xh:
        with open(path_source) as yh:
            with open(path_output + "fast_align_style.txt","w") as zh:
            #Read first file
                xlines = xh.readlines()
                #Read second file
                ylines = yh.readlines()
                #Combine content of both lists
                    #combine = list(zip(ylines,xlines))
                #Write to third file
                for i in range(len(xlines)):
                    line = ylines[i].strip() + ' ||| ' + xlines[i]
                    zh.write(line)



def generate_alignment(path_to_align,path_to_priors):
    """
    Uses eflomal generate alignments (with priors)

    Parameters:
        path_to_align(string): path to the file we want to get alignements from  
        path_to_priors(string): path to priors path (it has to be the same language)

    """

    print("---------------------Creating Alignments-------------------")
    os.system("python3 ./tools/eflomal/align.py -i " + path_to_align + " -f aligned.fwd -r aligned.rev --priors " + path_to_priors)



def process_single_alignment(alignment):
    """
    Alignments from aligner normally look like this : 0-7 1-1 2-1 2-3 3-0 3-5 4-2 5-8 6-9 7-4 8-11 9-11 10-12
    This function reads the text file and converts the pairs into a list of tuples : [(0,7),(1,1),(2,1),(2,3),(3,0),(3,5),(4,2),(5,8),(6,9),(7,4),(8,11),(9,11),(10,12)]

    Parameters:
        alignment(string): 1 line string containing sentence aligments

    Returns:
        alignment_list_of_tuples(list): list of tuples of alignments
    """

    tmp = [o.split('-') for o in alignment.split()]
    tmp_2 = []
    for t in tmp:
        numbers = [ int(x) for x in t ]
        numbers = tuple(numbers)
        tmp_2.append(numbers)
        
    return tmp_2


def process_every_alignment(path_aligned):
    """
    Processes every line in the alignent file and stores it as a list of list of tuples

    Parameters:
        path(string): path to aligned file

    Returns:
        all_lines(list): list containing the list of tuples for every line in the file 
    """
    with open(path_aligned,'r') as a:
        all_lines = []
        for line in a:
            tmp = process_single_alignment(line)
            all_lines.append(tmp)
            
        return all_lines
            

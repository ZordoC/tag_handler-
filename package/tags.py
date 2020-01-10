#!/usr/bin/env python3
from bs4 import BeautifulSoup
from pprint import pprint


def find_tuple(alignment, value_tgt):
    """
    This function finds the last position in the alignment list where the target value of an aligmment is found
    """
    for item in alignment:
        if item[0] == value_tgt:
            item_to_return = item
    return item_to_return



def find_max_in_target(alignment):
    """
    This function finds the maximum position target in the alignment list
    """
    max_target = 0
    for item in alignment:
        if item[1] > max_target:
            max_target = item[1]
    return max_target


def refine_individual_alignment(original, position,limit=4):
    """
    Function to refine the original alignment tuple. Assumption: diagonal alignment
    If the difference between the source and the target word position is larger than limit, we wil suppose a diagonal alignment.
    That is, the position in source will be the same as in target.
    """
    max_target = find_max_in_target(original)
    ind_alignment = original[position]
    #print(ind_alignment)
    if abs(ind_alignment[1] - ind_alignment[0]) >= limit:
        # Check if target is larger than source 
        if ind_alignment[1] > ind_alignment[0]:
            if ind_alignment[0] > max_target:
                return (ind_alignment[0],max_target)
            else:
                return (ind_alignment[0],ind_alignment[0])
        else:
            if ind_alignment[0] > max_target:
                return (ind_alignment[0],max_target)
            else:
                return (ind_alignment[0],ind_alignment[0])
            #if ind_alignment[0] > max_target:
            #    return (ind_alignment[0],max_target)
            #else:
            #    return (ind_alignment[0],ind_alignment[0]
    else:
        return (ind_alignment)



def refine_all_alignment(original, limit=4):
    """
    This function will take every tuple in the original alignment and refine that, returning a new alignment.
    The assumption is that the alignment is diagonal (same assumption used in many alignment algorithms).
    If the difference between the src and target alignment positions are larger than limit, the values will be reassigned.
    Limit value may be different according to language pairs, similarly to word reordering/distortion in SMT.
    """
    new_alignment = []
    for i, item in enumerate(original):
        new_alignment.append(refine_individual_alignment(original, i, limit = limit))
    return new_alignment


def return_duplicates_from_ranges(alignment_unique, alignment_src_or_tgt):
    """
    This function will return the duplicates in ranges of alignments.
    It is used to ensure that all words will be covered in the final composition
    """
    final_list = []
    for item in alignment_src_or_tgt:
        if item in alignment_unique:
            final_list.append(item)
    return final_list


def find_valid_tags(between_tags, alignment):
    """
    This function finds the intersection between all possible alignments and the tags alignments.
    """
    all_sources = [x[0] for x in alignment]
    intersection = list(set(all_sources) & set(between_tags))
    intersection.sort()
    return(intersection)



def find_target_alignment(source_tokens,new_alignment):
    """
    This function finds the target alignments of a given token
    """
    target_alignments = []
    for item in new_alignment:
        if item[0] in source_tokens:
            target_alignments.append(item[1])
    return target_alignments



def find_in_alignments_source(new_alignment, contents,src_no_tags):
    """
    This function attaches the tags to the source part of the alignment
    """
    last_processed_in_sentence = 0
    all_sources = [x[0] for x in new_alignment]
    all_targets = [x[1] for x in new_alignment]
    src_tokenized = src_no_tags.split(' ')
    list_contents = []
    for content in contents:
        if content.name ==  None:
            tmp_out = []
            tokens = content.strip().split(' ')
            for i,token in enumerate(tokens):
                #print(i)
                tmp_i = last_processed_in_sentence 
                if tmp_i in all_sources:
                    tmp_out.append(tmp_i)
                    last_processed_in_sentence = last_processed_in_sentence +1
                else:
                    tmp_workaround = min(all_sources, key=lambda x:abs(x-(tmp_i+1)))
                    tmp_out.append(tmp_workaround)
                    last_processed_in_sentence = last_processed_in_sentence + tmp_workaround
                    tmp_out.sort()
                min_tag=min(tmp_out)
                max_tag=max(tmp_out)
            last_processed_in_sentence = tmp_out[-1] +1
            tmp_out = list(range(min_tag,max_tag+1))
            tmp_out.sort()
            list_contents.append(dict(type_content='alignment_src',data=find_valid_tags(tmp_out,new_alignment)))
        else:
            list_contents.append(dict(type_content='other', data=str(content)))
    return list_contents

def find_in_alignments_target(new_alignment, dict_to_translate,tgt_no_tags):
    """
    This function links the tags in the source alignment to the target part of the alignment
    """
    last_aligned_in_target = -1
    all_sources = [x[0] for x in new_alignment]
    all_targets = [x[1] for x in new_alignment]
    tgt_tokenized = tgt_no_tags.split(' ')
    list_contents = []
    total_number_elements = sum([1 for x in dict_to_translate if x['type_content'] == 'alignment_src'])
    i = 1
    for item in dict_to_translate:
        if item['type_content'] == 'alignment_src':
            #print(item)
            item['alignment_tgt'] = []
            valid_alignments = return_duplicates_from_ranges(item['data'],all_sources)
            alignments_in_target_tmp = find_target_alignment(valid_alignments,new_alignment)
            alignments_in_target = [x for x in alignments_in_target_tmp if x > last_aligned_in_target]
            if(len(alignments_in_target)==0):
                alignments_in_target = last_aligned_in_target
                last_aligned_in_target = last_aligned_in_target
                span_in_target = (last_aligned_in_target, last_aligned_in_target)
            else:
                last_aligned_in_target= max(alignments_in_target)
                span_in_target = (min(alignments_in_target), max(alignments_in_target))
            #print(span_in_target)

            if i == total_number_elements:
                words_in_target = tgt_tokenized[span_in_target[0]:len(tgt_tokenized)-1]
            else:
                words_in_target = tgt_tokenized[span_in_target[0]:span_in_target[1]+1]
            #print(words_in_target)
            i = i+1
            list_contents.append(dict(type_content='alignment_src',
                                     data=item['data'],
                                     span_target=span_in_target,
                                     alignments_target=alignments_in_target,
                                     words_in_target = words_in_target))
        else:
            list_contents.append(item)
    return(list_contents)


def render_response(dict_new):
    """
    This function recomposes the MT sentence with the tags in the source.
    """
    list_to_render = []
    for item in dict_new:
        if item['type_content'] == 'alignment_src':
            list_to_render += item['words_in_target']
        else:
            list_to_render.append(item['data'])
    return ' '.join(list_to_render)

if __name__ == '__main__': 

    print("Bye Bye")
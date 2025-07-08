"""
Generate human-readable local names and ID maps for entities and predicates
based on attribute and relation triples.
"""

import os
import re
import string
from Param import *
import sys

# Save original stdout to restore later
orig_stdout = sys.stdout
# Open out.txt for capturing script output
f = open('out.txt', 'w')
# Redirect stdout to the log file
sys.stdout = f

# Convert KG1 attribute URI to lowercase for consistency
KG1_ATTR_URI = KG1_ATTR_URI.lower()
KG2_ATTR_URI = KG2_ATTR_URI.lower()
def ent_local_names():
    """
    For each KG:
      • Read reference entity links.
      • Extract attribute values for those entities.
      • Assign integer IDs to predicates and write att_ids file.
      • Derive and write human-readable local names for predicates and entities.
    """

    for i in range(2):
        ref_ent = []
        # Read reference entity pairs for alignment
        with open(INPUT_DIR+'ent_links', "r") as f:
            for line in f.readlines():
                l=line.rstrip('\n').split('\t')
                ref_ent.append(l[i])
                
        # Initialize mappings: local_dict for entity→labels, att_dict for predicate→ID
        local_dict = {}
        att_dict = {}
        count = 0
        # Open attribute triples file for KG i
        with open(INPUT_DIR+'attr_triples_'+str(i+1), "r") as f:
            for line in f.readlines():
                h, r, t = line.rstrip('\n').split('\t',2)
                h = h.strip('<>')
                # Select only certain attribute triples defined by the user in the Param file
                if r==KG1_ATTR_URI or r==KG2_ATTR_URI:
                    t = t.strip('""')
                    t = t.strip('" .')
                    for punctuation in string.punctuation:
                        t = t.replace(punctuation, ' ')
                    # Associate this attribute value with the referenced entity
                    if h in ref_ent:
                        if h in local_dict:
                            local_dict[h].append(t)
                        else:
                            local_dict[h] = [t]
                r = r.strip('<>')
                if r not in att_dict:
                    att_dict[r] = count
                    count +=1
        # Write attribute predicate → ID mapping
        with open("./raw_files/att_ids_"+str(i+1), "w") as f:
            for key in att_dict.keys():
                f.write(str(att_dict[key])+"\t"+key+'\n')
                
        # Generate human-readable local names for each attribute URI
        for att_url in att_dict.keys():
            att_local = att_url.split('/')[-1]
            for punctuation in string.punctuation:
                att_local = att_local.replace(punctuation, ' ')
            att_dict[att_url] = att_local
        # Output attribute predicate local names
        with open(INPUT_DIR+"predicate_local_name_"+str(i+1), 'w') as f:
            for att_url in att_dict.keys():
                f.write(att_url+"\t"+att_dict[att_url]+'\n')
                
        # Ensure every entity has at least an empty name entry
        for e in ref_ent:
            if e not in local_dict:
                local_dict[e] = " "
        # Write entity → concatenated label(s) mapping
        with open(INPUT_DIR+"entity_local_name_"+str(i+1), 'w') as f:
            for key in local_dict.keys():
                f.write(key+"\t")
                for val in local_dict[key]:
                    # Removing punctuations in string
                    val = re.sub(r'[^\w\s]', '', val)
                    f.write(val)
                f.write("\n")
        rel_dict = {}
        # Load relation predicate ID mapping
        with open('./raw_files/rel_ids_'+str(i+1), "r") as f:
            for line in f.readlines():
                _, rel_url = line.split('\t')
                rel_url = rel_url[:-1]
                rel_url = rel_url.strip()
                # Extract base name from relation URI
                rel_local = rel_url.split('/')[-1]
                #rel_local = re.sub(r'[^\w\s]', '', rel_local)
                for punctuation in string.punctuation:
                    rel_local = rel_local.replace(punctuation, ' ')
                rel_dict[rel_url] = rel_local
        # Append relation predicate local names to the same file
        with open(INPUT_DIR+"predicate_local_name_"+str(i+1), 'a') as f:
            for key in rel_dict.keys():
                f.write(key+"\t"+rel_dict[key]+'\n')

def cleanse_data():
    """Set delimiters in attribute/relation triples and the reference alignment
    files to be tab(\t)
    """
    # Verify and fix ent_links to use tab delimiters
    with open(INPUT_DIR+'ent_links', "r") as f:
        flag = True
        modified_ref = []
        for line in f.readlines():
            ll = line.rstrip('\n').split(' ')
            if len(ll)!=2:
                flag = False
                break
            else:
                h, t = ll
                modified_ref.append((h,t))
        if flag:
            with open(INPUT_DIR+'ent_links', "w") as f:
                for tup in modified_ref:
                    f.write(tup[0]+'\t'+tup[1]+'\n')
    for i in range(2):
        # Clean attribute triples: strip angle brackets and ensure tabs
        with open(INPUT_DIR+'attr_triples_'+str(i+1), "r") as f:
            modified_tri = []
            flag = True
            for line in f.readlines():
                ll = line.rstrip('\n').split(' ',2)
                if len(ll)!=3:
                    flag = False
                    break
                else:
                    h, r, t = ll
                    h = h.strip('<>')
                    r = r.strip('<>')
                    t = t.rstrip(' .')
                    modified_tri.append((h,r,t))
            if flag:
                with open(INPUT_DIR+'attr_triples_'+str(i+1), "w") as f:
                    for tri in modified_tri:
                        f.write(tri[0]+'\t'+tri[1]+'\t'+tri[2]+'\n')
                        
        # Clean relation triples: strip brackets and trailing punctuation
        with open(INPUT_DIR+'rel_triples_'+str(i+1), "r") as f:
            modified_tri = []
            for line in f.readlines():
                ll = line.rstrip('\n').split(' ',2)
                if len(ll)==3:
                    h, r, t = ll
                    h = h.strip('<>')
                    r = r.strip('<>')
                    t = t.strip('<>')
                    t = t.rstrip('> .')
                    modified_tri.append((h,r,t))
            if len(ll)==3:
                with open(INPUT_DIR+'rel_triples_'+str(i+1), "w") as f:
                    for tri in modified_tri:
                        f.write(tri[0]+'\t'+tri[1]+'\t'+tri[2]+'\n')

if __name__ == '__main__':

    print("----------------cleanse data and remove <> from triples--------------------")
    # Clean and reformat raw files before name generation
    cleanse_data()
    print("----------------create entity and predicate local names--------------------")
    # Build local name mappings for entities and predicates
    ent_local_names()

    sys.stdout = orig_stdout
    # Close log file
    f.close()

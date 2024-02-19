import os
import re
import string
from Param import *
import sys
orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f
KG1_ATTR_URI = KG1_ATTR_URI.lower()
KG2_ATTR_URI = KG2_ATTR_URI.lower()
def ent_local_names():
    for i in range(2):
        ref_ent = []
        with open(INPUT_DIR+'ent_links', "r") as f:
            for line in f.readlines():
                l=line.rstrip('\n').split('\t')
                ref_ent.append(l[i])
        local_dict = {}
        att_dict = {}
        count = 0
        with open(INPUT_DIR+'attr_triples_'+str(i+1), "r") as f:
            for line in f.readlines():
                h, r, t = line.rstrip('\n').split('\t',2)
                h = h.strip('<>')
                if r==KG1_ATTR_URI or r==KG2_ATTR_URI:
                    t = t.strip('""')
                    t = t.strip('" .')
                    for punctuation in string.punctuation:
                        t = t.replace(punctuation, ' ')
                    if h in ref_ent:
                        if h in local_dict:
                            local_dict[h].append(t)
                        else:
                            local_dict[h] = [t]
                r = r.strip('<>')
                if r not in att_dict:
                    att_dict[r] = count
                    count +=1
        with open("./raw_files/att_ids_"+str(i+1), "w") as f:
            for key in att_dict.keys():
                f.write(str(att_dict[key])+"\t"+key+'\n')
        #To get attribute local names
        for att_url in att_dict.keys():
            att_local = att_url.split('/')[-1]
            for punctuation in string.punctuation:
                att_local = att_local.replace(punctuation, ' ')
            att_dict[att_url] = att_local
        with open(INPUT_DIR+"predicate_local_name_"+str(i+1), 'w') as f:
            for att_url in att_dict.keys():
                f.write(att_url+"\t"+att_dict[att_url]+'\n')

        for e in ref_ent:
            if e not in local_dict:
                local_dict[e] = " "
        with open(INPUT_DIR+"entity_local_name_"+str(i+1), 'w') as f:
            for key in local_dict.keys():
                f.write(key+"\t")
                for val in local_dict[key]:
                    # Removing punctuations in string
                    val = re.sub(r'[^\w\s]', '', val)
                    f.write(val)
                f.write("\n")
        rel_dict = {}
        with open('./raw_files/rel_ids_'+str(i+1), "r") as f:
            for line in f.readlines():
                _, rel_url = line.split('\t')
                rel_url = rel_url[:-1]
                rel_url = rel_url.strip()
                rel_local = rel_url.split('/')[-1]
                #rel_local = re.sub(r'[^\w\s]', '', rel_local)
                for punctuation in string.punctuation:
                    rel_local = rel_local.replace(punctuation, ' ')
                rel_dict[rel_url] = rel_local
        with open(INPUT_DIR+"predicate_local_name_"+str(i+1), 'a') as f:
            for key in rel_dict.keys():
                f.write(key+"\t"+rel_dict[key]+'\n')

def cleanse_data():
    """Set delimiters in attribute/relation triples and the reference alignment
    files to be tab(\t)
    """
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
    cleanse_data()
    print("----------------create entity and predicate local names--------------------")
    ent_local_names()

    sys.stdout = orig_stdout
    f.close()

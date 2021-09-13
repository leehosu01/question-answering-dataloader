import recovery
def kmp_search(string, key, pi = None):
    # kmp_search_all
    # return [start, end]
    if pi is None:
        pi = [0 for _ in key]
        j = 0 
        for i in range(1, len(pi)):
            while j > 0 and key[i] != key[j]: j = pi[j-1]
            if key[i] == key[j]:
                j+=1
                pi[i] = j
    RET = []
    j = 0
    for i, I in enumerate(string):
        while j > 0 and I != key[j]:
            j = pi[j-1]
        if I == key[j]:
            if j == len(key) - 1:
                RET.append((i - len(key) + 1, i) )
                j = pi[j]
            else: j += 1
    return RET
def kmp_pi(key):
    # kmp_search_all
    # return [start, end]
    pi = [0 for _ in key]
    j = 0 
    for i in range(1, len(pi)):
        while j > 0 and key[i] != key[j]: j = pi[j-1]
        if key[i] == key[j]:
            j+=1
            pi[i] = j
    return pi
def search(istring:recovery._integrated_string, tokenizer, key, lower = True):
    def stride_support_search(input_ids):
        return [I for candidate_ids, pi in zip(candidates_ids, candidates_pi)
                    for I in kmp_search(input_ids, candidate_ids, pi = pi)]
    encoded = istring(tokenizer)
    ids = encoded['input_ids']
    candidates_ids = [ids[encoded.char_to_token(0, S) : encoded.char_to_token(0, E) + 1]
            for (S, E) in kmp_search(istring.__str__(lower = lower), key)]
    candidates_pi = [kmp_pi(candidate_ids) for candidate_ids in candidates_ids]
    return stride_support_search
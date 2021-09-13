import numpy as np
import transformers
from functools import partial, lru_cache

class _integrated_string(object):
    def __init__(self, input_str, original_string_method = False):
        self.original = input_str
        self.normalized  = _integrated_string.string_grinding(input_str)
        self.tokenizer_call_cache  = {}
        self.word_start_mapping = None
        self.original_string_method = original_string_method
    @staticmethod
    def string_grinding(input_str):
        return ' '.join(input_str.strip().split())
    @staticmethod
    def simple_search(target_string, key_string, start_idx):
        for i in range(start_idx, len(target_string)):
            if target_string[i] == key_string[0]:
                return i
    @staticmethod
    def head_char_original_index(input_str):
        words = input_str.strip().split()
        RET = {}
        current_joined_index = 0
        search_start_index = 0
        for W in words:
            search_start_index = _integrated_string.simple_search(input_str, W, search_start_index)
            RET[current_joined_index] = search_start_index
            current_joined_index += len(W) + 1
            search_start_index += len(W) + 1
        return np.asarray(list(RET.keys())), np.asarray(list(RET.values()))
    @lru_cache
    def __str__(self, lower = False, upper = False):
        assert not (lower and upper)
        if lower: return self.normalized.lower()
        if upper: return self.normalized.upper() 
        return self.normalized
    def __call__(self, tokenizer : transformers.tokenization_utils_base.PreTrainedTokenizerBase, *args, **kwargs):
        key = [id(tokenizer), *args, *list(kwargs.items())]
        key = tuple(key)
        if key not in self.tokenizer_call_cache:
            self.tokenizer_call_cache[key] = tokenizer(self.normalized, *args, **kwargs)
            if self.original_string_method:
                get_original_string_method = partial(_integrated_string.traceback_original, self = self, encoded = self.tokenizer_call_cache[key])
                self.tokenizer_call_cache[key].get_original_string = get_original_string_method
        return self.tokenizer_call_cache[key]
    def __hash__(self):
        return hash(self.normalized)
    def traceback_before_grinding(self, index):
        # grind 이전으로 돌아가는 것만 해결함
        if self.word_start_mapping is None:
            self.word_start_mapping = _integrated_string.head_char_original_index(self.original)
        argidx = np.searchsorted(self.word_start_mapping[0], index, side='right') - 1
        return self.word_start_mapping[1][argidx] + index - self.word_start_mapping[0][argidx]

def traceback_original(self, encoded, start_token_index, end_token_index):
    s_idx = encoded.token_to_chars(0, start_token_index).start
    e_idx = encoded.token_to_chars(0, end_token_index).end
    original_s_idx = self.traceback_original_index(s_idx)
    original_e_idx = self.traceback_original_index(e_idx)
    return self.original[original_s_idx : original_e_idx]
def integrated_string(input_str)-> _integrated_string:
    TMP = _integrated_string(input_str)
    KEY = hash(TMP)
    if TMP not in integrated_string.dicts:
        integrated_string.dicts[KEY] = TMP
    return integrated_string.dicts[KEY]
integrated_string.dicts = {}
import recovery, search
import transformers, torch
from typing import List
def fit_length(X:List, length : int):
    if len(X) < length: return X + [0] * length
    return X[:length]
class dataset(torch.utils.Dataset):
    def __init__(self, tokenizer:transformers.PreTrainedTokenizer, questions, contexts, answers = None, args = None):
        self.max_candidates = args.max_candidates

        contexts_istring = [recovery.integrated_string(context) for context in contexts]
        answers_istring = [recovery.integrated_string(answer) for answer in answers]
        try: pad_on_right = tokenizer.padding_side == "right"
        except: 
            print("tokenizer do not have `padding_side`")
            pad_on_right = True
        if pad_on_right:
            self.tokenized_samples = tokenizer(questions, contexts, return_tensors='np', 
                                            stride=args.stride, max_length = args.max_length, \
                                            truncation = "only_second",\
                                            padding = "max_length", return_overflowing_tokens = True, )
        else:                           
            self.tokenized_samples = tokenizer(contexts, questions, return_tensors='np', 
                                            stride=args.stride, max_length = args.max_length, \
                                            truncation = "only_first",\
                                            padding = "max_length", return_overflowing_tokens = True, )
                                            
        if answers is not None:
            context_answer_finder = [search.search(tokenizer, C_istr, A_istr, lower = args.consider_lower) 
                                        for C_istr, A_istr in zip(contexts_istring, answers_istring)]
                            
            self.answers = [context_answer_finder[sample_idx](input_ids) \
                for input_ids, sample_idx in zip(*[self.tokenized_samples[K]for K in [
                                                    "input_ids",
                                                    "overflow_to_sample_mapping",]])]
        else: self.answers = None

    def __getitem__(self, idx):
        RET = {}
        for K in "input_ids token_type_ids attention_mask":
            if K in self.tokenized_samples:
                RET[K] = self.tokenized_samples[K][idx]
        if self.answers is not None:
            sp, ep = list(zip(*self.answers[idx]))
            RET["start_positions"]  = fit_length(sp, self.max_candidates)
            RET["end_positions"]    = fit_length(ep, self.max_candidates)
            RET["is_candidate"]     = fit_length([1] * len(sp), self.max_candidates)
        RET["sequence_ids"]     = fit_length(self.tokenized_samples.sequence_ids(idx), self.max_sequence)
        return RET
    def __len__(self):
        return len(self.tokenized_samples["input_ids"])
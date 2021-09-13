import transformers

class quick_join:
    def __init__(self, tokenizer:transformers.PreTrainedTokenizer, padding :int):
        self.tokenizer = tokenizer
        self.padding = padding

        #if None, do not return
        self.build_input_ids, self.margin = self.input_ids_method()
        self.build_attention_mask = self.attention_mask_method()
        self.build_type_ids = self.type_ids_method()
    def input_ids_method(self):
        def _sub(S1, S2):
            return pre + S1 + inter + S2 + post + 
    def __call__(self, contexts:list, questions:list):
        RET = {}
        if self.build_input_ids is not None:
            RET["input_ids"] = self.build_input_ids(questions, contexts)
        if self.build_attention_mask is not None:
            RET["attention_mask"] = self.build_attention_mask(questions, contexts)
        if self.build_type_ids is not None:
            RET["token_type_ids"] = self.build_type_ids(questions, contexts)
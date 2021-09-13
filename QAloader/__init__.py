class config:
    def __init__(self,  padding  = 512, min_batch = 4, stride = 128,
                        max_candidates = 8, 
                        consider_lower = False,
                        batch_to_multiple_of = 4, pad_to_multiple_of = 64):
            # B_mul means batchsize 
            self.max_length = self.padding = padding
            self.min_batch = min_batch
            self.stride = stride
            self.max_candidates = max_candidates
            self.consider_lower = consider_lower
            self.batch_to_multiple_of = batch_to_multiple_of
            self.pad_to_multiple_of = pad_to_multiple_of
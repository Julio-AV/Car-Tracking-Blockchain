import hashlib
class Header:
    def __init__(self, previous_hash, block_number ,validator_sign):
        self.current_hash = None
        self.merkle_root = None
        self.previous_hash = previous_hash
        self.time_stamp = None
        self.block_number = block_number
        self.validator_sign = validator_sign
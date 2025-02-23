import json
class Header:
    def __init__(self, previous_hash, block_number):
        self.block_hash = None
        self.merkle_root = None
        self.previous_hash = previous_hash
        self.time_stamp = None
        self.block_number = block_number
        self.validator_sign = None

    def _as_dict(self):
        return {
            "block_hash": self.block_hash,
            "merkle_root": self.merkle_root,
            "previous_hash": self.previous_hash,
            "time_stamp": self.time_stamp,
            "block_number": self.block_number,
            "validator_sign": self.validator_sign
        }
    
    def _get_header_main_data(self):
        return {
            "previous_hash": self.previous_hash,
            "time_stamp": self.time_stamp,
            "block_number": self.block_number,
            "merkle_root": self.merkle_root
        }
    
    def serialize(self):
        return json.dumps(self._as_dict())
    

    def __str__(self):
        return (
            "==================== Block Header ====================\n"
            f"| Block Hash:      {self.block_hash}\n"
            f"| Merkle Root:     {self.merkle_root}\n"
            f"| Previous Hash:   {self.previous_hash}\n"
            f"| Time Stamp:      {self.time_stamp}\n"
            f"| Block Number:    {self.block_number}\n"
            f"| Validator Sign:  {self.validator_sign}\n"
            "======================================================"
        )
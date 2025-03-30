import json
class Header:
    def __init__(self, previous_hash, block_number, emmiter):
        self.block_hash = None
        self.merkle_root = None
        self.previous_hash = previous_hash
        self.time_stamp = None
        self.block_number = block_number
        self.validator_sign = None
        self.emitter = emmiter

    def _as_dict(self):
        return {
            "block_hash": self.block_hash,
            "merkle_root": self.merkle_root,
            "previous_hash": self.previous_hash,
            "time_stamp": self.time_stamp,
            "block_number": self.block_number,
            "validator_sign": self.validator_sign,
            "emitter": self.emitter
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
    

    def __eq__(self, value):
        return self._as_dict() == value._as_dict()

    # @abstractmethod
    # def deserialize(serialized_header):
    #     """Deserialize header received from network into a header object"""
    #     header_dict = json.loads(serialized_header)
    #     header = Header(
    #         previous_hash=header_dict["previous_hash"],
    #         block_number=header_dict["block_number"],
    #     )
    #     header.block_hash = header_dict["block_hash"]
    #     header.merkle_root = header_dict["merkle_root"]
    #     header.time_stamp = header_dict["time_stamp"]
    #     header.validator_sign = header_dict["validator_sign"]
    #     return header
    

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
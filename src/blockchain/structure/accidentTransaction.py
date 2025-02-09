from .transaction import Transaction
import json
class AccidentTransaction(Transaction):
    def __init__(self, emitter, car_id, driver_id, severity):
        self.transaction_type = "accident"
        self.car_id = car_id
        self.driver_id = driver_id
        self.severity = severity
        super().__init__(emitter)
    
    
    def validate(self, blockchain):
        pass


    def _as_dict(self):
        """Used to serialize the transaction to broadcast"""
        return {
            "transaction_type": self.transaction_type,
            "transaction_hash": self.transaction_hash,
            "emitter": self.emitter,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "car_id": self.car_id,
            "driver_id": self.driver_id,
            "severity": self.severity
        }
    def _get_transaction_main_data(self):
        """Used to calculate the hash of the transaction"""
        return {
            "transaction_type": self.transaction_type,
            "emitter": self.emitter,
            "timestamp": self.timestamp,
            "car_id": self.car_id,
            "driver_id": self.driver_id,
            "severity": self.severity
        }
if __name__ == '__main__':
    #python3 -m blockchain.structure.accidentTransaction
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    example_transaction = AccidentTransaction(
        emitter="user1",
        car_id="car123",
        driver_id="driver123",
        severity="high"
    )
    example_transaction.prepare_transaction(private_key)
    print(example_transaction.serialize())
    #Validate signature
    print(example_transaction.validate_signature(public_key))
    bullshit_signature = "0f882c006766064d11bcfe97e5c9e5d3d3b6c6471572d10c8c97714290714278bcf16d8f840a367ae2f50b60e1bb15963be9b53a5eba0f4b8be40d1ae7d56299edd2a9dcb864cea593b4fe110a547661a69caf3492f192de6b644b2ef83e36f5fc5a8ddfa5fc1ca9dae00bdbd1d42ce344980f1d963cf0722426db485657e19107b65129b3e5a16f9732e922c6ffc6ca00a94547de5e121a0a548b57084cdc1fca7320d8b2b5a82421524cfc305dadbb3d210fdfa33aa03290dd28f4f61a69859d9fdaaf801035227ce23ba218375fd446d4f8c654bfe9dedf5b7ebd9b1c01862ac8067e84e6ef79e2fa509b44177874f5630d51d0a56f05f8810a5f8bf43cef"
    example_transaction.signature = bullshit_signature
    print(example_transaction.validate_signature(public_key))
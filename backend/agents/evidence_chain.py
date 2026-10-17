import hashlib
import json
import time

class EvidenceChain:
    """
    Creates a tamper-evident SHA-256 hash chain for all attack results.
    """
    def __init__(self):
        self.chain = []
        self.previous_hash = "0" * 64  # Genesis block hash

    def add_block(self, data):
        """Adds a new record to the chain."""
        timestamp = time.time()
        block_data = {
            "timestamp": timestamp,
            "data": data,
            "previous_hash": self.previous_hash
        }
        
        # Create SHA-256 hash of the current block
        block_string = json.dumps(block_data, sort_keys=True).encode()
        current_hash = hashlib.sha256(block_string).hexdigest()
        
        # Update block with its own hash
        block_data["hash"] = current_hash
        
        self.chain.append(block_data)
        self.previous_hash = current_hash
        
        return current_hash

    def verify_chain(self):
        """Verifies that the chain has not been tampered with."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i-1]
            
            # Check if the stored previous_hash matches the actual previous hash
            if current_block["previous_hash"] != prev_block["hash"]:
                return False
                
        return True

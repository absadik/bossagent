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

    def add_block(self, test_id, expected, observed, severity):
        """Adds a new record to the chain with structured evidence."""
        timestamp = time.time()
        
        # Structured evidence data as suggested
        evidence_data = {
            "test_id": test_id,
            "timestamp": timestamp,
            "expected": expected,
            "observed": observed,
            "severity": severity
        }
        
        block_data = {
            "evidence": evidence_data,
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
            
            if current_block["previous_hash"] != prev_block["hash"]:
                return False
        return True

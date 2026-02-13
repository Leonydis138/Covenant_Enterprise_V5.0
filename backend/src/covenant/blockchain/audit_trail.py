"""Blockchain-based Immutable Audit Trail"""
import hashlib
import json
from typing import Dict, Any, List
from datetime import datetime

class Block:
    """Blockchain block"""
    
    def __init__(self, index: int, timestamp: str, data: Dict[str, Any], 
                 previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 4):
        """Proof of work mining"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class AuditBlockchain:
    """Immutable audit trail using blockchain"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block"""
        genesis = Block(0, datetime.utcnow().isoformat(), 
                       {"genesis": True}, "0")
        self.chain.append(genesis)
    
    def add_audit_entry(self, audit_data: Dict[str, Any]) -> str:
        """Add audit entry to blockchain"""
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.utcnow().isoformat(),
            data=audit_data,
            previous_hash=previous_block.hash
        )
        new_block.mine_block(difficulty=2)  # Low difficulty for demo
        self.chain.append(new_block)
        return new_block.hash
    
    def verify_chain(self) -> bool:
        """Verify blockchain integrity"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        
        return True
    
    def get_audit_trail(self, start_index: int = 0) -> List[Dict[str, Any]]:
        """Retrieve audit trail"""
        return [
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "hash": block.hash
            }
            for block in self.chain[start_index:]
        ]

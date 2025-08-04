from datetime import datetime
import hashlib

class Block:
    def __init__(self, data, prev_hash="0"):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_str = f"{self.timestamp}-{self.data}-{self.prev_hash}"
        return hashlib.sha256(block_str.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_block(self, data):
        prev_hash = self.chain[-1].hash if self.chain else "0"
        block = Block(data, prev_hash)
        self.chain.append(block)

    def get_history(self):
        return [
            {"filename": b.data["filename"], "timestamp": b.timestamp}
            for b in self.chain
        ]

    def get_submission_dates(self):
        return set(b.timestamp[:10] for b in self.chain)

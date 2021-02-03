from block import Block, State, BLOCK_SIZE
import math
import hashlib

# while using piece in other files set Piece().piece_size = <piece size from meta info>


class Piece(object):
    piece_size: int = 0
    no_of_blocks: int = int(math.ceil(float(piece_size) / BLOCK_SIZE))

    def __int__(self, piece_index: int, piece_size: int, piece_hash: str):
        self.piece_index = piece_index
        self.piece_size = piece_size
        self.piece_hash = piece_hash
        self.is_full: bool = False
        self.files = []
        self.raw_data: bytes = b''
        self.no_of_blocks: int = int(math.ceil( float(piece_size) / BLOCK_SIZE))
        self.blocks: list[Block] = []

        self._init_blocks()

    def _init_blocks(self):
        self.blocks = []
        number_of_blocks = type(self).no_of_blocks

        if number_of_blocks > 1:
            for i in range(number_of_blocks):
                self.blocks.append(Block())

            # Last block of last piece, the special block
            if (self.piece_size % BLOCK_SIZE) > 0:
                self.blocks[number_of_blocks - 1].block_size = type(self).piece_size % BLOCK_SIZE

        else:
            self.blocks.append(Block(block_size=int(type(self).piece_size)))

    def hash_check(self, piece_raw_data):
        hashed_piece_raw_data = hashlib.sha1(piece_raw_data).digest()

        if hashed_piece_raw_data == self.piece_hash:
            return True

        else:
            return False

    def set_block(self, offset, data):
        index = int(offset / BLOCK_SIZE)

        if not self.is_full and not self.blocks[index].state == State.FULL:
            self.blocks[index].data = data
            self.blocks[index].state = State.FULL

    def get_block(self, block_offset, block_length):
        return self.raw_data[block_offset:block_length]

    def are_all_blocks_full(self):
        for block in self.blocks:
            if block.state == State.FREE or block.state == State.PENDING:
                return False

        return True

    def merge_blocks(self):
        buffer = b''

        for block in self.blocks:
            buffer += block.data

        return buffer







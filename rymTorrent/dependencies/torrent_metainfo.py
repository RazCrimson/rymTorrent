from bcoding import bencode, bdecode
import hashlib
import time
import math
import os


class TorrentMetaInfo(object):
    def __init__(self, path):
        self.info = {}
        self.total_length: int = 0
        self.piece_length: int = 0
        self.pieces: int = 0
        self.info_hash: str = ''
        self.peer_id: str = ''
        self.announce_list = ''
        self.file_names = []
        self.number_of_pieces: int = 0
        self.is_private = False

    def load_from_file(self, path):
        # contents is a dict
        with open(path, 'rb') as file:
            meta_info = bdecode(file)

        self.info = meta_info['info']

        self.piece_length = meta_info['info']['piece length']
        self.pieces = meta_info['info']['pieces']
        raw_info_hash = bencode(meta_info['info'])
        self.info_hash = hashlib.sha1(raw_info_hash).digest()
        self.peer_id = self.generate_peer_id()

        if 'private' in meta_info['info']:
            self.is_private = meta_info['info']['private']

        # list of lists of strings
        if 'announce-list' in meta_info:
            self.announce_list = meta_info['announce-list']
        else:
            self.announce_list = [[meta_info['announce']]]

        self.make_directories()
        self.number_of_pieces = math.ceil(self.total_length / self.piece_length)

        print("peer_id ", self.peer_id)

    def make_directories(self):
        root = self.info['name']
        if 'files' in self.info:    # TODO: change root to a different path
            if not os.path.exists(root):
                os.mkdir(root, 0o0766)  # TODO: Too liberal permissions

            for file in self.info['files']:
                path_file = os.path.join(root, *file['path'])

                if not os.path.exists(os.path.dirname(path_file)):
                    os.makedirs(os.path.dirname(path_file))

                self.file_names.append({'path': path_file, 'length': file['length']})
                self.total_length += file['length']
        else:
            self.file_names.append({'path': root, 'length': self.info['length']})
            self.total_length = self.info['length']

    # custom algo
    @staticmethod
    def generate_peer_id():
        seed = str(time.time())
        return hashlib.sha1(seed.encode('utf-8')).digest()

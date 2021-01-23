from torrent_metainfo import TorrentMetaInfo
# Create and import tracker, pieces, peers manager

STATUS_LEECHING = 0
STATUS_PAUSED = 1   # Add a status stopped?
STATUS_SEEDING = 2
STATUS_COMPLETED = 3


class Torrent(object):
    def __init__(self, metainfo: TorrentMetaInfo):
        self.metainfo = metainfo
        self.current_status = STATUS_LEECHING

    @staticmethod
    def load_from_file(torrent_file):
        metainfo = TorrentMetaInfo(torrent_file)
        return Torrent(metainfo)

    async def check_hash(self):
        pass

    async def start(self):
        pass

    def stop(self):
        pass

    def pieces_status(self):
        pass

    def get_ratio(self):
        pass

    def get_state(self):
        raise NotImplementedError

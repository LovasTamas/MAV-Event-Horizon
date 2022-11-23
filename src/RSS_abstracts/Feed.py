from abc import ABC
from typing import List
from ..feed_handler.reflexive_feed_storage import ReflexiveFeedStorage
from ..feed_handler.feed_consumer import FeedConsumer
from .RSSEntry import RSSEntry


class Feed(object):
    storage: ReflexiveFeedStorage
    consumer: FeedConsumer

    def __init__(self, storage: ReflexiveFeedStorage, link: str) -> None:
        self.storage = storage
        self.consumer = FeedConsumer(link)

    def update(self) -> List[RSSEntry]:
        """
        Updates feed.
        Returns
        -------
        updated_entries:List[RSSEntry]
            A list with the Entries which are new.
        """
        feed_dict = self.consumer.fetch()
        new = list()

        for entry in feed_dict.entries:
            e = RSSEntry.from_dict(entry)
            unique = self.storage.add_event(e)
            if unique:
                new.append(e)

        return new

    def list_entries(self) -> List[RSSEntry]:
        return self.storage.get_all_latest_events()

    def list_entries_updates(self) -> List[List[RSSEntry]]:
        _r = list()
        ids = self.storage._load_all_event_ids()
        for id in ids:
            _r.append(self.storage._load_all_event_w_updates(id))
        return _r
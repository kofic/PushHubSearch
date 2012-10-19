from datetime import datetime
from persistent import Persistent
from persistent.mapping import PersistentMapping
from repoze.folder import Folder
import dateutil.parser
from dateutil.tz import tzutc


class Root(PersistentMapping):
    __parent__ = __name__ = None


class SharedItems(Folder):
    """A folder to hold the shared items
    """
    title = "Shared Items"


class SharedItem(Persistent):
    """An item shared to the CS Portal Pool
    """

    def __init__(self, Title='', portal_type='', Creator='', Modified=None,
                 url='', Description='', Subject=[], Category=None):
        self.Title = Title
        self.portal_type = portal_type
        self.url = url
        self.Creator = Creator
        if Modified is None:
            Modified = datetime.utcnow()
        self.Modified = Modified
        self.Description = Description
        self.Subject = Subject
        self.Category = Category

    def update_from_entry(self, entry):
        """Update the item based on the feed entry
        """
        if 'title' in entry:
            self.Title = entry['title']
        if 'push_portal_type' in entry:
            self.portal_type = entry['push_portal_type']
        if 'author' in entry:
            self.Creator = entry['author']
        if 'updated' in entry:
            mod_date = dateutil.parser.parse(entry['updated'])
            self.Modified = mod_date.astimezone(tzutc())
        if 'link' in entry:
            self.url = entry['link']
        if 'summary' in entry:
            self.Description = entry['summary']
        if 'tags' in entry:
            self.Subject = [i['term'] for i in entry['tags']]
        if 'category' in entry:
            self.Category = [i['term'] for i in entry['category']]


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Root()
        zodb_root['app_root'] = app_root

        shared_items = SharedItems()
        app_root.shared = shared_items
        shared_items.__name__ = 'shared'
        shared_items.__parent__ = app_root

        import transaction
        transaction.commit()
    return zodb_root['app_root']

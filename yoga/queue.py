"I should parametrize the dt variable in this file."
dt = DumpTruck(
    dbname = 'somatic.sqlite',
    auto_commit = False
)

def excavate(starting_documents, **kwargs):
    """
    Start everything.
    """
    bag = Bag(**kwargs)

    # The seed documents
    if dt.execute('select count(*) as "c" from `%s`' % bag._table_name)[0]['c'] == 0:
        for b in starting_documents:
            bag.add(b)

    # Go
    while True:
        current_document = bag.pop()

        if current_document == None:
            break

        for new_document in current_document._go():
            bag.add(new_document)

        log("Committing")
        # Commit at the end in case of errors.
        dt.commit()

        log("Taking a break") # Don't thrash the server
        sleep(3)

class Bag:
    "A fancier stack, at some point"
    def __init__(self, document_types = [], table_name = '_bag'):
        self._table_name = table_name
        self._document_types = document_types

        # The bag table
        dt.execute('''
CREATE TABLE IF NOT EXISTS `%s` (
  pk INTEGER PRIMARY KEY,
  document_type TEXT NOT NULL,
  kwargs JSON NOT NULL
 )''' % self._table_name)

    def add(self, element):
        dt.insert({
            u'document_type': element.document_type,
            u'kwargs': element.kwargs,
        }, self._table_name)

    def pop(self):
        sql1 = 'SELECT pk, document_type, kwargs FROM `%s` LIMIT 1' % self._table_name
        results = dt.execute(sql1)
        if len(results) == 0:
            return None
        else:
            document_params = results[0]
            sql2 = 'DELETE FROM `%s` WHERE pk = %d' % (self._table_name, document_params['pk'])
            dt.execute(sql2)

            document_class = self._documents_types[document_params['document_type']]
            document = document_class(**document_params['kwargs'])
            return document

class Queue:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def load(self):
        raise NotImplementedError('You need to implement the load function for this document')

    def parse(self, text):
        raise NotImplementedError('You need to implement the parse function for this document')


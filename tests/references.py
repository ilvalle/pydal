from ._compat import unittest
from ._adapt import DEFAULT_URI, drop
from pydal import DAL, Field

class TestReferenceAfterDefine(unittest.TestCase):

    def testRun(self):
        db = DAL(DEFAULT_URI, check_reserved=['all'])
        db.define_table('tt', Field('vv'))
        db.define_table('ttt', Field('tt_id', 'reference tt'))
        id_i = db.tt.insert(vv='pydal')
        db.ttt.insert(tt_id=id_i)
        row = db(db.ttt.tt_id == db.tt.id).select(db.tt.vv).first()
        self.assertEqual(row.vv, 'pydal')
        drop(db.ttt)
        drop(db.tt)
        db.close()
        
        
class TestReferenceBeforeDefine(unittest.TestCase):

    def testRun(self):
        db = DAL(DEFAULT_URI, check_reserved=['all'])
        db.define_table('ttt', Field('tt_id', 'reference tt'))
        db.define_table('tt', Field('vv'))
        id_i = db.tt.insert(vv='pydal')
        db.ttt.insert(tt_id=id_i)
        row = db(db.ttt.tt_id == db.tt.id).select(db.tt.vv).first()
        self.assertEqual(row.vv, 'pydal')
        drop(db.ttt)
        drop(db.tt)
        db.close()

class Test2ReferenceBeforeDefine(unittest.TestCase):

    def testRun(self):
        db = DAL(DEFAULT_URI, check_reserved=['all'])
        db.define_table('ttt', Field('tt1_id', 'reference tt1'), Field('tt2_id', 'reference tt2'))
        db.define_table('tt1', Field('vv'))
        db.define_table('tt2', Field('vv'))        
        id_i1 = db.tt1.insert(vv='pydal')
        id_i2 = db.tt2.insert(vv='pydal')
        db.ttt.insert(tt1_id=id_i1) #, tt2_id=id_i2)
        row = db(db.ttt.tt1_id == db.tt1.id).select(db.tt1.vv).first()
        self.assertEqual(row.vv, 'pydal')
        drop(db.ttt)
        drop(db.tt1)
        drop(db.tt2)        
        db.close()

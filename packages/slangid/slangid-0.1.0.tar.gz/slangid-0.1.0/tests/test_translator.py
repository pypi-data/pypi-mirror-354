import unittest
from slangid import Translator

class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.tr = Translator()

    def test_slang(self):
        self.assertEqual(self.tr.translate("gue"), "saya")
        
    def test_daerah(self):
        self.assertEqual(self.tr.translate("punten"), "permisi")
        
    def test_singkatan(self):
        self.assertEqual(self.tr.translate("otw"), "dalam perjalanan")

if __name__ == "__main__":
    unittest.main()
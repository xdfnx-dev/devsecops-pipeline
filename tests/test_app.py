import unittest
from app.app import Handler

class ContractTests(unittest.TestCase):
    def test_handler_exposes_get(self): self.assertTrue(callable(Handler.do_GET))

if __name__ == '__main__': unittest.main()

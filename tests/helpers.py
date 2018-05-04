import unittest

from helpers import titlecase

class HelpersTest(unittest.TestCase):
    def testTitlecase(self):
        self.assertEquals(titlecase("the poet's pen"), "The Poet's Pen")
        self.assertEquals(titlecase("THE POet'S PeN"), "The Poet's Pen")
        self.assertEquals(titlecase("Hand OF thought and Motion"), "Hand of Thought and Motion")

if __name__ == "__main__":
    tests = HelpersTest()
    tests.run()
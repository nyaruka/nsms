from django.test import TestCase
from .parser import Parser
import datetime

class ParserTest(TestCase):

    def assertNextWord(self, truth, sms):
        parser = Parser(sms)
        self.assertEquals(truth, parser.next_word())

    def test_word_parsing(self):
        self.assertNextWord("reg", "reg bach")
        self.assertNextWord("reg", "reg mozart")
        self.assertNextWord("r", "r handell")
        self.assertNextWord(None, "  ")
        self.assertNextWord("..", "..")

    def assertNextKeyword(self, truth, sms, keywords):
        parser = Parser(sms)
        self.assertEquals(truth, parser.next_keyword(keywords))

    def test_keyword_parsing(self):
        KEYWORDS = ["register", "reg"]
        self.assertNextKeyword("reg", "reg bach", KEYWORDS)
        self.assertNextKeyword("register", "register bach", KEYWORDS)
        self.assertNextKeyword("reg", "REG bach", KEYWORDS)
        self.assertNextKeyword(None, "notkeyword bach", KEYWORDS)
        self.assertNextKeyword(None, " ", KEYWORDS)

    def assertNextPhone(self, truth, sms):
        parser = Parser(sms)
        self.assertEquals(truth, parser.next_phone())

    def test_phone_parsing(self):
        self.assertNextPhone("0788383388", "  0788383388 Bach")
        self.assertNextPhone("250788383388", "  250788383388")
        self.assertNextPhone("250788383388", " +250788383388")

        # nothing there
        self.assertNextPhone(None, " ")

        # not numeric
        self.assertNextPhone(None, "078838338a")

        # not correct length
        self.assertNextPhone(None, "07883833881")

    def assertNextDate(self, truth_day, truth_month, truth_year, sms):
        parser = Parser(sms)
        truth = None

        if truth_day:
            truth = datetime.date(day=truth_day, month=truth_month, year=truth_year)

        self.assertEquals(truth, parser.next_date())

    def test_date_parsing(self):
        self.assertNextDate(23, 6, 1977, "23.6.77")
        self.assertNextDate(23, 6, 1977, "23.06.77")
        self.assertNextDate(23, 6, 2011, "23.06.11")
        self.assertNextDate(23, 6, 2000, "23.06.00")

        # invalid day
        self.assertNextDate(None, None, None, "31.6.77")

        # invalid month
        self.assertNextDate(None, None, None, "10.13.77")

        # invalid year
        self.assertNextDate(None, None, None, "10.13.113")

        # invalid format
        self.assertNextDate(None, None, None, "10 12 31")

    def assertWordCount(self, truth, sms):
        parser = Parser(sms)
        self.assertEquals(truth, parser.word_count)

    def test_word_count(self):
        self.assertWordCount(0, "  ")
        self.assertWordCount(0, "")
        self.assertWordCount(1, "  hello  ")
        self.assertWordCount(2, "  hello. world")
        self.assertWordCount(2, " hello world.foo")

    def test_parsing(self):
        parser = Parser("REG James Kirk 10.12.44 0788383381")

        self.assertEquals("reg", parser.next_keyword(["reg"]))
        self.assertEquals("James", parser.next_word())
        self.assertEquals("Kirk", parser.next_word())
        self.assertEquals(datetime.date(day=10, month=12, year=1944), parser.next_date())
        self.assertEquals("0788383381", parser.next_phone())

        self.assertFalse(parser.has_word())

import re
import datetime

class ParseException(Exception):
    def __init__(self, msg):
        super(ParseException, self).__init__(msg)

class Parser(object):

    def __init__(self, msg, delimiter=' '):
        self.msg = msg
        self.delimiter = delimiter

        # delimiters delimiters at both ends and space if available
        self.rest = self.msg.strip(delimiter).strip()

    def get_word_count(self):
        if len(self.rest) > 0:
            return len(self.rest.split(self.delimiter))
        return 0

    word_count = property(get_word_count)

    def has_word(self):
        return self.word_count > 0

    def next_keyword(self, keywords, error_msg=None):
        segment = self.next_word(error_msg)
        keyword = None

        if segment:
            segment = segment.lower()
            for curr in keywords:
                if curr.lower() == segment:
                    keyword = curr.lower()
                    break

        if not keyword and error_msg:
            raise ParseException(error_msg)
        else:
            return keyword

    def next_word(self, error_msg=None):
        next_delimiter = self.rest.find(self.delimiter)
        word = None

        if next_delimiter > 0:
            word = self.rest[:next_delimiter]

            self.rest = self.rest[next_delimiter:].strip(self.delimiter).strip()
        elif self.rest:
            word = self.rest
            self.rest = ""

        if not word and error_msg:
            raise ParseException(error_msg)
        else:
            return word

    def insert_word(self, word):
        self.rest = "%s %s" % (word, self.rest)

    def peek_word(self):
        next_space = self.rest.find(self.delimiter)
        word = None

        if next_space > 0:
            word = self.rest[:next_space]
        elif self.rest:
            word = self.rest

        return word
    
    def next_hour(self, error_msg=None):
        hour = self.next_word(error_msg)

        # four digits means this is hour and minute (1312 for 13), we care only about hour
        if len(hour) == 4:
            hour = hour[:2]

        # hours need to be integers
        try:
            hour_int = int(hour)
        except:
            raise ParseException(error_msg)

        # hours should be in 24 hour format, ie, 00-23
        if hour_int < 0 or hour_int > 23:
            raise ParseException(error_msg)            

        return hour_int

    def next_phone(self, error_msg=None):
        phone = self.next_word(error_msg)
        
        # if there is a leading '+' strip it
        if phone and phone[0] == '+':
            phone = phone[1:]

        # make sure it is numeric (an integer)
        try:
            int(phone)
        except:
            phone = None

        # make sure it is either 10 or 12 digits
        if phone and len(phone) != 10 and len(phone) != 12:
            phone = None

        if phone is None and error_msg:
            raise ParseException(error_msg)

        return phone

    def next_int(self, error_msg=None):
        integer = self.next_word(error_msg)
        
        # make sure it is numeric (an integer)
        try:
            int(integer)
        except:
            integer = None

        if integer is None and error_msg:
            raise ParseException(error_msg)

        return integer

    def next_date(self, separator='.', error_msg=None):
        date = self.next_word(error_msg)

        # does it match our format?  dd[separator]mm[separator]yy 
        date_regex = r"(\d+)"+ re.escape(separator) +r"(\d+)"+ re.escape(separator) +r"(\d+)"
        match = re.search(date_regex, date)
        if not match:
            date = None
        else:
            try:
                day = int(match.group(1))
                month = int(match.group(2))
                year = int(match.group(3))

                # two digit date, we'll figure out whether to add 1900 or 2000 based on the current date
                if year < 100:
                    this_year = datetime.datetime.now().date().year

                    # our first assumption is that it is in the 2000s.. but if the year is greater than today + 5
                    # (arbitrary but seems sane) then we downgrade it to 1900s
                    year = year + 2000
                    if year > this_year + 5:
                        year = year - 100

                # year has to be more than 1000 in our world
                if year > 1000:
                    date = datetime.date(day=day, month=month, year=year)
                else:
                    date = None
            except:
                date = None

        if not date and error_msg:
            raise ParseException(error_msg)

        return date

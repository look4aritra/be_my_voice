# -*- coding: utf-8 -*-

from utilities import list2string, sanitize


class TestUtilities:
    def test_list2string_1(self):
        out = list2string(["hey", "there"])
        print(out)
        assert "hey there" == out

    def test_sanitize_1(self):
        out = sanitize("")
        print(out)
        assert "" == out

    def test_sanitize_2(self):
        out = sanitize("hello")
        print(out)
        assert "hello" == out

    def test_sanitize_3(self):
        out = sanitize("<cust>hello</cust>")
        print(out)
        assert "hello" == out

    def test_sanitize_4(self):
        out = sanitize("<html>hello</html> all")
        print(out)
        assert "hello all" == out

    def test_sanitize_5(self):
        out = sanitize("<html>hello</html> \r\r     \nall")
        print(out)
        assert "hello all" == out

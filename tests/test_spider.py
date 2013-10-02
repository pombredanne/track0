from track.cli import TestImpl, OperatorImpl
from track.spider import URL


class TestRules(object):

    def test_path_level(self):
        test = lambda a: TestImpl.path_level(URL(a))

        assert test('http://example.org/') == 0
        assert test('http://example.org/foo') == 0
        assert test('http://example.org/foo/') == 1

    def test_path_distance(self):
        test = lambda a,b: TestImpl.path_distance(URL(a, URL(b)))

        assert test('http://example.org/foo', 'http://example.com') == False
        assert test('/foo', '/bar') == False
        assert test('/foo', '/foobar') == False
        assert test('/foo', '/foo') == 0
        assert test('/foo', '/foo/bar') == -1
        assert test('/foo/', '/foo/bar') == 0
        assert test('/foo/bar', '/foo') == 1
        assert test('/foo/bar', '/foo/') == 0

    def test_protocol(self):
        test = lambda a: TestImpl.protocol(URL(a))

        assert test('http://www.example.org/') == 'http'
        assert test('mailto:info@example.org') == 'mailto'

    def test_port(self):
        test = lambda a: TestImpl.port(URL(a))

        assert test('http://www.example.org/') == 80
        assert test('http://www.example.org:8080') == 8080

    def test_path(self):
        test = lambda a: TestImpl.path(URL(a))

        assert test('http://www.example.org/path/') == '/path/'
        assert test('http://www.example.org/') == '/'
        assert test('http://www.example.org') == '/'

    def test_filename(self):
        test = lambda a: TestImpl.filename(URL(a))

        assert test('http://www.example.org/path/') == ''
        assert test('http://www.example.org/path') == 'path'
        assert test('http://www.example.org/path/index.html') == 'index.html'

    def test_extension(self):
        test = lambda a: TestImpl.extension(URL(a))

        assert test('http://www.example.org/path/') == ''
        assert test('http://www.example.org/path') == ''
        assert test('http://www.example.org/index.html') == 'html'

    def test_querystring(self):
        test = lambda a: TestImpl.querystring(URL(a))

        assert test('http://www.example.org/path/?a=1&b=2') == 'a=1&b=2'
        assert test('http://www.example.org/path/') == ''


class TestOperators(object):

    def test_numeric(self):
        assert OperatorImpl.truth(True) is True
        assert OperatorImpl.truth(False) is False
        assert OperatorImpl.truth(1) is True
        assert OperatorImpl.truth('') is False

        assert OperatorImpl.equality(1, '1') is True
        assert OperatorImpl.equality(1, '2') is False
        assert OperatorImpl.equality(1, '') is False
        assert OperatorImpl.equality(0, '') is False
        assert OperatorImpl.equality(1, 'abc') is False
        assert OperatorImpl.equality(False, '') is True

        assert OperatorImpl.larger(4, '') is False

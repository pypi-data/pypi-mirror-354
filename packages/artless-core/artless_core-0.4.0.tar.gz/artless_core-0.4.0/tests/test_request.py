from io import BytesIO
from json import dumps
from typing import Any
from unittest import TestCase
from uuid import UUID

from artless_core import Request


class TestRequest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.common_headers = {
            "Host": "test.com",
            "User-Agent": "test ua",
        }
        cls.test_url = "/some/test/url?a=10&b=foo&b=bar#some-fragment"
        cls.test_body = b"some data"
        cls.test_json = {"some": {"data": True}}
        cls.test_form = {"a": "10", "b": "test"}

    def _create_request(self, method="GET", url=None, headers=None, body=None):
        return Request(
            method=method,
            url=url or self.test_url,
            headers=headers or self.common_headers,
            body=body or self.test_body,
        )

    def test_attributes(self):
        request = self._create_request(
            headers=(self.common_headers | {"Content-Length": len(self.test_body)})
        )

        self.assertIsInstance(request.id, UUID)
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.path, "/some/test/url")
        self.assertEqual(request.query, "a=10&b=foo&b=bar")
        self.assertEqual(request.fragment, "some-fragment")
        self.assertEqual(request.url, self.test_url)
        self.assertEqual(request.params, {"a": "10", "b": ["foo", "bar"]})
        self.assertEqual(request.headers, {"Content-Length": len(self.test_body), **self.common_headers})
        self.assertEqual(request.user_agent, "test ua")
        self.assertEqual(request.body, self.test_body)
        self.assertEqual(repr(request), f"<Request: GET {self.test_url}>")

    def test_request_body_without_ctype(self):
        headers = {"Content-Length": len(self.test_body), **self.common_headers}
        request = self._create_request(headers=headers)

        self.assertEqual(request.body, self.test_body)

    def test_request_with_json(self):
        body = dumps(self.test_json).encode()
        headers = {
            "Content-Length": len(body),
            "Content-Type": "application/json",
            **self.common_headers,
        }

        request = self._create_request(headers=headers, body=body)

        self.assertEqual(request.headers["Content-Type"], "application/json")
        self.assertEqual(request.content_type, "application/json")
        self.assertEqual(request.json, self.test_json)

    def test_request_json_with_invalid_ctype(self):
        body = dumps(self.test_json).encode()
        headers = {
            "Content-Length": len(body),
            "Content-Type": "application/some_app",
            **self.common_headers,
        }

        request = self._create_request(headers=headers, body=body)
        with self.assertRaises(ValueError) as exc:
            _ = request.json

        self.assertEqual(str(exc.exception), "Content type does not match as a json")

    def test_request_with_www_form_urlencoded(self):
        body = b"a=10&b=test"
        headers = {
            "Content-Length": len(body),
            "Content-Type": "application/x-www-form-urlencoded",
            **self.common_headers,
        }

        request = self._create_request(headers=headers, body=body)

        self.assertEqual(request.headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(request.content_type, "application/x-www-form-urlencoded")
        self.assertEqual(request.form, self.test_form)

    def test_request_form_with_invalid_ctype(self):
        body = b"a=10&b=test"
        headers = {
            "Content-Length": len(body),
            "Content-Type": "application/some_app",
            **self.common_headers,
        }

        request = self._create_request(headers=headers, body=body)
        with self.assertRaises(ValueError) as exc:
            _ = request.form

        self.assertEqual(str(exc.exception), "Content type does not match as a form")

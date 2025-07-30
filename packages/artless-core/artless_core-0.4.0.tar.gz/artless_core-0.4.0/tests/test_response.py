from http import HTTPStatus
from unittest import TestCase

from artless_core import Response, html, json, plain, redirect


class TestResponse(TestCase):
    def setUp(self):
        self.default_headers = {"Content-Type": "text/plain"}
        self.default_status = "200 OK"
        self.default_content_type = "text/plain"

    def test_repr(self):
        self.assertEqual(repr(Response()), f"<Response: {self.default_status}>")

    def test_headers_operations(self):
        response = Response()

        # Test default headers
        self.assertDictEqual(response.headers, self.default_headers)

        # Test adding new header
        response.headers["Set-Cookie"] = "userId=67890; Secure; HttpOnly"
        expected_headers = {**self.default_headers, "Set-Cookie": "userId=67890; Secure; HttpOnly"}
        self.assertDictEqual(response.headers, expected_headers)

        # Test replacing existing header
        response.headers["Content-Type"] = "application/json"
        self.assertDictEqual(
            response.headers,
            {"Content-Type": "application/json", "Set-Cookie": "userId=67890; Secure; HttpOnly"},
        )

    def test_status_property(self):
        # Test default status
        response = Response()
        self.assertEqual(response.status, self.default_status)

        # Test custom status
        response.status = HTTPStatus.CREATED
        self.assertEqual(response.status, "201 Created")

        # Test initialization with custom status
        no_content_response = Response(status=HTTPStatus.NO_CONTENT)
        self.assertEqual(no_content_response.status, "204 No Content")

    def test_content_type_property(self):
        response = Response()

        # Test default content type
        self.assertEqual(response.content_type, self.default_content_type)

        # Test setting content type
        response.content_type = "application/json"
        self.assertEqual(response.content_type, "application/json")

    def test_body_property(self):
        response = Response()

        # Test string body
        response.body = "regular string"
        self.assertEqual(response.body, b"regular string\n")

        # Test bytes body
        response.body = b"native strings"
        self.assertEqual(response.body, b"native strings\n")

        # Test invalid body type
        with self.assertRaises(TypeError) as exc:
            response.body = {"some": "data"}
        self.assertEqual(str(exc.exception), "Response body must be only string or bytes, not <class 'dict'>")

    def test_response_helpers(self):
        # Test plain helper
        plain_response = plain("some response message")
        self.assertEqual(plain_response.content_type, "text/plain")
        self.assertEqual(plain_response.body, b"some response message\n")

        # Test html helper
        html_content = "<html><body>Hello</body></html>"
        html_response = html(html_content)
        self.assertEqual(html_response.content_type, "text/html")
        self.assertEqual(html_response.body, f"{html_content}\n".encode())

        # Test json helper
        json_data = [{"some": {"native": ["structure"]}}]
        json_response = json(json_data)
        self.assertEqual(json_response.content_type, "application/json")
        self.assertEqual(json_response.body, b'[{"some": {"native": ["structure"]}}]\n')

        # Test redirect helper
        redirect_url = "/redirect/to/some/url/"
        redirect_response = redirect(redirect_url)
        self.assertDictEqual(redirect_response.headers, {"Location": redirect_url})
        self.assertEqual(redirect_response.body, b"")

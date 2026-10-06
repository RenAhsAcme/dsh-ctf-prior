"""无网络回放：验证终局分块、EOF、半包超时及粘包。"""

import socket
import unittest
from unittest.mock import patch

from buffered_io import BufferedReader, StreamClosed


class Replay:
    def __init__(self, chunks):
        self.chunks = iter(chunks)
        self.timeout = 17.0

    def gettimeout(self):
        return self.timeout

    def settimeout(self, timeout):
        self.timeout = timeout

    def recv(self, size):
        chunk = next(self.chunks, b"")
        if isinstance(chunk, Exception):
            raise chunk
        return chunk


class ReaderTests(unittest.TestCase):
    def test_every_terminal_split(self):
        data = b"You win!\nResult: flag{demo-value}\n"
        for offset in range(1, len(data)):
            with self.subTest(offset=offset):
                transport = Replay([data[:offset], data[offset:]])
                reader = BufferedReader(transport)
                result = reader.read_match(rb"flag\{[^}\r\n]+\}")
                self.assertTrue(result.endswith(b"flag{demo-value}"))
                self.assertEqual(reader.read_to_eof(), b"\n")
                self.assertEqual(transport.timeout, 17.0)

    def test_bytewise_terminal(self):
        reader = BufferedReader(Replay([bytes([b]) for b in b"flag{demo-value}"]))
        self.assertEqual(reader.read_match(rb"flag\{[^}]+\}"), b"flag{demo-value}")

    def test_coalesced_reset(self):
        reader = BufferedReader(Replay([b"lose\nLEVEL 1\nx = next"]))
        self.assertEqual(reader.read_until(b"x = "), b"lose\nLEVEL 1\nx = ")
        self.assertEqual(reader.buffer, b"next")

    def test_eof_preserves_final_data(self):
        chunks = []
        reader = BufferedReader(Replay([b"flag{demo-value}"]), on_chunk=chunks.append)
        with self.assertRaises(StreamClosed) as closed:
            reader.read_until(b"LEVEL")
        self.assertEqual(closed.exception.data, b"flag{demo-value}")
        self.assertEqual(reader.read_to_eof(), b"flag{demo-value}")
        self.assertEqual(chunks, [b"flag{demo-value}"])

    def test_timeout_can_resume(self):
        transport = Replay([b"flag{", socket.timeout(), b"demo-value}"])
        reader = BufferedReader(transport)
        with self.assertRaises(TimeoutError):
            reader.read_match(rb"flag\{[^}]+\}")
        self.assertEqual(reader.buffer, b"flag{")
        self.assertEqual(transport.timeout, 17.0)
        self.assertEqual(reader.read_match(rb"flag\{[^}]+\}"), b"flag{demo-value}")

    def test_buffer_limit_preserves_data(self):
        reader = BufferedReader(Replay([b"12345"]), max_buffer=4)
        with self.assertRaises(BufferError):
            reader.read_until(b"end")
        self.assertEqual(reader.buffer, b"12345")

    def test_timeout_is_total_not_per_chunk(self):
        transport = Replay([b"a", b"b"])
        reader = BufferedReader(transport, timeout=2)
        with patch("buffered_io.time.monotonic", side_effect=[0, 1, 3]):
            with self.assertRaises(TimeoutError):
                reader.read_until(b"end")
        self.assertEqual(reader.buffer, b"a")
        self.assertEqual(next(transport.chunks), b"b")

    def test_empty_boundary_rejected(self):
        reader = BufferedReader(Replay([]))
        with self.assertRaises(ValueError):
            reader.read_until(b"")
        with self.assertRaises(ValueError):
            reader.read_match(rb".*?")


if __name__ == "__main__":
    unittest.main()

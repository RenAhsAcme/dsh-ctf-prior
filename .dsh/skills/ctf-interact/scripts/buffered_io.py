"""有边界与总超时的字节流读取；连接、协议及重试由调用者负责。"""

import re
import socket
import time


class StreamClosed(EOFError):
    def __init__(self, data):
        super().__init__("stream closed before the requested boundary")
        self.data = data


class BufferedReader:
    def __init__(self, transport, *, timeout=30.0, max_buffer=1 << 20, on_chunk=None):
        if timeout <= 0 or max_buffer <= 0:
            raise ValueError("timeout and max_buffer must be positive")
        self.transport = transport
        self.timeout = timeout
        self.max_buffer = max_buffer
        self.on_chunk = on_chunk
        self.buffer = b""
        self.closed = False

    def _deadline(self, timeout):
        duration = self.timeout if timeout is None else timeout
        if duration <= 0:
            raise ValueError("timeout must be positive")
        return time.monotonic() + duration

    def _fill(self, deadline):
        if self.closed:
            raise StreamClosed(self.buffer)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("read deadline exceeded; buffer preserved")
        previous = self.transport.gettimeout()
        try:
            self.transport.settimeout(remaining)
            try:
                chunk = self.transport.recv(65536)
            except socket.timeout as error:
                raise TimeoutError("read deadline exceeded; buffer preserved") from error
        finally:
            self.transport.settimeout(previous)
        if not chunk:
            self.closed = True
            raise StreamClosed(self.buffer)
        self.buffer += chunk
        if self.on_chunk is not None:
            self.on_chunk(chunk)
        if len(self.buffer) > self.max_buffer:
            raise BufferError("read buffer limit exceeded; data preserved")

    def _take(self, end):
        result, self.buffer = self.buffer[:end], self.buffer[end:]
        return result

    def read_until(self, marker, *, timeout=None):
        if not marker:
            raise ValueError("marker must not be empty")
        deadline = self._deadline(timeout)
        while True:
            position = self.buffer.find(marker)
            if position >= 0:
                return self._take(position + len(marker))
            self._fill(deadline)

    def read_match(self, pattern, *, timeout=None):
        """消费到完整匹配末尾；pattern 必须描述完整结果而非起始前缀。"""
        compiled = re.compile(pattern)
        deadline = self._deadline(timeout)
        while True:
            match = compiled.search(self.buffer)
            if match is not None:
                if match.end() == match.start():
                    raise ValueError("pattern must not match empty data")
                return self._take(match.end())
            self._fill(deadline)

    def read_to_eof(self, *, timeout=None):
        deadline = self._deadline(timeout)
        try:
            while True:
                self._fill(deadline)
        except StreamClosed:
            return self._take(len(self.buffer))

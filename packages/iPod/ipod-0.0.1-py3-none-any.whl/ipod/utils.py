"""
various utilities
"""

from typing import BinaryIO


def buffered_copy(
	source: BinaryIO,
	destination: BinaryIO,
	*,
	limit: int = None,
	buffer_size: int = 0x1000
):
	offset = 0

	while True:
		read_amount = min(buffer_size, limit - offset) if limit else buffer_size
		buffer = source.read(read_amount)
		offset += read_amount

		destination.write(buffer)

		if len(buffer) < buffer_size:
			# either we've hit the limit or there is no more data
			break


def buffered(
	source: BinaryIO,
	*,
	limit: int = None,
	buffer_size: int = 0x1000
):
	offset = 0

	while True:
		read_amount = min(buffer_size, limit - offset) if limit else buffer_size
		buffer = source.read(read_amount)
		offset += read_amount

		yield buffer

		if len(buffer) < buffer_size:
			# either we've hit the limit or there is no more data
			break


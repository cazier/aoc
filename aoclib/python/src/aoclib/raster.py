import struct
import dataclasses


@dataclasses.dataclass
class Raster:
    pixels: list[list[bool]]
    depth: int = 0x20

    _width: int = dataclasses.field(init=False)
    _height: int = dataclasses.field(init=False)
    _size: int = dataclasses.field(init=False)

    _bmp_header = struct.pack("<H", 0x4D42)

    def __post_init__(self) -> None:
        self._height = len(self.pixels)
        self._width = len(self.pixels[0])
        self._size = self._height * max(self._width // 8, 1) * 8

    def write(self) -> list[bytes]:
        # fmt: off
        header = [
            self._bmp_header,                             # BMP magic bytes/signature
            struct.pack("<I", self._size + 0x0E + 0x28),  # File size + BMP header size + DIB header size
            struct.pack("<H", 0x00),                      # Unused
            struct.pack("<H", 0x00),                      # Unused
            struct.pack("<I", 0x0E + 0x28),               # Offset to pixel array
            *(
                                                  # BITMAPINFOHEADER
                struct.pack("<I", 0x28),          # DIB header size
                struct.pack("<I", self._width),   # Width in pixels
                struct.pack("<I", self._height),  # Height in pixels
                struct.pack("<H", 0x01),          # Number of color planes (must be one)
                struct.pack("<H", self.depth),    # Pixel depth (size in bits)
                struct.pack("<I", 0x00),          # Compression (None)
                struct.pack("<I", self._size),    # Image data size
                struct.pack("<I", 0x0B13),        # Horizontal resolution
                struct.pack("<I", 0x0B13),        # Vertical resolution
                struct.pack("<I", 0x02),          # Number of colors
                struct.pack("<I", 0x00),          # Color importance (must be zero)
            ),
        ]
        # fmt: on

        image_data = []

        for row in reversed(self.pixels):
            for pixel in row:
                if pixel:
                    image_data.append((0x00).to_bytes(4))
                else:
                    image_data.append((0xFFFFFF00).to_bytes(4))

            image_data.append((0x0).to_bytes((len(row) * 3) % 4))

        return b"".join((*header, *image_data))


if __name__ == "__main__":
    data = [
        [True, True, True, True, False, False, False, False],
        [True, True, True, True, False, False, False, False],
        [True, True, True, True, False, False, False, False],
        [True, True, True, True, False, False, False, False],
        [False, False, False, False, True, True, True, True],
        [False, False, False, False, True, True, True, True],
        [False, False, False, False, True, True, True, True],
        [False, False, False, False, True, True, True, True],
    ]

    img = Raster(data)

    with open("output.bmp", "wb") as f:
        f.write(img.write())

r"""ByteBlaster - Python implementation of the EMWIN ByteBlaster protocol.

This package provides a client for connecting to ByteBlaster servers and receiving
EMWIN (Emergency Managers Weather Information Network) data using the Quick Block
Transfer protocol.

Example usage:
    ```python
    import asyncio
    from pathlib import Path

    from byteblaster import (
        ByteBlasterClientOptions,
        ByteBlasterFileManager,
        CompletedFile,
    )

    async def save_file(file: CompletedFile) -> None:
        output_dir = Path("weather_data")
        output_dir.mkdir(exist_ok=True)
        path = output_dir / file.filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file.data)
        print(f"✓ Saved: {path} ({len(file.data)} bytes)")

    async def main() -> None:
        options = ByteBlasterClientOptions(email="user@example.com")
        file_manager = ByteBlasterFileManager(options)

        # Option 1: Callback-based approach
        file_manager.subscribe(save_file)

        # Option 2: Async iterator approach
        # async with file_manager.stream_files() as files:
        #     async for file in files:
        #         await save_file(file)

        await file_manager.start()
        print("Client started, waiting for files...")

        # Keep running until Ctrl+C is pressed
        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            print("\nStopping client...")
            await file_manager.stop()
            print("Client stopped.")

    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\nExiting.")
    ```
"""

from byteblaster.client import ByteBlasterClient, ByteBlasterClientOptions, SegmentStream
from byteblaster.file_manager import (
    ByteBlasterFileManager,
    CompletedFile,
    FileAssembler,
    FileStream,
)
from byteblaster.protocol.models import (
    ByteBlasterServerList,
    QBTSegment,
)
from byteblaster.utils import ServerListManager

__version__ = "1.0.0"
__author__ = "ByteBlaster Python Team"
__email__ = "support@example.com"

__all__ = [
    "ByteBlasterClient",
    "ByteBlasterClientOptions",
    "ByteBlasterFileManager",
    "ByteBlasterServerList",
    "CompletedFile",
    "FileAssembler",
    "FileStream",
    "QBTSegment",
    "SegmentStream",
    "ServerListManager",
]

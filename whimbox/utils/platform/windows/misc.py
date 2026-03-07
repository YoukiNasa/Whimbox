import numpy as np
from winrt.windows.storage.streams import Buffer
from winrt.windows.graphics.imaging import SoftwareBitmap, BitmapPixelFormat, BitmapAlphaMode
from common import is_rgba_image

def numpy_array_to_software_bitmap(image: np.ndarray):
    """将 NumPy 数组转换为 Windows SoftwareBitmap 对象。"""
    if len(image.shape) == 3 and image.shape[2] == 3:
        # 转换RGB到RGBA
        image = np.concatenate([image, np.full((image.shape[0], image.shape[1], 1), 255, dtype=image.dtype)], axis=2)

    if not is_rgba_image(image=image):
        raise ValueError(
            "Input image must be a 3D array with shape (H, W, 4) representing an RGBA image."
        )
    
    image_bytes = image.astype('uint8').tobytes()
    image_bytes_size = len(image_bytes)

    buffer = Buffer(image_bytes_size)
    buffer.length = image_bytes_size
    with memoryview(buffer) as mv:
        mv[:] = image_bytes

    software_bitmap = SoftwareBitmap(
        BitmapPixelFormat.RGBA8,
        image.shape[1],
        image.shape[0],
        BitmapAlphaMode.PREMULTIPLIED
    )
    software_bitmap.copy_from_buffer(buffer)
    return software_bitmap

########################################################################################
# Windows API utilities for finding windows by title or process name.
from ctypes import windll
from ctypes.wintypes import HWND, LPCWSTR

FindWindowW = windll.user32.FindWindowW
FindWindowW.argtypes = [LPCWSTR, LPCWSTR]
FindWindowW.restype = HWND

def find_window_by_title(window_title: str) -> HWND:
    """Find a window by its title and return its handle (HWND)."""
    hwnd = FindWindowW(None, window_title)
    return hwnd if hwnd else None

def find_window_by_process(process_name: str) -> HWND:
    pass

########################################################################################
# SPDX-License-Identifier: MIT
# Copyright 2024 David Lechner <david@pybricks.com>

from concurrent.futures import Future
from ctypes import WinError
from typing import Optional, TypeVar, Union, overload

from winrt.windows.foundation import AsyncStatus, IAsyncAction, IAsyncOperation

T = TypeVar("T")


@overload
def wait_for(operation: IAsyncOperation[T]) -> T: ...
@overload
def wait_for(operation: IAsyncAction) -> None: ...


def wait_for(operation: Union[IAsyncOperation[T], IAsyncAction]) -> Optional[T]:
    """
    Wait for the given async operation to complete and return its result.

    For use in non-asyncio apps.
    """
    future = Future[Optional[T]]()

    def completed(async_op: IAsyncOperation[T] | IAsyncAction, status: AsyncStatus):
        try:
            if status == AsyncStatus.COMPLETED:
                future.set_result(async_op.get_results())
            elif status == AsyncStatus.ERROR:
                future.set_exception(WinError(async_op.error_code.value))
            elif status == AsyncStatus.CANCELED:
                future.cancel()
        except BaseException as e:
            future.set_exception(e)

    operation.completed = completed

    return future.result()
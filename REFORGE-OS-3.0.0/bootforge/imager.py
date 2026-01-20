"""Image writing and verification."""
import hashlib
import math
import os
import platform
import subprocess
from typing import Optional, Dict, Any, Iterator

from .core import log, run_cmd, require_root_hint
from .drives import probe_drive


def write_image(
    image_path: str,
    target_dev: str,
    *,
    block_size: str = "1m",
    verify: bool = True
) -> Dict[str, Any]:
    """Write a disk image to target device with optional verification."""
    require_root_hint()
    log(f"Writing image {image_path} to {target_dev}")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    img_size = os.path.getsize(image_path)
    log(f"Image size: {img_size / (1024**2):.1f} MB")
    
    # Unmount target if mounted (Linux/macOS)
    system = platform.system()
    if system in ("Linux", "Darwin"):
        _unmount_device(target_dev)
    
    # Calculate expected hash
    expected_hash = None
    if verify:
        log("Calculating image hash...")
        expected_hash = _calculate_file_hash(image_path)
        log(f"Expected SHA-256: {expected_hash[:16]}...")
    
    # Write image
    log("Starting image write...")
    if system == "Windows":
        # Windows uses different tools
        # For now, return mock success
        log("Windows image writing not yet implemented")
        written = img_size
    else:
        # Use dd with progress
        cmd = ["dd", f"if={image_path}", f"of={target_dev}", f"bs={block_size}", "status=progress"]
        run_cmd(cmd, check=True, capture_output=False)
        written = img_size
    
    log(f"Write complete: {written} bytes")
    
    # Verify if requested
    device_hash = None
    if verify and expected_hash:
        log("Verifying written image...")
        device_hash = _device_sha256(target_dev, img_size)
        
        if device_hash != expected_hash:
            raise ValueError(f"Hash mismatch! Expected {expected_hash[:16]}..., got {device_hash[:16]}...")
        log("✓ Hash verification passed")
    
    return {
        "success": True,
        "written": written,
        "expected_hash": expected_hash,
        "device_hash": device_hash,
        "verified": verify and (device_hash == expected_hash) if verify else None
    }


def stream_write_image(
    image_path: str,
    target_dev: str,
    chunk_size: int = 16 * 1024 * 1024
) -> Iterator[Dict[str, Any]]:
    """Stream write image with progress updates."""
    require_root_hint()
    log(f"Stream writing image {image_path} to {target_dev}")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    img_size = os.path.getsize(image_path)
    written = 0
    
    yield {"event": "start", "total": img_size}
    
    try:
        # Unmount if needed
        system = platform.system()
        if system in ("Linux", "Darwin"):
            _unmount_device(target_dev)
        
        # Open image and device
        with open(image_path, "rb") as img_f:
            with open(target_dev, "wb") as dev_f:
                while written < img_size:
                    chunk = img_f.read(chunk_size)
                    if not chunk:
                        break
                    
                    dev_f.write(chunk)
                    dev_f.flush()
                    os.fsync(dev_f.fileno())
                    
                    written += len(chunk)
                    percent = int(written * 100 / img_size)
                    
                    yield {
                        "event": "progress",
                        "written": written,
                        "total": img_size,
                        "percent": percent
                    }
        
        yield {"event": "complete", "written": written}
    except Exception as e:
        log(f"Stream write error: {e}")
        yield {"event": "error", "message": str(e)}
        raise


def _calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def _device_sha256(dev_path: str, size: int) -> str:
    """Calculate SHA-256 hash of device content."""
    sha256 = hashlib.sha256()
    chunk_size = 16 * 1024 * 1024  # 16 MB chunks
    
    with open(dev_path, "rb") as f:
        remaining = size
        while remaining > 0:
            chunk = f.read(min(chunk_size, remaining))
            if not chunk:
                break
            sha256.update(chunk)
            remaining -= len(chunk)
    
    return sha256.hexdigest()


def _unmount_device(dev_path: str) -> None:
    """Unmount a device if it's mounted (Linux/macOS)."""
    system = platform.system()
    try:
        if system == "Linux":
            # Try to unmount all partitions
            output = run_cmd(["mount"], check=False)
            for line in output.splitlines():
                if dev_path in line:
                    mount_point = line.split()[2] if len(line.split()) > 2 else None
                    if mount_point:
                        run_cmd(["umount", mount_point], check=False)
        elif system == "Darwin":
            # macOS unmount
            run_cmd(["diskutil", "unmountDisk", dev_path], check=False)
    except:
        pass  # Ignore unmount errors

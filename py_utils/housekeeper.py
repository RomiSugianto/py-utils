import os
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

class Housekeeper:
    """A helper class for file housekeeping operations."""

    @staticmethod
    def housekeep_by_age(directory: str, days_old: int, confirm: bool = True) -> int:
        """
        Delete files older than the specified number of days based on modification time.

        Args:
            directory: Path to the directory
            days_old: Delete files older than this many days
            confirm: Whether to ask for confirmation

        Returns:
            Number of files deleted
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist")

        # Calculate cutoff time
        cutoff_time = datetime.now() - timedelta(days=days_old)
        cutoff_timestamp = cutoff_time.timestamp()

        # Get all files with their modification times
        files_to_delete = []
        for file_path in Path(directory).rglob('*'):
            if file_path.is_file() and file_path.stat().st_mtime < cutoff_timestamp:
                files_to_delete.append(file_path)

        if not files_to_delete:
            print(f"No files older than {days_old} days found.")
            return 0

        if confirm:
            print(f"Will delete {len(files_to_delete)} files older than {days_old} days:")
            for file in files_to_delete[:5]:  # Show first 5
                print(f"  {file}")
            if len(files_to_delete) > 5:
                print(f"  ... and {len(files_to_delete) - 5} more")
            response = input("Proceed? (y/N): ")
            if response.lower() != 'y':
                print("Deletion cancelled.")
                return 0

        deleted_count = 0
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

        return deleted_count

    @staticmethod
    def housekeep_by_count(directory: str, keep_count: int, confirm: bool = True) -> int:
        """
        Keep only the N newest files in the directory based on modification time.
        Deletes all other files.

        Args:
            directory: Path to the directory
            keep_count: Number of newest files to keep
            confirm: Whether to ask for confirmation

        Returns:
            Number of files deleted
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist")

        # Get all files with their modification times
        files = []
        for file_path in Path(directory).rglob('*'):
            if file_path.is_file():
                files.append((file_path, file_path.stat().st_mtime))

        if len(files) <= keep_count:
            print(f"Only {len(files)} files found, no deletion needed.")
            return 0

        # Sort by modification time (newest first)
        files.sort(key=lambda x: x[1], reverse=True)

        # Files to delete (beyond keep_count)
        files_to_delete = files[keep_count:]

        if confirm:
            print(f"Will delete {len(files_to_delete)} files, keeping {keep_count} newest.")
            response = input("Proceed? (y/N): ")
            if response.lower() != 'y':
                print("Deletion cancelled.")
                return 0

        deleted_count = 0
        for file_path, _ in files_to_delete:
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

        return deleted_count

# Convenience function
def cleanup_directory(directory: str, days_old: Optional[int] = None, keep_count: Optional[int] = None) -> int:
    """
    Convenience function for housekeeping operations.

    Args:
        directory: Path to the directory
        days_old: Delete files older than this many days (if specified)
        keep_count: Number of newest files to keep (if specified)

    Returns:
        Number of files deleted
    """
    if days_old is not None:
        return Housekeeper.housekeep_by_age(directory, days_old)
    elif keep_count is not None:
        return Housekeeper.housekeep_by_count(directory, keep_count)
    else:
        print("Specify days_old or keep_count")
        return 0

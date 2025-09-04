import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from pathlib import Path
from py_utils.housekeeper import Housekeeper, cleanup_directory


class TestHousekeeper:
    """Test cases for Housekeeper class."""

    def test_housekeep_by_age_no_files(self, tmp_path):
        """Test housekeep_by_age with no files in directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        # Should not raise any errors
        result = Housekeeper.housekeep_by_age(str(empty_dir), days_old=7, confirm=False)
        assert result == 0

    def test_housekeep_by_age_recent_files(self, tmp_path):
        """Test housekeep_by_age with only recent files."""
        test_dir = tmp_path / "test_recent"
        test_dir.mkdir()

        # Create a recent file
        recent_file = test_dir / "recent.txt"
        recent_file.write_text("test content")

        with patch("os.remove") as mock_remove:
            result = Housekeeper.housekeep_by_age(
                str(test_dir), days_old=7, confirm=False
            )

            # Should not delete recent files
            mock_remove.assert_not_called()
            assert result == 0

    def test_housekeep_by_age_old_files(self, tmp_path):
        """Test housekeep_by_age with old files."""
        test_dir = tmp_path / "test_old"
        test_dir.mkdir()

        # Create an old file
        old_file = test_dir / "old.txt"
        old_file.write_text("test content")

        # Mock the file modification time to be old (10 days ago)
        old_timestamp = (datetime.now() - timedelta(days=10)).timestamp()

        with patch.object(Path, "rglob") as mock_rglob:
            mock_file = MagicMock()
            mock_file.is_file.return_value = True
            mock_file.stat.return_value.st_mtime = old_timestamp
            mock_file.__str__ = lambda: str(old_file)
            mock_rglob.return_value = [mock_file]

            with patch("os.remove") as mock_remove:
                result = Housekeeper.housekeep_by_age(
                    str(test_dir), days_old=7, confirm=False
                )

                # Should delete old files
                mock_remove.assert_called_once()
                assert result == 1

    def test_housekeep_by_age_invalid_directory(self):
        """Test housekeep_by_age with invalid directory."""
        with pytest.raises(FileNotFoundError):
            Housekeeper.housekeep_by_age("/invalid/path", days_old=7, confirm=False)

    def test_housekeep_by_count_no_files(self, tmp_path):
        """Test housekeep_by_count with no files in directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = Housekeeper.housekeep_by_count(
            str(empty_dir), keep_count=5, confirm=False
        )
        assert result == 0

    def test_housekeep_by_count_fewer_files_than_keep(self, tmp_path):
        """Test housekeep_by_count when there are fewer files than keep count."""
        test_dir = tmp_path / "test_few"
        test_dir.mkdir()

        # Create 3 files
        for i in range(3):
            file_path = test_dir / f"file_{i}.txt"
            file_path.write_text(f"content {i}")

        with patch("os.remove") as mock_remove:
            result = Housekeeper.housekeep_by_count(
                str(test_dir), keep_count=5, confirm=False
            )

            # Should not delete any files
            mock_remove.assert_not_called()
            assert result == 0

    def test_housekeep_by_count_more_files_than_keep(self, tmp_path):
        """Test housekeep_by_count when there are more files than keep count."""
        test_dir = tmp_path / "test_many"
        test_dir.mkdir()

        # Create 7 files
        for i in range(7):
            file_path = test_dir / f"file_{i}.txt"
            file_path.write_text(f"content {i}")

        with patch.object(Path, "rglob") as mock_rglob:
            mock_files = []
            for i in range(7):
                mock_file = MagicMock()
                mock_file.is_file.return_value = True
                mock_file.stat.return_value.st_mtime = (
                    datetime.now().timestamp() - i * 3600
                )
                mock_file.__str__ = lambda i=i: str(test_dir / f"file_{i}.txt")
                mock_files.append(mock_file)
            mock_rglob.return_value = mock_files

            with patch("os.remove") as mock_remove:
                result = Housekeeper.housekeep_by_count(
                    str(test_dir), keep_count=3, confirm=False
                )

                # Should delete 4 oldest files (keep 3 newest)
                assert mock_remove.call_count == 4
                assert result == 4

    def test_housekeep_by_count_invalid_directory(self):
        """Test housekeep_by_count with invalid directory."""
        with pytest.raises(FileNotFoundError):
            Housekeeper.housekeep_by_count("/invalid/path", keep_count=5, confirm=False)


class TestCleanupDirectory:
    """Test cases for the cleanup_directory convenience function."""

    @patch("py_utils.housekeeper.Housekeeper.housekeep_by_age")
    def test_cleanup_directory_by_age(self, mock_housekeep_age):
        """Test cleanup_directory with age-based cleanup."""
        mock_housekeep_age.return_value = 5

        result = cleanup_directory("/test/dir", days_old=7)

        mock_housekeep_age.assert_called_once_with("/test/dir", 7)
        assert result == 5

    @patch("py_utils.housekeeper.Housekeeper.housekeep_by_count")
    def test_cleanup_directory_by_count(self, mock_housekeep_count):
        """Test cleanup_directory with count-based cleanup."""
        mock_housekeep_count.return_value = 3

        result = cleanup_directory("/test/dir", keep_count=5)

        mock_housekeep_count.assert_called_once_with("/test/dir", 5)
        assert result == 3

    def test_cleanup_directory_no_parameters(self, capsys):
        """Test cleanup_directory with no parameters specified."""
        result = cleanup_directory("/test/dir")

        assert result == 0
        captured = capsys.readouterr()
        assert "Specify days_old or keep_count" in captured.out

    def test_cleanup_directory_both_parameters(self):
        """Test cleanup_directory with both parameters (should use age)."""
        with patch(
            "py_utils.housekeeper.Housekeeper.housekeep_by_age"
        ) as mock_housekeep_age:
            mock_housekeep_age.return_value = 2

            result = cleanup_directory("/test/dir", days_old=10, keep_count=5)

            mock_housekeep_age.assert_called_once_with("/test/dir", 10)
            assert result == 2

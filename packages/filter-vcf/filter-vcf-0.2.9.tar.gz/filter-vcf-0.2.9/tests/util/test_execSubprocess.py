import subprocess
from unittest import TestCase
from unittest.mock import patch, MagicMock

from filter_vcf.util.execSubprocess import exec_subprocess


class TestFilterContigs(TestCase):
    @patch("subprocess.run")
    def test_exec_subprocess_success(self, mock_sub_process):
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stderr = ""
        mock_process.stdout = "command output"
        mock_sub_process.return_value = mock_process

        result = exec_subprocess("echo 'test'", MagicMock())

        mock_sub_process.assert_called_once_with(
            "echo 'test'", shell=True, capture_output=True, text=True
        )

        assert result == mock_process
        assert result.returncode == 0
        assert result.stdout == "command output"

    @patch("subprocess.run")
    def test_exec_subprocess_failure(self, mock_sub_process):
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = "command failed"
        mock_process.stdout = ""
        mock_sub_process.return_value = mock_process

        mock_logger = MagicMock()

        with self.assertRaises(subprocess.CalledProcessError):
            exec_subprocess("invalid_command", mock_logger)

        mock_sub_process.assert_called_once_with(
            "invalid_command", shell=True, capture_output=True, text=True
        )

        mock_logger.error.assert_called_once_with(
            "Command invalid_command failed with: command failed"
        )

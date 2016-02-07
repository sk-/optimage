import os.path
import subprocess

import pytest

import optimage


def test_prefix():
    tmp_filename = optimage._get_temporary_filename(prefix='prefix')
    assert os.path.basename(tmp_filename).startswith('prefix')
    assert not os.path.exists(tmp_filename)


@pytest.mark.parametrize('filename, expected_result', [
    ('test_data/valid1.png', True),
    ('test_data/valid1.jpg', False),
])
def test_is_png(filename, expected_result):
    assert optimage._is_png(filename) == expected_result


@pytest.mark.parametrize('filename, expected_result', [
    ('test_data/valid1.png', False),
    ('test_data/valid1.jpg', True),
])
def test_is_jpeg(filename, expected_result):
    assert optimage._is_jpeg(filename) == expected_result


@pytest.mark.parametrize('filename, magic, expected_result', [
    ('test_data/valid1.png', b'\x89\x50\x4E\x47', True),
    ('test_data/valid1.png', b'\x89\x50\x4E', True),
    ('test_data/valid1.png', b'\x89\x51', False),
])
def test_check_magic_number(filename, magic, expected_result):
    assert optimage._check_magic_number(filename, magic) == expected_result


@pytest.mark.parametrize('filename1, filename2, expected_result', [
    ('test_data/valid1.png', 'test_data/valid1_compressed.png', True),
    ('test_data/valid1.png', 'test_data/valid1.jpg', True),
    ('test_data/valid1.png', 'test_data/valid2.png', False),
])
def test_images_are_equal(filename1, filename2, expected_result):
    assert optimage._images_are_equal(filename1, filename2) == expected_result


class TestCallBinary:
    cmd_args = ['cmd', 'arg1', 'arg2']

    def test_success(self, monkeypatch):
        def mock_check_output(args, stderr=None):
            assert args == self.cmd_args
            assert stderr == subprocess.STDOUT
            return ''

        monkeypatch.setattr(subprocess, 'check_output', mock_check_output)
        optimage._call_binary(self.cmd_args)

    def test_missing_binary(self, monkeypatch):
        def mock_check_output(args, stderr=None):
            assert args == self.cmd_args
            assert stderr == subprocess.STDOUT
            raise optimage.FileNotFoundError(2, 'file not found', None)

        monkeypatch.setattr(subprocess, 'check_output', mock_check_output)
        with pytest.raises(optimage.MissingBinary) as excinfo:
            optimage._call_binary(self.cmd_args)

        assert excinfo.value.filename == self.cmd_args[0]

    def test_cmd_error(self, monkeypatch):
        def mock_check_output(args, stderr=None):
            assert args == self.cmd_args
            assert stderr == subprocess.STDOUT
            raise subprocess.CalledProcessError(1, args)

        monkeypatch.setattr(subprocess, 'check_output', mock_check_output)
        with pytest.raises(subprocess.CalledProcessError):
            optimage._call_binary(self.cmd_args)

# TODO(skreft): test compressors

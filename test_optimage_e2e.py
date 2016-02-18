import os
import shutil
import subprocess

import pytest
try:
  import pytest_catchlog
  catchlog_available = True
except ImportError:
  catchlog_available = False

import optimage


def test_missing_filename(capsys):
    with pytest.raises(SystemExit) as excinfo:
        exit_code = optimage.main([])
    assert excinfo.value.code == 2
    _, err = capsys.readouterr()
    py3_error = 'error: the following arguments are required: filename'
    py2_error = 'error: too few arguments'
    assert py3_error in err or py2_error in err


def test_input_is_directory(capsys):
    exit_code = optimage.main(['test_data'])
    assert exit_code == 3
    _, err = capsys.readouterr()
    assert err == 'test_data is not an image file\n'


def test_input_does_not_exist(capsys):
    exit_code = optimage.main(['test_data/nonexistent.png'])
    assert exit_code == 3
    _, err = capsys.readouterr()
    assert err == 'test_data/nonexistent.png is not an image file\n'


def test_unsupported_extension(capsys):
    exit_code = optimage.main(['test_data/valid1.gif'])
    assert exit_code == 4
    _, err = capsys.readouterr()
    assert err == 'No lossless compressor defined for extension ".gif"\n'


@pytest.mark.parametrize('filename', [
    ('wrong_extension.png'),
    ('wrong_extension.jpg'),
])
def test_invalid_extension(filename, capsys):
    exit_code = optimage.main([os.path.join('test_data', filename)])
    assert exit_code == 5
    _, err = capsys.readouterr()
    assert filename in err
    assert 'Please correct the extension\n' in err


@pytest.mark.parametrize('filename', [
    ('valid1_compressed.png'),
    ('valid2_compressed.png'),
    ('valid3_compressed.jpg'),
])
def test_optimized_file(filename, capsys):
    exit_code = optimage.main([os.path.join('test_data', filename)])
    assert exit_code == 0
    out, err = capsys.readouterr()
    assert (out, err) == ('', '')

@pytest.mark.parametrize('filename', [
    ('valid1.png'),
    ('valid2.png'),
    ('valid3.jpg'),
])
def test_check_optimized(filename, capsys):
    exit_code = optimage.main([os.path.join('test_data', filename)])
    assert exit_code == 1
    out, err = capsys.readouterr()
    assert 'File can be losslessly compressed to' in out
    assert err == ''


@pytest.mark.parametrize('filename', [
    ('valid1.png'),
    ('valid2.png'),
    ('valid3.jpg'),
])
def test_replace(filename, capsys, tmpdir):
    original_filename = os.path.join('test_data', filename)
    output_filename = os.path.join(tmpdir.dirname, filename)
    shutil.copy(original_filename, output_filename)
    os.chmod(output_filename, 420)  # 420 == 0o644

    exit_code = optimage.main(['--replace', output_filename])
    assert exit_code == 0
    out, err = capsys.readouterr()
    assert 'File was losslessly compressed to' in out
    assert err == ''

    original_size = os.path.getsize(original_filename)
    output_size = os.path.getsize(output_filename)

    assert optimage._images_are_equal(original_filename, output_filename)
    assert original_size > output_size


@pytest.mark.parametrize('filename', [
    ('valid1.png'),
    ('valid2.png'),
    ('valid3.jpg'),
])
def test_output_file(filename, capsys, tmpdir):
    original_filename = os.path.join('test_data', filename)
    output_filename = os.path.join(tmpdir.dirname, filename)

    exit_code = optimage.main(['--output', output_filename, original_filename])
    assert exit_code == 0
    out, err = capsys.readouterr()
    assert 'File was losslessly compressed to' in out
    assert err == ''

    original_size = os.path.getsize(original_filename)
    output_size = os.path.getsize(output_filename)

    assert optimage._images_are_equal(original_filename, output_filename)
    assert original_size > output_size


def test_binary_not_found(capsys, monkeypatch):
    def mock_check_output(args, stderr=None):
        raise optimage.FileNotFoundError()

    monkeypatch.setattr(subprocess, 'check_output', mock_check_output)
    exit_code = optimage.main([os.path.join('test_data', 'valid1.png')])
    assert exit_code == 6
    _, err = capsys.readouterr()
    assert err == 'The executable "pngcrush" was not found. Please install it and re-run this command.\n'


def test_commanderror(capsys, monkeypatch):
    def mock_check_output(args, stderr=None):
        raise subprocess.CalledProcessError(1, args, 'custom error'.encode('utf-8'))

    monkeypatch.setattr(subprocess, 'check_output', mock_check_output)
    exit_code = optimage.main([os.path.join('test_data', 'valid1.png')])
    assert exit_code == 7
    _, err = capsys.readouterr()
    assert 'Output:\ncustom error' in err


@pytest.mark.skipif(not catchlog_available,
                    reason='pytest_catchlog not available')
@pytest.mark.parametrize('filename, compressor', [
    # Do not specify compressor as it depends on the version of the commands
    # installed. In Mac I get that pngcrush is better than zopflipng, but not in
    # travis which has the latest version.
    ('valid1.png', ''),
    ('valid1_compressed.png', 'None'),
])
def test_debug(filename, compressor, caplog):
    exit_code = optimage.main([os.path.join('test_data', filename), '--debug'])
    assert '{}: best compressor for'.format(compressor) in caplog.text

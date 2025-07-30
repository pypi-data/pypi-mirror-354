from tera_tera import cli
import tera_tera.cli
import pytest
from datetime import date
from unittest import mock


def test_create_parser():
    parser = cli.create_parser()
    assert parser is not None


@pytest.fixture
def fake_history_file(tmp_path):
    path = tmp_path / "history.json"
    with mock.patch.object(tera_tera.cli, "HISTORY_FILE", str(path)):
        yield path


def test_load_history_empty(fake_history_file):
    if fake_history_file.exists():
        fake_history_file.unlink()
    assert tera_tera.cli.load_history() == {"dates": {}, "last_shown": None}


def test_save_and_load_history(fake_history_file):
    data = {"dates": {"2025-06-06": "img.jpg"}, "last_shown": "img.jpg"}
    tera_tera.cli.save_history(data)
    assert tera_tera.cli.load_history() == data


@mock.patch("tera_tera.cli.platform.system", return_value="Linux")
@mock.patch("tera_tera.cli.subprocess.run")
def test_open_image_linux(mock_run, _):
    tera_tera.cli.open_image("/path/to/img.jpg")
    mock_run.assert_called_once_with(["xdg-open", "/path/to/img.jpg"])


@mock.patch("tera_tera.cli.date")
@mock.patch("tera_tera.cli.open_image")
@mock.patch("tera_tera.cli.save_history")
@mock.patch("tera_tera.cli.load_history")
@mock.patch("tera_tera.cli.random.choice", return_value="b.png")
@mock.patch("tera_tera.cli.os.listdir", return_value=["a.jpg", "b.png", "c.jpeg"])
def test_main_selects_new_image(
    mock_list, mock_choice, mock_load, mock_save, mock_open, mock_date
):
    mock_date.today.return_value = date(2025, 6, 6)
    mock_load.return_value = {"dates": {}, "last_shown": "a.jpg"}

    with mock.patch.object(tera_tera.cli, "IMAGE_FOLDER", "/fake/folder"):
        tera_tera.cli.main([])

    mock_open.assert_called_with("/fake/folder/b.png")

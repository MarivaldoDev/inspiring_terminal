import json

from inspire_term import config


def test_first_run_saves_selected_language(tmp_path, mocker):
    config_file = tmp_path / "config.json"

    fake_console = mocker.Mock()
    fake_console.show_config.return_value = "pt"

    mocker.patch(
        "inspire_term.config.ConsoleRenderer",
        return_value=fake_console,
    )
    mocker.patch("inspire_term.config.CONFIG_DIR", tmp_path)
    mocker.patch("inspire_term.config.CONFIG_FILE", config_file)
    mocker.patch("inspire_term.config.sleep")

    result = config.first_run()

    assert result == {"language": "pt"}
    assert config_file.exists()

    with config_file.open("r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == {"language": "pt"}
    fake_console.welcome.assert_called_once()
    fake_console.show_config.assert_called_once()
    fake_console.console.clear.assert_called_once()


def test_load_config_returns_existing_configuration(tmp_path, mocker):
    config_file = tmp_path / "config.json"
    config_file.write_text(
        '{"language": "es"}',
        encoding="utf-8",
    )

    mocker.patch("inspire_term.config.CONFIG_FILE", config_file)

    result = config.load_config()

    assert result == {"language": "es"}


def test_load_config_calls_first_run_when_file_does_not_exist(
    tmp_path,
    mocker,
):
    config_file = tmp_path / "config.json"

    mocker.patch("inspire_term.config.CONFIG_FILE", config_file)
    first_run_mock = mocker.patch(
        "inspire_term.config.first_run",
        return_value={"language": "en"},
    )

    result = config.load_config()

    assert result == {"language": "en"}
    first_run_mock.assert_called_once()

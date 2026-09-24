from unittest.mock import Mock

from rich.panel import Panel
from rich.table import Table

from inspire_term.ui import ConsoleRenderer


def test_show_prints_panel_with_text_and_author():
    renderer = ConsoleRenderer()
    mock_console = Mock()
    renderer.console = mock_console

    renderer.show("Success is not final.", "Winston Churchill")

    mock_console.print.assert_called_once()
    printed_panel = mock_console.print.call_args[0][0]

    assert isinstance(printed_panel, Panel)
    content = str(printed_panel.renderable)
    assert "Success is not final." in content
    assert "Winston Churchill" in content
    assert printed_panel.title == "💡 Inspiring Terminal"
    assert printed_panel.border_style == "green"


def test_renderer_uses_default_style():
    renderer = ConsoleRenderer()

    assert renderer.style == "default"


def test_renderer_uses_selected_style():
    renderer = ConsoleRenderer(style="simple")

    assert renderer.style == "simple"


def test_show_simple_style_does_not_print_panel():
    renderer = ConsoleRenderer(style="simple")
    mock_console = Mock()
    renderer.console = mock_console

    renderer.show("Success is not final.", "Winston Churchill")

    printed = mock_console.print.call_args[0][0]

    assert not isinstance(printed, Table)


def test_show_simple_style_uses_rich_markup():
    renderer = ConsoleRenderer(style="simple")
    mock_console = Mock()
    renderer.console = mock_console

    renderer.show("Success is not final.", "Winston Churchill")

    printed = mock_console.print.call_args_list

    assert printed[0].args[0] == "[bold bright_yellow]Success is not final.[/]"
    assert printed[1].args[0] == "[italic cyan]— Winston Churchill[/]"


def test_welcome_message():
    renderer = ConsoleRenderer()
    mock_console = Mock()
    renderer.console = mock_console

    renderer.welcome()

    printed_panel = mock_console.print.call_args[0][0]

    assert isinstance(printed_panel, Panel)
    assert printed_panel.title == "Inspiring Terminal"
    assert printed_panel.border_style == "cyan"

    content = str(printed_panel.renderable)
    assert "Welcome to Inspiring Terminal!" in content
    assert "The initial setup will be completed now." in content
    assert "inspire" in content


def test_reset_return_true_if_choice_is_y(mocker):
    renderer = ConsoleRenderer()
    mock_console = Mock()
    renderer.console = mock_console

    mocker.patch(
        "inspire_term.ui.Prompt.ask",
        return_value="y",
    )

    result = renderer.screen_reset()

    printed_panel = mock_console.print.call_args[0][0]

    assert isinstance(printed_panel, Panel)
    assert result is True


def test_reset_return_false_if_choice_is_n(mocker):
    renderer = ConsoleRenderer()
    mock_console = Mock()
    renderer.console = mock_console

    mocker.patch(
        "inspire_term.ui.Prompt.ask",
        return_value="n",
    )

    result = renderer.screen_reset()

    printed_panel = mock_console.print.call_args[0][0]

    assert isinstance(printed_panel, Panel)
    assert not result


def test_reset_screen_config(mocker):
    renderer = ConsoleRenderer()
    mock_console = Mock()
    renderer.console = mock_console

    mocker.patch(
        "inspire_term.ui.Prompt.ask",
        return_value="y",
    )

    renderer.screen_reset()

    printed_panel = mock_console.print.call_args[0][0]

    assert printed_panel.title == "Inspiring Terminal"
    assert printed_panel.border_style == "yellow"


def test_show_config_display_table_options(mocker):
    renderer = ConsoleRenderer()
    mock_console = Mock()
    renderer.console = mock_console

    mocker.patch(
        "inspire_term.ui.Prompt.ask",
        return_value="en",
    )

    result = renderer.show_config()

    printed_panel = mock_console.print.call_args[0][0]

    assert isinstance(printed_panel, Panel)
    assert isinstance(printed_panel.renderable, Table)
    assert printed_panel.title == "Translation language"
    assert result == "en"


def test_error_prints_panel_with_message():
    renderer = ConsoleRenderer()
    mock_console = Mock()
    renderer.console = mock_console

    renderer.error("Something went wrong")

    mock_console.print.assert_called_once()
    printed_panel = mock_console.print.call_args[0][0]

    assert isinstance(printed_panel, Panel)
    content = str(printed_panel.renderable)
    assert "Something went wrong" in content
    assert printed_panel.title == "❌ Inspiring Terminal"
    assert printed_panel.border_style == "red"

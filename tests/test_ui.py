from unittest.mock import Mock

from rich.panel import Panel

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

    assert not isinstance(printed, Panel)


def test_show_simple_style_uses_rich_markup():
    renderer = ConsoleRenderer(style="simple")
    mock_console = Mock()
    renderer.console = mock_console

    renderer.show("Success is not final.", "Winston Churchill")

    printed = mock_console.print.call_args_list

    assert printed[0].args[0] == "[bold bright_yellow]Success is not final.[/]"
    assert printed[1].args[0] == "[italic cyan]— Winston Churchill[/]"


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

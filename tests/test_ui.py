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

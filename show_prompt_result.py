#!/usr/bin/env python3
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

if len(sys.argv) < 2:
    print("Usage: show_opencode_result.py /path/to/textfile")
    sys.exit(1)

path = sys.argv[1]
try:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
except Exception as e:
    text = f"Error reading file: {e}"

class ResultWindow(Gtk.Window):
    def __init__(self, content):
        super().__init__(title="PromptResult")
        self.set_wmclass("prompt-result", "PromptResult")
        self.set_resizable(False)
        self.set_border_width(0)
        
        lines = content.split('\n')
        line_count = len(lines)
        if line_count > 0 and lines[-1] == '':
            line_count -= 1
        max_line_length = max((len(line) for line in lines), default=0)
        
        width = min(max(max_line_length * 8 + 80, 450), 900)
        
        chars_per_line = max(1, (width - 32) // 8)
        wrapped_line_count = 0
        for line in lines:
            if line:
                wrapped_line_count += (len(line) + chars_per_line - 1) // chars_per_line
            else:
                wrapped_line_count += 1
        
        height = min(max(wrapped_line_count * 21 + 10, 25), 650)
        
        self.set_default_size(width, height)
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b'''
            * {
                font-family: "JetBrains Mono", "Fira Code", "Monospace", monospace;
            }
            window {
                background-color: #1e1e2e;
            }
            box.main-box {
                background-color: #1e1e2e;
                padding: 8px;
            }
            scrolledwindow {
                background-color: #1a1a26;
            }
            scrolledwindow text {
                background-color: #1a1a26;
                color: #cdd6f4;
            }
            textview {
                background-color: #1a1a26;
                color: #cdd6f4;
                font-size: 13px;
            }
            textview text {
                background-color: #1a1a26;
            }
            textview text selection {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            button {
                background-color: transparent;
                border: none;
                box-shadow: none;
                background-image: none;
            }
            button label {
                color: #6c7086;
                font-size: 18px;
            }
            button:hover {
                background-color: #2a2a3a;
                background-image: none;
            }
            button:hover label {
                color: #a6adc8;
            }
            button:active {
                background-color: #2a2a3a;
                background-image: none;
            }
        ''')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.get_style_context().add_class('scrolled')
        scrolled.get_style_context().add_class(Gtk.STYLE_CLASS_VIEW)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_shadow_type(Gtk.ShadowType.NONE)
        
        textview = Gtk.TextView()
        textview.get_style_context().add_class(Gtk.STYLE_CLASS_VIEW)
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        textview.set_left_margin(8)
        textview.set_right_margin(8)
        textview.set_top_margin(2)
        textview.set_bottom_margin(2)
        textview.set_accepts_tab(False)
        textview.set_can_focus(True)
        textview.set_property('can-default', True)
        
        buffer = textview.get_buffer()
        buffer.set_text(content)
        
        scrolled.add(textview)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        vbox.get_style_context().add_class('main-box')
        vbox.pack_start(scrolled, True, True, 0)
        
        close_btn = Gtk.Button(label="x")
        close_btn.set_halign(Gtk.Align.END)
        close_btn.set_valign(Gtk.Align.START)
        close_btn.set_relief(Gtk.ReliefStyle.NONE)
        close_btn.set_size_request(8, 8)
        close_btn.connect("clicked", lambda x: self.destroy())
        
        overlay = Gtk.Overlay()
        overlay.add(vbox)
        overlay.add_overlay(close_btn)
        
        self.add(overlay)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_position(Gtk.WindowPosition.CENTER)

win = ResultWindow(text)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

from gi.repository import GObject, RB, Peas, Gtk, Gst, GstPbutils

import src.fetch_lyrics

# thanks soooo much <333 https://github.com/dmo60/lLyrics


VIEW_MENU_UI = """
<ui>
    <menubar name="MenuBar">
        <menu name="ViewMenu" action="View">
            <menuitem name="lLyrics" action="ToggleLyricSideBar" />
        </menu>
    </menubar>
</ui>
"""


class SidePanel:
    def __init__(self, shell):
        self.shell = shell
        self.hide_label = False

        # create a TextView for displaying lyrics
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textview.set_left_margin(10)
        self.textview.set_right_margin(10)
        self.textview.set_pixels_above_lines(5)
        self.textview.set_pixels_below_lines(5)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)

        # create a ScrollView
        sw = Gtk.ScrolledWindow()
        sw.add(self.textview)
        sw.set_shadow_type(Gtk.ShadowType.IN)

        # initialize a TextBuffer to store lyrics in
        self.textbuffer = Gtk.TextBuffer()
        self.textview.set_buffer(self.textbuffer)

        # tag to style headers bold and underlined
        self.tag = self.textbuffer.create_tag(None, underline=Pango.Underline.SINGLE, weight=600,
                                              pixels_above_lines=10, pixels_below_lines=20)
        # tag to highlight synchronized lyrics
        self.sync_tag = self.textbuffer.create_tag(None, weight=600)

        # pack everything into side pane
        self.vbox.pack_start(hbox_header, False, False, 0)
        self.vbox.pack_start(sw, True, True, 0)
        self.vbox.pack_end(self.hbox, False, False, 3)
        self.vbox.pack_end(self.back_button, False, False, 3)

        self.vbox.show_all()
        self.hbox.hide()

        if self.hide_label:
            self.label.hide()

        self.visible = False

    def set_displayed_text(self, text):
        self.textbuffer.set_text(text)

from gi.repository import GObject, RB, Peas, Gtk, Gst, GstPbutils

import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from src.fetch_lyrics import LyricGrabber


def create_lyrics_view():
    tview = Gtk.TextView()
    tview.set_wrap_mode(Gtk.WrapMode.WORD)
    tview.set_editable(False)
    tview.set_left_margin(6)

    tview.set_size_request(0, 0)
    sw = Gtk.ScrolledWindow()
    sw.add(tview)
    sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    sw.set_shadow_type(Gtk.ShadowType.IN)

    vbox = Gtk.VBox(spacing=12)
    vbox.pack_start(sw, True, True, 0)

    return (vbox, tview.get_buffer(), tview)


class LyricsWidget(Gtk.Widget):
    def __init__(self, db, song_info):
        super().__init__()

        self.db = db
        self.song_info = song_info
        self.entry = self.song_info.props.current_entry

        self.hbox = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.set_spacing(6)
        self.hbox.set_layout(Gtk.ButtonBoxStyle.END)

        (self.view, self.buffer, self.tview) = create_lyrics_view()

        self.view.pack_start(self.hbox, False, False, 0)
        #self.view.set_spacing(6)
        #self.view.props.margin = 6
        self.view.set_editable(False)
        self.view.set_cursor_visible(False)
        self.view.set_left_margin(10)
        self.view.set_right_margin(10)
        self.view.set_pixels_above_lines(5)
        self.view.set_pixels_below_lines(5)
        self.view.set_wrap_mode(Gtk.WrapMode.WORD)

        self.view.show_all()
        self.page_num = song_info.append_page(_("Lyrics"), self.view)
        self.have_lyrics = 0
        self.visible = 0

        self.entry_change_id = song_info.connect('notify::current-entry', self.entry_changed)
        nb = self.view.get_parent()
        self.switch_page_id = nb.connect('switch-page', self.switch_page_cb)

    def entry_changed(self, pspec, duh):
        self.entry = self.song_info.props.current_entry
        self.have_lyrics = 0
        if self.visible != 0:
            self.get_lyrics()

    def switch_page_cb(self, notebook, page, page_num):
        if self.have_lyrics != 0:
            return

        if page_num != self.page_num:
            self.visible = 0
            return

        self.visible = 1
        self.get_lyrics()

    def __got_lyrics(self, text):
        self.buffer.set_text(text, -1)

    def get_lyrics(self):
        if self.entry is None:
            return

        self.buffer.set_text(_("Searching for lyrics..."), -1);
        lyrics_grabber = LyricGrabber(self.entry, self.buffer)

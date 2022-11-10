from gi.repository import GObject, RB, Peas, Gtk, Gst, GstPbutils, Pango

import src.fetch_lyrics
from src.utils import get_missing_lyrics_message

# thanks soooo much <333 https://github.com/dmo60/lLyrics


class SidePanel:
    def __init__(self, shell):
        self.shell = shell
        self.player = self.shell.props.shell_player
        self.position = RB.ShellUILocation.RIGHT_SIDEBAR
        self.hide_label = False

        self.vbox = Gtk.VBox()
        hbox_header = Gtk.HBox()

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


        # tag to highlight synchronized lyrics
        self.sync_tag = self.textbuffer.create_tag(None, weight=600)

        # pack everything into side pane
        self.vbox.pack_start(hbox_header, False, False, 0)
        self.vbox.pack_start(sw, True, True, 0)
        # self.vbox.pack_end(self.hbox, False, False, 3)
        # self.vbox.pack_end(self.back_button, False, False, 3)

        self.vbox.show_all()
        # self.hbox.hide()

        if self.hide_label:
            self.label.hide()

        self.shell.add_widget(self.vbox, self.position, True, True)


        # THIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Search lyrics everytime the song changes
        self.psc_id = self.player.connect('playing-song-changed', self.update_lyrics)
        self.set_displayed_text("sex")

    def set_displayed_text(self, text):
        self.textbuffer.set_text(text)


    def update_lyrics(self, player, entry):
        current_src = self.shell.props.shell_player.get_playing_source()
        if current_src is None:
            self.set_displayed_text(get_missing_lyrics_message())
            return

        lyrics_grabber = src.fetch_lyrics.LyricGrabber(entry, self.textbuffer)
        # lyrics_grabber.search_lyrics(self.set_displayed_text)


    def scan_selected_source_callback(self, action, activated_action):
        if not action.get_active():
            return

        source = activated_action
        if source == "SelectNothing" or source == self.current_source:
            return

        self.scan_source(source, self.clean_artist, self.clean_title)

    def show_lyrics(self, lyrics):
        if self.current_source is None:
            self.set_radio_menu_item_active("SelectNothing")
        elif self.current_source == "From cache file":
            self.set_radio_menu_item_active(_("From cache file"))
        else:
            self.set_radio_menu_item_active(self.current_source)

        if lyrics == "":
            print("no lyrics found")
            lyrics = _("No lyrics found")
        else:
            lyrics, self.tags = Util.parse_lrc(lyrics)

        self.textbuffer.set_text("%s - %s\n%s" % (self.artist, self.title, lyrics))

        # make 'artist - title' header bold and underlined
        start = self.textbuffer.get_start_iter()
        end = start.copy()
        end.forward_to_line_end()
        self.textbuffer.apply_tag(self.tag, start, end)

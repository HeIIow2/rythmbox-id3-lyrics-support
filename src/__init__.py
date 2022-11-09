from gi.repository import GObject, RB, Peas, Gtk, Gst, GstPbutils
from mutagen.id3 import ID3, USLT


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


class LyricGrabber(object):
    def __init__(self, db, entry):
        self.db = db
        self.entry = entry

    def search_lyrics(self, callback):
        self.callback = callback

        self.search_tags()

    def search_tags(self):
        """
        Initiate fetching meta tags.

        Result will be handled in search_tags_result
        """
        location = self.entry.get_playback_uri()
        self.discoverer = GstPbutils.Discoverer(timeout=Gst.SECOND * 3)
        self.discoverer.connect('discovered', self.search_tags_result)
        self.discoverer.start()
        self.discoverer.discover_uri_async(location)

    def search_tags_result(self, discoverer, info, error):
        """
        Extract lyrics from the file meta data (tags).

        If no lyrics tags are found, online services are tried next.

        Supported file formats and lyrics tags:
        - ogg/vorbis files with "LYRICS" and "SYNCLYRICS" tag
        """
        tags = info.get_tags()
        print(info)
        print("weeeeeeee")

        self.callback("different one")



class LyricsWidget(Gtk.Widget):
    def __init__(self, db, song_info):
        super().__init__()

        self.db = db
        self.song_info = song_info
        self.entry = self.song_info.props.current_entry

        self.hbox = Gtk.ButtonBox(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.set_spacing(6)
        self.hbox.set_layout(Gtk.ButtonBoxStyle.END)
        # self.hbox.add(self.edit)
        # self.hbox.add(self.clear)
        # self.hbox.add(self.discard)
        # self.hbox.set_child_secondary(self.clear, True)

        (self.view, self.buffer, self.tview) = create_lyrics_view()

        self.view.pack_start(self.hbox, False, False, 0)
        self.view.set_spacing(6)
        self.view.props.margin = 6

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
        lyrics_grabber = LyricGrabber(self.db, self.entry)
        lyrics_grabber.search_lyrics(self.__got_lyrics)
        self.__got_lyrics("these are lyrics xD")


class ID3Lyrics(GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(ID3Lyrics, self).__init__()

    def do_activate(self):
        print("activating support for id3 lyrics")

        shell = self.object
        self.csi_id = shell.connect("create_song_info", self.create_song_info)

    def do_deactivate(self):
        """
        The deactivation function is fairly simple, just undo everything what you did in your activation function,
        or while running. If you added UI, remove it; if you connected to some signals, disconnect them; if you
        created any objects destroy them. Most importantly, if you stored a reference to the shell object anywhere (
        or use it with a signal) the reference MUST BE released. If you have a reference to the shell object past the
        time your plugin's deactivation signal runs, it can make Rhythmbox not exit correctly. This is even more
        important with Python plugins, as it will cause a cross-runtime reference cycle. :return:
        """
        shell = self.object
        shell.disconnect(self.csi_id)
        del self.csi_id

    def create_song_info(self, shell, song_info, is_multiple):
        if is_multiple is False:
            pane = LyricsWidget(shell.props.db, song_info)

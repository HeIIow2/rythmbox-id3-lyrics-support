from gi.repository import GObject, Peas

# import os, sys
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import src.song_info_window

# from song_info_window import LyricsWidget

__all__ = ["fetch_lyrics", "song_info_window", "side_panel"]




"""
how to write those plugins: https://wiki.gnome.org/Apps/Rhythmbox/Plugins/WritingGuide

I took some code from this plugin: https://gitlab.gnome.org/GNOME/rhythmbox/-/tree/master/plugins/lyrics
thanks <33333 :3
"""

FILE_INDICATOR = "file://"


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
            pane = song_info_window.LyricsWidget(shell.props.db, song_info)

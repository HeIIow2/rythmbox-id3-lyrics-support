from gi.repository import GObject, RB, Peas, Gtk, Gst, GstPbutils, Pango
from mutagen.id3 import ID3
import urllib.parse

FILE_INDICATOR = "file://"


class LyricGrabber(object):
    def __init__(self, entry, textbuffer):
        self.entry = entry
        self.uri = self.entry.get_playback_uri()
        self.textbuffer = textbuffer

        # tag to style headers bold and underlined
        self.tag = self.textbuffer.create_tag(None, underline=Pango.Underline.SINGLE, weight=600,
                                              pixels_above_lines=10, pixels_below_lines=20)

        self.search_tags()


    def search_tags(self):
        """
        Initiate fetching meta tags.

        Result will be handled in search_tags_result
        """
        self.discoverer = GstPbutils.Discoverer(timeout=Gst.SECOND * 3)
        self.discoverer.connect('discovered', self.search_tags_result)
        self.discoverer.start()
        self.discoverer.discover_uri_async(self.uri)

    def search_tags_result(self, discoverer, info, error):
        """
        Extract lyrics from the file meta data (tags).

        If no lyrics tags are found, online services are tried next.

        Supported file formats and lyrics tags:
        - ogg/vorbis files with "LYRICS" and "SYNCLYRICS" tag
        """

        is_local = False

        path = ""
        if FILE_INDICATOR == self.uri[:len(FILE_INDICATOR)]:
            is_local = True
            path = urllib.parse.unquote(self.uri[len(FILE_INDICATOR):])
            print(path)

        if not is_local:
            self.callback("only local files are supported. Sorry :(")
            return

        print(path)
        tags = ID3(path)
        lyrics_list = tags.getall("USLT")

        if len(lyrics_list) == 0:
            self.callback("no lyrics available :(")
            return

        artist = self.entry.get_string(RB.RhythmDBPropType.ARTIST)
        title = self.entry.get_string(RB.RhythmDBPropType.TITLE)

        lyrics_text = lyrics_list[0].text
        lyrics_text = lyrics_text.strip()

        # final_lyrics = f"{artist} - {title} ({lyrics_list[0].lang})\n\n{lyrics_text}"

        # self.callback(final_lyrics)

        self.textbuffer.set_text("%s - %s\n%s" % (artist, title, lyrics))

        # make 'artist - title' header bold and underlined
        start = self.textbuffer.get_start_iter()
        end = start.copy()
        end.forward_to_line_end()
        self.textbuffer.apply_tag(self.tag, start, end)

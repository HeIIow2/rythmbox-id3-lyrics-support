import src.fetch_lyrics


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

        self.ui_manager = self.shell.get_ui_manager()
        self.ui_manager.add_ui_from_string(VIEW_MENU_UI)

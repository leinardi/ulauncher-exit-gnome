from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction


class GnomeSessionExtension(Extension):
    def __init__(self):
        super(GnomeSessionExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        options = ['logout', 'restart', 'reboot', 'shutdown', 'halt', 'power-off']
        my_list = event.query.split(" ")
        if len(my_list) == 1:
            items.append(get_logout_item())
            items.append(get_reboot_item())
            items.append(get_shutdown_item())

            return RenderResultListAction(items)
        else:
            my_query = my_list[1]
            included = []
            for option in options:
                if my_query in option:
                    if option in ['shutdown', 'halt', 'power-off'] and 'shutdown' not in included:
                        items.append(get_shutdown_item())
                        included.append('shutdown')
                    elif option in ['restart', 'reboot'] and 'reboot' not in included:
                        items.append(get_reboot_item())
                        included.append('reboot')
                    elif option in ['logout']:
                        items.append(get_logout_item())

            return RenderResultListAction(items)


def get_logout_item():
    return ExtensionResultItem(icon='images/gnome-logout.png',
                               name='Logout',
                               description='Logout from session',
                               on_enter=RunScriptAction("gnome-session-quit --logout --no-prompt", None))


def get_reboot_item():
    return ExtensionResultItem(icon='images/gnome-reboot.png',
                               name='Reboot',
                               description='Reboot computer',
                               on_enter=RunScriptAction("gnome-session-quit --reboot --force", None))


def get_shutdown_item():
    return ExtensionResultItem(icon='images/gnome-shutdown.png',
                               name='Shutdown',
                               description='Power off computer',
                               on_enter=RunScriptAction("gnome-session-quit --power-off --force", None))


if __name__ == '__main__':
    GnomeSessionExtension().run()

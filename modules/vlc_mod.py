import vlc

vlc_instance = None
vlc_mediaplayer = None


def initialize():
    global vlc_instance, vlc_mediaplayer
    vlc_instance = vlc.Instance()
    vlc_mediaplayer = vlc_instance.media_player_new()

    vlc_mediaplayer.video_set_mouse_input(False)
    vlc_mediaplayer.video_set_key_input(False)


def get_vlc_instance():
    return vlc_instance


def get_vlc_mediaplayer():
    return vlc_mediaplayer

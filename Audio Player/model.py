


class Model:
    def __init__(self):
        self.__play_list = []

    @property
    def play_list(self):
        return self.__play_list

    def get_file_to_play(self, file_index):
        return self.__play_list[file_index]

    def clear_play_list(self):
        self.__play_list.clear()

    def add_to_play_list(self, filename):
        self.__play_list.append(filename)

    def remove_item_from_playlist_at_index(self, index):
        del self.__play_list[index]

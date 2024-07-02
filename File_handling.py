import datetime
import os


class File_handling():
    def __init__(self, username: str) -> None:
        self.username = username
        self.added = []
        self.removed = []

    def getOldList(self, fileName: str):  # fileName = followers OR following

        if not (os.path.isfile(fr"Output\{self.username}\{fileName.lower()}.txt")):
            return []

        file = open(fr"Output\{self.username}\{fileName.lower()}.txt", 'r')

        lines = file.readlines()

        # removing the last 2 lines which are separators "===="
        lines.pop(-1)
        lines.pop(-1)

        lines.reverse()  # reverse the list, so we can access the last record easily

        oldList = []

        for line in lines:
            if line[0] == '-':
                break
            else:
                oldList.append(line[line.index('-') + 2: line.index('\n')])  # ex. 32- khaled\n       so it will neglect every thing before the space and the \n itself

        return oldList

    def compareLists(self, newList: list[str], fileName: str):

        old = self.getOldList(fileName.lower())
        self.added = list(set(newList) - set(old))
        self.removed = list(set(old) - set(newList))

    def fileAppend(self, profiles: list[str], fileName: str):

        if not os.path.isdir(fr"Output\{self.username}"):
            os.makedirs(fr"Output\{self.username}")
            txt_list = open(fr"Output\{self.username}\{fileName.lower()}.txt", "x")
            txt_list.close()

        elif os.path.isdir(fr"Output\{self.username}") and not os.path.isfile(fr"Output\{self.username}\{fileName.lower()}.txt"):
            txt_list = open(fr"Output\{self.username}\{fileName.lower()}.txt", "x")
            txt_list.close()

        if len(self.added) == 0 and len(self.removed) == 0:
            return

        file = open(fr"Output\{self.username}\{fileName.lower()}.txt", 'a')

        # header for the new append
        file.write(f"{'-' * 50}\n")
        file.write(f"{str(datetime.datetime.now().date())} \n")
        file.write(f"Number of {fileName.lower()} now is {len(profiles)}\n")
        file.write(f"{'-' * 50}\n")

        # write the increased users
        file.write("increased [")
        for name in self.added:
            if name == self.added[len(self.added) - 1]:
                file.write(f"{name}")
            else:
                file.write(f"{name}, ")
        file.write("]\n")

        # write the decreased users
        file.write("decreased [")
        for name in self.removed:
            if name == self.removed[len(self.removed) - 1]:
                file.write(f"{name}")
            else:
                file.write(f"{name}, ")
        file.write("]\n")

        file.write(f"{'-' * 50}\n")

        counter = 1
        for profile in profiles:
            file.write(f"{counter}- {profile}\n")
            counter += 1

        file.write(f"{'=' * 50}\n")
        file.write(f"{'=' * 50}\n")


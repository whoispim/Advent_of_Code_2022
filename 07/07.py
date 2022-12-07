class FileSystem:
    def __init__(self, start_dir: str = "/"):
        self.current_dir = (start_dir, )
        self.dir_links = {
            (start_dir, ): []
        }
        self.files_in_dir = {
            (start_dir, ): []

        }

    def change_dir(self, path: str):
        if path == "/":
            self.current_dir = (path, )
        elif path == "..":
            self.current_dir = self.current_dir[:-1]
        else:
            target_dir = self.current_dir + (path, )
            if target_dir in self.dir_links:
                self.current_dir = target_dir
            else:
                raise Exception("Folder hasn't been seen yet.")

    def list_of_dir(self, dir_contents: list[str]):
        for item in dir_contents:
            trait, name = item.split(" ")
            if trait == "dir":
                new_dir = self.current_dir + (name, )
                self.dir_links[new_dir] = []
                self.dir_links[self.current_dir].append(new_dir)
                self.files_in_dir[new_dir] = []
            else:
                self.files_in_dir[self.current_dir].append([int(trait), name])

    def dir_size(self, name: tuple) -> int:
        size = 0
        for file in self.files_in_dir[name]:
            size += file[0]
        for folder in self.dir_links[name]:
            size += self.dir_size(folder)
        return size


with open("input", "r") as f:
    commands = f.read().strip()[2:].split("\n$ ")

fs = FileSystem()
for com in commands:
    if com[:2] == "cd":
        fs.change_dir(com[3:])
    elif com[:2] == "ls":
        fs.list_of_dir(com[3:].split("\n"))
    else:
        raise Exception("???")
print("Filesystem generated.")

smol_dirs = [
    fs.dir_size(folder)
    for folder in fs.dir_links
    if fs.dir_size(folder) <= 100000
]

print(f"The sum of total sizes of directories with sizes <= 100000 is: "
      f"{sum(smol_dirs)}")

space_used = fs.dir_size(('/',))
space_empty = 70000000 - space_used
space_needed = 30000000 - space_empty
print(f"Disk space used:              {space_used:8d}")
print(f"Disk space available:         {space_empty:8d}")
print(f"Disk space needed for update: {space_needed:8d}")

big_dirs = [
    fs.dir_size(folder)
    for folder in fs.dir_links
    if fs.dir_size(folder) >= space_needed
]
big_dirs.sort()
print(f"Deleting element of size {big_dirs[0]} to free up space.")
print(f"Disk space available:         {space_empty + big_dirs[0]:8d}")

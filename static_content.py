from os import listdir
from os.path import isfile, join


_FRONTEND_ROOT = "../frontend"


def read_files_from_dir(path):
    contents = listdir(path)
    files = [f for f in contents if isfile(join(path, f))]
    return {f: open(f"{path}/{f}").read() for f in files}


html_files = read_files_from_dir(f"{_FRONTEND_ROOT}/")
css_files = read_files_from_dir(f"{_FRONTEND_ROOT}/styles")
js_files = read_files_from_dir(f"{_FRONTEND_ROOT}/scripts")
# img_files = read_files_from_dir(f"{_FRONTEND_ROOT}/images")


print(html_files.keys())
print(css_files.keys())
print(js_files.keys())
# print(img_files.keys())

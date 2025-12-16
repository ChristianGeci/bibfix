import os

library_path = "/media/geci/Mercury/Zotero/My Library.bib"

with open(library_path, 'r') as f:
    library_data: str = f.read().split('\n')
    f.close()

def find_library_citekeys() -> dict[str, int]:
    """
    Get a dictionary of (keys) all citekeys in a library 
    and (values) their respective line number in the bib
    file.
    """
    citekeys: dict[str, int] = {}
    for index, line in enumerate(library_data):
        if len(line) == 0:
            continue
        if line[0] != '@':
            continue
        citekeystart = line.find('{')
        citekey = line[citekeystart+1:-1]
        citekeys[citekey] = index
    return citekeys
citekeys = find_library_citekeys()

def find_typst_document() -> str:
    for item in os.listdir():
        if '.typ' in item:
            return item
typst_document = find_typst_document()

def find_used_citekeys() -> list[str]:
    with open(typst_document, 'r') as f:
        document_data = f.read()
    used_citekeys = []
    for citekey in citekeys:
        if citekey in document_data:
            used_citekeys.append(citekey)
    return used_citekeys
used_citekeys = find_used_citekeys()

def get_bibtex_data_for_used_citekeys() -> list[str]:
    bibtex_data = []
    for citekey in used_citekeys:
        line_number = citekeys[citekey]
        data_lines = []
        n = 0
        while True:
            line:str = library_data[line_number + n]
            data_lines.append(line)
            if line == "}":
                break
            n += 1
        bibtex_data.append("\n".join(data_lines))
    return bibtex_data
bibtex_data = get_bibtex_data_for_used_citekeys()

def write_bibliograpy():
    bib_filename = typst_document.split('.')[0] + ".bib"
    with open(bib_filename, "w") as f:
        for entry in bibtex_data:
            f.write(entry)
            f.write('\n')
write_bibliograpy()
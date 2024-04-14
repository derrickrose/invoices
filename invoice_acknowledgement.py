import os


def iterate_and_update_files(path: str):
    import glob
    invoice_index = 1
    for file in glob.glob(path, recursive=True):
        file_name = file[file.rfind("/") + 1:]
        os.rename(file, file.replace(file_name, f"Facture_{invoice_index}_{file_name}"))
        invoice_index += 1


if __name__ == "__main__":
    iterate_and_update_files("/home/frils/Documents/charges/2022/2022_ko/*")

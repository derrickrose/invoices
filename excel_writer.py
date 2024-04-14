import re
from typing import List

import pandas

INITIAL_DATE_FORMAT = "%d_%m_%Y"
TARGET_DATE_FORMAT = "%Y-%m-%d"
INVOICES_DIRECTORY = "/home/frils/Documents/charges/2022/2022_ok/"

DATE_FORMAT_REGEX_MAPPING = {
    INITIAL_DATE_FORMAT: "\d{2}_\d{2}_\d{4}",
    TARGET_DATE_FORMAT: "\d{4}-\d{2}-\d{2}",
}

PRICE_REGEX = "_\d{0,}euros\d{0,}_"


class Invoice:
    def __init__(
            self, date: str, label: str, seller: str, price: float
    ):
        self.date = date
        self.label = label
        self.seller = seller
        self.price = price

    def __repr__(self):
        return f"Invoice(date={self.date}, label={self.label}, price={self.price}, seller={self.seller})"

    def to_output(self):
        return Output(self)


class Output:
    def __init__(self, invoice: Invoice):
        self.DATE = invoice.date
        self.FRAIS = "Autre"
        self.DETAILS = invoice.label + " chez " + invoice.seller
        self.MONTANT = str(invoice.price).replace(".", ",")
        # self.MONTANT = invoice.price


def to_invoice(file_name: str) -> Invoice:
    # 2022-01-06_sac_dos_ordi_39euros99_amazon.pdf
    date_matcher = re.search(DATE_FORMAT_REGEX_MAPPING[TARGET_DATE_FORMAT], file_name)
    date_raw = ""
    if date_matcher:
        date_raw = date_matcher.group()
        file_name = file_name.replace(date_raw, "")
    else:
        raise Exception(f"Date not found on : {file_name}")
    # _sac_dos_ordi_39euros99_amazon.pdf

    price_raw = ""
    price_matcher = re.search(PRICE_REGEX, file_name)
    if price_matcher:
        price_raw = price_matcher.group().replace("_", "")
        file_name = file_name.replace(price_raw, "")
    else:
        raise Exception(f"Price not found on : {file_name}")
    # _sac_dos_ordi__amazon.pdf

    file_extension = file_name.split(".")[-1]
    seller = file_name[file_name.find("__"): file_name.rfind(f".{file_extension}")]
    file_name = file_name.replace(seller, "").replace(f".{file_extension}", "")
    seller = seller.replace("__", "")
    label = " ".join(file_name.split("_"))

    return Invoice(
        date_raw,
        label.strip(),
        seller,
        float(price_raw.replace("euros", ".").replace("euro", ".")),
    )


def iterate_invoices(path: str) -> List[Output]:
    outputs = []
    import glob
    for file in glob.glob(path, recursive=True):
        file_name = file[file.rfind("/") + 1:]
        try:
            output = to_invoice(file_name).to_output()
            outputs.append(output)
        except Exception as e:
            print(e)
    return outputs


if __name__ == "__main__":
    invoices = iterate_invoices(f"{INVOICES_DIRECTORY}*")
    invoices.sort(key=lambda x: x.DATE)
    df = pandas.DataFrame([invoice.__dict__ for invoice in invoices])
    df.to_excel("invoices.xlsx", index=False)

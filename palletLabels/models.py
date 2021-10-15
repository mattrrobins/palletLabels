#! python3

from simple_zpl2 import ZPLDocument, Code128_Barcode, NetworkPrinter
from datetime import date
import PIL
import io

today = date.today()


# Model Classes
class Pallet:
    def __init__(self, item, ctn_pairs, partials):
        self.item = item
        self.ctn_pairs = ctn_pairs
        self.partials = partials

    def add_pair(self, pair):
        self.ctn_pairs.append(pair)

    def add_partial(self, x):
        self.partials.append(x)

    def total(self):
        tot = sum(self.partials)
        for x in self.ctn_pairs:
            tot += x[0] * x[1]
        return str(tot)

    def text(self):
        sort_pairs = sorted(self.ctn_pairs, key=lambda x: x[1], reverse=True)
        sort_partials = sorted(self.partials, reverse=True)
        txt_list = [' * '.join(tuple(map(str, x))) for x in sort_pairs]
        txt = ' + '.join(txt_list)
        if txt == '':
            x = ''
        else:
            x = ' + '
        if len(self.partials) > 0:
            txt += x + ' + '.join(list(map(str, sort_partials)))
        return txt

class ZebraLabel(ZPLDocument):
    title_0 = (650, 320)
    qty_0 = (370, 100)
    maths_0 = (370, 280)
    maths_01 = (279, 350)
    equals_0 = (180, 200)
    date_0 = (50, 970)

    MYFONT = 'Verdana'

    def __init__(self, item, total, maths):
        super().__init__()
        self.item = item
        self.total = total # should be str
        self.maths = maths

        self.add_zpl_raw('^BY6') # Barcode width
        bc_item = Code128_Barcode(item, 'R', 100, 'Y')
        bc_total = Code128_Barcode(total, 'R', 70, 'Y', 'Y')
        item_0 = (550, self.center_bc_x(self.item))
        total_0 = (100, self.center_bc_x(self.total))

        self.add_default_font(self.MYFONT, 150, 150)
        self.add_text(self.title_0, 'COUNTED')
        self.add_bc(item_0, bc_item)

        self.add_default_font(self.MYFONT, 80, 80)
        self.add_text(self.qty_0, 'QTY:')
        self.add_text(self.equals_0, '=')

        self.add_default_font(self.MYFONT, 80, 50)

        maths1, maths2 = self.maths_split(maths)
        if maths2 == '':
            self.add_text(self.maths_0, maths1)
        elif maths2 == '':
            self.add_text(self.maths_0, maths2)
        else:
            self.add_text(self.maths_0, maths1)
            self.add_text(self.maths_01, '+' + maths2)

        self.add_bc(total_0, bc_total)

        self.add_default_font(25, 25)
        self.add_text(self.date_0, str(today))


    def add_bc(self, origin, bc):
        self.add_field_origin(*origin)
        #self.add_font('Verdana')
        self.add_barcode(bc)

    def add_text(self, origin, txt):
        self.add_field_origin(*origin) # Location where field starts
        self.add_zpl_raw('^AOR') # Rotate
        self.add_field_data(txt)

    def render(self):
        png = self.render_png(label_width=4, label_height=6)
        fake_file = io.BytesIO(png)
        img = PIL.Image.open(fake_file)
        img.transpose(PIL.Image.ROTATE_90).show()

    def to_printer(self, pr_id):
        prn = NetworkPrinter(pr_id)
        prn.print_zpl(self)

    def center_bc_x(self, txt):
        l = len(txt)
        dot_len = 64.0625 * l +217.8125
        return round((1230 - dot_len) / 2)

    def maths_split(self, txt):
        list_txt = txt.split('+')
        pairs = []
        partials = []
        for num in list_txt:
            if '*' in num:
                pairs.append(num)
            else:
                partials.append(num)
        return '+'.join(pairs), '+'.join(partials)

    def center_maths_x(self, txt):
        l = len(txt)
        #### dot_txt = ????? etc

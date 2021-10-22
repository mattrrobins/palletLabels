#! python3

from views import MainView
from models import Pallet, ZebraLabel

class Controller:
    def __init__(self):
        self.obs = Observable()
        self.view = MainView(self)

        self.view.mainloop()

    def render_label(self):
        pal = Pallet(self.obs.item, self.obs.ctn_pairs, self.obs.partials)
        zeb = ZebraLabel(pal.item, pal.total(), pal.text())
        zeb.render()

    def print_label(self, pr_id):
        pal = Pallet(self.obs.item, self.obs.ctn_pairs, self.obs.partials)
        zeb = ZebraLabel(pal.item, pal.total(), pal.text())
        zeb.to_printer(pr_id)


# Observable Class
class Observable:
    def __init__(self):
        self.item = ''
        self.unique_cp = 0
        self.partial_cp = 0
        self.ctn_pairs = []
        self.partials = []

    def set_item(self, x):
        self.item = x

    def set_unique_cp(self, x):
        self.unique_cp = x

    def set_partial_cp(self, x):
        self.partial_cp = x

    def add_ctn_pairs(self, x):
        self.ctn_pairs = x

    def add_partial(self, x):
        self.partials = x

    def print_att(self):
        #print('\n'.join('#s : #s' % item for item in vars(self).items()))
        for k, v in vars(self).items():
            print(f'{k} : {v}')

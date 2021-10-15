#! python3

import tkinter as tk
from tkinter import ttk


pr_id = '10.0.0.202'

# View Classes
MYFONT = ("Verdana", 25)


class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title('Create A Pallet Label')

        self.next_frame(InitialPage)

    def next_frame(self, F):
        frame = F(self, self.controller)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.tkraise()

    def init_model(self, item, pairs, partials):
        pass ##Maybe?


class InitialPage(tk.Frame):
    LBL_TXT = ['What is the Item Number?',
               'How many unique (unopened) carton-quantities exist on the pallet?',
               'How many partial case packs are on the pallet?']

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label_sku = ttk.Label(self, text=self.LBL_TXT[0], font=MYFONT)
        label_full = ttk.Label(self, text=self.LBL_TXT[1], font=MYFONT)
        label_partial = ttk.Label(self, text=self.LBL_TXT[2], font=MYFONT)

        entry_sku = ttk.Entry(self, width=10)
        entry_full = ttk.Entry(self, width=10)
        entry_partial = ttk.Entry(self, width=10)

        button = ttk.Button(
                    master=self,
                    text='NEXT',
                    command=lambda : [self.set_observation(entry_sku, entry_full, entry_partial),
                                        parent.next_frame(QtyPage)]
                            )

        # Layout
        label_sku.grid(row=0, column=0)
        entry_sku.grid(row=1, column=0)
        label_full.grid(row=2, column=0)
        entry_full.grid(row=3, column=0)
        label_partial.grid(row=4, column=0)
        entry_partial.grid(row=5, column=0)
        button.grid(row=6, column=0)


    def set_observation(self, item, full_cp, partial):
        self.controller.obs.set_item(item.get().upper())
        self.controller.obs.set_unique_cp(int(full_cp.get()))
        self.controller.obs.set_partial_cp(int(partial.get()))
        #self.controller.obs.print_att()


class QtyPage(tk.Frame):
    LBL_TXT = ['Enter Full Case Pack Information Here',
               '<--------------->',
               'QTY/CTN',
               '# of CTNs',
               'Enter Partial Case Pack Qty(s) Here']

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        co_unique = controller.obs.unique_cp
        co_partial = controller.obs.partial_cp
        entry_ctn_count = []
        entry_ctn_qty = []
        if co_unique > 0:
            label_full = ttk.Label(self, text=self.LBL_TXT[0], font=MYFONT)
            label_full.grid(row=0, column=2)
            #entry_ctn_count = []
            #entry_ctn_qty = []
            for i in range(co_unique):
                e_q = ttk.Entry(master=self, width=10)
                e_q.grid(row=(i + 1), column=1)
                lbl_dash = ttk.Label(self, text=self.LBL_TXT[1], font=MYFONT)
                lbl_dash.grid(row=(i + 1), column=2)
                e_c = ttk.Entry(master=self, width=10)
                e_c.grid(row=(i + 1), column=3)
                entry_ctn_count.append(e_c)
                entry_ctn_qty.append(e_q)
            lbl_left = ttk.Label(self, text=self.LBL_TXT[2], font=MYFONT)
            lbl_left.grid(row=(co_unique // 2), column=0)
            lbl_right = ttk.Label(self, text=self.LBL_TXT[3], font=MYFONT)
            lbl_right.grid(row=(co_unique // 2), column=4)

        entry_partials = []
        if co_partial > 0:
            label_partial = ttk.Label(self, text=self.LBL_TXT[4], font=MYFONT)
            label_partial.grid(row=(co_unique + 1), column=2)
            #entry_partials = []
            for i in range(co_partial):
                e = ttk.Entry(self, width=10)
                e.grid(row=(i + co_unique + 2), column=2)
                entry_partials.append(e)

        button_prev = ttk.Button(
                        master=self,
                        text='PREVIEW',
                        command=lambda : [self.set_obs_qty(entry_ctn_count,
                                            entry_ctn_qty, entry_partials),
                                            controller.render_label()]
                            )
        button_prev.grid(row=(co_partial + co_unique + 2), column=3)

        button_print = ttk.Button(
                        master=self,
                        text='PRINT',
                        command=lambda : [self.set_obs_qty(entry_ctn_count,
                                            entry_ctn_qty, entry_partials),
                                            controller.print_label(pr_id)]
                            )
        button_print.grid(row=(co_partial + co_unique + 3), column=3)

        button_back = ttk.Button(
                        master=self,
                        text='Back',
                        command=lambda : parent.next_frame(InitialPage)
                            )
        button_back.grid(row=(co_partial + co_unique + 3), column=1)

    def set_obs_qty(self, ctn_count=[], ctn_qty=[], partials=[]):
        pairs = [(int(x.get()), int(y.get()))
                    for (x, y) in list(zip(ctn_count, ctn_qty))]
        self.controller.obs.add_ctn_pairs(pairs)

        del_values = [int(p.get()) for p in partials]
        self.controller.obs.add_partial(del_values)
        #self.controller.obs.print_att()


class OutputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text='DONE', font=MYFONT)
        label.grid(row=0, column=0)

if __name__ == '__main__':
    app = MainView()
    app.mainloop()

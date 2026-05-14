import tkinter as tk
from tkinter import ttk, messagebox

BG     = "#0d1b2a"
CARD   = "#1b2838"
PANEL  = "#243447"
ACCENT = "#00d4aa"
BLUE   = "#3d9be9"
TEXT   = "#e8f4fd"
SUB    = "#7a9bb5"
DANGER = "#ff5f6d"
WARN   = "#ffc542"
SUCCESS= "#00d4aa"
WHITE  = "#ffffff"

SEMESTRES = ["1er Semestre", "2do Semestre", "Anual"]

def sfloat(val, default=0.0):
    try:
        v = val.get() if hasattr(val, "get") else val
        return float(str(v).replace(",", "").strip()) if str(v).strip() else default
    except Exception:
        return default

def fmt(n):
    try:
        return f"${float(n):,.2f}"
    except Exception:
        return "$0.00"

def fmtu(n):
    try:
        return f"{float(n):,.0f}"
    except Exception:
        return "0"

def make_tree(parent, cols, col_widths, height=14):
    frame = tk.Frame(parent, bg=CARD)
    frame.pack(fill="both", expand=True, pady=(4, 0))
    sb = ttk.Scrollbar(frame, orient="vertical")
    sb.pack(side="right", fill="y")
    tree = ttk.Treeview(frame, columns=cols, show="headings",
                        height=height, yscrollcommand=sb.set)
    tree.pack(fill="both", expand=True)
    sb.config(command=tree.yview)
    for c, w in zip(cols, col_widths):
        anc = "w" if c in ("Concepto", "Descripcion", "Producto",
                           "Material", "Categoria", "Tipo") else "e"
        tree.column(c, width=w, anchor=anc, minwidth=40)
        tree.heading(c, text=c)
    tree.tag_configure("total", foreground=ACCENT,  font=("Courier New", 10, "bold"))
    tree.tag_configure("sub",   foreground=SUB)
    tree.tag_configure("neg",   foreground=DANGER)
    tree.tag_configure("pos",   foreground=SUCCESS)
    tree.tag_configure("warn",  foreground=WARN)
    return tree

def section_label(parent, text):
    tk.Label(parent, text=text, bg=CARD, fg=ACCENT,
             font=("Courier New", 9, "bold")).pack(anchor="w", pady=(8, 2))

def lbl(parent, text, fg=None, font_size=9, bold=False):
    f = ("Courier New", font_size, "bold") if bold else ("Courier New", font_size)
    return tk.Label(parent, text=text, bg=CARD, fg=fg or SUB, font=f)

def entry_row(parent, row, label, default="0", width=14):
    lbl(parent, label).grid(row=row, column=0, sticky="w", pady=2, padx=(0, 8))
    var = tk.StringVar(value=str(default))
    tk.Entry(parent, textvariable=var, bg=PANEL, fg=TEXT,
             insertbackground=ACCENT, relief="flat", width=width,
             font=("Courier New", 10)).grid(row=row, column=1, pady=2, sticky="w")
    return var

def make_btn(parent, text, cmd, color=None, side="left"):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=color or ACCENT, fg=BG,
                  activebackground=PANEL, activeforeground=ACCENT,
                  relief="flat", font=("Courier New", 9, "bold"),
                  padx=12, pady=5, cursor="hand2")
    b.pack(side=side, padx=(0, 6))
    return b

def sem_entries(parent, row_start, label, default="0"):
    lbl(parent, label).grid(row=row_start, column=0, sticky="w", pady=2, padx=(0, 8))
    vars_ = []
    for i in range(2):
        v = tk.StringVar(value=str(default))
        tk.Entry(parent, textvariable=v, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=12,
                 font=("Courier New", 10)).grid(row=row_start, column=i+1,
                                                pady=2, padx=4, sticky="w")
        vars_.append(v)
    return vars_


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Presupuesto Maestro — Sistema Empresarial Completo")
        self.geometry("1200x750")
        self.minsize(1000, 650)
        self.configure(bg=BG)
        self.resizable(True, True)
        self._apply_styles()
        self._build_header()
        self._build_notebook()

    def _apply_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TNotebook",     background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background=PANEL, foreground=SUB,
                    padding=[14, 7], font=("Courier New", 9, "bold"))
        s.map("TNotebook.Tab",
              background=[("selected", CARD)],
              foreground=[("selected", ACCENT)])
        s.configure("TFrame", background=CARD)
        s.configure("Treeview", background=PANEL, foreground=TEXT,
                    fieldbackground=PANEL, rowheight=24, borderwidth=0,
                    font=("Courier New", 9))
        s.configure("Treeview.Heading", background=BG, foreground=ACCENT,
                    font=("Courier New", 8, "bold"), relief="flat")
        s.map("Treeview", background=[("selected", BLUE)])
        s.configure("Vertical.TScrollbar", background=PANEL,
                    troughcolor=BG, arrowcolor=ACCENT)

    def _build_header(self):
        h = tk.Frame(self, bg=BG, pady=8)
        h.pack(fill="x", padx=16)
        tk.Label(h, text="PRESUPUESTO MAESTRO",
                 bg=BG, fg=ACCENT,
                 font=("Courier New", 16, "bold")).pack(side="left")
        info = tk.Frame(h, bg=BG)
        info.pack(side="right")
        tk.Label(info, text="Empresa:", bg=BG, fg=SUB,
                 font=("Courier New", 9)).grid(row=0, column=0, sticky="e")
        self.empresa_var = tk.StringVar(value="Mi Empresa, S.A. de C.V.")
        tk.Entry(info, textvariable=self.empresa_var, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=30,
                 font=("Courier New", 9)).grid(row=0, column=1, padx=6)
        tk.Label(info, text="Ejercicio:", bg=BG, fg=SUB,
                 font=("Courier New", 9)).grid(row=0, column=2, sticky="e")
        self.anio_var = tk.StringVar(value="2025")
        tk.Entry(info, textvariable=self.anio_var, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=6,
                 font=("Courier New", 9)).grid(row=0, column=3, padx=6)
        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x")

    def _build_notebook(self):
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=8, pady=8)

        self.t_ventas     = VentasTab(self.nb, self)
        self.t_prod       = ProduccionTab(self.nb, self)
        self.t_mat        = MaterialesTab(self.nb, self)
        self.t_compras    = ComprasTab(self.nb, self)
        self.t_mod        = MODTab(self.nb, self)
        self.t_gif        = GIFTab(self.nb, self)
        self.t_gasop      = GastosOpTab(self.nb, self)
        self.t_costos     = CostosTab(self.nb, self)
        self.t_resultados = ResultadosTab(self.nb, self)
        self.t_flujo      = FlujoTab(self.nb, self)
        self.t_balance    = BalanceTab(self.nb, self)

        tabs = [
            (self.t_ventas,     " VENTAS"),
            (self.t_prod,       " PRODUCCION"),
            (self.t_mat,        " MATERIALES"),
            (self.t_compras,    " COMPRAS"),
            (self.t_mod,        " M.O.D."),
            (self.t_gif,        " G.I.F."),
            (self.t_gasop,      " GASTOS OP."),
            (self.t_costos,     " COSTOS"),
            (self.t_resultados, " RESULTADOS"),
            (self.t_flujo,      " FLUJO"),
            (self.t_balance,    " BALANCE"),
        ]
        for widget, title in tabs:
            self.nb.add(widget, text=f" {title} ")

        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _on_tab_change(self, event):
        tab = self.nb.select()
        idx  = self.nb.index(tab)
        refresh_map = {
            7:  self.t_costos.calcular,
            8:  self.t_resultados.calcular,
            9:  self.t_flujo.calcular,
            10: self.t_balance.calcular,
        }
        if idx in refresh_map:
            try:
                refresh_map[idx]()
            except Exception:
                pass


class BaseTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=CARD)
        self.app = app

class VentasTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.productos = []
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=CARD, padx=12, pady=10)
        left.pack(side="left", fill="y")

        section_label(left, "AGREGAR PRODUCTO")
        form = tk.Frame(left, bg=CARD)
        form.pack(anchor="w")

        lbl(form, "Nombre del producto:").grid(row=0, column=0, sticky="w", pady=2)
        self.nombre_v = tk.StringVar()
        tk.Entry(form, textvariable=self.nombre_v, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=20,
                 font=("Courier New", 10)).grid(row=0, column=1, columnspan=2,
                                                pady=2, padx=4, sticky="w")

        lbl(form, "").grid(row=1, column=0)
        lbl(form, "1er Sem", fg=BLUE).grid(row=1, column=1, padx=4)
        lbl(form, "2do Sem", fg=WARN).grid(row=1, column=2, padx=4)

        self.precio1_v, self.precio2_v = sem_entries(form, 2, "Precio de venta ($):", "0")
        self.uds1_v,    self.uds2_v    = sem_entries(form, 3, "Unidades a vender:",   "0")

        bf = tk.Frame(left, bg=CARD)
        bf.pack(anchor="w", pady=8)
        make_btn(bf, "+ AGREGAR", self._agregar)
        make_btn(bf, "X ELIMINAR", self._eliminar, color=DANGER)

        right = tk.Frame(self, bg=CARD, padx=8, pady=10)
        right.pack(fill="both", expand=True)

        section_label(right, "PRESUPUESTO DE VENTAS")
        cols   = ["Producto", "P.1Sem", "Uds.1Sem", "Importe 1Sem",
                  "P.2Sem",  "Uds.2Sem", "Importe 2Sem", "TOTAL ANUAL"]
        widths = [130, 75, 80, 110, 75, 80, 110, 110]
        self.tree = make_tree(right, cols, widths, height=15)

        self.total_lbl = tk.Label(right, text="TOTAL VENTAS: $0.00",
                                  bg=CARD, fg=SUCCESS,
                                  font=("Courier New", 12, "bold"))
        self.total_lbl.pack(anchor="e", pady=4)

    def _agregar(self):
        nombre = self.nombre_v.get().strip()
        if not nombre:
            messagebox.showwarning("Aviso", "Ingrese el nombre del producto.")
            return
        p1, p2   = sfloat(self.precio1_v), sfloat(self.precio2_v)
        u1, u2   = sfloat(self.uds1_v),    sfloat(self.uds2_v)
        imp1, imp2 = p1*u1, p2*u2
        total      = imp1 + imp2
        self.productos.append(dict(nombre=nombre, p1=p1, p2=p2,
                                   u1=u1, u2=u2, imp1=imp1, imp2=imp2, total=total))
        self._refresh()
        self.nombre_v.set("")
        for v in (self.precio1_v, self.precio2_v, self.uds1_v, self.uds2_v):
            v.set("0")

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = list(self.tree.get_children()).index(sel[0])
        if 0 <= idx < len(self.productos):
            self.productos.pop(idx)
            self._refresh()

    def _refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for p in self.productos:
            self.tree.insert("", "end", values=(
                p["nombre"], fmt(p["p1"]), fmtu(p["u1"]), fmt(p["imp1"]),
                fmt(p["p2"]), fmtu(p["u2"]), fmt(p["imp2"]), fmt(p["total"])
            ))
        self.total_lbl.config(text=f"TOTAL VENTAS: {fmt(self.get_total())}")

    def get_total(self):
        return sum(p["total"] for p in self.productos)

    def get_sem(self):
        s1 = sum(p["imp1"] for p in self.productos)
        s2 = sum(p["imp2"] for p in self.productos)
        return s1, s2

class ProduccionTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.items = []
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=CARD, padx=12, pady=10)
        left.pack(side="left", fill="y")

        section_label(left, "AGREGAR PRODUCTO")
        form = tk.Frame(left, bg=CARD)
        form.pack(anchor="w")

        lbl(form, "Producto:").grid(row=0, column=0, sticky="w", pady=2)
        self.prod_v = tk.StringVar()
        tk.Entry(form, textvariable=self.prod_v, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=18,
                 font=("Courier New", 10)).grid(row=0, column=1, columnspan=2,
                                                pady=2, padx=4, sticky="w")

        lbl(form, "").grid(row=1, column=0)
        lbl(form, "1er Sem", fg=BLUE).grid(row=1, column=1, padx=4)
        lbl(form, "2do Sem", fg=WARN).grid(row=1, column=2, padx=4)

        self.uv1_v, self.uv2_v = sem_entries(form, 2, "Unidades a vender:")
        self.if1_v, self.if2_v = sem_entries(form, 3, "Inventario final:")
        self.ii1_v, self.ii2_v = sem_entries(form, 4, "Inventario inicial:")

        tk.Label(left,
                 text="Unidades a Producir = Vender + Inv.Final - Inv.Inicial",
                 bg=CARD, fg=SUB, font=("Courier New", 8),
                 wraplength=240, justify="left").pack(anchor="w", pady=(4, 0))

        bf = tk.Frame(left, bg=CARD)
        bf.pack(anchor="w", pady=8)
        make_btn(bf, "+ AGREGAR", self._agregar)
        make_btn(bf, "X ELIMINAR", self._eliminar, color=DANGER)

        right = tk.Frame(self, bg=CARD, padx=8, pady=10)
        right.pack(fill="both", expand=True)

        section_label(right, "PRESUPUESTO DE PRODUCCION (Unidades)")
        cols   = ["Producto",
                  "Vender 1S", "Inv.F 1S", "Inv.I 1S", "Prod. 1S",
                  "Vender 2S", "Inv.F 2S", "Inv.I 2S", "Prod. 2S",
                  "Total Prod."]
        widths = [100, 70, 65, 65, 70, 70, 65, 65, 70, 85]
        self.tree = make_tree(right, cols, widths, height=15)

    def _agregar(self):
        prod = self.prod_v.get().strip()
        if not prod:
            messagebox.showwarning("Aviso", "Ingrese el nombre del producto.")
            return

        uv1, uv2 = sfloat(self.uv1_v), sfloat(self.uv2_v)
        if1_, if2_ = sfloat(self.if1_v), sfloat(self.if2_v)
        ii1_, ii2_ = sfloat(self.ii1_v), sfloat(self.ii2_v)

        # CORRECCION: cada semestre usa su propio inventario inicial
        up1 = uv1 + if1_ - ii1_
        up2 = uv2 + if2_ - ii2_
        total = up1 + up2

        self.items.append(dict(prod=prod,
                               uv1=uv1, uv2=uv2,
                               if1=if1_, if2=if2_,
                               ii1=ii1_, ii2=ii2_,
                               up1=up1,  up2=up2, total=total))
        self._refresh()
        self.prod_v.set("")
        for v in (self.uv1_v, self.uv2_v, self.if1_v, self.if2_v,
                  self.ii1_v, self.ii2_v):
            v.set("0")

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = list(self.tree.get_children()).index(sel[0])
        if 0 <= idx < len(self.items):
            self.items.pop(idx)
            self._refresh()

    def _refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for it in self.items:
            self.tree.insert("", "end", values=(
                it["prod"],
                fmtu(it["uv1"]), fmtu(it["if1"]), fmtu(it["ii1"]), fmtu(it["up1"]),
                fmtu(it["uv2"]), fmtu(it["if2"]), fmtu(it["ii2"]), fmtu(it["up2"]),
                fmtu(it["total"])
            ))

    def get_items(self):
        return self.items


class MaterialesTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.reqs = []
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=CARD, padx=12, pady=10)
        left.pack(side="left", fill="y")

        section_label(left, "REQUERIMIENTO DE MATERIAL")
        form = tk.Frame(left, bg=CARD)
        form.pack(anchor="w")

        lbl(form, "Producto:").grid(row=0, column=0, sticky="w", pady=2)
        self.prod_v = tk.StringVar()
        tk.Entry(form, textvariable=self.prod_v, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=16,
                 font=("Courier New", 10)).grid(row=0, column=1, pady=2, padx=4)

        lbl(form, "Material:").grid(row=1, column=0, sticky="w", pady=2)
        self.mat_v = tk.StringVar()
        tk.Entry(form, textvariable=self.mat_v, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=16,
                 font=("Courier New", 10)).grid(row=1, column=1, pady=2, padx=4)

        self.req_v = entry_row(form, 2, "Req. unitario:", "1", width=10)

        lbl(form, "Unidades a producir por semestre:",
            fg=TEXT, bold=True).grid(row=3, column=0, columnspan=2,
                                     sticky="w", pady=(8, 2))

        self.up1_v = entry_row(form, 4, "Prod. 1er Sem:", "0", width=10)
        self.up2_v = entry_row(form, 5, "Prod. 2do Sem:", "0", width=10)

        # CORRECCION: texto completo, sin truncar
        tk.Label(left,
                 text="Puede consultar el tab Produccion\ny copiar las unidades a producir.",
                 bg=CARD, fg=SUB, font=("Courier New", 8),
                 wraplength=220, justify="left").pack(anchor="w", pady=(4, 0))

        bf = tk.Frame(left, bg=CARD)
        bf.pack(anchor="w", pady=8)
        make_btn(bf, "+ AGREGAR", self._agregar)
        make_btn(bf, "X ELIMINAR", self._eliminar, color=DANGER)

        right = tk.Frame(self, bg=CARD, padx=8, pady=10)
        right.pack(fill="both", expand=True)

        section_label(right, "REQUERIMIENTO TOTAL DE MATERIALES")
        cols   = ["Producto", "Material", "Req/Und",
                  "Prod.1S", "Total Mat.1S",
                  "Prod.2S", "Total Mat.2S", "Total Anual"]
        widths = [100, 90, 65, 75, 100, 75, 100, 100]
        self.tree = make_tree(right, cols, widths, height=15)

    def _agregar(self):
        prod = self.prod_v.get().strip()
        mat  = self.mat_v.get().strip()
        if not prod or not mat:
            messagebox.showwarning("Aviso", "Ingrese producto y material.")
            return
        req = sfloat(self.req_v)
        up1 = sfloat(self.up1_v)
        up2 = sfloat(self.up2_v)
        t1  = req * up1
        t2  = req * up2
        self.reqs.append(dict(prod=prod, mat=mat, req=req,
                              up1=up1, up2=up2, t1=t1, t2=t2, total=t1+t2))
        self._refresh()
        for v in (self.prod_v, self.mat_v):
            v.set("")
        for v in (self.req_v, self.up1_v, self.up2_v):
            v.set("0")

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = list(self.tree.get_children()).index(sel[0])
        if 0 <= idx < len(self.reqs):
            self.reqs.pop(idx)
            self._refresh()

    def _refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for it in self.reqs:
            self.tree.insert("", "end", values=(
                it["prod"], it["mat"], fmtu(it["req"]),
                fmtu(it["up1"]), fmtu(it["t1"]),
                fmtu(it["up2"]), fmtu(it["t2"]),
                fmtu(it["total"])
            ))

    def get_totales_por_material(self):
        d = {}
        for it in self.reqs:
            m = it["mat"]
            if m not in d:
                d[m] = {"t1": 0, "t2": 0, "total": 0}
            d[m]["t1"]    += it["t1"]
            d[m]["t2"]    += it["t2"]
            d[m]["total"] += it["total"]
        return d


class ComprasTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.items = []
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=CARD, padx=12, pady=10)
        left.pack(side="left", fill="y")

        section_label(left, "COMPRA DE MATERIAL")
        form = tk.Frame(left, bg=CARD)
        form.pack(anchor="w")

        lbl(form, "Material:").grid(row=0, column=0, sticky="w", pady=2)
        self.mat_v = tk.StringVar()
        tk.Entry(form, textvariable=self.mat_v, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=16,
                 font=("Courier New", 10)).grid(row=0, column=1, columnspan=2,
                                                pady=2, padx=4)

        lbl(form, "").grid(row=1, column=0)
        lbl(form, "1er Sem", fg=BLUE).grid(row=1, column=1, padx=4)
        lbl(form, "2do Sem", fg=WARN).grid(row=1, column=2, padx=4)

        self.req1_v, self.req2_v = sem_entries(form, 2, "Requerimiento total:")
        self.if1_v,  self.if2_v  = sem_entries(form, 3, "Inventario final:")
        self.ii1_v,  self.ii2_v  = sem_entries(form, 4, "Inventario inicial:")
        self.pc1_v,  self.pc2_v  = sem_entries(form, 5, "Precio de compra ($):")

        bf = tk.Frame(left, bg=CARD)
        bf.pack(anchor="w", pady=8)
        make_btn(bf, "+ AGREGAR", self._agregar)
        make_btn(bf, "X ELIMINAR", self._eliminar, color=DANGER)

        right = tk.Frame(self, bg=CARD, padx=8, pady=10)
        right.pack(fill="both", expand=True)

        section_label(right, "PRESUPUESTO DE COMPRAS")
        cols   = ["Material",
                  "Req.1S","IF.1S","II.1S","Cmp.1S","P.1S","Imp.1S",
                  "Req.2S","IF.2S","II.2S","Cmp.2S","P.2S","Imp.2S",
                  "TOTAL $"]
        widths = [90,65,55,55,65,55,80,
                     65,55,55,65,55,80,90]
        self.tree = make_tree(right, cols, widths, height=13)

        self.total_lbl = tk.Label(right, text="TOTAL COMPRAS: $0.00",
                                  bg=CARD, fg=WARN,
                                  font=("Courier New", 11, "bold"))
        self.total_lbl.pack(anchor="e", pady=4)

    def _agregar(self):
        mat = self.mat_v.get().strip()
        if not mat:
            messagebox.showwarning("Aviso", "Ingrese el nombre del material.")
            return
        req1, req2 = sfloat(self.req1_v), sfloat(self.req2_v)
        if1_,  if2_  = sfloat(self.if1_v),  sfloat(self.if2_v)
        ii1_,  ii2_  = sfloat(self.ii1_v),  sfloat(self.ii2_v)
        pc1,   pc2   = sfloat(self.pc1_v),  sfloat(self.pc2_v)

        cmp1 = req1 + if1_ - ii1_
        cmp2 = req2 + if2_ - ii2_
        imp1 = cmp1 * pc1
        imp2 = cmp2 * pc2
        total = imp1 + imp2

        self.items.append(dict(mat=mat,
                               req1=req1, if1=if1_, ii1=ii1_, cmp1=cmp1, pc1=pc1, imp1=imp1,
                               req2=req2, if2=if2_, ii2=ii2_, cmp2=cmp2, pc2=pc2, imp2=imp2,
                               total=total))
        self._refresh()
        self.mat_v.set("")
        for v in (self.req1_v, self.req2_v, self.if1_v, self.if2_v,
                  self.ii1_v, self.ii2_v, self.pc1_v, self.pc2_v):
            v.set("0")

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = list(self.tree.get_children()).index(sel[0])
        if 0 <= idx < len(self.items):
            self.items.pop(idx)
            self._refresh()

    def _refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for it in self.items:
            self.tree.insert("", "end", values=(
                it["mat"],
                fmtu(it["req1"]), fmtu(it["if1"]), fmtu(it["ii1"]),
                fmtu(it["cmp1"]), fmt(it["pc1"]), fmt(it["imp1"]),
                fmtu(it["req2"]), fmtu(it["if2"]), fmtu(it["ii2"]),
                fmtu(it["cmp2"]), fmt(it["pc2"]), fmt(it["imp2"]),
                fmt(it["total"])
            ))
        self.total_lbl.config(text=f"TOTAL COMPRAS: {fmt(self.get_total())}")

    def get_total(self):
        return sum(i["total"] for i in self.items)

    def get_sem(self):
        s1 = sum(i["imp1"] for i in self.items)
        s2 = sum(i["imp2"] for i in self.items)
        return s1, s2


class MODTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.items = []
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=CARD, padx=12, pady=10)
        left.pack(side="left", fill="y")

        section_label(left, "MANO DE OBRA DIRECTA")
        form = tk.Frame(left, bg=CARD)
        form.pack(anchor="w")

        lbl(form, "Producto:").grid(row=0, column=0, sticky="w", pady=2)
        self.prod_v = tk.StringVar()
        tk.Entry(form, textvariable=self.prod_v, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=16,
                 font=("Courier New", 10)).grid(row=0, column=1, columnspan=2,
                                                pady=2, padx=4)

        lbl(form, "").grid(row=1, column=0)
        lbl(form, "1er Sem", fg=BLUE).grid(row=1, column=1, padx=4)
        lbl(form, "2do Sem", fg=WARN).grid(row=1, column=2, padx=4)

        self.up1_v,    self.up2_v    = sem_entries(form, 2, "Unidades a producir:")
        self.hrs_u1_v, self.hrs_u2_v = sem_entries(form, 3, "Horas/unidad:")
        self.cuota1_v, self.cuota2_v = sem_entries(form, 4, "Cuota por hora ($):")

        bf = tk.Frame(left, bg=CARD)
        bf.pack(anchor="w", pady=8)
        make_btn(bf, "+ AGREGAR", self._agregar)
        make_btn(bf, "X ELIMINAR", self._eliminar, color=DANGER)

        right = tk.Frame(self, bg=CARD, padx=8, pady=10)
        right.pack(fill="both", expand=True)

        section_label(right, "PRESUPUESTO DE MANO DE OBRA DIRECTA")
        cols   = ["Producto",
                  "Up.1S","Hrs/U.1S","THrs.1S","Cuota.1S","MOD.1S",
                  "Up.2S","Hrs/U.2S","THrs.2S","Cuota.2S","MOD.2S",
                  "TOTAL MOD"]
        widths = [100,65,65,65,65,80,
                      65,65,65,65,80,95]
        self.tree = make_tree(right, cols, widths, height=13)

        self.total_lbl = tk.Label(right, text="TOTAL M.O.D.: $0.00",
                                  bg=CARD, fg=WARN,
                                  font=("Courier New", 11, "bold"))
        self.total_lbl.pack(anchor="e", pady=4)

        self.hrs_lbl = tk.Label(right, text="Total horas: 0 hrs",
                                bg=CARD, fg=SUB,
                                font=("Courier New", 9))
        self.hrs_lbl.pack(anchor="e")

    def _agregar(self):
        prod = self.prod_v.get().strip()
        if not prod:
            messagebox.showwarning("Aviso", "Ingrese el nombre del producto.")
            return
        up1, up2 = sfloat(self.up1_v),    sfloat(self.up2_v)
        hu1, hu2 = sfloat(self.hrs_u1_v), sfloat(self.hrs_u2_v)
        c1,  c2  = sfloat(self.cuota1_v), sfloat(self.cuota2_v)
        th1, th2 = up1*hu1, up2*hu2
        mod1, mod2 = th1*c1, th2*c2
        total = mod1 + mod2
        self.items.append(dict(prod=prod,
                               up1=up1, up2=up2, hu1=hu1, hu2=hu2,
                               c1=c1, c2=c2, th1=th1, th2=th2,
                               mod1=mod1, mod2=mod2, total=total))
        self._refresh()
        self.prod_v.set("")
        for v in (self.up1_v, self.up2_v, self.hrs_u1_v, self.hrs_u2_v,
                  self.cuota1_v, self.cuota2_v):
            v.set("0")

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = list(self.tree.get_children()).index(sel[0])
        if 0 <= idx < len(self.items):
            self.items.pop(idx)
            self._refresh()

    def _refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for it in self.items:
            self.tree.insert("", "end", values=(
                it["prod"],
                fmtu(it["up1"]), fmtu(it["hu1"]), fmtu(it["th1"]),
                fmt(it["c1"]),   fmt(it["mod1"]),
                fmtu(it["up2"]), fmtu(it["hu2"]), fmtu(it["th2"]),
                fmt(it["c2"]),   fmt(it["mod2"]),
                fmt(it["total"])
            ))
        self.total_lbl.config(text=f"TOTAL M.O.D.: {fmt(self.get_total())}")
        self.hrs_lbl.config(text=f"Total horas: {fmtu(self.get_total_horas())} hrs")

    def get_total(self):
        return sum(i["total"] for i in self.items)

    def get_total_horas(self):
        return sum(i["th1"] + i["th2"] for i in self.items)

    def get_sem(self):
        s1 = sum(i["mod1"] for i in self.items)
        s2 = sum(i["mod2"] for i in self.items)
        return s1, s2



class GIFTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.items = []
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=CARD, padx=12, pady=10)
        left.pack(side="left", fill="y")

        section_label(left, "AGREGAR GASTO INDIRECTO")
        form = tk.Frame(left, bg=CARD)
        form.pack(anchor="w")

        lbl(form, "Concepto:").grid(row=0, column=0, sticky="w", pady=2)
        self.conc_v = tk.StringVar()
        tk.Entry(form, textvariable=self.conc_v, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=18,
                 font=("Courier New", 10)).grid(row=0, column=1, columnspan=2,
                                                pady=2, padx=4)

        lbl(form, "").grid(row=1, column=0)
        lbl(form, "1er Sem", fg=BLUE).grid(row=1, column=1, padx=4)
        lbl(form, "2do Sem", fg=WARN).grid(row=1, column=2, padx=4)

        self.m1_v, self.m2_v = sem_entries(form, 2, "Monto ($):")

        self.paga_v = tk.BooleanVar(value=True)
        tk.Checkbutton(form, text="Se paga en efectivo?",
                       variable=self.paga_v, bg=CARD, fg=TEXT,
                       selectcolor=PANEL, activebackground=CARD,
                       font=("Courier New", 9)).grid(
            row=3, column=0, columnspan=3, sticky="w", pady=4)

        bf = tk.Frame(left, bg=CARD)
        bf.pack(anchor="w", pady=8)
        make_btn(bf, "+ AGREGAR", self._agregar)
        make_btn(bf, "X ELIMINAR", self._eliminar, color=DANGER)

        coef_f = tk.Frame(left, bg=PANEL, padx=10, pady=8)
        coef_f.pack(fill="x", pady=8)
        tk.Label(coef_f, text="COSTO POR HORA (G.I.F.)",
                 bg=PANEL, fg=ACCENT,
                 font=("Courier New", 9, "bold")).pack(anchor="w")
        self.coef_lbl = tk.Label(coef_f, text="$0.0000 / hr",
                                 bg=PANEL, fg=WARN,
                                 font=("Courier New", 14, "bold"))
        self.coef_lbl.pack(anchor="w")
        tk.Label(coef_f, text="(Total GIF / Total horas MOD)",
                 bg=PANEL, fg=SUB,
                 font=("Courier New", 8)).pack(anchor="w")
        make_btn(coef_f, "Calcular coeficiente", self._calc_coef, color=BLUE)

        right = tk.Frame(self, bg=CARD, padx=8, pady=10)
        right.pack(fill="both", expand=True)

        section_label(right, "PRESUPUESTO DE GASTOS INDIRECTOS DE FABRICACION")
        cols   = ["Concepto", "1er Semestre", "2do Semestre", "TOTAL", "Paga?"]
        widths = [160, 130, 130, 130, 70]
        self.tree = make_tree(right, cols, widths, height=14)

        self.total_lbl = tk.Label(right, text="TOTAL G.I.F.: $0.00",
                                  bg=CARD, fg=WARN,
                                  font=("Courier New", 11, "bold"))
        self.total_lbl.pack(anchor="e", pady=4)

    def _agregar(self):
        conc = self.conc_v.get().strip()
        if not conc:
            messagebox.showwarning("Aviso", "Ingrese el concepto.")
            return
        m1, m2 = sfloat(self.m1_v), sfloat(self.m2_v)
        paga   = self.paga_v.get()
        total  = m1 + m2
        self.items.append(dict(conc=conc, m1=m1, m2=m2, total=total, paga=paga))
        self._refresh()
        self.conc_v.set("")
        for v in (self.m1_v, self.m2_v):
            v.set("0")
        self.paga_v.set(True)

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = list(self.tree.get_children()).index(sel[0])
        if 0 <= idx < len(self.items):
            self.items.pop(idx)
            self._refresh()

    def _calc_coef(self):
        total_gif = self.get_total()
        total_hrs = self.app.t_mod.get_total_horas()
        if total_hrs > 0:
            coef = total_gif / total_hrs
            self.coef_lbl.config(text=f"${coef:,.4f} / hr")
        else:
            self.coef_lbl.config(text="Sin horas MOD registradas")

    def _refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for it in self.items:
            self.tree.insert("", "end", values=(
                it["conc"], fmt(it["m1"]), fmt(it["m2"]),
                fmt(it["total"]), "Si" if it["paga"] else "No (depr.)"
            ))
        self.total_lbl.config(text=f"TOTAL G.I.F.: {fmt(self.get_total())}")

    def get_total(self):
        return sum(i["total"] for i in self.items)

    def get_total_paga(self):
        return sum(i["total"] for i in self.items if i["paga"])

    def get_coef(self):
        total_gif = self.get_total()
        total_hrs = self.app.t_mod.get_total_horas()
        return total_gif / total_hrs if total_hrs > 0 else 0

    def get_sem(self):
        s1 = sum(i["m1"] for i in self.items)
        s2 = sum(i["m2"] for i in self.items)
        return s1, s2


class GastosOpTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.items = []
        self._build()

    def _build(self):
        left = tk.Frame(self, bg=CARD, padx=12, pady=10)
        left.pack(side="left", fill="y")

        section_label(left, "AGREGAR GASTO DE OPERACION")
        form = tk.Frame(left, bg=CARD)
        form.pack(anchor="w")

        lbl(form, "Concepto:").grid(row=0, column=0, sticky="w", pady=2)
        self.conc_v = tk.StringVar()
        tk.Entry(form, textvariable=self.conc_v, bg=PANEL, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", width=18,
                 font=("Courier New", 10)).grid(row=0, column=1, columnspan=2,
                                                pady=2, padx=4)

        cats = ["Administrativo", "Ventas/Mktg", "Financiero", "RRHH", "TI", "Otros"]
        lbl(form, "Categoria:").grid(row=1, column=0, sticky="w", pady=2)
        self.cat_v = tk.StringVar(value=cats[0])
        ttk.Combobox(form, textvariable=self.cat_v, values=cats,
                     width=16, state="readonly",
                     font=("Courier New", 9)).grid(row=1, column=1, columnspan=2,
                                                   pady=2, padx=4)

        lbl(form, "").grid(row=2, column=0)
        lbl(form, "1er Sem", fg=BLUE).grid(row=2, column=1, padx=4)
        lbl(form, "2do Sem", fg=WARN).grid(row=2, column=2, padx=4)

        self.m1_v, self.m2_v = sem_entries(form, 3, "Monto ($):")

        self.paga_v = tk.BooleanVar(value=True)
        tk.Checkbutton(form, text="Se paga en efectivo?",
                       variable=self.paga_v, bg=CARD, fg=TEXT,
                       selectcolor=PANEL, activebackground=CARD,
                       font=("Courier New", 9)).grid(
            row=4, column=0, columnspan=3, sticky="w", pady=4)

        bf = tk.Frame(left, bg=CARD)
        bf.pack(anchor="w", pady=8)
        make_btn(bf, "+ AGREGAR", self._agregar)
        make_btn(bf, "X ELIMINAR", self._eliminar, color=DANGER)

        right = tk.Frame(self, bg=CARD, padx=8, pady=10)
        right.pack(fill="both", expand=True)

        section_label(right, "PRESUPUESTO DE GASTOS DE OPERACION")
        cols   = ["Concepto", "Categoria", "1er Semestre", "2do Semestre",
                  "TOTAL", "Paga?"]
        widths = [150, 110, 120, 120, 110, 70]
        self.tree = make_tree(right, cols, widths, height=14)

        self.total_lbl = tk.Label(right, text="TOTAL GASTOS OP.: $0.00",
                                  bg=CARD, fg=DANGER,
                                  font=("Courier New", 11, "bold"))
        self.total_lbl.pack(anchor="e", pady=4)

    def _agregar(self):
        conc = self.conc_v.get().strip()
        if not conc:
            messagebox.showwarning("Aviso", "Ingrese el concepto.")
            return
        cat  = self.cat_v.get()
        m1, m2 = sfloat(self.m1_v), sfloat(self.m2_v)
        paga   = self.paga_v.get()
        total  = m1 + m2
        self.items.append(dict(conc=conc, cat=cat, m1=m1, m2=m2,
                               total=total, paga=paga))
        self._refresh()
        self.conc_v.set("")
        for v in (self.m1_v, self.m2_v):
            v.set("0")
        self.paga_v.set(True)

    def _eliminar(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = list(self.tree.get_children()).index(sel[0])
        if 0 <= idx < len(self.items):
            self.items.pop(idx)
            self._refresh()

    def _refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for it in self.items:
            self.tree.insert("", "end", values=(
                it["conc"], it["cat"], fmt(it["m1"]), fmt(it["m2"]),
                fmt(it["total"]), "Si" if it["paga"] else "No (depr.)"
            ))
        self.total_lbl.config(text=f"TOTAL GASTOS OP.: {fmt(self.get_total())}")

    def get_total(self):
        return sum(i["total"] for i in self.items)

    def get_total_paga(self):
        return sum(i["total"] for i in self.items if i["paga"])

    def get_sem(self):
        s1 = sum(i["m1"] for i in self.items)
        s2 = sum(i["m2"] for i in self.items)
        return s1, s2


class CostosTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=CARD, padx=12, pady=8)
        top.pack(fill="x")

        section_label(top, "DATOS DE INVENTARIOS (para Estado de Costo)")
        inp = tk.Frame(top, bg=CARD)
        inp.pack(anchor="w")

        self.inv_ini_mat_v = entry_row(inp, 0, "Inv. inicial de materiales ($):", "45000")
        self.inv_fin_mat_v = entry_row(inp, 1, "Inv. final de materiales ($):",   "47100")
        self.inv_ini_pt_v  = entry_row(inp, 2, "Inv. inicial prod. terminado ($):", "135000")
        self.inv_fin_pt_v  = entry_row(inp, 3, "Inv. final prod. terminado ($):",   "0")

        bf = tk.Frame(top, bg=CARD)
        bf.pack(anchor="w", pady=6)
        make_btn(bf, "Calcular", self.calcular, color=BLUE)

        res = tk.Frame(self, bg=CARD, padx=12, pady=4)
        res.pack(fill="both", expand=True)

        section_label(res, "ESTADO DE COSTO DE PRODUCCION Y VENTAS")
        cols   = ["Concepto", "Importe"]
        widths = [420, 180]
        self.tree = make_tree(res, cols, widths, height=16)

    def calcular(self):
        a = self.app
        compras  = a.t_compras.get_total()
        mod      = a.t_mod.get_total()
        gif      = a.t_gif.get_total()
        inv_im   = sfloat(self.inv_ini_mat_v)
        inv_fm   = sfloat(self.inv_fin_mat_v)
        inv_ipt  = sfloat(self.inv_ini_pt_v)
        inv_fpt  = sfloat(self.inv_fin_pt_v)

        mat_disp    = inv_im + compras
        mat_util    = mat_disp - inv_fm
        costo_prod  = mat_util + mod + gif
        prod_disp   = costo_prod + inv_ipt
        costo_ventas= prod_disp - inv_fpt
        ventas      = a.t_ventas.get_total()
        util_bruta  = ventas - costo_ventas

        for r in self.tree.get_children():
            self.tree.delete(r)

        rows = [
            ("Saldo inicial de materiales",         inv_im,       "sub"),
            ("(+) Compras de materiales",           compras,      "sub"),
            ("(=) Material disponible",             mat_disp,     "warn"),
            ("(-) Inventario final de materiales",  inv_fm,       "sub"),
            ("(=) Materiales utilizados",           mat_util,     "warn"),
            ("(+) Mano de Obra Directa",            mod,          "sub"),
            ("(+) Gastos Indirectos de Fabricacion",gif,          "sub"),
            ("(=) COSTO DE PRODUCCION",             costo_prod,   "total"),
            ("(+) Inv. inicial prod. terminado",    inv_ipt,      "sub"),
            ("(=) Total produccion disponible",     prod_disp,    "warn"),
            ("(-) Inv. final prod. terminado",      inv_fpt,      "sub"),
            ("(=) COSTO DE VENTAS",                 costo_ventas, "total"),
            ("", 0, "sub"),
            ("VENTAS TOTALES",                      ventas,       "pos"),
            ("UTILIDAD BRUTA",                      util_bruta,   "pos"),
        ]
        for concepto, importe, tag in rows:
            if concepto == "":
                self.tree.insert("", "end", values=("", ""), tags=(tag,))
            else:
                self.tree.insert("", "end", values=(concepto, fmt(importe)),
                                 tags=(tag,))

        self.app._costo_ventas  = costo_ventas
        self.app._utilidad_bruta= util_bruta

    def get_costo_ventas(self):
        return getattr(self.app, "_costo_ventas", 0)


class ResultadosTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=CARD, padx=12, pady=8)
        top.pack(fill="x")

        section_label(top, "PARAMETROS FISCALES")
        inp = tk.Frame(top, bg=CARD)
        inp.pack(anchor="w")
        self.isr_v = entry_row(inp, 0, "Tasa ISR (%):", "30")
        self.ptu_v = entry_row(inp, 1, "Tasa PTU (%):", "10")

        bf = tk.Frame(top, bg=CARD)
        bf.pack(anchor="w", pady=6)
        make_btn(bf, "Calcular", self.calcular, color=BLUE)

        kpi_f = tk.Frame(self, bg=CARD, padx=12)
        kpi_f.pack(fill="x")
        self.kpi_ventas  = self._kpi(kpi_f, "VENTAS",       "$0.00", BLUE)
        self.kpi_cventas = self._kpi(kpi_f, "COSTO VENTAS", "$0.00", WARN)
        self.kpi_ubruta  = self._kpi(kpi_f, "UTIL. BRUTA",  "$0.00", SUCCESS)
        self.kpi_uneta   = self._kpi(kpi_f, "UTIL. NETA",   "$0.00", ACCENT)

        res = tk.Frame(self, bg=CARD, padx=12, pady=4)
        res.pack(fill="both", expand=True)
        section_label(res, "ESTADO DE RESULTADOS")
        cols   = ["Concepto", "Importe"]
        widths = [380, 200]
        self.tree = make_tree(res, cols, widths, height=12)

    def _kpi(self, parent, label, value, color):
        box = tk.Frame(parent, bg=PANEL, padx=14, pady=8)
        box.pack(side="left", fill="x", expand=True, padx=4, pady=4)
        tk.Label(box, text=label, bg=PANEL, fg=SUB,
                 font=("Courier New", 8, "bold")).pack(anchor="w")
        lbl_ = tk.Label(box, text=value, bg=PANEL, fg=color,
                        font=("Courier New", 13, "bold"))
        lbl_.pack(anchor="w")
        return lbl_

    def calcular(self):
        try:
            self.app.t_costos.calcular()
        except Exception:
            pass

        ventas      = self.app.t_ventas.get_total()
        costo_ventas= self.app.t_costos.get_costo_ventas()
        gastos_op   = self.app.t_gasop.get_total()
        isr_tasa    = sfloat(self.isr_v) / 100
        ptu_tasa    = sfloat(self.ptu_v) / 100

        util_bruta = ventas - costo_ventas
        util_op    = util_bruta - gastos_op
        isr        = util_op * isr_tasa
        ptu        = util_op * ptu_tasa
        util_neta  = util_op - isr - ptu

        self.kpi_ventas.config(text=fmt(ventas))
        self.kpi_cventas.config(text=fmt(costo_ventas))
        self.kpi_ubruta.config(text=fmt(util_bruta),
                               fg=SUCCESS if util_bruta >= 0 else DANGER)
        self.kpi_uneta.config(text=fmt(util_neta),
                              fg=SUCCESS if util_neta >= 0 else DANGER)

        for r in self.tree.get_children():
            self.tree.delete(r)

        rows = [
            ("Ventas",                              ventas,       "pos"),
            ("(-) Costo de Ventas",                 costo_ventas, "sub"),
            ("(=) Utilidad Bruta",                  util_bruta,   "total"),
            ("(-) Gastos de Operacion",             gastos_op,    "sub"),
            ("(=) Utilidad de Operacion",           util_op,      "warn"),
            (f"(-) ISR ({sfloat(self.isr_v):.0f}%)",isr,         "sub"),
            (f"(-) PTU ({sfloat(self.ptu_v):.0f}%)",ptu,         "sub"),
            ("(=) UTILIDAD NETA",                   util_neta,    "total"),
        ]
        for concepto, importe, tag in rows:
            t = "neg" if importe < 0 else tag
            self.tree.insert("", "end", values=(concepto, fmt(importe)), tags=(t,))

        self.app._util_neta = util_neta
        self.app._isr       = isr
        self.app._ptu       = ptu
        self.app._util_op   = util_op


class FlujoTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=CARD, padx=12, pady=8)
        top.pack(fill="x")

        section_label(top, "DATOS ADICIONALES DE FLUJO")
        inp = tk.Frame(top, bg=CARD)
        inp.pack(anchor="w")

        self.ef_ini_v        = entry_row(inp, 0, "Efectivo inicial ($):",             "100000")
        self.clientes_ini_v  = entry_row(inp, 1, "Saldo clientes año ant. ($):",      "80000")
        self.pct_cobro_ant_v = entry_row(inp, 2, "% cobro de clientes ant.:",         "100")
        self.pct_cobro_act_v = entry_row(inp, 3, "% cobro de ventas actuales:",       "80")
        self.prov_ini_v      = entry_row(inp, 4, "Saldo proveedores año ant. ($):",   "33500")
        self.pct_pago_ant_v  = entry_row(inp, 5, "% pago proveedores ant.:",          "100")
        self.pct_pago_act_v  = entry_row(inp, 6, "% pago compras actuales:",          "50")
        self.isr_ant_v       = entry_row(inp, 7, "ISR año anterior a pagar ($):",     "50000")
        self.activo_fijo_v   = entry_row(inp, 8, "Compra activo fijo ($):",           "0")

        bf = tk.Frame(top, bg=CARD)
        bf.pack(anchor="w", pady=6)
        make_btn(bf, "Calcular", self.calcular, color=BLUE)

        res = tk.Frame(self, bg=CARD, padx=12, pady=4)
        res.pack(fill="both", expand=True)
        section_label(res, "ESTADO DE FLUJO DE EFECTIVO")
        cols   = ["Concepto", "Importe"]
        widths = [380, 200]
        self.tree = make_tree(res, cols, widths, height=16)

        self.saldo_lbl = tk.Label(res, text="SALDO FINAL DE EFECTIVO: $0.00",
                                  bg=CARD, fg=SUCCESS,
                                  font=("Courier New", 12, "bold"))
        self.saldo_lbl.pack(anchor="e", pady=4)

    def calcular(self):
        try:
            self.app.t_costos.calcular()
        except Exception:
            pass
        try:
            self.app.t_resultados.calcular()
        except Exception:
            pass

        ventas      = self.app.t_ventas.get_total()
        compras     = self.app.t_compras.get_total()
        mod         = self.app.t_mod.get_total()
        gif_paga    = self.app.t_gif.get_total_paga()
        gasop_paga  = self.app.t_gasop.get_total_paga()
        isr_act     = getattr(self.app, "_isr", 0)
        ptu_act     = getattr(self.app, "_ptu", 0)

        ef_ini      = sfloat(self.ef_ini_v)
        cl_ini      = sfloat(self.clientes_ini_v)
        pct_ca      = sfloat(self.pct_cobro_ant_v) / 100
        pct_cv      = sfloat(self.pct_cobro_act_v) / 100
        pr_ini      = sfloat(self.prov_ini_v)
        pct_pa      = sfloat(self.pct_pago_ant_v) / 100
        pct_pc      = sfloat(self.pct_pago_act_v) / 100
        isr_ant     = sfloat(self.isr_ant_v)
        activo      = sfloat(self.activo_fijo_v)

        cobro_ant   = cl_ini  * pct_ca
        cobro_act   = ventas  * pct_cv
        total_ent   = cobro_ant + cobro_act
        ef_disp     = ef_ini + total_ent

        pago_pr_ant = pr_ini  * pct_pa
        pago_pr_act = compras * pct_pc

        total_sal   = (pago_pr_ant + pago_pr_act + mod +
                       gif_paga + gasop_paga + activo + isr_ant +
                       isr_act + ptu_act)

        saldo_final    = ef_disp - total_sal
        saldo_clientes = ventas  - cobro_act
        saldo_prov     = compras - pago_pr_act

        for r in self.tree.get_children():
            self.tree.delete(r)

        rows = [
            ("Saldo inicial de efectivo",              ef_ini,       "sub"),
            ("ENTRADAS:",                              None,         "warn"),
            ("  Cobranza de clientes año anterior",    cobro_ant,    "sub"),
            ("  Cobranza de ventas actuales",          cobro_act,    "sub"),
            ("  Total de entradas",                    total_ent,    "total"),
            ("Efectivo disponible",                    ef_disp,      "pos"),
            ("SALIDAS:",                               None,         "warn"),
            ("  Pago proveedores año anterior",        pago_pr_ant,  "sub"),
            ("  Pago proveedores actuales",            pago_pr_act,  "sub"),
            ("  Mano de Obra Directa",                 mod,          "sub"),
            ("  GIF (sin depreciacion)",               gif_paga,     "sub"),
            ("  Gastos de Operacion (sin depr.)",      gasop_paga,   "sub"),
            ("  Compra de activo fijo",                activo,       "sub"),
            ("  ISR año anterior",                     isr_ant,      "sub"),
            ("  ISR ejercicio actual",                 isr_act,      "sub"),
            ("  PTU ejercicio actual",                 ptu_act,      "sub"),
            ("  Total de salidas",                     total_sal,    "total"),
            ("", None, "sub"),
            ("SALDO FINAL DE EFECTIVO",                saldo_final,  "pos"),
            ("", None, "sub"),
            ("-> Saldo de clientes (Balance)",         saldo_clientes,"warn"),
            ("-> Saldo de proveedores (Balance)",      saldo_prov,   "warn"),
        ]

        for concepto, importe, tag in rows:
            if importe is None:
                self.tree.insert("", "end", values=(concepto, ""), tags=(tag,))
            elif concepto == "":
                self.tree.insert("", "end", values=("", ""),       tags=(tag,))
            else:
                t = "neg" if importe < 0 else tag
                self.tree.insert("", "end",
                                 values=(concepto, fmt(importe)), tags=(t,))

        color = SUCCESS if saldo_final >= 0 else DANGER
        self.saldo_lbl.config(
            text=f"SALDO FINAL DE EFECTIVO: {fmt(saldo_final)}", fg=color)

        self.app._ef_final        = saldo_final
        self.app._saldo_clientes  = saldo_clientes
        self.app._saldo_prov      = saldo_prov

class BalanceTab(BaseTab):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=CARD, padx=12, pady=8)
        top.pack(fill="x")

        section_label(top, "DATOS DEL BALANCE ANTERIOR")
        inp = tk.Frame(top, bg=CARD)
        inp.pack(anchor="w")

        self.terreno_v    = entry_row(inp,  0, "Terreno ($):",                    "905000")
        self.planta_v     = entry_row(inp,  1, "Planta y equipo ($):",            "1500000")
        self.depr_acum_v  = entry_row(inp,  2, "Depreciacion acumulada ($):",     "650000")
        self.nueva_maq_v  = entry_row(inp,  3, "Equipo nuevo adquirido ($):",     "0")
        self.depr_anual_v = entry_row(inp,  4, "Depreciacion del ejercicio ($):", "0")
        self.deudores_v   = entry_row(inp,  5, "Deudores diversos ($):",          "35000")
        self.func_emp_v   = entry_row(inp,  6, "Funcionarios y empleados ($):",   "10500")
        self.inv_fin_mat_v= entry_row(inp,  7, "Inv. final materiales ($):",      "47100")
        self.inv_fin_pt_v = entry_row(inp,  8, "Inv. final prod. terminado ($):", "0")
        self.doc_pagar_v  = entry_row(inp,  9, "Documentos por pagar ($):",       "95000")
        self.prestamo_v   = entry_row(inp, 10, "Prestamos bancarios LP ($):",     "120000")
        self.cap_contrib_v= entry_row(inp, 11, "Capital contribuido ($):",        "1500000")
        self.cap_ganado_v = entry_row(inp, 12, "Capital ganado ($):",             "362000")

        tk.Label(top,
                 text="Nota: Los inventarios finales deben coincidir con los del tab Costos.",
                 bg=CARD, fg=WARN, font=("Courier New", 8)).pack(anchor="w", pady=(4, 0))

        bf = tk.Frame(top, bg=CARD)
        bf.pack(anchor="w", pady=6)
        make_btn(bf, "Calcular", self.calcular, color=BLUE)

        res = tk.Frame(self, bg=CARD, padx=12, pady=4)
        res.pack(fill="both", expand=True)
        section_label(res, "BALANCE GENERAL PRESUPUESTADO")
        cols   = ["Concepto", "Parcial", "Total"]
        widths = [320, 180, 180]
        self.tree = make_tree(res, cols, widths, height=16)

        self.check_lbl = tk.Label(res, text="",
                                  bg=CARD, fg=WARN,
                                  font=("Courier New", 11, "bold"))
        self.check_lbl.pack(anchor="e", pady=4)

    def calcular(self):
        try:
            self.app.t_costos.calcular()
        except Exception:
            pass
        try:
            self.app.t_resultados.calcular()
        except Exception:
            pass
        try:
            self.app.t_flujo.calcular()
        except Exception:
            pass

        ef_final   = getattr(self.app, "_ef_final",       0)
        clientes   = getattr(self.app, "_saldo_clientes", 0)
        prov       = getattr(self.app, "_saldo_prov",     0)
        util_neta  = getattr(self.app, "_util_neta",      0)
        isr        = getattr(self.app, "_isr",            0)
        ptu        = getattr(self.app, "_ptu",            0)

        terreno    = sfloat(self.terreno_v)
        planta     = sfloat(self.planta_v)   + sfloat(self.nueva_maq_v)
        depr_acum  = sfloat(self.depr_acum_v)+ sfloat(self.depr_anual_v)
        deudores   = sfloat(self.deudores_v)
        func_emp   = sfloat(self.func_emp_v)
        inv_mat    = sfloat(self.inv_fin_mat_v)
        inv_pt     = sfloat(self.inv_fin_pt_v)
        doc_pagar  = sfloat(self.doc_pagar_v)
        prestamo   = sfloat(self.prestamo_v)
        cap_contrib= sfloat(self.cap_contrib_v)
        cap_ganado = sfloat(self.cap_ganado_v)

        total_circ  = ef_final + clientes + deudores + func_emp + inv_mat + inv_pt
        total_no_c  = terreno + planta - depr_acum
        activo_tot  = total_circ + total_no_c

        total_cp    = prov + doc_pagar + isr + ptu
        total_lp    = prestamo
        pasivo_tot  = total_cp + total_lp

        cap_tot     = cap_contrib + cap_ganado + util_neta
        pasivo_cap  = pasivo_tot  + cap_tot
        diferencia  = activo_tot  - pasivo_cap

        for r in self.tree.get_children():
            self.tree.delete(r)

        def row(concepto, parcial=None, total=None, tag="sub"):
            p = fmt(parcial) if parcial is not None else ""
            t = fmt(total)   if total   is not None else ""
            self.tree.insert("", "end", values=(concepto, p, t), tags=(tag,))

        row("ACTIVO", tag="warn")
        row("  Circulante", tag="sub")
        row("    Efectivo",                   ef_final)
        row("    Clientes",                   clientes)
        row("    Deudores diversos",          deudores)
        row("    Funcionarios y empleados",   func_emp)
        row("    Inv. de materiales",         inv_mat)
        row("    Inv. prod. terminado",       inv_pt)
        row("  Total Activo Circulante",      total=total_circ, tag="total")
        row("  No Circulante", tag="sub")
        row("    Terreno",                    terreno)
        row("    Planta y equipo",            planta)
        row("    (-) Depreciacion acum.",     depr_acum)
        row("  Total Activo No Circulante",   total=total_no_c, tag="total")
        row("ACTIVO TOTAL",                   total=activo_tot, tag="pos")
        row("", tag="sub")
        row("PASIVO", tag="warn")
        row("  Corto Plazo", tag="sub")
        row("    Proveedores",                prov)
        row("    Documentos por pagar",       doc_pagar)
        row("    ISR por pagar",              isr)
        row("    PTU por pagar",              ptu)
        row("  Total Pasivo CP",              total=total_cp,   tag="total")
        row("  Largo Plazo", tag="sub")
        row("    Prestamos bancarios",        prestamo)
        row("  Total Pasivo LP",              total=total_lp,   tag="total")
        row("PASIVO TOTAL",                   total=pasivo_tot, tag="warn")
        row("", tag="sub")
        row("CAPITAL CONTABLE", tag="warn")
        row("    Capital contribuido",        cap_contrib)
        row("    Capital ganado",             cap_ganado)
        row("    Utilidad del ejercicio",     util_neta)
        row("CAPITAL CONTABLE TOTAL",         total=cap_tot,    tag="total")
        row("", tag="sub")
        row("SUMA PASIVO + CAPITAL",          total=pasivo_cap, tag="pos")

        if abs(diferencia) < 0.01:
            self.check_lbl.config(text="BALANCE CUADRADO", fg=SUCCESS)
        else:
            self.check_lbl.config(text=f"Diferencia: {fmt(diferencia)}", fg=DANGER)

if __name__ == "__main__":
    app = App()
    app.mainloop()

import os, sys, threading
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QColor, QFont, QFontDatabase
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem,
                             QSlider, QScrollArea, QFileDialog, QMessageBox, QComboBox)
from font_mgr import list_all_fonts, refresh_cache, download_and_install, install_local, remove_font_files, get_preview_font_file
from i18n import detect_lang, TRANSLATIONS

BASE = os.path.dirname(os.path.abspath(__file__))

def is_dark():
    cf = os.path.expanduser("~/.config/cutefish/services.conf")
    if os.path.exists(cf) and "darkmode=true" in open(cf).read().lower().replace(" ", ""): return True
    return QApplication.palette().window().color().lightness() < 128

class PrevBus(QObject):
    ready = pyqtSignal(str, str)

class CutefishFonts(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cutefish Fonts"); self.setWindowIcon(QIcon(os.path.join(BASE, "icon.png")))
        self.setMinimumSize(780, 520); self.resize(980, 640); self.setAcceptDrops(True)
        self.lang = detect_lang()
        self.all_fonts, self.cur_font, self.psize = [], None, 26
        self.bus = PrevBus(); self.bus.ready.connect(self.on_prev_ready)
        self.init_ui(); self.apply_lang(); self.sync_theme(); self.reload_fonts()
        self.tm = QTimer(self); self.tm.timeout.connect(self.sync_theme); self.tm.start(1500)
    def init_ui(self):
        cw = QWidget(); self.setCentralWidget(cw); root = QVBoxLayout(cw); root.setContentsMargins(16,16,16,16); root.setSpacing(12)
        bar = QHBoxLayout()
        self.cmb_cat = QComboBox(); self.cmb_cat.currentIndexChanged.connect(self.filter_fonts); bar.addWidget(self.cmb_cat)
        self.in_search = QLineEdit(); self.in_search.textChanged.connect(self.filter_fonts); bar.addWidget(self.in_search, 1)
        self.btn_dl = QPushButton(); self.btn_dl.setObjectName("PrimaryBtn"); self.btn_dl.clicked.connect(self.on_dl); bar.addWidget(self.btn_dl)
        self.btn_add = QPushButton(); self.btn_add.clicked.connect(self.on_add); bar.addWidget(self.btn_add)
        self.btn_del = QPushButton(); self.btn_del.setObjectName("DangerBtn"); self.btn_del.clicked.connect(self.on_remove); bar.addWidget(self.btn_del)
        self.btn_cache = QPushButton(); self.btn_cache.clicked.connect(self.on_cache); bar.addWidget(self.btn_cache)
        self.cmb_lang = QComboBox(); self.cmb_lang.addItems(list(TRANSLATIONS.keys())); self.cmb_lang.setCurrentText(self.lang)
        self.cmb_lang.currentTextChanged.connect(self.on_lang_chg); bar.addWidget(self.cmb_lang)
        root.addLayout(bar)

        body = QHBoxLayout(); root.addLayout(body, 1)
        self.flist = QListWidget(); self.flist.setFixedWidth(290); self.flist.currentItemChanged.connect(self.on_select); body.addWidget(self.flist)
        right = QVBoxLayout(); body.addLayout(right, 1)
        pctrl = QHBoxLayout()
        self.in_prev = QLineEdit(); self.in_prev.textChanged.connect(self.render_preview); pctrl.addWidget(self.in_prev, 1)
        self.lbl_sz = QLabel("26 pt"); pctrl.addWidget(self.lbl_sz)
        self.sld = QSlider(Qt.Horizontal); self.sld.setRange(12, 72); self.sld.setValue(26); self.sld.setFixedWidth(120)
        self.sld.valueChanged.connect(self.on_sz); pctrl.addWidget(self.sld); right.addLayout(pctrl)

        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.pbox = QWidget(); pl = QVBoxLayout(self.pbox); pl.setContentsMargins(16,16,16,16); pl.setSpacing(14)
        self.lbl_phead = QLabel(""); self.lbl_p1 = QLabel(""); self.lbl_p1.setWordWrap(True)
        self.lbl_p2 = QLabel(""); self.lbl_p3 = QLabel(""); self.lbl_p3.setWordWrap(True)
        for w in (self.lbl_phead, self.lbl_p1, self.lbl_p2, self.lbl_p3): pl.addWidget(w)
        pl.addStretch(); self.scroll.setWidget(self.pbox); right.addWidget(self.scroll, 1)
        self.lbl_info = QLabel(""); self.lbl_info.setMinimumWidth(100); self.lbl_info.setStyleSheet("opacity:0.75; font-size:12px;"); right.addWidget(self.lbl_info)
    def t(self): return TRANSLATIONS.get(self.lang, TRANSLATIONS["en"])
    def on_lang_chg(self, l): self.lang = l; self.apply_lang(); self.on_select(self.flist.currentItem(), None)
    def apply_lang(self):
        tr = self.t(); idx = max(0, self.cmb_cat.currentIndex())
        self.cmb_cat.blockSignals(True); self.cmb_cat.clear(); self.cmb_cat.addItems(tr["cats"]); self.cmb_cat.setCurrentIndex(idx); self.cmb_cat.blockSignals(False)
        self.in_search.setPlaceholderText(tr["search"]); self.btn_dl.setText(tr["dl"]); self.btn_add.setText(tr["add"])
        self.btn_del.setText(tr["del"]); self.btn_cache.setText(tr["cache"]); self.in_prev.setText(tr["pangram"]); self.lbl_p2.setText(tr["alpha"])

    def sync_theme(self):
        dk = is_dark()
        if getattr(self, "_dk", None) == dk: return
        self._dk = dk
        bg, card, txt, brd = ("#16181D", "#1E2028", "#F3F4F6", "#2D313D") if dk else ("#F4F6F8", "#FFFFFF", "#111827", "#E5E7EB")
        self.setStyleSheet(f"QMainWindow,QWidget{{background:{bg};color:{txt};}} QListWidget,QScrollArea,QLineEdit,QComboBox{{background:{card};color:{txt};border:1px solid {brd};border-radius:8px;padding:6px;}} QPushButton{{background:{card};color:{txt};border:1px solid {brd};border-radius:8px;padding:6px 12px;}} QPushButton#PrimaryBtn{{background:#10B981;color:#FFF;border:none;font-weight:bold;}} QPushButton#DangerBtn{{background:#DC2626;color:#FFF;border:none;}}")

    def reload_fonts(self): QFontDatabase.removeAllApplicationFonts(); self.all_fonts = list_all_fonts(); self.filter_fonts()
    def filter_fonts(self):
        cat = self.cmb_cat.currentIndex(); q = self.in_search.text().lower().strip(); self.flist.clear()
        for f in self.all_fonts:
            if (cat == 1 and not f["installed"]) or (cat == 2 and not f["user"]) or (cat == 3 and not f["mono"]) or (q and q not in f["family"].lower()): continue
            it = QListWidgetItem(("✓  " if f["installed"] else "○  ") + f["family"]); it.setData(Qt.UserRole, f)
            if f["installed"]: it.setForeground(QColor("#10B981"))
            self.flist.addItem(it)
        if self.flist.count(): self.flist.setCurrentRow(0)

    def on_select(self, cur, _):
        if not cur: return
        self.cur_font = cur.data(Qt.UserRole); tr = self.t()
        self.btn_dl.setEnabled(not self.cur_font["installed"]); self.btn_del.setEnabled(self.cur_font["user"])
        self.lbl_info.setText(tr["st_inst"].format(n=len(self.cur_font["files"])) if self.cur_font["installed"] else tr["st_cat"])
        self.render_preview()

    def on_sz(self, v): self.psize = v; self.lbl_sz.setText(f"{v} pt"); self.render_preview()
    def apply_font_html(self, fam, real_fam, installed):
        tr = self.t(); txt = self.in_prev.text() or "Aa Bb Cc 123"
        badge = f"<span style='background:#10B981;color:#FFF;padding:2px 8px;border-radius:6px;font-size:11px;'>{tr['b_inst']}</span>" if installed else f"<span style='background:#3B82F6;color:#FFF;padding:2px 8px;border-radius:6px;font-size:11px;'>{tr['b_cat']}</span>"
        self.lbl_phead.setText(f"<b>{fam}</b> &nbsp; {badge}")
        self.lbl_p1.setFont(QFont(real_fam, self.psize)); self.lbl_p1.setText(txt); self.lbl_p2.setFont(QFont(real_fam, 14)); self.lbl_p3.setFont(QFont(real_fam, 30)); self.lbl_p3.setText(txt)

    def on_prev_ready(self, fam, fp):
        if not self.cur_font or self.cur_font["family"] != fam: return
        fid = QFontDatabase.addApplicationFont(fp); fams = QFontDatabase.applicationFontFamilies(fid) if fid != -1 else []
        self.apply_font_html(fam, next(iter(fams), fam), False)

    def render_preview(self):
        if not self.cur_font: return
        fam = self.cur_font["family"]
        if self.cur_font["installed"]:
            fp = next(iter(self.cur_font["files"]), None); fid = QFontDatabase.addApplicationFont(fp) if fp else -1
            fams = QFontDatabase.applicationFontFamilies(fid) if fid != -1 else []
            self.apply_font_html(fam, next(iter(fams), fam), True)
        else:
            cached = os.path.join("/tmp/cf_font_prev", f"{fam.replace(' ', '')}.ttf")
            if os.path.exists(cached) and os.path.getsize(cached) > 4096: self.on_prev_ready(fam, cached)
            else:
                self.apply_font_html(fam, "sans-serif", False)
                threading.Thread(target=lambda f=fam: (lambda p: self.bus.ready.emit(f, p) if p else None)(get_preview_font_file(f)), daemon=True).start()

    def on_dl(self):
        if not self.cur_font: return
        tr = self.t(); self.btn_dl.setText(tr["dl_busy"]); QApplication.processEvents()
        ok = download_and_install(self.cur_font["family"]); self.btn_dl.setText(tr["dl"])
        if ok: self.reload_fonts()
        else: QMessageBox.warning(self, "Cutefish Fonts", tr["dl_err"])

    def on_add(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Fonts", os.path.expanduser("~"), "Fonts (*.ttf *.otf *.ttc)")
        if files and install_local(files): self.reload_fonts()

    def on_remove(self):
        if self.cur_font and self.cur_font["user"] and QMessageBox.question(self, "Cutefish Fonts", self.t()["del_q"].format(fam=self.cur_font["family"])) == QMessageBox.Yes:
            remove_font_files(self.cur_font["files"]); self.reload_fonts()

    def on_cache(self): refresh_cache(); self.reload_fonts(); QMessageBox.information(self, "Cutefish Fonts", self.t()["cache_ok"])
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls(): e.acceptProposedAction()
    def dropEvent(self, e):
        if install_local([u.toLocalFile() for u in e.mimeData().urls()]): self.reload_fonts()

app = QApplication(list(("cutefish-fonts",))); app.setDesktopFileName("cutefish-fonts")
w = CutefishFonts(); w.show(); sys.exit(app.exec_())

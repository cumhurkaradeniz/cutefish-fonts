import os, locale

def detect_lang():
    raw = os.environ.get("LC_ALL") or os.environ.get("LANG") or (locale.getdefaultlocale() or "en")
    code = str(raw)[:2].lower()
    return code if code in TRANSLATIONS else "en"

TRANSLATIONS = {
    "tr": {
        "cats": ["Tüm Katalog", "✓ Sistemde Kurulu", "★ Kullanıcı Fontları", "Monospace (Kod)"],
        "search": "Açık kaynak fontlarda ara...", "dl": "⬇ İndir ve Kur", "dl_busy": "İndiriliyor...",
        "add": "+ Dosyadan", "del": "Kaldır", "cache": "↻ Bellek",
        "pangram": "Pijamalı hasta yağız şoföre çabucak güvendi. 0123456789",
        "alpha": "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ\nabcçdefgğhıijklmnoöprsştuüvyz\n0123456789 !@#$%^&*()_+-=",
        "b_inst": "✓ Sistemde Kurulu", "b_cat": "Canlı Katalog Önizlemesi",
        "st_inst": "Durum: Kurulu ({n} dosya)", "st_cat": "Durum: Açık Kaynak Katalog (Kurulu değil)",
        "dl_err": "Bu font otomatik indirilemedi; tarayıcıdan .ttf indirip sürükleyebilirsiniz.",
        "del_q": "'{fam}' fontu kaldırılsın mı?", "cache_ok": "Sistem font önbelleği (fc-cache) güncellendi."
    },
    "en": {
        "cats": ["All Catalog", "✓ Installed", "★ User Fonts", "Monospace (Code)"],
        "search": "Search open-source fonts...", "dl": "⬇ Download & Install", "dl_busy": "Downloading...",
        "add": "+ From File", "del": "Remove", "cache": "↻ Cache",
        "pangram": "The quick brown fox jumps over the lazy dog. 0123456789",
        "alpha": "ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n0123456789 !@#$%^&*()_+-=",
        "b_inst": "✓ Installed", "b_cat": "Live Catalog Preview",
        "st_inst": "Status: Installed ({n} files)", "st_cat": "Status: Open-Source Catalog (Not installed)",
        "dl_err": "Could not auto-download this font; you can drag and drop a .ttf file.",
        "del_q": "Remove font '{fam}'?", "cache_ok": "System font cache (fc-cache) refreshed."
    },
    "de": {
        "cats": ["Gesamtkatalog", "✓ Installiert", "★ Benutzerschriften", "Monospace (Code)"],
        "search": "Open-Source-Schriften suchen...", "dl": "⬇ Installieren", "dl_busy": "Lädt...",
        "add": "+ Datei", "del": "Entfernen", "cache": "↻ Cache",
        "pangram": "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern. 0123456789",
        "alpha": "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß\nabcdefghijklmnopqrstuvwxyzäöüß\n0123456789 !@#$%^&*()_+-=",
        "b_inst": "✓ Installiert", "b_cat": "Live-Vorschau",
        "st_inst": "Status: Installiert ({n} Dateien)", "st_cat": "Status: Katalog (Nicht installiert)",
        "dl_err": "Schriftart konnte nicht geladen werden.", "del_q": "Schriftart '{fam}' entfernen?", "cache_ok": "Schriftarten-Cache aktualisiert."
    },
    "fr": {
        "cats": ["Tout le catalogue", "✓ Installées", "★ Polices utilisateur", "Monospace (Code)"],
        "search": "Rechercher des polices...", "dl": "⬇ Installer", "dl_busy": "Téléchargement...",
        "add": "+ Fichier", "del": "Supprimer", "cache": "↻ Cache",
        "pangram": "Portez ce vieux whisky au juge blond qui fume. 0123456789",
        "alpha": "ABCDEFGHIJKLMNOPQRSTUVWXYZÉÈÊÀÇ\nabcdefghijklmnopqrstuvwxyzéèêàç\n0123456789 !@#$%^&*()_+-=",
        "b_inst": "✓ Installée", "b_cat": "Aperçu en direct",
        "st_inst": "Statut : Installée ({n} fichiers)", "st_cat": "Statut : Catalogue (Non installée)",
        "dl_err": "Téléchargement impossible.", "del_q": "Supprimer la police '{fam}' ?", "cache_ok": "Cache des polices mis à jour."
    },
    "es": {
        "cats": ["Todo el catálogo", "✓ Instaladas", "★ Fuentes de usuario", "Monospace (Código)"],
        "search": "Buscar fuentes...", "dl": "⬇ Instalar", "dl_busy": "Descargando...",
        "add": "+ Archivo", "del": "Eliminar", "cache": "↻ Caché",
        "pangram": "Benjamín pidió una bebida de kiwi y fresa. 0123456789",
        "alpha": "ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ\nabcdefghijklmnñopqrstuvwxyzáéíóú\n0123456789 !@#$%^&*()_+-=",
        "b_inst": "✓ Instalada", "b_cat": "Vista previa",
        "st_inst": "Estado: Instalada ({n} archivos)", "st_cat": "Estado: Catálogo (No instalada)",
        "dl_err": "No se pudo descargar la fuente.", "del_q": "¿Eliminar la fuente '{fam}'?", "cache_ok": "Caché de fuentes actualizada."
    },
    "ru": {
        "cats": ["Весь каталог", "✓ Установленные", "★ Пользовательские", "Моноширинные"],
        "search": "Поиск шрифтов...", "dl": "⬇ Установить", "dl_busy": "Загрузка...",
        "add": "+ Из файла", "del": "Удалить", "cache": "↻ Кэш",
        "pangram": "Съешь ещё этих мягких французских булок, да выпей чаю. 0123456789",
        "alpha": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ\nабвгдеёжзийклмнопрстуфхцчшщъыьэюя\n0123456789 !@#$%^&*()_+-=",
        "b_inst": "✓ Установлен", "b_cat": "Предпросмотр",
        "st_inst": "Статус: Установлен ({n} файлов)", "st_cat": "Статус: Каталог (Не установлен)",
        "dl_err": "Не удалось скачать шрифт.", "del_q": "Удалить шрифт '{fam}'?", "cache_ok": "Кэш шрифтов обновлен."
    },
    "ar": {
        "cats": ["كل الخطوط", "✓ المثبتة", "★ خطوط المستخدم", "أحادية العرض"],
        "search": "البحث في الخطوط...", "dl": "⬇ تنزيل وتثبيت", "dl_busy": "جاري التنزيل...",
        "add": "+ من ملف", "del": "حذف", "cache": "↻ تحديث الذاكرة",
        "pangram": "نص حكيم له سر قاطع وذو شأن عظيم مكتوب على ثوب أخضر. 0123456789",
        "alpha": "أ ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن هـ و ي\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n0123456789 !@#$%^&*()_+-=",
        "b_inst": "✓ مثبت", "b_cat": "معاينة مباشرة",
        "st_inst": "الحالة: مثبت ({n} ملفات)", "st_cat": "الحالة: غير مثبت",
        "dl_err": "تعذر التنزيل التلقائي.", "del_q": "هل تريد حذف الخط '{fam}'؟", "cache_ok": "تم تحديث ذاكرة الخطوط."
    }
}

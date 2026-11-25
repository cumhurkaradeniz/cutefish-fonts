import os, shutil, base64, subprocess, urllib.request

USER_DIR = os.path.expanduser("~/.local/share/fonts")
os.makedirs(USER_DIR, exist_ok=True)

POPULAR_FONTS = [
    ("Roboto", "SANS"), ("Open Sans", "SANS"), ("Montserrat", "SANS"), ("Lato", "SANS"), ("Poppins", "SANS"),
    ("Inter", "SANS"), ("Roboto Condensed", "SANS"), ("Oswald", "SANS"), ("Raleway", "SANS"), ("Nunito", "SANS"),
    ("Nunito Sans", "SANS"), ("Ubuntu", "SANS"), ("Rubik", "SANS"), ("Work Sans", "SANS"), ("Mulish", "SANS"),
    ("Quicksand", "SANS"), ("Barlow", "SANS"), ("DM Sans", "SANS"), ("Kanit", "SANS"), ("Manrope", "SANS"),
    ("PT Sans", "SANS"), ("Noto Sans", "SANS"), ("Fira Sans", "SANS"), ("Titillium Web", "SANS"), ("Josefin Sans", "SANS"),
    ("Libre Franklin", "SANS"), ("Karla", "SANS"), ("Cabin", "SANS"), ("Dosis", "SANS"), ("Anton", "SANS"),
    ("Bebas Neue", "SANS"), ("Oxygen", "SANS"), ("Exo 2", "SANS"), ("Hind", "SANS"), ("Varela Round", "SANS"),
    ("Plus Jakarta Sans", "SANS"), ("Space Grotesk", "SANS"), ("Outfit", "SANS"), ("Figtree", "SANS"), ("Lexend", "SANS"),
    ("Syne", "SANS"), ("Archivo", "SANS"), ("Rajdhani", "SANS"), ("Signika", "SANS"), ("Catamaran", "SANS"),
    ("Asap", "SANS"), ("Maven Pro", "SANS"), ("Comfortaa", "SANS"), ("Questrial", "SANS"), ("Abel", "SANS"),
    ("Playfair Display", "SERIF"), ("Merriweather", "SERIF"), ("Lora", "SERIF"), ("PT Serif", "SERIF"), ("Noto Serif", "SERIF"),
    ("Libre Baskerville", "SERIF"), ("EB Garamond", "SERIF"), ("Crimson Text", "SERIF"), ("Cormorant Garamond", "SERIF"), ("Bitter", "SERIF"),
    ("Arvo", "SERIF"), ("Domine", "SERIF"), ("Zilla Slab", "SERIF"), ("Vollkorn", "SERIF"), ("Spectral", "SERIF"),
    ("Cardo", "SERIF"), ("Cinzel", "SERIF"), ("Abril Fatface", "SERIF"), ("Bodoni Moda", "SERIF"), ("Prata", "SERIF"),
    ("Fraunces", "SERIF"), ("Source Serif 4", "SERIF"), ("Newsreader", "SERIF"), ("Literata", "SERIF"), ("Alegreya", "SERIF"),
    ("Fira Code", "MONO"), ("JetBrains Mono", "MONO"), ("Roboto Mono", "MONO"), ("Source Code Pro", "MONO"), ("IBM Plex Mono", "MONO"),
    ("Space Mono", "MONO"), ("Inconsolata", "MONO"), ("Ubuntu Mono", "MONO"), ("Courier Prime", "MONO"), ("DM Mono", "MONO"),
    ("Cousine", "MONO"), ("Anonymous Pro", "MONO"), ("Overpass Mono", "MONO"), ("Red Hat Mono", "MONO"), ("Azeret Mono", "MONO"),
    ("Dancing Script", "DISPLAY"), ("Pacifico", "DISPLAY"), ("Lobster", "DISPLAY"), ("Caveat", "DISPLAY"), ("Satisfy", "DISPLAY"),
    ("Great Vibes", "DISPLAY"), ("Sacramento", "DISPLAY"), ("Kaushan Script", "DISPLAY"), ("Amatic SC", "DISPLAY"), ("Shadows Into Light", "DISPLAY"),
    ("Indie Flower", "DISPLAY"), ("Permanent Marker", "DISPLAY"), ("Courgette", "DISPLAY"), ("Cookie", "DISPLAY"), ("Yellowtail", "DISPLAY"),
    ("Righteous", "DISPLAY"), ("Fredoka", "DISPLAY"), ("Alfa Slab One", "DISPLAY"), ("Patua One", "DISPLAY"), ("Russo One", "DISPLAY"),
    ("Teko", "SANS"), ("Chakra Petch", "SANS"), ("Orbitron", "DISPLAY"), ("Press Start 2P", "MONO"), ("Silkscreen", "MONO")
]
def get_installed_map():
    out = subprocess.check_output(["fc-list", "--format=%{file}|%{family}|%{spacing}\n"], text=True, errors="ignore")
    inst = {}
    for line in out.splitlines():
        if "|" not in line: continue
        fpath, fams, sp = line.split("|", 2)
        fpath = fpath.strip()
        fam = next(iter(fams.split(",")), "").strip()
        if not fam or not fpath: continue
        is_user = fpath.startswith(USER_DIR)
        is_mono = sp.strip() in ("100", "90")
        if fam not in inst: inst[fam] = {"files": [], "user": is_user, "mono": is_mono}
        if fpath not in inst[fam]["files"]: inst[fam]["files"].append(fpath)
        if is_user: inst[fam]["user"] = True
    return inst

def list_all_fonts():
    inst = get_installed_map()
    merged = {}
    for fam, cat in POPULAR_FONTS:
        info = inst.get(fam)
        merged[fam] = {"family": fam, "installed": bool(info), "user": info["user"] if info else False, "mono": (info["mono"] if info else cat == "MONO"), "files": info["files"] if info else []}
    for fam, info in inst.items():
        if fam not in merged:
            merged[fam] = {"family": fam, "installed": True, "user": info["user"], "mono": info["mono"], "files": info["files"]}
    return sorted(merged.values(), key=lambda x: (not x["installed"], x["family"].lower()))

def refresh_cache(): subprocess.run(["fc-cache", "-f"], check=False)

import re, urllib.parse

def resolve_ttf_url(family):
    slug = family.lower().replace(" ", "-")
    return base64.b64decode("aHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2ZvbnRzb3VyY2UvZm9udHMv").decode() + f"{slug}@latest/latin-400-normal.ttf"

def download_and_install(family):
    clean = family.replace(" ", "")
    dst = os.path.join(USER_DIR, f"{clean}.ttf")
    try:
        u = resolve_ttf_url(family)
        if u:
            urllib.request.urlretrieve(u, dst)
            if os.path.getsize(dst) > 4096:
                refresh_cache(); return True
    except Exception:
        pass
    if os.path.exists(dst): os.remove(dst)
    return False

def install_local(paths):
    c = 0
    for p in paths:
        if os.path.isfile(p) and p.lower().endswith((".ttf", ".otf", ".ttc")):
            shutil.copy2(p, os.path.join(USER_DIR, os.path.basename(p))); c += 1
    if c: refresh_cache()
    return c

def remove_font_files(files):
    r = 0
    for f in files:
        if f.startswith(USER_DIR) and os.path.exists(f):
            os.remove(f); r += 1
    if r: refresh_cache()
    return r

PREV_DIR = "/tmp/cf_font_prev"
os.makedirs(PREV_DIR, exist_ok=True)

def get_preview_font_file(family):
    clean = family.replace(" ", "")
    dst = os.path.join(PREV_DIR, f"{clean}.ttf")
    if os.path.exists(dst) and os.path.getsize(dst) > 4096: return dst
    tmp = dst + ".part"
    try:
        u = resolve_ttf_url(family)
        if u:
            urllib.request.urlretrieve(u, tmp)
            if os.path.getsize(tmp) > 4096:
                os.replace(tmp, dst); return dst
    except Exception:
        pass
    if os.path.exists(tmp): os.remove(tmp)
    return None

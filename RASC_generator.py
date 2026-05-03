#======================================================
#                 (c) AEROPIC 2026
#  
# https://github.com/aeropic/RASC_catalog_generator
# http://www.messier.seds.org/xtra/similar/rasc-ngc.html
#
#   V1.2 : fixed arc seconds units in size
#======================================================

# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
from datetime import datetime

# --- PAGE LAYOUT PARAMETERS ---
CARD_SIZE_MIN = "120px"
THUMB_SIZE = (400, 400)

# --- DEPENDANCIES AUTO-INSTALL ---
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    print("Installation de Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image
    from PIL.ExifTags import TAGS

# --- CONFIGURATION & TRADUCTIONS ---
lang = 'fr'

type_map = {
    'G': 'Galaxie',
    'PN': 'Nébuleuse Planétaire',
    'OC': 'Amas Ouvert',
    'GC': 'Amas Globulaire',
    'EN': 'Nébuleuse par émission',
    'RN': 'Nébuleuse par réflexion',
    'SNR': 'Reste de Supernova',
    'E/RN': 'Nébuleuse Ém./Réf.'
}

season_map = {
    'P': 'Printemps',
    'E': 'Été',
    'A': 'Automne',
    'H': 'Hiver'
}

texts = {
    'fr': {
        'title': "Catalogue RASC - Finest NGC Objects",
        'type': "Type",
        'season': "Saison",
        'constellation': "Constellation",
        'magnitude': "Magnitude",
        'size': "Taille",
        'description': "Description",
        'date': "Date",
        'file': "Fichier",
        'all': "Tous"
    }
}

# Catalogue avec unités corrigées (utilisation de ' pour éviter les conflits HTML/JS)
rasc_data = [
    # AUTUMN (A)
    ["1", "7009", "PN", "A", "8.3", "Aqr", "25''", "Saturn Nebula"],
    ["2", "7293", "PN", "A", "6.5", "Aqr", "12'50''", "Helix Nebula"],
    ["3", "7331", "G", "A", "9.5", "Peg", "10.7x4.0'", "Large bright spiral"],
    ["4", "7635", "EN", "A", "-", "Cas", "15x8'", "Bubble Nebula"],
    ["5", "7789", "OC", "A", "6.7", "Cas", "16'", "300* faint but rich"],
    ["6", "185", "G", "A", "11.7", "Cas", "2x2'", "Companion to M31"],
    ["7", "281", "EN", "A", "-", "Cas", "35x30'", "Large faint nebulosity"],
    ["8", "457", "OC", "A", "6.4", "Cas", "13'", "80* Owl Cluster"],
    ["9", "663", "OC", "A", "7.1", "Cas", "16'", "80* cluster"],
    ["10", "I289", "PN", "A", "12.3", "Cas", "34''", "Dim oval smudge"],
    ["11", "7662", "PN", "A", "9.2", "And", "20''", "Blue Snowball"],
    ["12", "891", "G", "A", "10", "And", "13.5x2.8'", "Classic edge-on"],
    ["13", "253", "G", "A", "7.1", "Scl", "25.1x7.4'", "Silver Coin Galaxy"],
    ["14", "772", "G", "A", "10.3", "Ari", "7.1x4.5'", "Diffuse spiral"],
    ["15", "246", "PN", "A", "8.0", "Cet", "3'45''", "Skull Nebula"],
    ["16", "936", "G", "A", "10.1", "Cet", "5.2x4.4'", "Near M77"],
    ["17", "869", "OC", "A", "4.4", "Per", "30'/30'", "Double Cluster"],
    ["18", "1023", "G", "A", "9.5", "Per", "8.7x4.3'", "Lens-shaped galaxy"],
    ["19", "1491", "EN", "A", "-", "Per", "3.0x3.0'", "Small emission nebula"],
    ["20", "1501", "PN", "A", "12.0", "Cam", "52''", "Oyster Nebula"],
    ["21", "1232", "G", "A", "9.9", "Eri", "7.8x6.9'", "Face-on spiral"],
    ["22", "1535", "PN", "A", "10.4", "Eri", "18''", "Cleopatra's Eye"],
    # WINTER (H)
    ["23", "1514", "PN", "H", "10.8", "Tau", "1'54''", "Crystal Ball Nebula"],
    ["24", "1931", "E/RN", "H", "-", "Aur", "3.0x3.0'", "Haze around 4 stars"],
    ["25", "1788", "RN", "H", "-", "Ori", "8.0x5.0'", "Reflection nebula"],
    ["26", "1973", "E/RN", "H", "-", "Ori", "40x25'", "Running Man Nebula"],
    ["27", "2022", "PN", "H", "12.4", "Ori", "18''", "Small annular PN"],
    ["28", "2024", "EN", "H", "-", "Ori", "30x30'", "Flame Nebula"],
    ["29", "2194", "OC", "H", "8.5", "Ori", "10'", "80* rich cluster"],
    ["30", "2371", "PN", "H", "13.0", "Gem", "55''", "Double-lobed PN"],
    ["31", "2392", "PN", "H", "8.3", "Gem", "13''", "Eskimo Nebula"],
    ["32", "2237", "EN", "H", "-", "Mon", "80x60'", "Rosette Nebula"],
    ["33", "2261", "E/RN", "H", "var", "Mon", "2x1'", "Hubble's Variable Neb."],
    ["34", "2359", "EN", "H", "-", "CMa", "8.0x6.0'", "Thor's Helmet"],
    ["35", "2440", "PN", "H", "10.3", "Pup", "14''", "Planetary nebula"],
    ["36", "2539", "OC", "H", "6.5", "Pup", "22'", "50* rich cluster"],
    ["37", "2403", "G", "H", "8.4", "Cam", "17.8x11.0'", "Large spiral"],
    ["38", "2655", "G", "H", "10.1", "Cam", "5.1x4.4'", "Bright ellipse"],
    # SPRING (P)
    ["39", "2683", "G", "P", "9.7", "Lyn", "9.3x2.5'", "UFO Galaxy"],
    ["40", "2841", "G", "P", "9.3", "UMa", "8.1x3.8'", "Elongated spiral"],
    ["41", "3079", "G", "P", "10.6", "UMa", "7.6x1.7'", "Edge-on spiral"],
    ["42", "3184", "G", "P", "9.7", "UMa", "6.9x6.8'", "Face-on spiral"],
    ["43", "3877", "G", "P", "10.9", "UMa", "5.4x1.5'", "Edge-on"],
    ["44", "3941", "G", "P", "9.8", "UMa", "3.8x2.5'", "Small elliptical"],
    ["45", "4026", "G", "P", "10.7", "UMa", "5.1x1.4'", "Lens-shaped"],
    ["46", "4088", "G", "P", "10.5", "UMa", "5.8x2.5'", "Nearly edge-on"],
    ["47", "4157", "G", "P", "11.9", "UMa", "6.9x1.7'", "Thin sliver"],
    ["48", "4605", "G", "P", "9.6", "UMa", "5.5x2.3'", "Bright edge-on"],
    ["49", "3115", "G", "P", "9.2", "Sex", "8.3x3.2'", "Spindle Galaxy"],
    ["50", "3242", "PN", "P", "8.6", "Hya", "16''", "Ghost of Jupiter"],
    ["51", "3003", "G", "P", "11.7", "LMi", "5.9x1.7'", "Faint streak"],
    ["52", "3344", "G", "P", "9.9", "LMi", "6.9x6.5'", "Diffuse face-on spiral"],
    ["53", "3432", "G", "P", "11.3", "LMi", "6.2x1.5'", "Faint flat streak"],
    ["54", "2903", "G", "P", "8.9", "Leo", "12.6x6.6'", "Large bright spiral"],
    ["55", "3384", "G", "P", "9.9", "Leo", "5.9x2.6'", "Near M105"],
    ["56", "3521", "G", "P", "8.7", "Leo", "9.5x5.0'", "Bright spiral"],
    ["57", "3607", "G", "P", "10.0", "Leo", "3.7x3.2'", "Elliptical galaxy"],
    ["58", "3628", "G", "P", "9.5", "Leo", "14.8x3.6'", "Hamburger Galaxy"],
    ["59", "4111", "G", "P", "10.8", "CVn", "4.8x1.1'", "Lens-shaped edge-on"],
    ["60", "4214", "G", "P", "9.7", "CVn", "7.9x6.3'", "Large irregular"],
    ["61", "4244", "G", "P", "10.2", "CVn", "16.2x2.5'", "Large edge-on"],
    ["62", "4449", "G", "P", "9.4", "CVn", "5.1x3.7'", "Rectangular shape"],
    ["63", "4490", "G", "P", "9.8", "CVn", "5.9x3.1'", "Cocoon Galaxy"],
    ["64", "4631", "G", "P", "9.3", "CVn", "15.1x3.3'", "Whale Galaxy"],
    ["65", "4656", "G", "P", "10.4", "CVn", "13.8x3.3'", "Hockey Stick Galaxy"],
    ["66", "5005", "G", "P", "9.8", "CVn", "5.4x2.7'", "Bright elongated"],
    ["67", "5033", "G", "P", "10.1", "CVn", "10.5x5.6'", "Large bright spiral"],
    ["68", "4274", "G", "P", "10.4", "Com", "6.9x2.8'", "Spiral galaxy"],
    ["69", "4414", "G", "P", "10.2", "Com", "3.6x2.2'", "Bright spiral"],
    ["70", "4494", "G", "P", "9.8", "Com", "4.8x3.8'", "Bright elliptical"],
    ["71", "4559", "G", "P", "9.8", "Com", "10.5x4.9'", "Large spiral"],
    ["72", "4565", "G", "P", "9.6", "Com", "16.2x2.8'", "Needle Galaxy"],
    ["73", "4725", "G", "P", "9.2", "Com", "11.0x7.9'", "Very bright spiral"],
    ["74", "4038", "G", "P", "10.7", "Crv", "~3x2'", "Antennae Galaxies"],
    ["75", "4361", "PN", "P", "10.3", "Crv", "45''", "Small and bright"],
    ["76", "4216", "G", "P", "9.9", "Vir", "8.3x2.2'", "Nearly edge-on"],
    ["77", "4388", "G", "P", "11.0", "Vir", "5.1x1.4'", "Markarian's Chain"],
    ["78", "4438", "G", "P", "10.1", "Vir", "9.3x3.9'", "The Eyes"],
    ["79", "4517", "G", "P", "10.5", "Vir", "10.2x1.9'", "Faint edge-on"],
    ["80", "4526", "G", "P", "9.6", "Vir", "7.6x2.3'", "Lost Galaxy"],
    ["81", "4535", "G", "P", "9.8", "Vir", "6.8x5.0'", "Near M49"],
    ["82", "4567", "G", "P", "~11", "Vir", "4.6x2.1'", "Siamese Twins"],
    ["83", "4699", "G", "P", "9.6", "Vir", "3.5x2.7'", "Small and bright"],
    ["84", "4762", "G", "P", "10.2", "Vir", "8.7x1.6'", "Flattest galaxy"],
    ["85", "5746", "G", "P", "10.6", "Vir", "7.9x1.7'", "Fine edge-on"],
    ["86", "5466", "GC", "P", "9.1", "Boo", "11.0'", "Loose class XII"],
    ["87", "5907", "G", "P", "10.4", "Dra", "12.3x1.8'", "Splinter Galaxy"],
    ["88", "6503", "G", "P", "10.2", "Dra", "6.2x2.3'", "Elongated spiral"],
    ["89", "6543", "PN", "P", "8.8", "Dra", "18''", "Cat's Eye Nebula"],
    # SUMMER (E)
    ["90", "6210", "PN", "E", "9.3", "Her", "14''", "Turtle Nebula"],
    ["91", "6369", "PN", "E", "10.4", "Oph", "30''", "Little Ghost"],
    ["92", "6572", "PN", "E", "9.0", "Oph", "8''", "Emerald Nebula"],
    ["93", "6633", "OC", "E", "4.6", "Oph", "27'", "Italy Cluster"],
    ["94", "6712", "GC", "E", "8.2", "Sct", "7.2'", "Small globular"],
    ["95", "6781", "PN", "E", "11.8", "Aql", "1'49''", "Planetary nebula"],
    ["96", "6819", "OC", "E", "7.3", "Cyg", "5'", "150* faint but rich"],
    ["97", "6826", "PN", "E", "9.8", "Cyg", "30''", "Blinking Planetary"],
    ["98", "6888", "SNR", "E", "-", "Cyg", "20x10'", "Crescent Nebula"],
    ["99a", "6960", "SNR", "E", "-", "Cyg", "70x6'", "Western Veil Nebula"],
    ["99b", "6992", "SNR", "E", "-", "Cyg", "78x8'", "Eastern Veil Nebula"],
    ["100", "7000", "EN", "E", "-", "Cyg", "120x100'", "North America Neb."],
    ["101", "7027", "PN", "E", "10.4", "Cyg", "15''", "Protoplanetary neb."],
    ["102", "6445", "PN", "E", "11.8", "Sgr", "34''", "Box Nebula"],
    ["103", "6520", "OC", "E", "8.1", "Sgr", "6'", "Near Dark Neb B86"],
    ["104", "6818", "PN", "E", "9.9", "Sgr", "17''", "Little Gem Nebula"],
    ["105", "6802", "OC", "E", "8.8", "Vul", "3.2'", "At end of Coathanger"],
    ["106", "6940", "OC", "E", "6.3", "Vul", "31'", "60* rich cluster"],
    ["107", "6939", "OC", "E", "7.8", "Cep", "8'", "80* very rich"],
    ["108", "6946", "G", "E", "8.9", "Cep", "11.0x9.8'", "Fireworks Galaxy"],
    ["109", "7129", "RN", "E", "-", "Cep", "8x7'", "Reflection nebula"],
    ["110", "40", "PN", "E", "10.2", "Cep", "37''", "Bow-Tie Nebula"]
]

# --- FONCTIONS DE TRAITEMENT ---

def make_thumbnail(src, dest):
    if not os.path.exists("thumbnails"): 
        os.makedirs("thumbnails")
    if os.path.exists(dest) and os.path.getmtime(src) <= os.path.getmtime(dest): 
        return
    try:
        with Image.open(src) as img:
            img.thumbnail(THUMB_SIZE)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(dest, "JPEG", quality=85)
    except Exception as e: 
        print(f"Erreur vignette pour {src}: {e}")

def get_image_info(filepath):
    date_str, filename = "Inconnue", os.path.basename(filepath)
    try:
        img = Image.open(filepath)
        exif = img._getexif()
        if exif:
            for tag, val in exif.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    date_str = datetime.strptime(val, '%Y:%m:%d %H:%M:%S').strftime('%d/%m/%Y')
                    break
        if date_str == "Inconnue":
            date_str = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%d/%m/%Y')
    except: pass
    return date_str, filename

def find_image(directory, ngc_id):
    pattern = re.compile(rf"NGC{ngc_id}(?!\d)", re.IGNORECASE)
    for f in os.listdir(directory):
        if pattern.search(f) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            return f
    return None

def generate_catalog():
    img_dir, out_file, t = ".", "planche_RASC.html", texts[lang]
    imaged_count = 0
    entries = []
    
    for item in rasc_data:
        fname = find_image(img_dir, item[1])
        meta = {"date": "", "file": ""}
        thumb_path = None
        
        if fname:
            imaged_count += 1
            meta["date"], meta["file"] = get_image_info(os.path.join(img_dir, fname))
            name_part, _ = os.path.splitext(fname)
            thumb_name = f"{name_part}_thumbnail.jpg"
            thumb_path = os.path.join("thumbnails", thumb_name)
            make_thumbnail(os.path.join(img_dir, fname), thumb_path)
        
        decoded_item = list(item)
        decoded_item[2] = type_map.get(item[2], item[2])
        decoded_item[3] = season_map.get(item[3], item[3])
        entries.append((decoded_item, fname, thumb_path, meta))

    html = f"""<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8"><title>{t['title']}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0f0f0f; color: #e0e0e0; margin: 0; padding: 20px; overflow-x: hidden; }}
        header {{ text-align: center; margin-bottom: 20px; }}
        .score {{ color: #888; font-size: 0.6em; }}
        
        .filter-bar {{ text-align: center; margin-bottom: 30px; }}
        .filter-btn {{ background: #252525; border: 1px solid #444; color: #aaa; padding: 8px 16px; margin: 0 4px; border-radius: 20px; cursor: pointer; transition: 0.2s; }}
        .filter-btn:hover {{ border-color: #4dabf7; color: #fff; }}
        .filter-btn.active {{ background: #4dabf7; color: #fff; border-color: #4dabf7; }}

        .container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax({CARD_SIZE_MIN}, 1fr)); gap: 20px; }}
        .card {{ background: #1e1e1e; border-radius: 8px; border: 1px solid #333; overflow: hidden; transition: 0.2s; display: block; }}
        .card:hover {{ transform: scale(1.03); border-color: #4dabf7; }}
        .img-box {{ width: 100%; aspect-ratio: 1 / 1; background: #2c2c2c; display: flex; justify-content: center; align-items: center; cursor: pointer; }}
        .card img {{ width: 100%; height: 100%; object-fit: cover; }}
        .placeholder {{ text-align: center; color: #666; font-size: 0.8em; padding: 5px; }}
        .title {{ background: #252525; padding: 10px; text-align: center; font-weight: bold; font-size: 0.85em; }}
        .title a {{ color: #fff; text-decoration: none; }}
        
        #tooltip {{ position: fixed; display: none; background: rgba(20,20,20,0.98); border: 1px solid #4dabf7; padding: 12px; border-radius: 6px; z-index: 2000; pointer-events: none; font-size: 0.85em; box-shadow: 0 4px 15px #000; min-width: 200px; }}
        .lbl {{ color: #4dabf7; font-weight: bold; margin-right: 5px; }}
        
        #modal {{ display: none; position: fixed; z-index: 3000; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); overflow: hidden; }}
        #modal-img {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); cursor: grab; user-select: none; max-width: 95%; max-height: 95%; transition: transform 0.05s linear; }}
        #modal:active #modal-img {{ cursor: grabbing; }}
    </style></head><body>
    <header>
        <h1>{t['title']}<br><span class="score">({imaged_count}/{len(rasc_data)})</span></h1>
    </header>

    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterS('all', this)">{t['all']}</button>
        <button class="filter-btn" onclick="filterS('Printemps', this)">Printemps</button>
        <button class="filter-btn" onclick="filterS('Été', this)">Été</button>
        <button class="filter-btn" onclick="filterS('Automne', this)">Automne</button>
        <button class="filter-btn" onclick="filterS('Hiver', this)">Hiver</button>
    </div>

    <div class="container" id="main-grid">"""

    for item, filename, thumb, meta in entries:
        r_id, n_id, o_type, o_season, mag, const, size, desc = item
        # Sécurisation des chaînes pour éviter le crash des guillemets
        safe_size = size.replace('"', '&quot;')
        safe_desc = desc.replace('"', '&quot;')
        
        data = f'data-type="{o_type}" data-season="{o_season}" data-const="{const}" data-mag="{mag}" data-size="{safe_size}" data-desc="{safe_desc}" data-date="{meta["date"]}" data-file="{meta["file"]}"'
        html += f"""<div class="card" {data} onmousemove="showT(event, this)" onmouseleave="hideT()">
            <div class="img-box" {"onclick='openM(\""+filename+"\")'" if filename else ""}>
                {f'<img src="{thumb}">' if thumb else f'<div class="placeholder">{o_type}<br>{o_season}</div>'}
            </div>
            <div class="title">RASC {r_id} - <a href="https://telescopius.com/deep-sky-objects/ngc-{n_id.lower()}" target="_blank">NGC {n_id}</a></div>
        </div>"""

    html += f"""</div><div id="tooltip"></div>
    <div id="modal" onclick="if(event.target===this) closeM()">
        <img id="modal-img">
    </div>
    <script>
        function filterS(season, btn) {{
            const cards = document.querySelectorAll('.card');
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            cards.forEach(card => {{
                card.style.display = (season === 'all' || card.getAttribute('data-season') === season) ? 'block' : 'none';
            }});
        }}

        const tt = document.getElementById('tooltip');
        function showT(e, el) {{
            const d = el.dataset;
            let c = d.file ? `<div style="border-bottom:1px solid #444;margin-bottom:8px;padding-bottom:5px;"><div style="color:#4dabf7;font-weight:bold;font-family:monospace;">${{d.file}}</div><div style="color:#aaa;font-style:italic;font-size:0.9em;">{t['date']}: ${{d.date}}</div></div>` : "";
            // Affichage propre des unités via template literals
            c += `<div><span class="lbl">{t['type']}:</span>${{d.type}}</div><div><span class="lbl">{t['season']}:</span>${{d.season}}</div>
                  <div><span class="lbl">{t['constellation']}:</span>${{d.const}}</div><div><span class="lbl">{t['magnitude']}:</span>${{d.mag}}</div>
                  <div><span class="lbl">{t['size']}:</span>${{d.size}}</div><div style="margin-top:8px;color:#eee"><em>${{d.desc}}</em></div>`;
            tt.innerHTML = c; tt.style.display = 'block';
            let x = e.clientX + 15, y = e.clientY + 15;
            if (x + 250 > window.innerWidth) x = e.clientX - tt.offsetWidth - 15;
            if (y + tt.offsetHeight > window.innerHeight) y = e.clientY - tt.offsetHeight - 15;
            tt.style.left = x + 'px'; tt.style.top = y + 'px';
        }}
        function hideT() {{ tt.style.display = 'none'; }}

        let m = document.getElementById("modal"), mi = document.getElementById("modal-img");
        let scale = 1, posX = 0, posY = 0, isDragging = false, startX, startY;
        function updateTransform() {{ mi.style.transform = `translate(calc(-50% + ${{posX}}px), calc(-50% + ${{posY}}px)) scale(${{scale}})`; }}
        function openM(s) {{ if(!s) return; scale = 1; posX = 0; posY = 0; mi.src = s; m.style.display = "block"; updateTransform(); }}
        function closeM() {{ m.style.display = "none"; }}

        m.addEventListener('wheel', e => {{
            e.preventDefault();
            scale = Math.min(Math.max(0.5, scale * (e.deltaY > 0 ? 0.9 : 1.1)), 10);
            updateTransform();
        }}, {{passive: false}});
        mi.addEventListener('mousedown', e => {{ isDragging = true; startX = e.clientX - posX; startY = e.clientY - posY; e.preventDefault(); }});
        window.addEventListener('mousemove', e => {{ if (isDragging) {{ posX = e.clientX - startX; posY = e.clientY - startY; updateTransform(); }} }});
        window.addEventListener('mouseup', () => isDragging = false);
    </script></body></html>"""

    with open(out_file, "w", encoding="utf-8") as f: f.write(html)
    print(f"Catalogue généré : {out_file} ({len(rasc_data)} objets)")

if __name__ == "__main__":
    generate_catalog()

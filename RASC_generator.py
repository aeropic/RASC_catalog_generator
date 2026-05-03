#======================================================
#                 (c) AEROPIC 2026
#  
# https://github.com/aeropic/RASC_catalog_generator
#
#======================================================

# -*- coding: utf-8 -*-


import os
import re
import subprocess
import sys
from datetime import datetime

# --- PAGE LAYOUT PARAMETERS ---
CARD_SIZE_MIN = "120px"  # minimal size of a thumbnail

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
    'G': 'Galaxie',              # Galaxy
    'NP': 'Nébuleuse Planétaire', # Planetary Nebula
    'AO': 'Amas Ouvert',          # Open Cluster
    'AG': 'Amas Globulaire',      # Globular Cluster
    'N': 'Nébuleuse',             # Nebula
    'RS': 'Reste Supernova',      # Supernova Remnant
    'NA': 'Nébuleuse/Amas'        # Nebula/Cluster
}

season_map = {
    'P': 'Printemps', # Spring
    'E': 'Été',       # Summer
    'A': 'Automne',   # Autumn
    'H': 'Hiver'      # Winter
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

# Catalogue : [RASC_ID, NGC_ID, Type_Code, Season_Code, Mag, Constellation, Taille, Description]
rasc_data = [
    ["1", "6503", "G", "E", "10.2", "Dragon", "7.1'x2.4'", "Dwarf spiral"], # Summer
    ["2", "6543", "NP", "E", "8.1", "Dragon", "18\"", "Cat's Eye Nebula"], # Summer
    ["3", "6633", "AO", "E", "4.6", "Ophiuchus", "27'", "Italy Cluster"], # Summer
    ["4", "6572", "NP", "E", "8.1", "Ophiuchus", "11\"x9\"", "Emerald Nebula"], # Summer
    ["5", "6369", "NP", "E", "11.4", "Ophiuchus", "28\"", "Little Ghost Nebula"], # Summer
    ["6", "6210", "NP", "E", "8.8", "Hercule", "14\"x11\"", "Turtle Nebula"], # Summer
    ["7", "6207", "G", "E", "11.4", "Hercule", "3.3'x1.2'", "Spiral near M13"], # Summer
    ["8", "6445", "NP", "E", "11.2", "Sagittaire", "34\"", "Box Nebula"], # Summer
    ["9", "6514", "NA", "E", "6.3", "Sagittaire", "28'", "M20 Trifid Nebula"], # Summer
    ["10", "6818", "NP", "E", "9.3", "Sagittaire", "17\"", "Little Gem Nebula"], # Summer
    ["11", "6826", "NP", "E", "8.8", "Cygne", "25\"", "Blinking Planetary"], # Summer
    ["12", "7000", "N", "E", "4.0", "Cygne", "120'x100'", "North America Nebula"], # Summer
    ["13", "6960", "RS", "E", "7.0", "Cygne", "70'x6'", "Western Veil Nebula"], # Summer
    ["14", "6992", "RS", "E", "7.0", "Cygne", "60'x30'", "Eastern Veil Nebula"], # Summer
    ["15", "7009", "NP", "E", "8.0", "Verseau", "28\"", "Saturn Nebula"], # Summer
    ["16", "7293", "NP", "A", "7.3", "Verseau", "18'", "Helix Nebula"], # Autumn
    ["17", "7331", "G", "A", "9.5", "Pégase", "10.5'x3.7'", "Deer Lick Group"], # Autumn
    ["18", "7662", "NP", "A", "8.3", "Andromède", "15\"", "Blue Snowball"], # Autumn
    ["19", "891", "G", "A", "9.9", "Andromède", "13.5'x2.5'", "Outer Limits Galaxy"], # Autumn
    ["20", "253", "G", "A", "7.2", "Sculpteur", "27.5'x6.8'", "Silver Coin Galaxy"], # Autumn
    ["21", "772", "G", "A", "10.3", "Bélier", "7.2'x4.3'", "Spiral galaxy"], # Autumn
    ["22", "1232", "G", "A", "9.8", "Eridan", "7.4'x6.4'", "Face-on spiral"], # Autumn
    ["23", "1365", "G", "H", "9.6", "Fourneau", "11.2'x6.2'", "Great Barred Spiral"], # Winter
    ["24", "1097", "G", "H", "9.5", "Fourneau", "9.3'x6.3'", "Spiral with jets"], # Winter
    ["25", "2022", "NP", "H", "11.6", "Orion", "18\"", "Planetary nebula"], # Winter
    ["26", "1973", "N", "H", "7.0", "Orion", "5'x5'", "Running Man Nebula"], # Winter
    ["27", "2024", "N", "H", "4.0", "Orion", "30'x30'", "Flame Nebula"], # Winter
    ["28", "2194", "AO", "H", "8.5", "Orion", "10'", "Rich open cluster"], # Winter
    ["29", "2359", "N", "H", "11.5", "Grand Chien", "10'x8'", "Thor's Helmet"], # Winter
    ["30", "2362", "AO", "H", "4.1", "Grand Chien", "9'", "Tau Canis Majoris Cluster"], # Winter
    ["31", "2403", "G", "H", "8.2", "Girafe", "21.9'x12.3'", "Spiral galaxy"], # Winter
    ["32", "1501", "NP", "H", "11.5", "Girafe", "52\"", "Oyster Nebula"], # Winter
    ["33", "1502", "AO", "H", "6.9", "Girafe", "20'", "Kemble's Cascade"], # Winter
    ["34", "1535", "NP", "H", "9.6", "Eridan", "18\"", "Cleopatra's Eye"], # Winter
    ["35", "2903", "G", "P", "9.0", "Lion", "12.6'x6.0'", "Bright spiral"], # Spring
    ["36", "3344", "G", "P", "9.7", "Petit Lion", "7.1'x6.5'", "Face-on spiral"], # Spring
    ["37", "3521", "G", "P", "9.0", "Lion", "11'x5'", "Bubble Galaxy"], # Spring
    ["38", "3115", "G", "P", "9.1", "Hydre", "7.2'x2.4'", "Spindle Galaxy"], # Spring
    ["39", "3242", "NP", "P", "7.7", "Hydre", "25\"", "Ghost of Jupiter"], # Spring
    ["40", "4361", "NP", "P", "10.9", "Corbeau", "1.3'", "Planetary nebula"], # Spring
    ["41", "4038", "G", "P", "10.3", "Corbeau", "3.4'x1.7'", "Antennae Galaxies"], # Spring
    ["42", "4565", "G", "P", "9.2", "Chevelure", "15.8'x2.1'", "Needle Galaxy"], # Spring
    ["43", "4559", "G", "P", "10.0", "Chevelure", "10.7'x4.4'", "Spiral galaxy"], # Spring
    ["44", "4494", "G", "P", "9.8", "Chevelure", "4.8'x3.5'", "Elliptical galaxy"], # Spring
    ["45", "4725", "G", "P", "9.1", "Chevelure", "10.7'x7.6'", "One-armed spiral"], # Spring
    ["46", "4631", "G", "P", "9.2", "Ch. Chasse", "15.5'x2.7'", "Whale Galaxy"], # Spring
    ["47", "4656", "G", "P", "10.5", "Ch. Chasse", "15.3'x3.0'", "Hockey Stick Galaxy"], # Spring
    ["48", "4244", "G", "P", "10.4", "Ch. Chasse", "16.6'x1.8'", "Silver Needle Galaxy"], # Spring
    ["49", "4449", "G", "P", "9.4", "Ch. Chasse", "6.2'x4.4'", "Irregular galaxy"], # Spring
    ["50", "5128", "G", "P", "6.7", "Centaure", "25.7'x20'", "Centaurus A"], # Spring
    ["51", "5139", "AG", "P", "3.7", "Centaure", "36'", "Omega Centauri"], # Spring
    ["52", "4945", "G", "P", "8.6", "Centaure", "20'x3.8'", "Spiral galaxy"], # Spring
    ["53", "5457", "G", "P", "7.9", "Grande Ourse", "28.8'", "M101 Pinwheel Galaxy"], # Spring
    ["54", "3077", "G", "H", "10.0", "Grande Ourse", "5.4'x4.5'", "M81 companion"], # Winter
    ["55", "3628", "G", "P", "9.5", "Lion", "14.8'x3.0'", "Hamburger Galaxy"], # Spring
    ["56", "3384", "G", "P", "9.9", "Lion", "5.9'x2.6'", "Elliptical galaxy"], # Spring
    ["57", "3607", "G", "P", "9.9", "Lion", "4.9'x2.5'", "Elliptical galaxy"], # Spring
    ["58", "4088", "G", "P", "10.3", "Grande Ourse", "5.8'x2.2'", "Distorted spiral"], # Spring
    ["59", "4217", "G", "P", "11.2", "Grande Ourse", "5.1'x1.5'", "Edge-on spiral"], # Spring
    ["60", "4605", "G", "P", "10.1", "Grande Ourse", "5.8'x2.2'", "Spiral galaxy"], # Spring
    ["61", "5195", "G", "P", "9.6", "Ch. Chasse", "5.4'x4.3'", "M51 companion"], # Spring
    ["62", "5466", "AG", "P", "9.1", "Bouvier", "9'", "Loose globular cluster"], # Spring
    ["63", "4027", "G", "P", "11.0", "Corbeau", "3.2'x2.4'", "Barred spiral"], # Spring
    ["64", "4753", "G", "P", "10.0", "Vierge", "6.0'x2.8'", "Lenticular galaxy"], # Spring
    ["65", "4762", "G", "P", "10.3", "Vierge", "8.7'x1.7'", "Edge-on lenticular"], # Spring
    ["66", "5248", "G", "P", "10.3", "Bouvier", "6.2'x4.5'", "Spiral galaxy"], # Spring
    ["67", "5746", "G", "P", "10.3", "Vierge", "7.4'x1.3'", "Edge-on spiral"], # Spring
    ["68", "6171", "AG", "E", "7.8", "Ophiuchus", "10'", "M107 Globular Cluster"], # Summer
    ["69", "6235", "AG", "E", "10.0", "Ophiuchus", "5'", "Small globular"], # Summer
    ["70", "6284", "AG", "E", "8.9", "Ophiuchus", "6.2'", "Globular cluster"], # Summer
    ["71", "6287", "AG", "E", "9.3", "Ophiuchus", "4.8'", "Globular cluster"], # Summer
    ["72", "6293", "AG", "E", "8.2", "Ophiuchus", "8.2'", "Globular cluster"], # Summer
    ["73", "6304", "AG", "E", "8.2", "Ophiuchus", "8'", "Globular cluster"], # Summer
    ["74", "6316", "AG", "E", "8.1", "Ophiuchus", "5.4'", "Globular cluster"], # Summer
    ["75", "6342", "AG", "E", "9.5", "Ophiuchus", "4.4'", "Globular cluster"], # Summer
    ["76", "6355", "AG", "E", "8.6", "Ophiuchus", "4.2'", "Globular cluster"], # Summer
    ["77", "6356", "AG", "E", "8.2", "Ophiuchus", "10'", "Globular cluster"], # Summer
    ["78", "6362", "AG", "E", "8.1", "Autel", "15'", "Globular cluster"], # Summer
    ["79", "6388", "AG", "E", "6.8", "Scorpion", "10.4'", "Globular cluster"], # Summer
    ["80", "6401", "AG", "E", "7.4", "Ophiuchus", "12'", "Globular cluster"], # Summer
    ["81", "6517", "AG", "E", "10.1", "Ophiuchus", "4.3'", "Globular cluster"], # Summer
    ["82", "6539", "AG", "E", "8.9", "Serpent", "7.9'", "Globular cluster"], # Summer
    ["83", "6624", "AG", "E", "7.6", "Sagittaire", "8.8'", "Globular cluster"], # Summer
    ["84", "6638", "AG", "E", "9.2", "Sagittaire", "7.3'", "Globular cluster"], # Summer
    ["85", "6642", "AG", "E", "8.9", "Sagittaire", "4.8'", "Globular cluster"], # Summer
    ["86", "6652", "AG", "E", "8.5", "Sagittaire", "6'", "Globular cluster"], # Summer
    ["87", "6712", "AG", "E", "8.1", "Ecu", "9.8'", "Globular cluster"], # Summer
    ["88", "6723", "AG", "E", "6.8", "Sagittaire", "13'", "Globulaire cluster"], # Summer
    ["89", "6752", "AG", "E", "5.4", "Paon", "29'", "Great Peacock Globular"], # Summer
    ["90", "6809", "AG", "E", "6.3", "Sagittaire", "19'", "M55 Globular Cluster"], # Summer
    ["91", "6934", "AG", "A", "8.9", "Dauphin", "7.1'", "Globular cluster"], # Autumn
    ["92", "7006", "AG", "A", "10.6", "Dauphin", "3.6'", "Distant globular"], # Autumn
    ["93", "7492", "AG", "A", "11.2", "Verseau", "6.2'", "Globular cluster"], # Autumn
    ["94", "246", "NP", "A", "10.9", "Baleine", "3.8'", "Skull Nebula"], # Autumn
    ["95", "1535", "NP", "H", "9.6", "Eridan", "18\"", "Cleopatra's Eye"], # Winter
    ["96", "2371", "NP", "H", "11.2", "Gémeaux", "54\"", "Double Bubble Nebula"], # Winter
    ["97", "2392", "NP", "H", "9.1", "Gémeaux", "45\"", "Eskimo Nebula"], # Winter
    ["98", "2438", "NP", "H", "10.8", "Poupe", "1.1'", "Planetary in M46"], # Winter
    ["99", "2440", "NP", "H", "9.4", "Poupe", "1.3'", "Planetary nebula"], # Winter
    ["100", "3132", "NP", "P", "9.2", "Voiles", "1.4'", "Eight-Burst Nebula"], # Spring
    ["101", "40", "NP", "A", "12.3", "Céphée", "38\"", "Bow-Tie Nebula"], # Autumn
    ["102", "7635", "N", "A", "10.0", "Cassiopée", "15'x8'", "Bubble Nebula"], # Autumn
    ["103", "7538", "N", "A", "11.0", "Céphée", "10'x7'", "Emission nebula"], # Autumn
    ["104", "147", "G", "A", "9.5", "Cassiopée", "13'x8'", "Dwarf spheroid"], # Autumn
    ["105", "185", "G", "A", "9.2", "Cassiopée", "11'x10'", "Dwarf spheroid"], # Autumn
    ["106", "404", "G", "A", "10.3", "Andromède", "3.5'x3.5'", "Mirach's Ghost"], # Autumn
    ["107", "6946", "G", "A", "9.0", "Céphée", "11.5'x11.5'", "Fireworks Galaxy"], # Autumn
    ["108", "1023", "G", "A", "9.4", "Persée", "7.4'x2.5'", "Lenticular galaxy"], # Autumn
    ["109", "1275", "G", "H", "11.9", "Persée", "2.2'x1.7'", "Perseus A"], # Winter
    ["110", "6781", "NP", "E", "11.4", "Aigle", "1.8'", "Planetary nebula"] # Summer
]

# --- CODE ---
lang = 'fr'

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
        if fname:
            imaged_count += 1
            meta["date"], meta["file"] = get_image_info(os.path.join(img_dir, fname))
        
        decoded_item = list(item)
        decoded_item[2] = type_map.get(item[2], item[2])
        decoded_item[3] = season_map.get(item[3], item[3])
        entries.append((decoded_item, fname, meta))

    html = f"""<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8"><title>{t['title']}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0f0f0f; color: #e0e0e0; margin: 0; padding: 20px; }}
        header {{ text-align: center; margin-bottom: 20px; }}
        .score {{ color: #888; font-size: 0.6em; }}
        
        /* Filtres */
        .filter-bar {{ text-align: center; margin-bottom: 30px; }}
        .filter-btn {{ background: #252525; border: 1px solid #444; color: #aaa; padding: 8px 16px; margin: 0 4px; border-radius: 20px; cursor: pointer; transition: 0.2s; }}
        .filter-btn:hover {{ border-color: #4dabf7; color: #fff; }}
        .filter-btn.active {{ background: #4dabf7; color: #fff; border-color: #4dabf7; }}

        .container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax({CARD_SIZE_MIN}, 1fr)); gap: 20px; }}
        .card {{ background: #1e1e1e; border-radius: 8px; border: 1px solid #333; overflow: hidden; transition: 0.2s; display: block; }}
        .card:hover {{ transform: scale(1.03); border-color: #4dabf7; }}
        .img-box {{ width: 100%; aspect-ratio: 1 / 1; background: #2c2c2c; display: flex; justify-content: center; align-items: center; cursor: pointer; }}
        .card img {{ width: 100%; height: 100%; object-fit: cover; }}
        .placeholder {{ text-align: center; color: #666; font-size: 0.8em; }}
        .title {{ background: #252525; padding: 10px; text-align: center; font-weight: bold; font-size: 0.85em; }}
        .title a {{ color: #fff; text-decoration: none; }}
        
        #tooltip {{ position: fixed; display: none; background: rgba(20,20,20,0.98); border: 1px solid #4dabf7; padding: 12px; border-radius: 6px; z-index: 2000; pointer-events: none; font-size: 0.85em; box-shadow: 0 4px 15px #000; min-width: 200px; }}
        .lbl {{ color: #4dabf7; font-weight: bold; margin-right: 5px; }}
        #modal {{ display: none; position: fixed; z-index: 3000; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); cursor: grab; }}
        #modal-img {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 95%; max-height: 95%; }}
    </style></head><body>
    <header>
        <h1>{t['title']}<br><span class="score">({imaged_count}/110)</span></h1>
    </header>

    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterS('all', this)">{t['all']}</button>
        <button class="filter-btn" onclick="filterS('Printemps', this)">Printemps</button>
        <button class="filter-btn" onclick="filterS('Été', this)">Été</button>
        <button class="filter-btn" onclick="filterS('Automne', this)">Automne</button>
        <button class="filter-btn" onclick="filterS('Hiver', this)">Hiver</button>
    </div>

    <div class="container" id="main-grid">"""

    for item, filename, meta in entries:
        r_id, n_id, o_type, o_season, mag, const, size, desc = item
        data = f'data-type="{o_type}" data-season="{o_season}" data-const="{const}" data-mag="{mag}" data-size="{size}" data-desc="{desc}" data-date="{meta["date"]}" data-file="{meta["file"]}"'
        html += f"""<div class="card" {data} onmousemove="showT(event, this)" onmouseleave="hideT()">
            <div class="img-box" {"onclick='openM(\""+filename+"\")'" if filename else ""}>
                {f'<img src="{filename}">' if filename else f'<div class="placeholder">{o_type}<br>{o_season}</div>'}
            </div>
            <div class="title">RASC {r_id} - <a href="https://telescopius.com/deep-sky-objects/ngc-{n_id.lower()}" target="_blank">NGC {n_id}</a></div>
        </div>"""

    html += f"""</div><div id="tooltip"></div><div id="modal" onclick="closeM()"><img id="modal-img"></div>
    <script>
        // Logique de filtrage
        function filterS(season, btn) {{
            const cards = document.querySelectorAll('.card');
            const btns = document.querySelectorAll('.filter-btn');
            
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            cards.forEach(card => {{
                if (season === 'all' || card.getAttribute('data-season') === season) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        const tt = document.getElementById('tooltip');
        function showT(e, el) {{
            const d = el.dataset;
            let c = d.file ? `<div style="border-bottom:1px solid #444;margin-bottom:8px;padding-bottom:5px;"><div style="color:#4dabf7;font-weight:bold;font-family:monospace;">${{d.file}}</div><div style="color:#aaa;font-style:italic;font-size:0.9em;">{t['date']}: ${{d.date}}</div></div>` : "";
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
        function openM(s) {{ if(!s) return; m.style.display="block"; mi.src=s; }}
        function closeM() {{ m.style.display="none"; }}
    </script></body></html>"""

    with open(out_file, "w", encoding="utf-8") as f: f.write(html)
    print(f"Catalogue généré avec filtres : {out_file}")

if __name__ == "__main__":
    generate_catalog()

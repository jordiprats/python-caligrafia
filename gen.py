#!/usr/bin/env python3
"""
Calligraphy Practice PDF Generator
Generates A4 PDFs with random Catalan sentences for calligraphy practice
"""

import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import argparse
import os
import base64

# Collection of Catalan sentences for calligraphy practice
CATALAN_SENTENCES = [
    "La pau comença amb un somriure.",
    "El temps és or, però l'amistat és un tresor.",
    "Cada dia és una nova oportunitat.",
    "La paciència és la clau de l'èxit.",
    "El coneixement és poder.",
    "La bellesa està en els petits detalls.",
    "Un viatge de mil llegües comença amb un pas.",
    "L'amor és l'idioma universal.",
    "Aprendre és créixer cada dia.",
    "La natura ens ensenya la perfecció.",
    "Els somnis són el motor del futur.",
    "La música alimenta l'esperit.",
    "Cada esforç té la seva recompensa.",
    "La felicitat és un camí, no un destí.",
    "L'alegria compartida es multiplica.",
    "El silenci també és una resposta.",
    "La humilitat és signe de grandesa.",
    "Les paraules tenen poder i màgia.",
    "Barcelona és una ciutat meravellosa.",
    "El Mediterrani banya les nostres costes.",
    "La tramuntana bufa amb força.",
    "Les muntanyes de Montserrat són sagrades.",
    "El pa amb tomàquet és deliciós.",
    "La sardana és la nostra dansa tradicional.",
    "Sant Jordi és la festa dels llibres.",
    "Els castellers demostren força i equilibri.",
    "La Rambla és plena de vida.",
    "El Modernisme marca la ciutat.",
    "Catalunya és una nació amb història pròpia.",
    "Volem ser lliures i sobirans.",
    "Independència per construir el nostre futur.",
    "Som una nació sense estat propi.",
    "El poble català té dret a l'autodeterminació.",
    "Lluitarem pacíficament pels nostres drets.",
    "La nostra llengua és senyal d'identitat.",
    "El diàleg és l'eina de la pau.",
    "Junts som més forts i units.",
    "República catalana, somni de molts.",
    "Treballem per un país millor per a tothom.",
]


# Base64 encoded Dancing Script font (cursive/script style)
# This is a lightweight cursive font perfect for calligraphy practice
DANCING_SCRIPT_FONT_B64 = None  # Will use fallback

def setup_cursive_font():
    """Try to setup a cursive/script font for calligraphy"""
    # Priority: Educational fonts for children (Playwrite), then simple cursive fonts
    # Playwrite fonts are specifically designed for teaching handwriting to children
    cursive_fonts = [
        # Playwrite fonts - Educational (best for children)
        # Check both variable and static versions
        '/Library/Fonts/PlaywriteES-VariableFont_wght.ttf',
        os.path.expanduser('~/Library/Fonts/PlaywriteES-VariableFont_wght.ttf'),
        '/Library/Fonts/PlaywriteES-Regular.ttf',
        os.path.expanduser('~/Library/Fonts/PlaywriteES-Regular.ttf'),
        # Static versions in subdirectories
        '/Library/Fonts/static/PlaywriteES-Regular.ttf',
        os.path.expanduser('~/Library/Fonts/static/PlaywriteES-Regular.ttf'),
        # Other Playwrite variants
        '/Library/Fonts/PlaywriteUSModern-VariableFont_wght.ttf',
        os.path.expanduser('~/Library/Fonts/PlaywriteUSModern-VariableFont_wght.ttf'),
        '/Library/Fonts/PlaywriteUSTrad-VariableFont_wght.ttf',
        os.path.expanduser('~/Library/Fonts/PlaywriteUSTrad-VariableFont_wght.ttf'),
        # Simple cursive fonts from Google Fonts (good for children)
        '/Library/Fonts/GreatVibes-Regular.ttf',
        os.path.expanduser('~/Library/Fonts/GreatVibes-Regular.ttf'),
        '/Library/Fonts/Allura-Regular.ttf',
        os.path.expanduser('~/Library/Fonts/Allura-Regular.ttf'),
        '/Library/Fonts/Pacifico-Regular.ttf',
        os.path.expanduser('~/Library/Fonts/Pacifico-Regular.ttf'),
        '/Library/Fonts/DancingScript-Regular.ttf',
        os.path.expanduser('~/Library/Fonts/DancingScript-Regular.ttf'),
        '/Library/Fonts/DancingScript-VariableFont_wght.ttf',
        os.path.expanduser('~/Library/Fonts/DancingScript-VariableFont_wght.ttf'),
        '/Library/Fonts/LeagueScript-Regular.ttf',
        os.path.expanduser('~/Library/Fonts/LeagueScript-Regular.ttf'),
        # System fonts (fallback)
        '/usr/share/fonts/truetype/ubuntu/Ubuntu-Italic.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf',
    ]
    
    for font_path in cursive_fonts:
        if os.path.exists(font_path):
            try:
                font_name = os.path.basename(font_path).replace('.ttf', '')
                pdfmetrics.registerFont(TTFont('CursiveFont', font_path))
                print(f"✓ Font cursiva carregada: {font_name}")
                return 'CursiveFont'
            except Exception as e:
                # Debug: show which font failed
                # print(f"  No es pot carregar {font_name}: {e}")
                continue
    
    # Fallback: Use Helvetica-Oblique which is always available in reportlab
    print("⚠ No s'ha trobat cap font cursiva instal·lada.")
    print("  Utilitzant Helvetica-Oblique com a font per defecte.")
    print("\n  Per millorar la qualitat, instal·la una d'aquestes fonts:")
    print("  - Playwrite ES: https://fonts.google.com/specimen/Playwrite+ES")
    print("  - Great Vibes: https://fonts.google.com/specimen/Great+Vibes")
    print("  - Allura: https://fonts.google.com/specimen/Allura")
    return 'Helvetica-Oblique'


def draw_practice_line(c, y_position, page_width):
    """Draw a single practice line for writing"""
    margin = 20 * mm
    
    # Main writing line (solid black)
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(margin, y_position, page_width - margin, y_position)
    
    # Small starting mark to show where to begin
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.setLineWidth(1.5)
    c.line(margin, y_position - 2*mm, margin, y_position + 2*mm)


def draw_dotted_guide(c, sentence, y_position, page_width, cursive_font='Helvetica-Oblique'):
    """Draw a dotted/light gray version of the sentence as a tracing guide"""
    margin = 20 * mm
    
    # Draw the sentence in very light gray for tracing
    c.setFillColorRGB(0.7, 0.7, 0.7)  # Light gray for tracing
    
    c.setFont(cursive_font, 13)
    
    # Draw the sentence with baseline sitting exactly ON the line (y_position)
    # The y_position IS the baseline, so we draw at y_position directly
    c.drawString(margin, y_position, sentence)


def draw_sentence_header(c, sentence, y_position, page_width, cursive_font='ZapfChancery-MediumItalic'):
    """Draw a sentence as an example to copy"""
    margin = 20 * mm
    
    # Draw "Model:" label
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y_position, "Model:")
    
    # Draw the sentence in cursive/script font (lletra lligada)
    c.setFillColorRGB(0, 0, 0)
    c.setFont(cursive_font, 13)
    c.drawString(margin + 15*mm, y_position, sentence)


def generate_calligraphy_pdf(filename, num_pages=5, lines_per_sentence=3, line_spacing=12, use_cursive_font=True):
    """
    Generate a PDF with calligraphy practice lines
    
    Args:
        filename: Output PDF filename
        num_pages: Number of pages to generate
        lines_per_sentence: Number of practice lines per sentence
        line_spacing: Spacing between practice lines in mm
        use_cursive_font: Whether to use cursive font (lletra lligada)
    """
    # Setup cursive font
    cursive_font = 'ZapfChancery-MediumItalic'  # Default fallback
    if use_cursive_font:
        cursive_font = setup_cursive_font()
    
    page_width, page_height = A4
    c = canvas.Canvas(filename, pagesize=A4)
    
    line_spacing_mm = line_spacing * mm
    sentence_spacing = 20 * mm  # Space between different sentence blocks
    top_margin = 20 * mm
    bottom_margin = 20 * mm
    
    # Create a shuffled copy of sentences to use without repetition
    available_sentences = CATALAN_SENTENCES.copy()
    random.shuffle(available_sentences)
    sentence_index = 0
    
    for page in range(num_pages):
        y_position = page_height - top_margin
        
        # Add title on first page
        if page == 0:
            c.setFont("Helvetica-Bold", 16)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(page_width / 2, y_position, "Pràctica de Cal·ligrafia")
            y_position -= 15 * mm
        
        # Draw sentences with practice lines
        while y_position > bottom_margin + (lines_per_sentence * line_spacing_mm) + sentence_spacing:
            # Get next sentence from shuffled list
            sentence = available_sentences[sentence_index % len(available_sentences)]
            sentence_index += 1
            
            # If we've used all sentences, reshuffle and start over
            if sentence_index % len(available_sentences) == 0:
                random.shuffle(available_sentences)
            
            # Draw the model sentence
            y_position -= 8 * mm
            draw_sentence_header(c, sentence, y_position, page_width, cursive_font)
            
            # Draw multiple practice lines for this sentence
            y_position -= 10 * mm
            for i in range(lines_per_sentence):
                draw_practice_line(c, y_position, page_width)
                
                # On the first line, add dotted guide text to trace
                if i == 0:
                    draw_dotted_guide(c, sentence, y_position, page_width, cursive_font)
                
                y_position -= line_spacing_mm
            
            # Add space before next sentence
            y_position -= (sentence_spacing - line_spacing_mm)
        
        # Add page number at bottom
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawCentredString(page_width / 2, 10 * mm, f"Pàgina {page + 1} de {num_pages}")
        
        if page < num_pages - 1:
            c.showPage()
    
    c.save()
    print(f"PDF generat: {filename}")
    print(f"  - Pàgines: {num_pages}")
    print(f"  - Línies per frase: {lines_per_sentence}")
    print(f"  - Espaiat entre línies: {line_spacing} mm")
    print(f"  - Total frases úniques: {min(sentence_index, len(CATALAN_SENTENCES))}")
    print(f"  - Font lletra lligada: {cursive_font if use_cursive_font else 'No'}")


def main():
    parser = argparse.ArgumentParser(
        description="Genera un PDF A4 per practicar cal·ligrafia amb frases en català"
    )
    parser.add_argument(
        "-o", "--output",
        default="calligrafia_practica.pdf",
        help="Nom del fitxer PDF de sortida (per defecte: calligrafia_practica.pdf)"
    )
    parser.add_argument(
        "-p", "--pages",
        type=int,
        default=5,
        help="Nombre de pàgines (per defecte: 5)"
    )
    parser.add_argument(
        "-l", "--lines",
        type=int,
        default=3,
        help="Nombre de línies per practicar cada frase (per defecte: 3)"
    )
    parser.add_argument(
        "-s", "--spacing",
        type=int,
        default=12,
        help="Espaiat entre línies de pràctica en mm (per defecte: 12)"
    )
    parser.add_argument(
        "--no-cursive",
        action="store_true",
        help="No utilitzar font de lletra lligada"
    )
    parser.add_argument(
        "--find-fonts",
        action="store_true",
        help="Mostra on buscar les fonts instal·lades i surt"
    )
    
    args = parser.parse_args()
    
    # Debug mode: find installed fonts
    if args.find_fonts:
        print("🔍 Cercant fonts instal·lades...\n")
        font_dirs = [
            '/Library/Fonts',
            os.path.expanduser('~/Library/Fonts'),
        ]
        
        for font_dir in font_dirs:
            print(f"📁 Buscant a: {font_dir}")
            if os.path.exists(font_dir):
                try:
                    files = os.listdir(font_dir)
                    playwrite = [f for f in files if 'Playwrite' in f or 'playwrite' in f]
                    cursive = [f for f in files if any(x in f for x in ['Great', 'Allura', 'Dancing', 'Pacifico'])]
                    
                    if playwrite:
                        print("  ✓ Fonts Playwrite trobades:")
                        for f in playwrite:
                            print(f"    - {f}")
                    
                    if cursive:
                        print("  ✓ Fonts cursives trobades:")
                        for f in cursive:
                            print(f"    - {f}")
                    
                    if not playwrite and not cursive:
                        print("  ✗ No s'han trobat fonts cursives")
                except Exception as e:
                    print(f"  ✗ Error llegint directori: {e}")
            else:
                print(f"  ✗ Directori no existeix")
            print()
        
        print("💡 Si has instal·lat Playwrite ES però no apareix:")
        print("   1. Obre Font Book")
        print("   2. Selecciona la font Playwrite ES")
        print("   3. Mira a File > Show Font Info per veure la ubicació")
        print("   4. Si està en un subdirectori, mou-la a ~/Library/Fonts/")
        return
    
    generate_calligraphy_pdf(
        filename=args.output,
        num_pages=args.pages,
        lines_per_sentence=args.lines,
        line_spacing=args.spacing,
        use_cursive_font=not args.no_cursive
    )


if __name__ == "__main__":
    main()
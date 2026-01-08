#!/usr/bin/env python3
"""
Calligraphy Practice PDF Generator
Generates A4 PDFs with random Catalan sentences for calligraphy practice
"""

import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import argparse

# Collection of Catalan sentences for calligraphy practice
CATALAN_SENTENCES = [
    "La pau comença amb un somriure.",
    "El temps és or, però l'amistat és un tresor.",
    "Cada dia és una nova oportunitat.",
    "L'art és l'expressió de l'ànima.",
    "La paciència és la clau de l'èxit.",
    "El coneixement és poder.",
    "La bellesa està en els petits detalls.",
    "Un viatge de mil llegües comença amb un pas.",
    "La vida és bella quan comparteixes moments.",
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
]


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


def draw_sentence_header(c, sentence, y_position, page_width):
    """Draw a sentence as an example to copy"""
    margin = 20 * mm
    
    # Draw "Model:" label
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y_position, "Model:")
    
    # Draw the sentence in a clear, readable font
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 11)
    c.drawString(margin + 15*mm, y_position, sentence)


def generate_calligraphy_pdf(filename, num_pages=5, lines_per_sentence=3, line_spacing=12):
    """
    Generate a PDF with calligraphy practice lines
    
    Args:
        filename: Output PDF filename
        num_pages: Number of pages to generate
        lines_per_sentence: Number of practice lines per sentence
        line_spacing: Spacing between practice lines in mm
    """
    page_width, page_height = A4
    c = canvas.Canvas(filename, pagesize=A4)
    
    line_spacing_mm = line_spacing * mm
    sentence_spacing = 20 * mm  # Space between different sentence blocks
    top_margin = 20 * mm
    bottom_margin = 20 * mm
    
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
            # Get a random sentence
            sentence = random.choice(CATALAN_SENTENCES)
            
            # Draw the model sentence
            y_position -= 8 * mm
            draw_sentence_header(c, sentence, y_position, page_width)
            
            # Draw multiple practice lines for this sentence
            y_position -= 10 * mm
            for i in range(lines_per_sentence):
                draw_practice_line(c, y_position, page_width)
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
    
    args = parser.parse_args()
    
    generate_calligraphy_pdf(
        filename=args.output,
        num_pages=args.pages,
        lines_per_sentence=args.lines,
        line_spacing=args.spacing
    )


if __name__ == "__main__":
    main()
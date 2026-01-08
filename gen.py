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


def draw_guidelines(c, y_position, line_height, width, page_width, page_height):
    """Draw calligraphy practice guidelines"""
    margin = 20 * mm
    
    # Base line (solid)
    c.setStrokeColorRGB(0.3, 0.3, 0.3)
    c.setLineWidth(0.5)
    c.line(margin, y_position, page_width - margin, y_position)
    
    # Top line (solid)
    c.line(margin, y_position + line_height, page_width - margin, y_position + line_height)
    
    # Middle dotted line (x-height)
    c.setDash(2, 3)
    c.setStrokeColorRGB(0.6, 0.6, 0.6)
    c.line(margin, y_position + line_height * 0.5, page_width - margin, y_position + line_height * 0.5)
    
    # Ascender line (dotted)
    c.line(margin, y_position + line_height * 0.75, page_width - margin, y_position + line_height * 0.75)
    
    # Descender line (dotted)
    c.line(margin, y_position - line_height * 0.25, page_width - margin, y_position - line_height * 0.25)
    
    c.setDash()  # Reset to solid line


def draw_sentence(c, sentence, y_position, line_height, page_width):
    """Draw a sentence above the guidelines in light gray"""
    margin = 20 * mm
    
    c.setFillColorRGB(0.8, 0.8, 0.8)
    c.setFont("Helvetica", 10)
    c.drawString(margin, y_position + line_height + 3, sentence)


def generate_calligraphy_pdf(filename, num_pages=5, line_height=15, spacing=25):
    """
    Generate a PDF with calligraphy practice lines
    
    Args:
        filename: Output PDF filename
        num_pages: Number of pages to generate
        line_height: Height of each practice line in mm
        spacing: Spacing between practice line sets in mm
    """
    page_width, page_height = A4
    c = canvas.Canvas(filename, pagesize=A4)
    
    line_height_mm = line_height * mm
    spacing_mm = spacing * mm
    top_margin = 20 * mm
    bottom_margin = 20 * mm
    
    for page in range(num_pages):
        y_position = page_height - top_margin - line_height_mm
        
        # Add title on first page
        if page == 0:
            c.setFont("Helvetica-Bold", 16)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(page_width / 2, page_height - 15 * mm, "Pràctica de Cal·ligrafia")
            y_position -= 10 * mm
        
        # Draw practice lines with sentences
        while y_position > bottom_margin + line_height_mm:
            # Get a random sentence
            sentence = random.choice(CATALAN_SENTENCES)
            
            # Draw the sentence above the guidelines
            draw_sentence(c, sentence, y_position, line_height_mm, page_width)
            
            # Draw the guidelines
            draw_guidelines(c, y_position, line_height_mm, page_width, page_width, page_height)
            
            # Move down for next line set
            y_position -= (line_height_mm + spacing_mm)
        
        # Add page number at bottom
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawCentredString(page_width / 2, 10 * mm, f"Pàgina {page + 1} de {num_pages}")
        
        if page < num_pages - 1:
            c.showPage()
    
    c.save()
    print(f"PDF generat: {filename}")
    print(f"  - Pàgines: {num_pages}")
    print(f"  - Alçada de línia: {line_height} mm")
    print(f"  - Espaiat: {spacing} mm")


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
        "-l", "--line-height",
        type=int,
        default=15,
        help="Alçada de cada línia en mm (per defecte: 15)"
    )
    parser.add_argument(
        "-s", "--spacing",
        type=int,
        default=25,
        help="Espaiat entre línies en mm (per defecte: 25)"
    )
    
    args = parser.parse_args()
    
    generate_calligraphy_pdf(
        filename=args.output,
        num_pages=args.pages,
        line_height=args.line_height,
        spacing=args.spacing
    )


if __name__ == "__main__":
    main()
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Preformatted, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (on page > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "SCSE3040 — Machine Learning Operations | Practical 05 Submission")
            self.drawRightString(612 - 54, 750, "Divakar Maurya (S24CSEU0807)")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, page_str)
        self.drawString(54, 36, "Bennett University — School of Computer Science Engineering & Technology")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 612 - 54, 48)
        
        self.restoreState()


def create_submission_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1A365D')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#4A5568')
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748')
    )

    link_style = ParagraphStyle(
        'RepoLink',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1D4ED8')
    )

    table_label_style = ParagraphStyle(
        'TableLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#2D3748')
    )

    table_val_style = ParagraphStyle(
        'TableValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1A202C')
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1A202C')
    )

    elements = []

    # Title & Header
    elements.append(Paragraph("SCSE3040: Machine Learning Operations (MLOps)", title_style))
    elements.append(Paragraph("Practical 05 — Settings in a File, Bugs Caught by a Robot (Laboratory Submission)", subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceBefore=2, spaceAfter=10))

    # 1. Student & Lab Session Details
    elements.append(Paragraph("1. Student & Laboratory Session Details", section_heading))
    
    student_table_data = [
        [Paragraph("Student Name:", table_label_style), Paragraph("Divakar Maurya", table_val_style),
         Paragraph("Batch:", table_label_style), Paragraph("EB31", table_val_style)],
        [Paragraph("Roll Number:", table_label_style), Paragraph("S24CSEU0807", table_val_style),
         Paragraph("Lab Date:", table_label_style), Paragraph("04 October 2026", table_val_style)],
        [Paragraph("Course:", table_label_style), Paragraph("SCSE3040 — Machine Learning Operations", table_val_style),
         Paragraph("Practical:", table_label_style), Paragraph("P05 (L08 / CO3)", table_val_style)]
    ]

    col_widths = [85, 170, 75, 180]
    t = Table(student_table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 10))

    # 2. Repository Link
    elements.append(Paragraph("2. Repository Link", section_heading))
    repo_url = "https://github.com/div339175/P05-config-tests"
    elements.append(Paragraph(
        f'<font color="#1A202C">Full GitHub Repository URL: </font><a href="{repo_url}"><font color="#1D4ED8"><u><b>{repo_url}</b></u></font></a>',
        link_style
    ))
    elements.append(Spacer(1, 10))

    # 3. Contents of config.yaml
    elements.append(Paragraph("3. Contents of config.yaml", section_heading))
    
    with open("work/config.yaml", "r", encoding="utf-8") as f:
        yaml_text = f.read()

    # Format yaml text with safe xml escapes
    yaml_lines = yaml_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    yaml_table_data = [[Paragraph(yaml_lines.replace('\n', '<br/>'), code_style)]]
    yaml_table = Table(yaml_table_data, colWidths=[510])
    yaml_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(yaml_table)
    elements.append(Spacer(1, 12))

    # 4. Terminal Screenshot
    elements.append(Paragraph("4. Terminal Output (pytest Test Suite Execution)", section_heading))
    elements.append(Paragraph("Terminal session running pytest inside the <font face='Courier'>work/</font> directory showing all unit and behavioural tests passing:", body_style))
    elements.append(Spacer(1, 6))

    # Terminal screenshot image
    img_path = "terminal_screenshot_clean.png"
    if os.path.exists(img_path):
        # original size is 900x630
        disp_width = 510
        disp_height = 510 * (630 / 900)
        img = Image(img_path, width=disp_width, height=disp_height)
        elements.append(img)
    elements.append(Spacer(1, 12))

    # 5. Model Output Comparison (One Line)
    elements.append(Paragraph("5. Model Performance Comparison Before &amp; After Refactor", section_heading))
    statement = (
        "<b>Comparison:</b> Before the refactor (hardcoded values in script), the package produced a test Mean Absolute Error "
        "(MAE) of <b>1.92 minutes</b>, and after refactoring settings into <font face='Courier'>config.yaml</font>, it produces "
        "identically <b>1.92 minutes</b> (and <b>2.18 minutes</b> when constrained to <font face='Courier'>max_rows: 300</font> in Task T1)."
    )
    elements.append(Paragraph(statement, body_style))
    elements.append(Spacer(1, 12))

    # 6. AI Use Disclosure
    elements.append(Paragraph("6. AI Use Disclosure", section_heading))
    disclosure = "None"
    elements.append(Paragraph(f"<b>Disclosure:</b> {disclosure}", body_style))

    # Build document
    doc.build(elements, canvasmaker=NumberedCanvas)
    print("PDF build finished successfully!")

if __name__ == "__main__":
    create_submission_pdf("S24CSEU0807_p05.pdf")

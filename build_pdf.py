import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Preformatted, PageBreak, HRFlowable
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
            self.drawString(50, 752, "SCSE3040 — Machine Learning Operations | Practical 05")
            self.drawRightString(612 - 50, 752, "Divakar Maurya (S24CSEU0807) | Batch EB31")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(50, 745, 612 - 50, 745)
            
        # Footer (on all pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 50, 32, page_str)
        self.drawString(50, 32, "Bennett University — School of Computer Science Engineering & Technology")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(50, 42, 612 - 50, 42)
        
        self.restoreState()


def create_submission_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=45,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0F172A')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569')
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=8,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155')
    )

    link_style = ParagraphStyle(
        'RepoLink',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1D4ED8')
    )

    table_label_style = ParagraphStyle(
        'TableLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )

    table_val_style = ParagraphStyle(
        'TableValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0F172A')
    )

    elements = []

    # ==================== PAGE 1 ====================
    # Title & Header
    elements.append(Paragraph("SCSE3040: Machine Learning Operations (MLOps)", title_style))
    elements.append(Paragraph("Practical 05: Settings in a File, Bugs Caught by a Robot — Lab Report", subtitle_style))
    elements.append(Spacer(1, 4))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=2, spaceAfter=8))

    # 1. Student & Laboratory Session Details
    elements.append(Paragraph("1. Student &amp; Laboratory Session Details", section_heading))
    
    student_table_data = [
        [Paragraph("Student Name:", table_label_style), Paragraph("Divakar Maurya", table_val_style),
         Paragraph("Batch:", table_label_style), Paragraph("EB31", table_val_style)],
        [Paragraph("Roll Number:", table_label_style), Paragraph("S24CSEU0807", table_val_style),
         Paragraph("Date of Lab Session:", table_label_style), Paragraph("04 October 2026", table_val_style)],
        [Paragraph("Course Name:", table_label_style), Paragraph("SCSE3040 — Machine Learning Operations", table_val_style),
         Paragraph("Academic Session:", table_label_style), Paragraph("2026–2027 (Session L08 / CO3)", table_val_style)]
    ]

    col_widths = [90, 165, 110, 145]
    t = Table(student_table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 8))

    # 2. Repository Link
    elements.append(Paragraph("2. Repository Link", section_heading))
    repo_url = "https://github.com/div339175/P05-config-tests"
    elements.append(Paragraph(
        f'<font color="#334155">Full Repository URL: </font><a href="{repo_url}"><font color="#1D4ED8"><u><b>{repo_url}</b></u></font></a>',
        link_style
    ))
    elements.append(Spacer(1, 8))

    # 3. Contents of config.yaml
    elements.append(Paragraph("3. Contents of config.yaml (Pasted as Text)", section_heading))
    
    with open("work/config.yaml", "r", encoding="utf-8") as f:
        yaml_text = f.read().strip()

    # Format yaml text with safe xml escapes
    yaml_lines = yaml_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    yaml_table_data = [[Paragraph(yaml_lines.replace('\n', '<br/>'), code_style)]]
    yaml_table = Table(yaml_table_data, colWidths=[510])
    yaml_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    elements.append(yaml_table)
    
    # PageBreak to cleanly start Section 4 on Page 2
    elements.append(PageBreak())

    # ==================== PAGE 2 ====================
    # 4. Terminal Screenshot
    elements.append(Paragraph("4. Terminal Screenshot (pytest Test Suite Report)", section_heading))
    elements.append(Paragraph(
        "Screenshot of the terminal execution of <font face='Courier'>pytest -v</font> inside the <font face='Courier'>work/</font> directory, displaying the test collection, individual test passes (unit tests for orders, speed, and model behaviour fixtures), and the complete summary line:",
        body_style
    ))
    elements.append(Spacer(1, 8))

    img_path = "terminal_screenshot_clean.png"
    if os.path.exists(img_path):
        disp_width = 510
        disp_height = 510 * (630 / 900)
        img = Image(img_path, width=disp_width, height=disp_height)
        elements.append(img)
    elements.append(Spacer(1, 14))

    # 5. One Line Stating Package Produced Number Before and Now
    elements.append(Paragraph("5. Model Output Comparison Before &amp; After Refactor", section_heading))
    statement = (
        "<b>Metric Output Comparison:</b> Before the refactor, the baseline hardcoded model produced a Mean Absolute Error "
        "(MAE) of <b>1.92 minutes</b>, and after refactoring settings into <font face='Courier'>config.yaml</font>, it produces "
        "identically <b>1.92 minutes</b> (and <b>2.18 minutes</b> when constrained to <font face='Courier'>max_rows: 300</font> as implemented in Task T1)."
    )
    elements.append(Paragraph(statement, body_style))
    elements.append(Spacer(1, 14))

    # 6. AI Use Disclosure
    elements.append(Paragraph("6. AI Use Disclosure", section_heading))
    disclosure_text = (
        "<b>Disclosure:</b> None"
    )
    elements.append(Paragraph(disclosure_text, body_style))

    # Build document
    doc.build(elements, canvasmaker=NumberedCanvas)
    print("S24CSEU0807_p05.pdf built successfully!")

if __name__ == "__main__":
    create_submission_pdf("S24CSEU0807_p05.pdf")

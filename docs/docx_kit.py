"""实验报告/指导书 DOCX 生成工具库。

统一处理：中文字体（eastAsia）、代码块底纹、截图占位框、表格样式、编号。

注意两处 OOXML 细节（踩过坑）：
1. w:shd 必须按 schema 顺序插入 pPr / tcPr，直接 append 到末尾会让
   LibreOffice / Word 丢弃该段落的底纹甚至整段格式；
2. w:cantSplit 要排在 w:trHeight 之前、w:tblHeader 要排在 trHeight 之后，
   否则跨页时行会被切断、表头不会重复。
"""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SONG = "宋体"
HEI = "黑体"
KAI = "楷体"
MONO = "Consolas"
LATIN = "Times New Roman"

# pPr 中排在 w:shd 之后的元素，插入时需要避开它们
_PPR_AFTER_SHD = (
    "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
    "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
    "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
    "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
    "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
    "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange",
)

# tcPr 中排在 w:shd 之后的元素
_TCPR_AFTER_SHD = (
    "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign",
    "w:hideMark", "w:headers", "w:cellIns", "w:cellDel", "w:cellMerge",
    "w:tcPrChange",
)

_TCPR_AFTER_MAR = (
    "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark", "w:headers",
    "w:cellIns", "w:cellDel", "w:cellMerge", "w:tcPrChange",
)

# 编号计数器：每个编号组独立从 1 开始
_num = [0]


def reset_numbering():
    """重新开始编号，每个任务的步骤都从 1 起。"""
    _num[0] = 0


def _rfonts(run, latin, eastasia):
    """python-docx 的 font.name 只设 ascii，中文必须单独指定 w:eastAsia。"""
    run.font.name = latin
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    rfonts.set(qn("w:ascii"), latin)
    rfonts.set(qn("w:hAnsi"), latin)
    rfonts.set(qn("w:eastAsia"), eastasia)
    rfonts.set(qn("w:cs"), latin)


def style_run(run, size=12, bold=False, font=SONG, latin=LATIN, color=None):
    _rfonts(run, latin, font)
    run.font.size = Pt(size)
    run.font.bold = bold
    if font == MONO:
        # 等宽字体不要额外压缩，保持代码可读
        run.font.name = MONO
    if color:
        run.font.color.rgb = RGBColor(*color)
    return run


def _make(tag, **attrs):
    el = OxmlElement(tag)
    for k, v in attrs.items():
        el.set(qn(k), v)
    return el


def shade(paragraph, fill):
    """给段落加底纹，按 schema 顺序插入，避免底纹丢失。"""
    ppr = paragraph._p.get_or_add_pPr()
    shd = _make("w:shd", **{"w:val": "clear", "w:color": "auto", "w:fill": fill})
    ppr.insert_element_before(shd, *_PPR_AFTER_SHD)


def cell_shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = _make("w:shd", **{"w:val": "clear", "w:color": "auto", "w:fill": fill})
    tcpr.insert_element_before(shd, *_TCPR_AFTER_SHD)


def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tcpr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for tag, val in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        mar.append(_make("w:" + tag, **{"w:w": str(val), "w:type": "dxa"}))
    tcpr.insert_element_before(mar, *_TCPR_AFTER_MAR)


def set_row_height(row, cm):
    trpr = row._tr.get_or_add_trPr()
    trpr.append(_make("w:trHeight", **{"w:val": str(int(cm * 567)), "w:hRule": "atLeast"}))


def set_cant_split(row):
    """禁止该行跨页被切断。"""
    trpr = row._tr.get_or_add_trPr()
    trpr.insert(0, _make("w:cantSplit", **{"w:val": "true"}))


def set_cell_valign_center(cell):
    """单元格内容垂直居中，避免窄列内容顶在上面。"""
    tcpr = cell._tc.get_or_add_tcPr()
    tcpr.append(_make("w:vAlign", **{"w:val": "center"}))


def set_header_row(row):
    """标记为标题行，跨页时自动重复。"""
    trpr = row._tr.get_or_add_trPr()
    trpr.append(_make("w:tblHeader", **{"w:val": "true"}))


def new_document(title_text):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.4)
    sec.bottom_margin = Cm(2.2)
    sec.left_margin = Cm(2.6)
    sec.right_margin = Cm(2.4)

    normal = doc.styles["Normal"]
    normal.font.size = Pt(12)
    normal.font.name = LATIN
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), SONG)
    pf = normal.paragraph_format
    pf.line_spacing = 1.45
    pf.space_before = Pt(0)
    pf.space_after = Pt(3)

    for name, size in (("Heading 1", 18), ("Heading 2", 15), ("Heading 3", 13)):
        st = doc.styles[name]
        st.font.name = LATIN
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor(0x1F, 0x2D, 0x3D)
        st.element.rPr.rFonts.set(qn("w:eastAsia"), HEI)
        st.paragraph_format.space_before = Pt(14 if name == "Heading 1" else 10)
        st.paragraph_format.space_after = Pt(6)

    core = doc.core_properties
    core.title = title_text
    return doc


def title(doc, text, subtitle=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(24)
    p.paragraph_format.space_after = Pt(6)
    style_run(p.add_run(text), size=25, bold=True, font=HEI, color=(0x14, 0x2A, 0x4A))
    if subtitle:
        sp = doc.add_paragraph()
        sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp.paragraph_format.space_after = Pt(16)
        style_run(sp.add_run(subtitle), size=13, font=KAI, color=(0x55, 0x55, 0x55))
    return p


def h1(doc, text):
    reset_numbering()
    return doc.add_heading(text, level=1)


def h2(doc, text):
    reset_numbering()
    return doc.add_heading(text, level=2)


def h3(doc, text):
    reset_numbering()
    return doc.add_heading(text, level=3)


def para(doc, text, size=12, bold=False, indent=True, align=None, space_after=3,
         color=None, style=None):
    p = doc.add_paragraph(style=style) if style else doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Pt(size * 2)
    p.paragraph_format.space_after = Pt(space_after)
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_run(p.add_run(text), size=size, bold=bold, font=SONG, color=color)
    return p


def bullet(doc, text, size=12, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(0.74 + level * 0.6)
    p.paragraph_format.space_after = Pt(2)
    style_run(p.add_run(text), size=size, font=SONG)
    return p


def numbered(doc, text, size=12):
    """手写编号，不依赖 List Number 样式，保证每组从 1 开始且渲染稳定。"""
    _num[0] += 1
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.95)
    p.paragraph_format.first_line_indent = Cm(-0.55)
    p.paragraph_format.space_after = Pt(3)
    style_run(p.add_run("%d. " % _num[0]), size=size, bold=True, font=SONG)
    style_run(p.add_run(text), size=size, font=SONG)
    return p


def kv_line(doc, label, value=None, size=12):
    """基础信息行：标签加粗 + 值留空下划线供手填。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(7)
    style_run(p.add_run(label), size=size, bold=True, font=HEI)
    if value is None:
        r = p.add_run("　" * 16)
        r.font.underline = True
        style_run(r, size=size, font=SONG)
        r.font.underline = True
    else:
        style_run(p.add_run(value), size=size, font=SONG)
    return p


def code_block(doc, code, size=9.5, caption=None):
    """等宽字体代码块，浅灰底纹，用于重点代码与注释。"""
    if caption:
        cp = doc.add_paragraph()
        cp.paragraph_format.space_before = Pt(6)
        cp.paragraph_format.space_after = Pt(3)
        style_run(cp.add_run(caption), size=10, bold=True, font=HEI)
    for line in code.rstrip("\n").split("\n"):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.12
        pf.left_indent = Cm(0.45)
        pf.right_indent = Cm(0.1)
        shade(p, "F4F5F7")
        style_run(p.add_run(line if line else " "), size=size, font=MONO, latin=MONO)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def placeholder(doc, index, name, what, height_cm=5.2):
    """截图占位框：带底纹的单格表格，提示要截什么内容。"""
    table_obj = doc.add_table(rows=1, cols=1)
    table_obj.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_obj.style = "Table Grid"
    row = table_obj.rows[0]
    set_cant_split(row)
    set_row_height(row, height_cm)
    cell = table_obj.cell(0, 0)
    cell_shade(cell, "FAFAFA")
    set_cell_margins(cell, 140, 140, 160, 160)

    p0 = cell.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_after = Pt(6)
    style_run(p0.add_run("【 截图 %d 占位 】%s" % (index, name)),
              size=11, bold=True, font=HEI, color=(0xB0, 0x3A, 0x2E))

    p1 = cell.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_after = Pt(3)
    style_run(p1.add_run("请在 Word 中删除本框，粘贴对应的运行截图"),
              size=9.5, font=KAI, color=(0x77, 0x77, 0x77))

    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_run(p2.add_run("拍摄内容：" + what), size=9, font=SONG, color=(0x55, 0x55, 0x55))

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(3)
    cap.paragraph_format.space_after = Pt(10)
    style_run(cap.add_run("图 %d　%s" % (index, name)), size=10, bold=True, font=SONG)
    return table_obj


def table(doc, headers, rows, widths=None, font_size=10, header_fill="E8EDF3",
          first_col_bold=False):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    # 固定列宽布局，避免 LibreOffice/Word 按内容自动加宽导致超出版心
    t.autofit = False
    hdr = t.rows[0]
    for i, text in enumerate(headers):
        c = hdr.cells[i]
        c.text = ""
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        style_run(p.add_run(text), size=font_size, bold=True, font=HEI)
        cell_shade(c, header_fill)
        set_cell_margins(c)
        set_cell_valign_center(c)
    set_cant_split(hdr)
    set_header_row(hdr)          # 跨页时重复表头
    for r in rows:
        row = t.add_row()
        set_cant_split(row)      # 单行内容不跨页拆开
        for i, text in enumerate(r):
            c = row.cells[i]
            c.text = ""
            p = c.paragraphs[0]
            p.alignment = (WD_ALIGN_PARAGRAPH.LEFT if i == len(r) - 1
                           else WD_ALIGN_PARAGRAPH.CENTER)
            p.paragraph_format.space_after = Pt(0)
            style_run(p.add_run(str(text)), size=font_size,
                      bold=(first_col_bold and i == 0), font=SONG)
            set_cell_margins(c)
            set_cell_valign_center(c)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    return t


def note(doc, text, size=10.5):
    """浅黄底纹的注意事项。"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    p.paragraph_format.right_indent = Cm(0.2)
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(7)
    shade(p, "FFF8E1")
    style_run(p.add_run(text), size=size, font=SONG, color=(0x6B, 0x4E, 0x16))
    return p


def page_break(doc):
    doc.add_page_break()

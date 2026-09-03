#!/usr/bin/env python3
"""Create a lightweight Kstudy graduation thesis DOCX skeleton.

Uses only Python standard library so the skill can run in restricted agent environments.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import pathlib
import zipfile


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="160" w:line="360" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:sz w:val="24"/><w:lang w:val="vi-VN"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="240"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="1D237D"/><w:sz w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="360" w:after="160"/><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="1D237D"/><w:sz w:val="30"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="247DF9"/><w:sz w:val="26"/></w:rPr>
  </w:style>
</w:styles>
"""


def esc(value: str) -> str:
    return html.escape(value or "", quote=False)


def paragraph(text: str = "", style: str | None = None, center: bool = False, bold: bool = False) -> str:
    ppr = ""
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if center:
        ppr += '<w:jc w:val="center"/>'
    rpr = "<w:b/>" if bold else ""
    return (
        "<w:p>"
        + (f"<w:pPr>{ppr}</w:pPr>" if ppr else "")
        + f"<w:r><w:rPr>{rpr}</w:rPr><w:t>{esc(text)}</w:t></w:r>"
        + "</w:p>"
    )


def page_break() -> str:
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def bullet(text: str) -> str:
    return paragraph(f"- {text}")


def document_xml(args: argparse.Namespace) -> str:
    today = dt.date.today().strftime("%m/%Y")
    chapter_sections = [
        ("Tóm tắt đề tài", [
            "Bối cảnh: [CAN_BO_SUNG]",
            "Vấn đề chính: [CAN_BO_SUNG]",
            "Mục tiêu: [CAN_BO_SUNG]",
            "Phương pháp: [CAN_BO_SUNG]",
            "Kết quả/kỳ vọng: [CAN_BO_SUNG]",
            "Từ khóa: AI, automation, Digital Marketing, Kstudy, [CAN_BO_SUNG]",
        ]),
        ("Chương 1: Bối cảnh và vấn đề", [
            "1.1. Bối cảnh doanh nghiệp/sản phẩm/kênh",
            "1.2. Vấn đề cần giải quyết và tác động",
            "1.3. Mục tiêu đề tài",
            "1.4. Câu hỏi nghiên cứu/thực hành",
            "1.5. Phạm vi và giới hạn",
        ]),
        ("Chương 2: Cơ sở lý thuyết và khung phân tích", [
            "2.1. Khái niệm và mô hình liên quan",
            "2.2. Khung phân tích áp dụng cho đề tài",
            "2.3. Tiêu chí đánh giá giải pháp",
        ]),
        ("Chương 3: Phương pháp và kế hoạch thực hiện", [
            "3.1. Nguồn dữ liệu và cách thu thập",
            "3.2. Quy trình thực hiện theo CDIO",
            "3.3. Công cụ sử dụng",
            "3.4. KPI/rubric đánh giá",
        ]),
        ("Chương 4: Giải pháp / sản phẩm / chiến dịch / workflow", [
            "4.1. Thiết kế giải pháp",
            "4.2. Kế hoạch triển khai",
            "4.3. Output minh chứng",
            "4.4. Rủi ro và điểm cần human approval",
        ]),
        ("Chương 5: Đánh giá kết quả và khuyến nghị", [
            "5.1. Kết quả theo KPI",
            "5.2. Phân tích nguyên nhân",
            "5.3. Bài học rút ra",
            "5.4. Khuyến nghị triển khai tiếp",
        ]),
        ("Kết luận", [
            "Tóm tắt giá trị đề tài, giới hạn, và bước phát triển tiếp theo.",
        ]),
        ("Tài liệu tham khảo", [
            "[CAN_BO_SUNG: nguồn học thuật, báo cáo công cụ, tài liệu nội bộ được phép dùng]",
        ]),
        ("Phụ lục / minh chứng", [
            "Ảnh chụp màn hình, bảng số liệu, campaign asset, workflow, prompt, khảo sát, log triển khai.",
        ]),
        ("Checklist tự rà soát", [
            "Có vấn đề, mục tiêu, phạm vi, KPI rõ.",
            "Không bịa số liệu; chỗ thiếu dùng [CAN_BO_SUNG].",
            "Giải pháp có owner, tool, input, output, timeline, risk.",
            "Có minh chứng để bảo vệ trước hội đồng.",
            "Văn phong Kstudy: thực chiến, rõ, không hype.",
        ]),
    ]
    body = [
        paragraph("HỌC VIỆN KSTUDY", center=True, bold=True),
        paragraph("KSTUDY ACADEMY", center=True),
        paragraph("ĐỀ TÀI TỐT NGHIỆP", style="Title"),
        paragraph(args.title, center=True, bold=True),
        paragraph(f"Học viên: {args.student}", center=True),
        paragraph(f"Mã học viên: {args.student_id}", center=True) if args.student_id else "",
        paragraph(f"Chương trình: {args.program}", center=True),
        paragraph(f"Giảng viên/Mentor hướng dẫn: {args.mentor}", center=True),
        paragraph(f"Lớp/Khóa: {args.cohort}", center=True) if args.cohort else "",
        paragraph(f"Thời gian: {today}", center=True),
        page_break(),
        paragraph("Cam kết tính trung thực", style="Heading1"),
        paragraph("Tôi cam kết nội dung, số liệu, hình ảnh minh chứng và tài liệu tham khảo trong đề tài được sử dụng trung thực. Các phần còn thiếu dữ liệu được đánh dấu rõ để bổ sung trước khi nộp chính thức."),
    ]
    for heading, items in chapter_sections:
        body.append(paragraph(heading, style="Heading1"))
        for item in items:
            body.append(bullet(item))
    content = "\n".join(item for item in body if item)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {content}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>
"""


def core_xml(title: str) -> str:
    now = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{esc(title)}</dc:title>
  <dc:creator>Kstudy Tot Nghiep Skill</dc:creator>
  <cp:lastModifiedBy>Kstudy Tot Nghiep Skill</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""


APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Kstudy Tot Nghiep Skill</Application>
</Properties>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Kstudy graduation thesis DOCX skeleton.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--student", default="[CAN_BO_SUNG]")
    parser.add_argument("--student-id", default="")
    parser.add_argument("--program", default="Digital Marketing định hướng AI Automation")
    parser.add_argument("--mentor", default="[CAN_BO_SUNG]")
    parser.add_argument("--cohort", default="")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = pathlib.Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", CONTENT_TYPES)
        docx.writestr("_rels/.rels", RELS)
        docx.writestr("word/_rels/document.xml.rels", DOC_RELS)
        docx.writestr("word/styles.xml", STYLES)
        docx.writestr("word/document.xml", document_xml(args))
        docx.writestr("docProps/core.xml", core_xml(args.title))
        docx.writestr("docProps/app.xml", APP_XML)
    print(output)


if __name__ == "__main__":
    main()

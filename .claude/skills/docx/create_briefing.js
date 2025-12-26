const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat } = require('docx');

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Malgun Gothic", size: 24 } }
    },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { size: 56, bold: true, color: "1a1a1a", font: "Malgun Gothic" },
        paragraph: { spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER }
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 32, bold: true, color: "2c3e50", font: "Malgun Gothic" },
        paragraph: { spacing: { before: 240, after: 180 }, outlineLevel: 0 }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, color: "34495e", font: "Malgun Gothic" },
        paragraph: { spacing: { before: 180, after: 120 }, outlineLevel: 1 }
      }
    ]
  },
  numbering: {
    config: [
      {
        reference: "bullet-list",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          }
        ]
      },
      {
        reference: "news-list",
        levels: [
          {
            level: 0,
            format: LevelFormat.DECIMAL,
            text: "%1.",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          }
        ]
      }
    ]
  },
  sections: [{
    properties: {
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    children: [
      // Title
      new Paragraph({
        heading: HeadingLevel.TITLE,
        children: [new TextRun("당신이 잠든 사이 | 2025.12.05")]
      }),

      // Spacing
      new Paragraph({ children: [new TextRun("")] }),

      // H1: 오늘의 화제 종목
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("오늘의 화제 종목: TESLA (TSLA)")]
      }),

      // Bullet list
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [
          new TextRun("주가: $385.20 ("),
          new TextRun({ text: "+8.7%", color: "27ae60", bold: true }),
          new TextRun(")")
        ]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("선정 기준: 거래량 1위")]
      }),

      // Spacing
      new Paragraph({ children: [new TextRun("")] }),

      // H2: 왜 화제인가?
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("왜 화제인가?")]
      }),

      // Bullet list
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("사이버트럭 판매량 급증")]
      }),
      new Paragraph({
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("FSD v13 출시 예고")]
      }),

      // Spacing
      new Paragraph({ children: [new TextRun("")] }),

      // H2: 관련 뉴스 TOP 3
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("관련 뉴스 TOP 3")]
      }),

      // Numbered list
      new Paragraph({
        numbering: { reference: "news-list", level: 0 },
        children: [new TextRun("테슬라 사이버트럭 미국 판매 3위 - Reuters")]
      }),
      new Paragraph({
        numbering: { reference: "news-list", level: 0 },
        children: [new TextRun("FSD v13 무감독 자율주행 - Bloomberg")]
      }),
      new Paragraph({
        numbering: { reference: "news-list", level: 0 },
        children: [new TextRun("중국 시장 반등 - CNBC")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("c:/Users/tlduf/Downloads/ica-project/backend/output/reports/briefing_2025-12-05.docx", buffer);
  console.log("Document created successfully: briefing_2025-12-05.docx");
});

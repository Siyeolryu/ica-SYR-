const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, AlignmentType,
        HeadingLevel, BorderStyle, WidthType, ShadingType, VerticalAlign, LevelFormat, PageBreak } = require('docx');
const fs = require('fs');
const path = require('path');

// 샘플 브리핑 데이터
const sampleBriefingData = {
  briefing: {
    title: "당신이 잠든 사이 - 미국 주식 브리핑",
    subtitle: "오늘의 화제 종목 분석",
    generated_at: new Date().toISOString(),
    stock_symbol: "NVDA",
    stock_name: "NVIDIA Corporation",
    sections: [
      {
        stock_symbol: "NVDA",
        title: "종목 개요",
        content: "NVIDIA는 AI와 데이터센터 시장을 선도하는 글로벌 반도체 기업입니다. 최근 AI 붐에 힘입어 주가가 급등하고 있으며, 데이터센터용 GPU 수요가 폭발적으로 증가하고 있습니다."
      },
      {
        stock_symbol: "NVDA",
        title: "오늘의 주가 동향",
        content: "NVIDIA 주가는 전일 대비 3.5% 상승하며 $485.20에 마감했습니다. 거래량은 평균 대비 150% 증가한 5천만 주를 기록했습니다."
      },
      {
        stock_symbol: "NVDA",
        title: "주요 뉴스 및 이벤트",
        content: "• Microsoft와 대규모 AI 칩 공급 계약 체결\n• 새로운 Blackwell 아키텍처 GPU 양산 시작 발표\n• JP Morgan이 목표주가를 $550으로 상향 조정\n• 데이터센터 매출이 전년 동기 대비 200% 증가 전망"
      },
      {
        stock_symbol: "NVDA",
        title: "애널리스트 의견",
        content: "대부분의 애널리스트들이 NVIDIA에 대해 긍정적인 전망을 유지하고 있습니다. AI 인프라 수요 증가로 인해 향후 2-3년간 고성장이 지속될 것으로 예상됩니다."
      },
      {
        stock_symbol: "NVDA",
        title: "투자 포인트",
        content: "장점:\n• AI 시장 선도적 위치\n• 강력한 기술 경쟁력\n• 높은 마진율과 수익성\n\n주의사항:\n• 높은 밸류에이션\n• 중국 시장 규제 리스크\n• 경쟁사 추격 가능성"
      }
    ]
  },
  stock_data: {
    symbol: "NVDA",
    name: "NVIDIA Corporation",
    price: 485.20,
    change_percent: 3.5,
    volume: 50000000,
    news_summary: "NVIDIA가 Microsoft와 대규모 AI 칩 공급 계약을 체결하며 주가가 상승했습니다. 새로운 Blackwell GPU의 양산 시작 소식도 긍정적으로 작용했습니다.",
    analysis: "NVIDIA는 AI 반도체 시장의 확고한 리더로서 지속적인 성장이 예상됩니다.",
    why_trending: "Microsoft와의 대규모 계약 체결 및 신제품 양산 소식으로 투자자들의 관심이 집중되고 있습니다."
  }
};

function createBriefingDocument(data) {
  const { briefing, stock_data } = data;

  // 테이블 보더 스타일
  const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
  const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

  // 넘버링 설정
  const numberingConfig = {
    config: [
      {
        reference: "bullet-list",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  };

  // 문서 스타일
  const styles = {
    default: { document: { run: { font: "맑은 고딕", size: 24 } } },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { size: 56, bold: true, color: "1a1a1a", font: "맑은 고딕" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER }
      },
      {
        id: "Subtitle",
        name: "Subtitle",
        basedOn: "Normal",
        run: { size: 32, bold: true, color: "4a4a4a", font: "맑은 고딕" },
        paragraph: { spacing: { before: 120, after: 240 }, alignment: AlignmentType.CENTER }
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        run: { size: 32, bold: true, color: "2c5aa0", font: "맑은 고딕" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        run: { size: 28, bold: true, color: "3d7bc6", font: "맑은 고딕" },
        paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 }
      }
    ]
  };

  // 문서 컨텐츠 생성
  const children = [];

  // 제목
  children.push(new Paragraph({
    heading: HeadingLevel.TITLE,
    children: [new TextRun(briefing.title)]
  }));

  // 부제목
  children.push(new Paragraph({
    style: "Subtitle",
    children: [new TextRun(briefing.subtitle)]
  }));

  // 생성 날짜
  const generatedDate = new Date(briefing.generated_at).toLocaleString('ko-KR');
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({
      text: `생성 일시: ${generatedDate}`,
      size: 20,
      color: "666666"
    })]
  }));

  // 종목 요약 테이블
  children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("종목 정보")]
  }));

  children.push(new Table({
    columnWidths: [3120, 6240],
    margins: { top: 100, bottom: 100, left: 180, right: 180 },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: cellBorders,
            width: { size: 3120, type: WidthType.DXA },
            shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
            verticalAlign: VerticalAlign.CENTER,
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: "종목코드", bold: true })]
            })]
          }),
          new TableCell({
            borders: cellBorders,
            width: { size: 6240, type: WidthType.DXA },
            children: [new Paragraph({
              children: [new TextRun(stock_data.symbol)]
            })]
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            borders: cellBorders,
            width: { size: 3120, type: WidthType.DXA },
            shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
            verticalAlign: VerticalAlign.CENTER,
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: "회사명", bold: true })]
            })]
          }),
          new TableCell({
            borders: cellBorders,
            width: { size: 6240, type: WidthType.DXA },
            children: [new Paragraph({
              children: [new TextRun(stock_data.name)]
            })]
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            borders: cellBorders,
            width: { size: 3120, type: WidthType.DXA },
            shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
            verticalAlign: VerticalAlign.CENTER,
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: "현재가", bold: true })]
            })]
          }),
          new TableCell({
            borders: cellBorders,
            width: { size: 6240, type: WidthType.DXA },
            children: [new Paragraph({
              children: [new TextRun(`$${stock_data.price.toFixed(2)}`)]
            })]
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            borders: cellBorders,
            width: { size: 3120, type: WidthType.DXA },
            shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
            verticalAlign: VerticalAlign.CENTER,
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: "변동률", bold: true })]
            })]
          }),
          new TableCell({
            borders: cellBorders,
            width: { size: 6240, type: WidthType.DXA },
            children: [new Paragraph({
              children: [new TextRun({
                text: `${stock_data.change_percent > 0 ? '+' : ''}${stock_data.change_percent.toFixed(2)}%`,
                color: stock_data.change_percent > 0 ? "E74C3C" : "3498DB",
                bold: true
              })]
            })]
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            borders: cellBorders,
            width: { size: 3120, type: WidthType.DXA },
            shading: { fill: "E8F4F8", type: ShadingType.CLEAR },
            verticalAlign: VerticalAlign.CENTER,
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: "거래량", bold: true })]
            })]
          }),
          new TableCell({
            borders: cellBorders,
            width: { size: 6240, type: WidthType.DXA },
            children: [new Paragraph({
              children: [new TextRun(stock_data.volume.toLocaleString())]
            })]
          })
        ]
      })
    ]
  }));

  children.push(new Paragraph({ children: [new TextRun("")] }));

  // 브리핑 섹션들
  briefing.sections.forEach((section) => {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_1,
      children: [new TextRun(section.title)]
    }));

    // 내용을 줄바꿈으로 분리하여 처리
    const lines = section.content.split('\n').filter(line => line.trim());

    lines.forEach((line) => {
      // 불릿 포인트 처리
      if (line.trim().startsWith('•')) {
        children.push(new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun(line.trim().substring(1).trim())]
        }));
      } else {
        children.push(new Paragraph({
          spacing: { after: 120 },
          children: [new TextRun(line.trim())]
        }));
      }
    });

    children.push(new Paragraph({ children: [new TextRun("")] }));
  });

  // 화제가 된 이유
  if (stock_data.why_trending) {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_1,
      children: [new TextRun("왜 화제인가?")]
    }));

    children.push(new Paragraph({
      spacing: { after: 240 },
      children: [new TextRun(stock_data.why_trending)]
    }));
  }

  // 푸터
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 400 },
    children: [new TextRun({
      text: "이 브리핑은 자동으로 생성되었습니다.",
      size: 20,
      color: "999999",
      italics: true
    })]
  }));

  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({
      text: "당신이 잠든 사이 - 미국 주식 브리핑 서비스",
      size: 20,
      color: "999999",
      italics: true
    })]
  }));

  // 문서 생성
  return new Document({
    numbering: numberingConfig,
    styles: styles,
    sections: [{
      properties: {
        page: {
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
        }
      },
      children: children
    }]
  });
}

// JSON 파일에서 브리핑 데이터 로드 (옵션)
function loadBriefingFromJson(jsonPath) {
  try {
    const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    return data;
  } catch (error) {
    console.error(`JSON 파일 로드 실패: ${error.message}`);
    return null;
  }
}

// 메인 실행 함수
async function generateBriefingDocx(inputData = null, outputPath = null) {
  try {
    // 입력 데이터 결정
    let data = inputData || sampleBriefingData;

    // 문서 생성
    console.log('브리핑 Word 문서 생성 중...');
    const doc = createBriefingDocument(data);

    // 출력 경로 결정
    if (!outputPath) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
      const symbol = data.stock_data?.symbol || 'SAMPLE';
      outputPath = path.join(__dirname, 'output', `briefing_${symbol}_${timestamp}.docx`);
    }

    // 출력 디렉토리 생성
    const outputDir = path.dirname(outputPath);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // 문서 저장
    const buffer = await Packer.toBuffer(doc);
    fs.writeFileSync(outputPath, buffer);

    console.log(`✓ 브리핑 문서 생성 완료: ${outputPath}`);
    return outputPath;
  } catch (error) {
    console.error(`문서 생성 실패: ${error.message}`);
    throw error;
  }
}

// CLI 실행
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length > 0) {
    // JSON 파일 경로가 제공된 경우
    const jsonPath = args[0];
    const outputPath = args[1] || null;

    console.log(`JSON 파일에서 브리핑 로드: ${jsonPath}`);
    const data = loadBriefingFromJson(jsonPath);

    if (data) {
      generateBriefingDocx(data, outputPath);
    } else {
      console.error('JSON 파일 로드 실패. 샘플 데이터로 생성합니다.');
      generateBriefingDocx();
    }
  } else {
    // 샘플 데이터로 생성
    console.log('샘플 데이터로 브리핑 생성');
    generateBriefingDocx();
  }
}

module.exports = { generateBriefingDocx, loadBriefingFromJson, createBriefingDocument };

const pptxgen = require('pptxgenjs');
const html2pptx = require('../scripts/html2pptx');
const path = require('path');

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'While You Were Sleeping Team';
  pptx.title = '당신이 잠든 사이 - 주간 개발 보고서';

  // Slide 1: Title
  await html2pptx('slide1.html', pptx);

  // Slide 2: Goals
  await html2pptx('slide2.html', pptx);

  // Slide 3: Subagent Achievement
  await html2pptx('slide3.html', pptx);

  // Slide 4: Refactoring Achievement
  await html2pptx('slide4.html', pptx);

  // Slide 5: GitHub Actions Achievement
  await html2pptx('slide5.html', pptx);

  // Slide 6: Tech Stack
  await html2pptx('slide6.html', pptx);

  // Slide 7: Next Steps
  await html2pptx('slide7.html', pptx);

  // Save presentation
  const outputPath = path.join(__dirname, '..', '..', '..', '..', 'backend', 'output', 'reports', 'weekly_report_20251226.pptx');
  await pptx.writeFile({ fileName: outputPath });
  console.log('Presentation created:', outputPath);
}

createPresentation().catch(console.error);

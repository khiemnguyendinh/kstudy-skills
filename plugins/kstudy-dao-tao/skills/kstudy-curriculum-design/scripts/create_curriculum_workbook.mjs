import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  console.error("Usage: create_curriculum_workbook.mjs <curriculum-design.json> <output.xlsx>");
  process.exit(2);
}

const data = JSON.parse(await fs.readFile(inputPath, "utf8"));
const brief = data.project_brief ?? {};
const courses = Array.isArray(data.curriculum_map) ? data.curriculum_map : [];
const research = data.research ?? {};
const workload = data.workload ?? {};
const quality = data.quality_review ?? {};
const handoff = data.handoff ?? {};

const HOUR_FIELDS = [
  "direct_live_hours",
  "elearning_hours",
  "self_study_hours",
  "practice_project_hours",
  "assessment_feedback_hours",
  "mentor_coaching_hours",
];

const asArray = (value) => (Array.isArray(value) ? value : []);
const join = (value) => (Array.isArray(value) ? value.join("\n") : value ?? "");
const safeNumber = (value) => (typeof value === "number" && Number.isFinite(value) ? value : null);
const plos = new Map(asArray(data.program_outcomes).map((item) => [item.plo_id, item]));
const tasks = new Map(asArray(data.occupation_analysis?.tasks).map((item) => [item.task_id, item]));
const competencies = new Map(
  asArray(data.competency_architecture?.competencies).map((item) => [item.competency_id, item]),
);
const courseWorkloads = new Map(
  asArray(workload.course_totals).map((item) => [item.course_id, item]),
);

function excelColumn(number) {
  let result = "";
  let current = number;
  while (current > 0) {
    const remainder = (current - 1) % 26;
    result = String.fromCharCode(65 + remainder) + result;
    current = Math.floor((current - 1) / 26);
  }
  return result;
}

function hoursFor(course) {
  const record = courseWorkloads.get(course.course_id) ?? course.workload ?? {};
  return Object.fromEntries(HOUR_FIELDS.map((field) => [field, safeNumber(record[field])]));
}

function styleRange(range, { fill, font, wrap = true, horizontal = "left", vertical = "top", borders } = {}) {
  if (fill) range.format.fill = fill;
  if (font) range.format.font = font;
  range.format.wrapText = wrap;
  range.format.horizontalAlignment = horizontal;
  range.format.verticalAlignment = vertical;
  if (borders) range.format.borders = borders;
}

function styleTable(sheet, headers, rowCount, widths, startRow = 1) {
  const endColumn = excelColumn(headers.length);
  const endRow = startRow + rowCount - 1;
  const header = sheet.getRange(`A${startRow}:${endColumn}${startRow}`);
  styleRange(header, {
    fill: "#EFEFEF",
    font: { bold: true, fontSize: 10, color: "#1F1F1F" },
    horizontal: "center",
    vertical: "center",
    borders: { preset: "all", style: "thin", color: "#1F2329" },
  });
  header.format.rowHeight = 34;
  if (rowCount > 1) {
    const body = sheet.getRange(`A${startRow + 1}:${endColumn}${endRow}`);
    styleRange(body, {
      font: { fontSize: 10, color: "#1F1F1F" },
      borders: { preset: "all", style: "thin", color: "#D9D9D9" },
    });
  }
  for (const [column, width] of Object.entries(widths)) {
    sheet.getRange(`${column}${startRow}:${column}${endRow}`).format.columnWidth = width;
  }
}

function writeTable(sheet, headers, rows, tableName, widths, startRow = 1) {
  const endColumn = excelColumn(headers.length);
  const endRow = startRow + rows.length;
  sheet.getRange(`A${startRow}:${endColumn}${endRow}`).values = [headers, ...rows];
  styleTable(sheet, headers, rows.length + 1, widths, startRow);
  if (rows.length) sheet.tables.add(`A${startRow}:${endColumn}${endRow}`, true, tableName);
}

function addSectionTitle(sheet, row, endColumn, title) {
  const range = sheet.getRange(`A${row}:${endColumn}${row}`);
  range.merge();
  range.values = [[title]];
  styleRange(range, {
    fill: "#D9EAF7",
    font: { bold: true, fontSize: 11, color: "#1F1F1F" },
    horizontal: "left",
    vertical: "center",
    borders: { preset: "all", style: "thin", color: "#9ECAE1" },
  });
  range.format.rowHeight = 24;
}

const workbook = Workbook.create();
const year = brief.year ?? new Date().getFullYear();
const mainSheet = workbook.worksheets.add(`Khung chương trình ${year}`);
const evidenceSheet = workbook.worksheets.add("Traceability & Evidence");

const mainHeaders = [
  "STT", "Course ID", "Tên cũ (nếu có)", "Học phần", "Giai đoạn", "Môn điều kiện",
  "Nội dung trọng tâm", "PLO đóng góp", "Sản phẩm đầu ra", "Học trực tiếp/Zoom (Giờ)",
  "E-learning (Giờ)", "Tự học (Giờ)", "Thực hành/Dự án (Giờ)", "Feedback (Giờ)",
  "Mentor (Giờ)", "Tổng giờ", "Học (Buổi)", "E-learning (Bài)", "Hướng dẫn dự án",
  "AI Mentor", "PIC", "Vai trò chiến lược", "Trạng thái", "Tham khảo",
];
const mainLastColumn = excelColumn(mainHeaders.length);

mainSheet.getRange(`A1:${mainLastColumn}1`).merge();
mainSheet.getRange("A1").values = [[brief.working_title ?? "Khung chương trình Kstudy"]];
styleRange(mainSheet.getRange(`A1:${mainLastColumn}1`), {
  fill: "#1F4E78",
  font: { bold: true, fontSize: 14, color: "#FFFFFF" },
  horizontal: "left",
  vertical: "center",
  borders: { preset: "all", style: "thin", color: "#1F4E78" },
});
mainSheet.getRange(`A1:${mainLastColumn}1`).format.rowHeight = 28;

mainSheet.getRange("A2:H3").values = [
  ["Lĩnh vực", brief.field ?? "", "Ngành/nghề", brief.occupation ?? "", "Learner", brief.target_learner ?? "", "Delivery", brief.delivery_model ?? ""],
  ["Status", data.status ?? "", "Research", data.research_level ?? "", "Tổng giờ", null, "Capstone", data.capstone?.title ?? ""],
];
styleRange(mainSheet.getRange("A2:H3"), {
  font: { fontSize: 10, color: "#1F1F1F" },
  borders: { preset: "all", style: "thin", color: "#D9D9D9" },
});
mainSheet.getRange("A2:A3").format.font = { bold: true };
mainSheet.getRange("C2:C3").format.font = { bold: true };
mainSheet.getRange("E2:E3").format.font = { bold: true };
mainSheet.getRange("G2:G3").format.font = { bold: true };

const courseRows = courses.map((course, index) => {
  const hours = hoursFor(course);
  const ploSummary = Object.entries(course.plo_mapping ?? {})
    .map(([ploId, level]) => `${ploId} (${level})`)
    .join("\n");
  return [
    index + 1,
    course.course_id ?? "",
    course.legacy_title ?? course.old_title ?? "",
    course.title ?? "",
    course.stage ?? "",
    course.prerequisite_ids?.length ? course.prerequisite_ids.join(", ") : "Không",
    join(course.core_topics),
    ploSummary,
    join(course.artifacts),
    hours.direct_live_hours,
    hours.elearning_hours,
    hours.self_study_hours,
    hours.practice_project_hours,
    hours.assessment_feedback_hours,
    hours.mentor_coaching_hours,
    null,
    course.live_sessions ?? "",
    course.elearning_units ?? "",
    join(course.project_guidance),
    join(course.ai_mentor_support),
    course.pic ?? "",
    course.strategic_role ?? "",
    course.handoff_status ?? "PROPOSED",
    join(course.references ?? course.source_ids),
  ];
});

const headerRow = 5;
const firstCourseRow = headerRow + 1;
writeTable(mainSheet, mainHeaders, courseRows, "CurriculumTable", {
  A: 7, B: 16, C: 22, D: 30, E: 15, F: 22, G: 40, H: 20, I: 28,
  J: 18, K: 16, L: 14, M: 20, N: 16, O: 16, P: 14, Q: 12, R: 14,
  S: 20, T: 20, U: 14, V: 34, W: 18, X: 34,
}, headerRow);
if (courses.length) {
  mainSheet.getRange(`P${firstCourseRow}:P${firstCourseRow + courses.length - 1}`).formulas = courses.map((_, index) => [
    `=SUM(J${firstCourseRow + index}:O${firstCourseRow + index})`,
  ]);
  mainSheet.getRange(`J${firstCourseRow}:P${firstCourseRow + courses.length - 1}`).setNumberFormat("0.0");
}
const mainTotalRow = firstCourseRow + courses.length;
mainSheet.getRange(`A${mainTotalRow}:X${mainTotalRow}`).values = [[
  "TỔNG PROGRAM", "", "", "", "", "", "", "", "", null, null, null, null, null, null, null, "", "", "", "", "", "", "", "",
]];
if (courses.length) {
  mainSheet.getRange(`J${mainTotalRow}:O${mainTotalRow}`).formulas = [HOUR_FIELDS.map((_, index) =>
    `=SUM(${excelColumn(10 + index)}${firstCourseRow}:${excelColumn(10 + index)}${mainTotalRow - 1})`,
  )];
  mainSheet.getRange(`P${mainTotalRow}`).formulas = [[`=SUM(P${firstCourseRow}:P${mainTotalRow - 1})`]];
} else {
  mainSheet.getRange(`J${mainTotalRow}:P${mainTotalRow}`).formulas = [["=0", "=0", "=0", "=0", "=0", "=0", "=0"]];
}
mainSheet.getRange(`A${mainTotalRow}:X${mainTotalRow}`).format.fill = "#E2F0D9";
mainSheet.getRange(`A${mainTotalRow}:X${mainTotalRow}`).format.font = { bold: true };
mainSheet.getRange(`A${mainTotalRow}:X${mainTotalRow}`).format.borders = { preset: "all", style: "thin", color: "#70AD47" };
mainSheet.getRange("F3").formulas = [[`=P${mainTotalRow}`]];
mainSheet.getRange("F3").setNumberFormat("0.0");
mainSheet.showGridLines = false;
mainSheet.freezePanes.freezeRows(headerRow);
mainSheet.freezePanes.freezeColumns(4);

const evidenceLastColumn = "M";
evidenceSheet.getRange(`A1:${evidenceLastColumn}1`).merge();
evidenceSheet.getRange("A1").values = [["Traceability & Evidence"]];
styleRange(evidenceSheet.getRange(`A1:${evidenceLastColumn}1`), {
  fill: "#1F4E78",
  font: { bold: true, fontSize: 14, color: "#FFFFFF" },
  horizontal: "left",
  vertical: "center",
  borders: { preset: "all", style: "thin", color: "#1F4E78" },
});
evidenceSheet.getRange(`A1:${evidenceLastColumn}1`).format.rowHeight = 28;
evidenceSheet.getRange("A2:D2").values = [["Handoff", handoff.status ?? "", "Target", handoff.target_skill ?? ""]];
styleRange(evidenceSheet.getRange("A2:D2"), {
  font: { fontSize: 10, color: "#1F1F1F" },
  borders: { preset: "all", style: "thin", color: "#D9D9D9" },
});
evidenceSheet.getRange("A2:A2").format.font = { bold: true };
evidenceSheet.getRange("C2:C2").format.font = { bold: true };

const traceHeaders = [
  "Task ID", "Task", "Competency ID", "Competency", "PLO ID", "PLO statement",
  "Course ID", "I/R/M", "CLO/Placeholder", "Activity/Artifact", "Assessment/Rubric", "Source IDs", "Status",
];
const traceRows = asArray(data.traceability?.links).map((link) => {
  const task = tasks.get(link.task_id) ?? {};
  const competency = competencies.get(link.competency_id) ?? {};
  const plo = plos.get(link.plo_id) ?? {};
  const course = courses.find((item) => item.course_id === link.course_id) ?? {};
  return [
    link.task_id ?? "", task.statement ?? "", link.competency_id ?? "", competency.statement ?? "",
    link.plo_id ?? "", plo.statement ?? "", link.course_id ?? "", course.plo_mapping?.[link.plo_id] ?? "",
    link.clo_id_or_placeholder ?? "", link.activity_id_or_placeholder ?? "", link.assessment_id_or_direction ?? "",
    join(link.source_ids), link.status ?? data.traceability?.status ?? "PROPOSED",
  ];
});
const traceTitleRow = 4;
addSectionTitle(evidenceSheet, traceTitleRow, evidenceLastColumn, "1. Traceability matrix");
const traceHeaderRow = traceTitleRow + 1;
writeTable(evidenceSheet, traceHeaders, traceRows, "TraceabilityTable", {
  A: 14, B: 36, C: 18, D: 36, E: 14, F: 42, G: 16, H: 10, I: 22, J: 26, K: 30, L: 20, M: 16,
}, traceHeaderRow);

const findings = asArray(research.findings).map((finding) => [
  finding.finding_id ?? "", finding.finding_type ?? "", finding.claim ?? finding.statement ?? "",
  finding.impact ?? "", finding.evidence_status ?? "", join(finding.source_ids), finding.recommendation ?? "",
]);
const benchmarkSignals = asArray(research.competitor_benchmarks).map((item, index) => [
  item.provider ?? item.organization ?? `BENCH-${index + 1}`,
  "Competitor",
  [item.promise, join(item.public_outline)].filter(Boolean).join(" — "),
  item.gap ?? item.access_status ?? "",
  item.confidence ?? "",
  join(item.source_ids),
  item.recommendation ?? "",
]);
const jdSignals = asArray(research.jd_signals).map((item) => [
  item.source_id ?? "", "JD",
  [item.job_title, item.task, item.skill_tool ?? item.skill].filter(Boolean).join(" — "),
  item.work_output ?? item.output ?? "",
  item.evidence_level ?? "",
  item.source_id ?? "",
  item.limitation ?? "",
]);
const evidenceRows = [...findings, ...benchmarkSignals, ...jdSignals];
const evidenceTitleRow = traceHeaderRow + traceRows.length + 3;
addSectionTitle(evidenceSheet, evidenceTitleRow, evidenceLastColumn, "2. Evidence, benchmark và JD signals");
const evidenceHeaderRow = evidenceTitleRow + 1;
const evidenceHeaders = ["Evidence ID", "Type", "Claim/Signal", "Implication", "Status/Confidence", "Source IDs", "Recommendation/Limitations"];
writeTable(evidenceSheet, evidenceHeaders, evidenceRows, "EvidenceTable", { A: 20, B: 18, C: 58, D: 36, E: 18, F: 22, G: 42 }, evidenceHeaderRow);

const qualityRows = [
  ["Evidence", quality.evidence_gate ?? "", join(quality.evidence_notes), join(quality.blockers)],
  ["Academic coherence", quality.academic_gate ?? "", join(quality.academic_notes), ""],
  ["Workload and delivery", quality.workload_gate ?? "", join(quality.workload_notes), ""],
  ["Traceability", quality.traceability_gate ?? "", join(quality.traceability_notes), ""],
  ["Handoff", quality.handoff_gate ?? "", join(quality.handoff_notes), ""],
];
const qualityTitleRow = evidenceHeaderRow + evidenceRows.length + 3;
addSectionTitle(evidenceSheet, qualityTitleRow, evidenceLastColumn, "3. Quality gates & handoff");
const qualityHeaderRow = qualityTitleRow + 1;
writeTable(evidenceSheet, ["Gate", "Status", "Notes", "Blockers"], qualityRows, "QualityGateTable", { A: 24, B: 18, C: 58, D: 42 }, qualityHeaderRow);
const handoffRow = qualityHeaderRow + qualityRows.length + 2;
evidenceSheet.getRange(`A${handoffRow}:D${handoffRow + 6}`).values = [
  ["Handoff field", "Value", "Status", "Next action"],
  ["Course specs ready", join(handoff.course_specs_ready), handoff.status ?? "", ""],
  ["Blocking questions", join(handoff.blocking_questions), handoff.blocking_questions?.length ? "BLOCKED" : "CLEAR", ""],
  ["Assumptions requiring approval", join(handoff.assumptions_requiring_approval), "PROPOSED", ""],
  ["Source gaps", join(handoff.source_gaps), handoff.source_gaps?.length ? "REVIEW" : "CLEAR", ""],
  ["Next action", handoff.next_action ?? "", "", ""],
  ["Output rule", "JSON is source of truth; Excel is compact audit view", "", ""],
];
styleTable(evidenceSheet, ["Handoff field", "Value", "Status", "Next action"], 7, { A: 32, B: 56, C: 18, D: 36 }, handoffRow);
evidenceSheet.showGridLines = false;
evidenceSheet.freezePanes.freezeRows(traceHeaderRow);
evidenceSheet.freezePanes.freezeColumns(2);

await fs.mkdir(path.dirname(outputPath), { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(`Wrote ${outputPath}`);

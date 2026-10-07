import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const root = process.cwd();
const skill = "C:/Users/iamsa/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/skills/presentations";
const out = path.join(root, "ppt", "OSInsight_AI_Presentation.pptx");
const stage = path.join(root, ".artifact-build", "ppt");
await fs.mkdir(stage, { recursive: true }); await fs.mkdir(path.dirname(out), { recursive: true });
const { resolvePresentationFont, finalizePresentation } = await import(pathToFileURL(path.join(skill, "container_tools/artifact_tool_utils.mjs")).href);
const font = resolvePresentationFont();
const deck = Presentation.create({slideSize:{width:1280,height:720}});
const slides = [
 ["OSInsight AI", "AI Powered Performance Analyzer for Operating System Processes\nUniversity Project Presentation\nOctober 2026"],
 ["Problem Statement", "Raw process lists show current values but rarely explain rising resource pressure. Users need one local view that relates CPU, memory, disk, process activity, and likely next-step demand."],
 ["Objectives", "Collect live telemetry\nMaintain a portable history\nForecast CPU and memory consumption\nDetect bottlenecks and offer safe recommendations\nExport review-ready reports"],
 ["Existing System", "Operating-system task managers provide valuable instantaneous readings. They often require manual interpretation and do not include a small, explainable forecast or a project-focused health summary."],
 ["Proposed System", "OSInsight-AI turns local psutil readings into a dashboard, a retained CSV history, an explainable trend forecast, bottleneck rules, and exportable PDF or CSV evidence."],
 ["Architecture", "Operating system telemetry\n  psutil SystemMonitor\n  CSV DataLogger\n  AnalyticsEngine\n  CustomTkinter dashboard and report exports\n\nEditable Mermaid architecture source: diagrams/system_architecture.mmd"],
 ["Monitoring Module", "SystemMonitor samples CPU, virtual memory, disk use, process count, and top processes. DataLogger appends the normalized snapshot to CSV. Inaccessible processes are safely skipped."],
 ["AI Analytics Module", "A recent sliding window receives sequential indices. Linear regression forecasts the following CPU and memory values. Threshold rules identify pressure at 80% and generate recommendations."],
 ["Dashboard Module", "The CustomTkinter interface refreshes every three seconds. It shows four metrics, a health status line, ranked processes, and export buttons. The application does not terminate processes or send telemetry."],
 ["Application Workflow", "Sample resources\nLog snapshot\nAnalyze recent history\nUpdate score and forecast\nRender dashboard\nRepeat after three seconds"],
 ["Screenshots", "Run python main.py to capture an approved local dashboard image under screenshots/. The live dashboard includes metric cards, a status forecast, top processes, and export controls. Screens are intentionally not bundled because they expose machine-specific data."],
 ["Results", "The supplied sample history demonstrates an increasing CPU and memory trend with stable disk usage. Results vary by host because measurements are local and live. A health score summarizes the current pressure level."],
 ["Challenges", "Operating systems may deny access to process metadata. The monitor handles those exceptions. Early CPU readings can be low while psutil initializes. Forecast confidence depends on the quantity and quality of retained history."],
 ["Future Scope", "Add per-process time series, configurable alerts, stronger anomaly models, model persistence, and opt-in fleet aggregation with access controls."],
 ["Thank You", "OSInsight-AI\nSource, diagrams, tests, report, and presentation are included in the project repository.\n\ngithub.com/sanchit11092007/OSInsight-AI"]
];
for (let i=0;i<slides.length;i++) {
 const [title, body] = slides[i]; const s=deck.slides.add(); s.background.fill="#F7FAFC";
 const band=s.shapes.add({geometry:"rect",position:{left:0,top:0,width:1280,height:18},fill:"#0B3D5C",line:{fill:"none",width:0}});
 const t=s.shapes.add({geometry:"textbox",position:{left:80,top:72,width:1120,height:80},fill:"none",line:{fill:"none",width:0}});
 t.text=title; t.text.style={typeface:font,fontSize:40,bold:true,color:"#0B3D5C",autoFit:"shrinkText"};
 const b=s.shapes.add({geometry:"textbox",position:{left:90,top:190,width:1060,height:400},fill:"none",line:{fill:"none",width:0}});
 b.text=body; b.text.style={typeface:font,fontSize:24,color:"#1F2937",autoFit:"shrinkText",breakLine:false};
 const f=s.shapes.add({geometry:"textbox",position:{left:80,top:665,width:1120,height:24},fill:"none",line:{fill:"none",width:0}});
 f.text=`OSInsight-AI   |   ${i+1} / ${slides.length}`; f.text.style={typeface:font,fontSize:11,color:"#4B5563",autoFit:"shrinkText"};
 s.speakerNotes.textFrame.setText("OSInsight-AI project deliverable. Claims describe the source code in this repository.");
}
const candidate=path.join(stage,"candidate.pptx");
await (await PresentationFile.exportPptx(deck)).save(candidate);
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:out,pythonExecutable:"C:/Users/iamsa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe",integrityValidatorPath:path.join(skill,"container_tools/inspect_presentation_package_integrity.py"),layoutValidatorPath:path.join(skill,"container_tools/inspect_presentation_layout_geometry.py"),layoutArgs:["--expected-slide-size-emu","12192000,6858000","--validate-heading-fit"],explicitTotalSlideCount:15,requiredNativeTableOwnerSlides:[],fontPolicy:{basis:"design",families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(stage,"validation.json")});

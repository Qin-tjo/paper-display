import json, base64, os

# Load figures
figs = {}
for i in range(1, 7):
    path = f'paper_assets/figures/fig{i}_page.png'
    with open(path, 'rb') as f:
        figs[f'fig{i}'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
    print(f'fig{i}: {len(figs[f"fig{i}"])//1024}KB')

PLANETS_DATA = [
    {
        "id": 0,
        "name": "ORIGIN",
        "color": "#4fc3f7",
        "glow": "#0288d1",
        "question": "What is this discovery about?",
        "subtitle": "The Paper at a Glance",
        "context": "Metastatic solid tumors remain the leading cause of cancer death worldwide. CAR T cell therapy has transformed outcomes in B cell malignancies — patients with relapsed or refractory B cell lymphoma achieve durable remissions. But in solid tumors like lung cancer and melanoma, CAR T cells fail to expand, persist, or control disease. This paper asks a precise mechanistic question: can tumor-directed radiotherapy overcome the barriers that defeat CAR T cells in solid tumors?",
        "finding": "A single 8 Gy dose of thoracic radiotherapy, combined with adoptive transfer of CAR T cells, dramatically extends CAR T cell persistence and eliminates established lung metastases — without increasing toxicity to normal tissue. The mechanism is a previously undescribed role for dendritic cells: irradiation conditions tumor cells to transfer intact surface antigens onto DCs, which then re-stimulate CAR T cells through the chimeric receptor, sustaining expansion selectively within the tumor.",
        "method": "Orthotopic syngeneic mouse models of extensive lung metastases: KP lung adenocarcinoma (C57BL/6 female mice) and B16-F10 melanoma. 8 Gy thoracic radiotherapy (TRT) delivered via RS2000 small animal irradiator (Rad Source Technologies, 160 kV, 2.1 Gy/min) followed 2 days later by adoptive transfer of lymphodepleted, syngeneic 28ζ CAR T cells targeting hCD19, GD2, or EpCAM.",
        "figKey": None,
        "authors": "Navarre S, Ishibashi MN, Nair A et al. | Nature Cancer, 2026",
        "doi": "https://doi.org/10.1038/s43018-026-01167-6",
        "extraHtml": None
    },
    {
        "id": 1,
        "name": "THRESHOLD",
        "color": "#ef5350",
        "glow": "#b71c1c",
        "question": "Why do CAR T cells fail in solid tumors?",
        "subtitle": "The Unsolved Problem",
        "context": "CAR T cell therapy revolutionized treatment for B cell malignancies — patients with advanced CD19+ lymphoma achieve complete remissions at rates unmatched by prior therapies. But when oncologists attempted the same approach in solid tumors, the results were stark: CAR T cells fail to expand within the immunosuppressive tumor microenvironment, disappear within days, and produce no meaningful clinical responses.",
        "finding": "Two problems converge to defeat CAR T cells in solid tumors: (1) an immunosuppressive tumor microenvironment that prevents CAR T cell activation and persistence, and (2) a dangerously narrow therapeutic window — doses sufficient to achieve antitumor effects cause fatal on-target, off-tumor toxicity in normal tissue that shares the target antigen. No existing strategy resolves both barriers simultaneously.",
        "method": "Historical clinical evidence cited by the authors: (1) Fatal cytokine storm with pulmonary edema reported at 1×10¹⁰ HER2 (ERBB2)-targeted CAR T cells — Morgan et al., 2010, J Mol Ther — a landmark cautionary trial demonstrating on-target off-tumor toxicity. (2) No objective radiographic responses at doses ≤3×10⁸ mesothelin-targeted CAR T cells in mesothelioma patients. (3) CAR transgene undetectable in multiple organs at autopsy in subsequent solid tumor CAR T trials. These historical failures set the stage for the problem this paper addresses.",
        "figKey": None,
        "authors": None,
        "doi": None,
        "extraHtml": "<div class='stat-grid'><div class='stat-card'><span class='stat-n'>~0</span><span class='stat-l'>Durable remissions in solid tumor CAR T clinical trials to date</span></div><div class='stat-card'><span class='stat-n'>Fatal</span><span class='stat-l'>On-target off-tumor toxicity at therapeutic doses in HER2 CAR T trial (Morgan et al., 2010)</span></div><div class='stat-card'><span class='stat-n'>None</span><span class='stat-l'>Prior strategy that solved both efficacy and toxicity simultaneously</span></div></div>"
    },
    {
        "id": 2,
        "name": "CATALYST",
        "color": "#ffd54f",
        "glow": "#f57f17",
        "question": "Does tumor irradiation boost CAR T cell efficacy?",
        "subtitle": "The Discovery",
        "context": "The researchers hypothesized that tumor-directed radiotherapy — precisely targeted to the thorax, not the whole body — might remodel the tumor immune microenvironment in a way that enhances CAR T cell activity. They tested a single 8 Gy dose of thoracic radiation (TRT) in mice bearing established lung metastases, followed by adoptive transfer of CAR T cells two days later.",
        "finding": "8 Gy of thoracic irradiation, combined with CAR T cells, produced dramatic and sustained reductions in tumor bioluminescence and significantly improved survival. CD8+ CAR T cell numbers were <strong>~8-fold higher</strong> in irradiated tumor-bearing lungs compared to unirradiated controls — but not in tumor-draining lymph nodes or adjacent normal tissue, demonstrating spatial selectivity. Neither TRT alone nor CAR T cells alone produced durable responses; the combination was required.",
        "method": "C57BL/6 female mice injected i.v. with 5×10⁵ KP19 (KP lung adenocarcinoma expressing hCD19) cells. 3 weeks after tumor inoculation, mice received 8 Gy TRT (RS2000 irradiator, Rad Source Technologies; 160 kV photons, 2.1 Gy/min) via thoracic anterior-posterior fields with lead shielding of head/neck and abdomen. Cyclophosphamide lymphodepletion 3–4 days before i.v. transfer of 4×10⁶ syngeneic h1928ζ (CD28/CD3ζ) CAR T cells 2 days post-TRT. Tumor burden tracked by bioluminescence imaging; CAR T cells quantified by flow cytometry in lungs at days 3, 9, and 15 post-transfer.",
        "figKey": "fig1",
        "authors": None,
        "doi": None,
        "extraHtml": None
    },
    {
        "id": 3,
        "name": "SIGNAL",
        "color": "#26c6da",
        "glow": "#006064",
        "question": "What changes inside CAR T cells after irradiation?",
        "subtitle": "The Reprogramming",
        "context": "Finding 8-fold more CAR T cells in irradiated tumors raised an important question: were these cells phenotypically and functionally different from CAR T cells in unirradiated tumors, or were they simply more numerous? To answer this, the team performed bulk RNA sequencing on CAR T cells isolated and FACS-sorted from irradiated versus unirradiated tumor-bearing lungs.",
        "finding": "<strong>522 differentially expressed genes</strong> distinguished CAR T cells from irradiated versus unirradiated tumors. Cells from irradiated tumors upregulated pathways for mitochondrial respiration and oxidative phosphorylation, effector function genes including granzyme B (<em>Gzmb</em>) and Rab27a (secretory vesicle trafficking), and IL-2 receptor signaling. Surface expression of co-inhibitory receptors PD-1 and TIGIT was elevated — yet these cells remained highly cytotoxic in direct killing assays. The authors interpret this as a profile of heightened activation, not terminal exhaustion.",
        "method": "CD8+ DsRed+ CAR T cells FACS-sorted from enzymatically dissociated tumor-bearing lungs 10–12 days after adoptive transfer (n=5 per group). Bulk RNA-seq libraries prepared and analyzed using DESeq2 (adjusted P<0.05). Gene set enrichment: WikiPathways and Gene Ontology over-representation analysis (WEBGestalt). Surface protein expression confirmed by flow cytometry on a BD LSR Fortessa or CYTEK Aurora. Data deposited: GSE263352.",
        "figKey": "fig2",
        "authors": None,
        "doi": None,
        "extraHtml": None
    },
    {
        "id": 4,
        "name": "GUARDIAN",
        "color": "#66bb6a",
        "glow": "#1b5e20",
        "question": "Are dendritic cells the key to persistence?",
        "subtitle": "The Essential Player",
        "context": "The persistent elevation of CAR T cells in irradiated tumors, despite ongoing antigen, was unexpected. Something in the irradiated tumor microenvironment was actively sustaining them. The team suspected conventional dendritic cells (cDCs) — the most potent professional antigen-presenting cells. Previous work had suggested DCs were not required for CAR T cell responses, since CAR T cells use a chimeric receptor that bypasses MHC-I-dependent antigen presentation.",
        "finding": "Selective depletion of conventional DCs using Zbtb46-DTR bone marrow chimeras <strong>completely abolished the irradiation benefit</strong>: without DCs, CAR T cell numbers declined with identical kinetics in irradiated and unirradiated mice, and tumors relapsed. In contrast, depletion of macrophages using anti-CSF1R antibody had no effect on CAR T cell persistence. Both DC1 (XCR1+ cross-presenting) and DC2 (SiglecH⁻) subsets, when sorted from irradiated tumor-bearing lungs, were capable of antigen dressing and expanding CAR T cells in vitro. DCs are therefore the essential intermediary between irradiation and sustained CAR T cell persistence.",
        "method": "DC depletion via Zbtb46-DTR bone marrow chimeras: Zbtb46DTR/DTR donor BM transplanted into WT C57BL/6 recipients using nongenotoxic anti-CD117 (c-Kit) saporin-conjugate immunodepletion of host hematopoietic progenitors; diphtheria toxin (DT) administered to selectively deplete cDCs. Macrophage depletion: anti-CSF1R antibody; depletion confirmed by ≥50% reduction of MERTK+ lung macrophages by flow cytometry. DC subsets (DC1: XCR1+; DC2: SiglecH⁻) sorted by FACS from CD45+CD3−mCD19−Ly6G− lung single-cell suspensions 10 days post-TRT (GSE316247).",
        "figKey": "fig3",
        "figKey2": "fig5",
        "authors": None,
        "doi": None,
        "extraHtml": None
    },
    {
        "id": 5,
        "name": "BRIDGE",
        "color": "#ab47bc",
        "glow": "#4a148c",
        "question": "How exactly do DCs activate CAR T cells?",
        "subtitle": "The Molecular Mechanism",
        "context": "DCs are indispensable — but the mechanism was baffling. Conventional DC biology holds that DCs activate T cells by presenting peptide fragments on MHC molecules to T cell receptors. But CAR T cells carry a chimeric antigen receptor that bypasses MHC entirely; their activation is MHC-independent. How, then, could DCs be driving CAR T cell expansion? The answer required a completely new way of thinking about antigen presentation.",
        "finding": "Irradiation causes tumor cells to transfer <strong>intact, membrane-bound surface antigens</strong> directly onto DCs through a trogocytic process — termed <em>antigen dressing</em>. DCs acquire full-length target protein on their own surface, not processed peptides. Trypsin treatment of antigen-dressed DCs removed the eGFP signal, confirming true surface display rather than endocytosed antigen. These antigen-dressed DCs directly engage CAR T cells via the chimeric receptor, driving proliferative expansion. Antigen-dressed macrophages did not expand CAR T cells, demonstrating DC-specific co-stimulatory signals are also required beyond antigen display alone.",
        "method": "Bone marrow-derived DCs (BMDCs) generated over 9 days in GM-CSF and cocultured with nonenzymatically dissociated irradiated hCD19–eGFP+ KP tumor cells (DC:tumor ratio 1:10). Antigen dressing quantified as %eGFP+ among CD11c+ cells by flow cytometry. Surface vs intracellular localization confirmed by trypsinization prior to staining. In vivo antigen-dressed DCs identified in tumor-bearing lungs by flow cytometry. CAR T cell expansion measured over 7 days in coculture with antigen-dressed DCs sorted from irradiated tumors. Specificity confirmed using non-targeting scFv control CAR T cells.",
        "figKey": "fig4",
        "authors": None,
        "doi": None,
        "extraHtml": None
    },
    {
        "id": 6,
        "name": "FRONTIER",
        "color": "#ff7043",
        "glow": "#bf360c",
        "question": "Does this work for real cancers — without toxicity?",
        "subtitle": "The Clinical Promise",
        "context": "Prior experiments used hCD19, an artificial antigen not expressed in normal mouse tissue, avoiding on-target off-tumor toxicity by design. Clinically relevant cancer antigens — GD2 (expressed on melanoma but also normal peripheral nerve and brain) and EpCAM (expressed on lung adenocarcinoma but also normal lung epithelium) — are shared with healthy tissue. The key question: would irradiation drive tumor-selective CAR T cell expansion even when the target antigen is abundantly expressed in adjacent normal tissue?",
        "finding": "Yes. Despite normal lung tissue expressing <strong>37-fold more EpCAM+ cells than GD2+ cells</strong>, GD2-targeted and EpCAM-targeted CAR T cells expanded potently inside irradiated tumors but remained at equivalently low numbers in adjacent normal lung parenchyma — in both irradiated and unirradiated mice. Critically, irradiated EpCAM CAR T cell-treated mice showed no increase in body weight loss and no acute lethality compared to controls. Irradiation widened the therapeutic window: antitumor efficacy equivalent to hCD19 CAR T cells was achieved without measurable increase in normal-tissue toxicity.",
        "method": "B16-F10 subcutaneous-to-lung melanoma model: GD2 28ζ CAR T cells (3×10⁶). KP lung adenocarcinoma: EpCAM 28ζ CAR T cells (scFv clone G8.8; 3×10⁶). All mice received cyclophosphamide lymphodepletion. Antigen expression in tumor vs normal tissue quantified by flow cytometry and histology. Intratumoral vs adjacent normal lung parenchyma CAR T cell density measured by immunohistochemistry with AEC chromogen (StarDist segmentation). Toxicity assessed by body weight, lung histopathology, and acute lethality.",
        "figKey": "fig6",
        "authors": None,
        "doi": None,
        "extraHtml": None
    },
    {
        "id": 7,
        "name": "HORIZON",
        "color": "#b0bec5",
        "glow": "#37474f",
        "question": "What does this mean for patients — and what remains to be proven?",
        "subtitle": "Implications & Limitations",
        "context": "Every rigorous study earns the right to speculate — and carries the obligation to name what it has not yet proven. The authors present a coherent mechanistic model with potential clinical implications, while explicitly identifying the boundaries of the current evidence. Understanding both is essential for translating this work toward patients.",
        "finding": "This study establishes a <strong>three-mechanism radiobiological model</strong>: irradiation (1) conditions tumor cells for trogocytic antigen transfer to DCs, (2) licenses productive DC–CAR T cell engagement that is functionally absent without irradiation, and (3) drives spatially restricted CAR T cell expansion selectively within the irradiated tumor microenvironment — sparing adjacent normal tissue. The data suggest that <em>hypofractionated conformal radiotherapy</em> (which spares uninvolved tissue) may achieve equivalent immune conditioning to the bilateral lung fields used experimentally. If confirmed in humans, widening the therapeutic window through irradiation could unlock CAR T cell efficacy for a broad range of solid tumors accessible to radiotherapy — without proportionally increasing toxicity.",
        "method": "Scope of current evidence — mouse models only: orthotopic KP lung adenocarcinoma and subcutaneous B16-F10 melanoma in female C57BL/6 mice. Low-dose radiation (TBI or focal low-dose) did not enhance CAR T cell persistence in these models. Optimal radiation fractionation schedule untested: three fractions of 4 Gy showed a delayed benefit with EpCAM CAR T cells; single 8 Gy remains best-characterized. Endogenous T cells did not significantly contribute to tumor control in this model. Precise DC-derived co-stimulatory signals beyond antigen display remain undefined. Whether antigen dressing by DCs occurs in human tumor biopsies after radiotherapy has not yet been demonstrated.",
        "figKey": None,
        "authors": "Navarre S, Ishibashi MN, Nair A et al. | Nature Cancer, 2026",
        "doi": "https://doi.org/10.1038/s43018-026-01167-6",
        "extraLabel": "Discussion",
        "extraHtml": "<div style='display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:.5rem'><div><div style='font-family:JetBrains Mono,monospace;font-size:.55rem;letter-spacing:.3em;color:#b0bec5;text-transform:uppercase;margin-bottom:.7rem;opacity:.7'>Clinical Implications</div><div style='font-size:.83rem;line-height:2;color:rgba(255,255,255,.72)'>→ New rationale for TRT + CAR T combination<br>→ Therapeutic window widens without added toxicity<br>→ DC antigen dressing as a CAR design target<br>→ Applicable to any tumor accessible to focal RT<br>→ Hypofractionated conformal RT may suffice</div></div><div><div style='font-family:JetBrains Mono,monospace;font-size:.55rem;letter-spacing:.3em;color:rgba(255,120,100,.7);text-transform:uppercase;margin-bottom:.7rem'>Current Limitations</div><div style='font-size:.83rem;line-height:2;color:rgba(255,255,255,.52)'>⚠ Pre-clinical mouse models only<br>⚠ Female C57BL/6 mice exclusively<br>⚠ Optimal RT fractionation undefined<br>⚠ DC antigen dressing in humans unverified<br>⚠ Precise DC co-stimulatory signals unknown</div></div></div>"
    }
]

# Build figures JS snippet
figures_js_lines = []
for key, val in figs.items():
    figures_js_lines.append(f'  "{key}": "{val}"')
figures_js = '{\n' + ',\n'.join(figures_js_lines) + '\n}'

planets_js = json.dumps(PLANETS_DATA, ensure_ascii=False, indent=2)

# Read HTML template
with open('template.html', 'r') as f:
    html = f.read()

html = html.replace('/*PLANETS_DATA*/', f'const PLANETS = {planets_js};')
html = html.replace('/*FIGURES_DATA*/', f'const FIGURES = {figures_js};')

with open('index.html', 'w') as f:
    f.write(html)

size_kb = os.path.getsize('index.html') // 1024
print(f'Built index.html: {size_kb} KB')

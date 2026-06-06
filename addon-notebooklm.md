# Studio Add-On: Technical Specification & Plan

## Executive Summary

Build an enterprise-grade content creation surface ("Studio") for the Insight platform that enables users to reference documents, perform AI-powered research, and produce company-branded deliverables — presentations, one-pagers, meeting briefs, status updates, and more — using corporate templates. Studio is a separate UI surface accessible via a top-level toggle in the app navigation, positioned as the "builder" counterpart to the main Search & Chat experience. Priced per-seat as a paid add-on.

Studio leverages Insight's existing RAG infrastructure, Projects system, LLM integration, Voice/TTS pipeline, and shared service layer (template rendering, PPTX generation, audio synthesis), while maintaining a purpose-built UX optimized for meeting content preparation and structured deliverable creation.

---

## 1. Product Vision & Features

### 1.1 Core Capabilities (Google NotebookLM Parity)

| Feature | Description |
|---------|-------------|
| **Notebook (Source Collection)** | Users curate a set of sources (uploaded files, connector documents, URLs, text). Answers are grounded exclusively in these sources. |
| **Grounded Chat** | RAG-based Q&A scoped to the notebook's sources. Zero hallucination design: LLM refuses to answer if context is insufficient. In-line citations with page/section references. |
| **Study Guide / Briefing Doc** | One-click generation of structured reports (study guides, FAQs, timelines, executive briefs) from the notebook sources. |
| **Mind Map** | Interactive concept map generated from source relationships. |
| **Flashcards & Quizzes** | Auto-generated Q&A cards and multiple-choice questions grounded in sources. |
| **Audio Overview (Podcast)** | Multi-speaker conversational audio synthesis from notebook content. Customizable speaker personas and TTS voices. |

### 1.2 Enterprise Differentiators

| Feature | Description |
|---------|-------------|
| **Company-Branded Templates** | Admin uploads DOCX/PPTX templates with corporate branding. All generated artifacts (reports, slides, briefs) render into these templates. |
| **Template Library** | Organization-wide library of approved templates (executive brief, quarterly review, project update, sales deck, one-pager, status update, etc.). |
| **Presentation Generation** | One-click PPTX generation from project sources using corporate slide masters. |
| **Meeting Prep Workflows** | Purpose-built flows for common meeting outputs: board deck, weekly status, leadership update, RFP response, one-pager. |
| **RBAC & Sharing** | Projects inherit Insight's existing permission model: private, shared-with-team, organization-wide. |
| **Connector-Sourced Projects** | Pull sources from any of the 50+ connectors (Confluence, Slack, Google Drive, SharePoint, etc.) in addition to uploads. |
| **Deep Research Mode** | Multi-step agentic research (leveraging existing Deep Research pipeline) scoped to project sources + optional web search. |
| **Citation Viewer** | Click a citation to jump to the exact page/section in the source PDF/document with text highlighting. |
| **Export Flexibility** | Export to DOCX, PPTX, PDF, Markdown, HTML. All use brand templates where applicable. |

---

## 2. Codebase Analysis: What Already Exists

### 2.1 Directly Reusable Components

| Existing Module | Location | Relevance |
|----------------|----------|-----------|
| **Projects** | `backend/onyx/server/features/projects/` | 1:1 mapping to "Notebook" concept. UserProject has files, chat sessions, instructions. |
| **User Files** | `backend/onyx/db/user_file.py`, `db/projects.py` | File upload, chunking, embedding, indexing pipeline. |
| **Chat + RAG** | `backend/onyx/chat/`, `server/query_and_chat/` | Full LLM conversation loop with citation extraction and streaming. |
| **Deep Research** | `backend/onyx/deep_research/` | Multi-cycle orchestrator with research agents and final report generation. |
| **Voice / TTS** | `backend/onyx/voice/` | OpenAI, ElevenLabs, Azure TTS with streaming. Already supports multi-voice. |
| **Craft (Build Mode)** | `backend/onyx/server/features/build/` | Sandbox system running AI agents that produce web apps, markdown, PPTX. Has PPTX skill. |
| **Connectors** | `backend/onyx/connectors/` (50+) | Pull documents from enterprise sources into notebooks. |
| **Document Sets** | `backend/onyx/db/document_set.py` | Curated document collections with access control. |
| **Search Tool** | `backend/onyx/tools/tool_implementations/search/` | Internal semantic search scoped to document sets/files. |
| **File Processing** | `backend/onyx/file_processing/` | PDF, DOCX, PPTX, HTML, images extraction pipeline. |
| **Feature Flags** | `backend/onyx/feature_flags/` | PostHog-based feature gating for gradual rollout. |
| **Hooks** | `backend/onyx/hooks/` | Pipeline extension points (document ingestion, query processing). |

### 2.2 Extension Points for Add-On Architecture

1. **Feature Flag Gate**: Like Craft (`ONYX_CRAFT_ENABLED_FLAG`), gate Studio behind a feature flag (`studio-addon-enabled`).
2. **Router Registration**: Add a new router group in `main.py` under `/studio` prefix, gated by the flag + per-seat entitlement.
3. **Projects as Studio Projects**: Extend `UserProject` model with studio-specific metadata (output_format_preferences, template_id, audio_config).
4. **Settings Extension**: Add `studio_enabled: bool` to the `Settings`/`UserSettings` model.
5. **Template Store**: New DB model + file_store integration for admin-managed brand templates.
6. **Shared Service Layer**: Template rendering, PPTX generation, and TTS services live in a shared location usable by both Craft and Studio.

---

## 3. Open-Source Landscape & Reference Implementations

### 3.1 Open-Source NotebookLM Alternatives

| Project | Stars | Key Strengths | License |
|---------|-------|---------------|---------|
| **[lfnovo/open-notebook](https://github.com/lfnovo/open_notebook)** | 12k+ | Most complete: multi-model, 1-4 speaker podcasts, REST API, Docker, MCP integration, content transformations, Next.js frontend | MIT |
| **[2212-spc/Open-NotebookLM](https://github.com/2212-spc/Open-NotebookLM)** | 8k+ | Full-featured: PPT gen, mind maps, podcasts, DrawIO diagrams, flashcards, quizzes, deep research, Supabase auth | Apache-2.0 |
| **[souzatharsis/podcastfy](https://github.com/souzatharsis/podcastfy)** | 5k+ | Best-in-class podcast generation: 100+ LLM models, multi-language, multi-speaker, CLI + Python API | Apache-2.0 |
| **[plaban1981/Mimic_notebookllm](https://github.com/plaban1981/Mimic_notebookllm)** | 2k+ | Citation-first: page numbers, interactive citations UI, Milvus vector DB, Zep memory | MIT |
| **[gabrielchua/open-notebooklm](https://github.com/gabrielchua/open-notebooklm)** | 10k+ | Original open-source NotebookLM podcast implementation. MeloTTS + Bark audio synthesis | Apache-2.0 |

### 3.2 Content Generation Libraries

| Library | Use Case | Integration Path |
|---------|----------|-----------------|
| **[python-docx-template (docxtpl)](https://docxtpl.readthedocs.io/)** | Render branded DOCX from Jinja2 templates | LLM generates structured data, docxtpl renders into corporate template |
| **[pptx-cli](https://pypi.org/project/pptx-cli/)** | Template-bound PPTX generation with manifest validation | Lock deck generation to approved corporate layouts |
| **[PptxGenJS](https://github.com/gitbrent/PptxGenJS)** | Programmatic PPTX generation (already used in Craft sandbox) | Extend Craft PPTX skill for notebook-scoped generation |
| **[Pandoc](https://pandoc.org/)** | Markdown to DOCX/PDF with `--reference-doc` for branding | Convert LLM markdown output to branded documents |
| **[docsmith](https://github.com/dawsonlp/docsmith)** | YAML-in, Word-out. Built for LLM pipelines | Structured LLM output directly to DOCX |
| **[Marp CLI](https://github.com/marp-team/marp-cli)** | Markdown to branded PPTX/PDF with custom CSS themes | Alternative lightweight presentation path |

### 3.3 Audio/Podcast Generation

| Library | Use Case | Integration Path |
|---------|----------|-----------------|
| **[lfnovo/podcast-creator](https://github.com/lfnovo/podcast-creator)** | LangGraph-based podcast pipeline: outline, dialogue, TTS | pip-installable, multi-provider TTS, Jinja2 prompt templates |
| **[Podcastfy](https://github.com/souzatharsis/podcastfy)** | Multi-modal content to podcast conversion | Standalone Python package, 100+ LLM models, multi-language |
| **[Dia TTS Server](https://github.com/devnen/Dia-TTS-Server)** | Native 2-speaker dialogue with non-verbal sounds | FastAPI server, OpenAI-compatible endpoint, voice cloning |
| **[pyKokoro](https://github.com/holgern/pykokoro)** | Local ONNX-based TTS, 54+ voices, 8 languages | Zero API cost, runs on CPU, privacy-first |
| **Insight Voice Module** | Already has OpenAI, ElevenLabs, Azure TTS | Extend `VoiceProviderInterface` for multi-speaker podcast |

### 3.4 Citation & Grounding

| Approach | Implementation |
|----------|---------------|
| **Page-level metadata in chunks** | Insight already stores chunk metadata. Extend to include `page_number`, `section_title`. |
| **PDF text highlighting** | Use PyMuPDF (`fitz`) to find retrieved chunk text on source PDF page, return highlight coordinates. |
| **Structured citations in LLM output** | Use Pydantic structured output to extract `{source_file, page_number, quote}` from LLM responses. |
| **Citation viewer component** | Frontend PDF viewer (e.g., `react-pdf`) with annotation overlay for highlighted passages. |

---

## 4. Architecture Design

### 4.1 Surface Architecture Decision

**Decision: Separate Surface, Shared Services**

Studio is its own top-level route and purpose-built UX, but delegates generation tasks to a shared service layer that Craft can also consume.

**Rationale:**
- Studio's UX paradigm (curated sources → structured one-click outputs) is fundamentally different from Craft's (freeform prompt → agent-driven creative output)
- Studio enforces strict source grounding at the retrieval layer (not a prompt instruction) — different trust model than Craft
- Studio is lightweight (no sandbox provisioning, no K8s pods for Q&A) — sub-second chat latency
- Template rendering, TTS, and PPTX generation are shared services — built once, consumed by both surfaces
- Clear product positioning: Studio = research & meeting deliverables, Craft = creative/code generation

```
┌─────────────────────────────────────────────────────────────────┐
│                      Shared Service Layer                         │
│                                                                   │
│  TemplateRenderer     │  PodcastGenerator   │  PPTX Generator    │
│  (docxtpl/pandoc)     │  (script + TTS)     │  (pptx-cli)        │
│                                                                   │
│  LLM Gateway (LiteLLM)   │  File Store   │  Voice Providers     │
└───────────┬─────────────────────────────────────────┬────────────┘
            │                                         │
┌───────────▼─────────────────┐        ┌──────────────▼────────────┐
│        Studio UI             │        │        Craft UI            │
│      /app/studio/            │        │      /app/craft/           │
│                              │        │                            │
│  - Source panel              │        │  - Chat + live preview     │
│  - Grounded chat             │        │  - Sandbox agent           │
│  - Generate panel (1-click)  │        │  - Web app builder         │
│  - Citation viewer           │        │  - File browser            │
│  - Template picker           │        │                            │
└──────────────────────────────┘        └────────────────────────────┘
```

### 4.2 UI Navigation & Surface Switching

Studio is accessed via a top-level toggle in the app header, establishing it as an equal-weight surface to the main Search & Chat experience.

```
┌────────────────────────────────────────────────────────────────┐
│  [Logo]   [ Search & Chat | Studio ]             [User] [⚙️]   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  (active surface content)                                       │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

**Navigation behavior:**
- Toggle is always visible in the app header for all users (drives awareness/upsell)
- Non-entitled users see an upgrade modal on click
- Entitled users enter the Studio surface
- Left sidebar and main content area change completely on switch
- URL changes to `/app/studio/*` routes
- Browser back/forward navigation works naturally between surfaces

**Studio surface layout:**

```
┌────────────────────────────────────────────────────────────────────┐
│  [Logo]   [ Search & Chat | Studio ▾ ]              [User] [⚙️]    │
├──────────────┬─────────────────────────────────────────────────────┤
│              │                                                      │
│  Projects    │   Project: "Q3 Board Update"                        │
│              │                                                      │
│  ──────────  │   ┌──────────────────┐  ┌─────────────────────┐    │
│  > Q3 Board  │   │ Sources (12)      │  │ Generate             │    │
│  > RFP Resp  │   │                   │  │                      │    │
│  > Weekly    │   │ • quarterly.pdf   │  │ [Board Deck]         │    │
│  > Onboard   │   │ • metrics.xlsx    │  │ [One-Pager]          │    │
│              │   │ • confluence/OKRs  │  │ [Executive Brief]    │    │
│  ──────────  │   │ • slack/#q3-rev   │  │ [Meeting Prep]       │    │
│              │   └──────────────────┘  │ [Status Update]      │    │
│  Templates   │                          │ [Audio Overview]     │    │
│              │   ┌──────────────────────┴─────────────────────┐    │
│  ──────────  │   │ Grounded Chat                               │    │
│              │   │ "Summarize the key metrics from Q3..."       │    │
│  Artifacts   │   │                                             │    │
│              │   └─────────────────────────────────────────────┘    │
└──────────────┴─────────────────────────────────────────────────────┘
```

### 4.3 High-Level System Architecture

```
                         ┌─────────────────────────────────────┐
                         │           Frontend (Next.js)          │
                         │   /app/studio/*  routes               │
                         │   ProjectView, SourcePanel,           │
                         │   GeneratePanel, CitationViewer       │
                         └──────────────┬──────────────────────┘
                                        │ REST + SSE
                         ┌──────────────▼──────────────────────┐
                         │       API Server (FastAPI)            │
                         │   /studio/* router group              │
                         │   StudioService orchestrates:         │
                         │     - SourceManager                   │
                         │     - GroundedChatService             │
                         │     - GenerationService (artifacts)   │
                         │     - TemplateService (branding)      │
                         │     - PodcastService (audio)          │
                         └──────────────┬──────────────────────┘
                                        │
              ┌─────────────────────────┼────────────────────────┐
              │                         │                         │
    ┌─────────▼────────┐    ┌──────────▼──────────┐   ┌─────────▼────────┐
    │  Existing RAG     │    │   Celery Workers     │   │  File Store       │
    │  Pipeline         │    │   (async generation) │   │  (MinIO/S3)       │
    │  - Embeddings     │    │   - Podcast gen      │   │  - Templates      │
    │  - Vespa search   │    │   - PPTX gen         │   │  - Generated docs │
    │  - Chat/LLM loop  │    │   - DOCX gen         │   │  - Audio files    │
    │  - Citations      │    │   - Deep Research    │   │  - Source files    │
    └──────────────────┘    └─────────────────────┘   └──────────────────┘
```

### 4.4 Database Schema (New Tables)

```sql
-- Per-seat entitlement for Studio add-on
CREATE TABLE studio_entitlement (
    id SERIAL PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    enabled BOOLEAN DEFAULT FALSE,
    seat_count INT NOT NULL DEFAULT 0,
    plan_tier TEXT NOT NULL DEFAULT 'starter',  -- 'starter', 'professional', 'enterprise'
    stripe_subscription_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tracks which users have been assigned a Studio seat
CREATE TABLE studio_seat_assignment (
    id SERIAL PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    assigned_by UUID REFERENCES "user"(id),
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, user_id)
);

-- Studio project config (extends UserProject with studio-specific settings)
CREATE TABLE studio_project_config (
    id SERIAL PRIMARY KEY,
    project_id INT UNIQUE NOT NULL REFERENCES user_project(id) ON DELETE CASCADE,
    output_preferences JSONB DEFAULT '{}',
    default_template_id INT REFERENCES brand_template(id),
    audio_config JSONB DEFAULT '{}',  -- speaker personas, voice model prefs
    source_scope TEXT DEFAULT 'files_only',  -- 'files_only', 'connectors', 'mixed'
    connector_ids INT[] DEFAULT '{}',
    document_set_ids INT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Admin-managed brand templates (shared service — usable by Craft and Studio)
CREATE TABLE brand_template (
    id SERIAL PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    template_type TEXT NOT NULL,  -- 'docx', 'pptx', 'pdf_theme'
    template_category TEXT,  -- 'board_deck', 'one_pager', 'status_update', 'executive_brief', 'meeting_prep', 'custom'
    file_id TEXT NOT NULL,  -- reference to file_store
    preview_image_id TEXT,
    is_default BOOLEAN DEFAULT FALSE,
    created_by UUID REFERENCES "user"(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Generated artifacts from a Studio project
CREATE TABLE studio_artifact (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id INT NOT NULL REFERENCES user_project(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES "user"(id),
    artifact_type TEXT NOT NULL,  -- 'board_deck', 'one_pager', 'executive_brief', 'meeting_prep', 'status_update', 'study_guide', 'flashcards', 'quiz', 'mind_map', 'podcast', 'custom_report'
    title TEXT NOT NULL,
    file_id TEXT,  -- reference to file_store (for downloadable artifacts)
    content_json JSONB,  -- structured content for in-app rendering
    template_id INT REFERENCES brand_template(id),
    generation_config JSONB DEFAULT '{}',
    status TEXT DEFAULT 'completed',  -- 'generating', 'completed', 'failed'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Podcast/audio overview metadata
CREATE TABLE studio_podcast (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    artifact_id UUID NOT NULL REFERENCES studio_artifact(id) ON DELETE CASCADE,
    script_json JSONB NOT NULL,  -- dialogue script with speaker assignments
    audio_file_id TEXT,  -- final mixed audio in file_store
    duration_seconds INT,
    speaker_config JSONB NOT NULL,  -- [{name, persona, voice_model, voice_id}]
    tts_provider TEXT NOT NULL,  -- 'openai', 'elevenlabs', 'azure', 'local'
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.5 Backend Module Structure

```
backend/onyx/server/features/studio/
├── __init__.py
├── api.py                     # FastAPI router (/studio/*)
├── models.py                  # Pydantic request/response models
├── service.py                 # StudioService orchestrator
├── entitlement.py             # Per-seat entitlement checks
├── source_manager.py          # Source curation (files, connectors, URLs)
├── grounded_chat.py           # Chat scoped to project sources (strict grounding)
├── generators/
│   ├── __init__.py
│   ├── board_deck.py          # Board presentation generation
│   ├── one_pager.py           # One-pager / executive summary
│   ├── meeting_prep.py        # Meeting preparation brief
│   ├── status_update.py       # Leadership status update
│   ├── study_guide.py         # Study guide / briefing generation
│   ├── flashcards.py          # Flashcard generation
│   ├── quiz.py                # Quiz generation
│   ├── mind_map.py            # Mind map generation (Mermaid output)
│   └── custom_report.py       # Custom report generation
├── podcast/
│   ├── __init__.py
│   ├── script_generator.py    # LLM-driven dialogue script
│   ├── audio_synthesizer.py   # Multi-speaker TTS orchestration
│   └── models.py              # Speaker personas, episode config
├── citations/
│   ├── __init__.py
│   ├── extractor.py           # Extract structured citations from LLM output
│   └── highlighter.py         # PDF page highlighting coordinates
└── prompts/
    ├── board_deck.py
    ├── one_pager.py
    ├── meeting_prep.py
    ├── status_update.py
    ├── study_guide.py
    ├── flashcards.py
    ├── quiz.py
    ├── mind_map.py
    └── podcast_script.py

# Shared services (consumed by both Studio and Craft)
backend/onyx/services/
├── __init__.py
├── templates/
│   ├── __init__.py
│   ├── template_manager.py    # CRUD for brand templates
│   └── renderer.py            # docxtpl / pptx-cli / pandoc rendering
└── audio/
    ├── __init__.py
    └── podcast_generator.py   # Multi-speaker audio synthesis orchestration
```

### 4.6 Frontend Structure

```
web/src/app/app/studio/
├── layout.tsx                  # Studio layout (sidebar + main content)
├── page.tsx                    # Project list / create new project
├── [id]/
│   ├── page.tsx               # Studio project workspace (three-panel)
│   ├── components/
│   │   ├── SourcePanel.tsx    # Left panel: source list, upload, connector picker
│   │   ├── ChatPanel.tsx      # Center: grounded chat with inline citations
│   │   ├── GeneratePanel.tsx  # Right: one-click generation buttons
│   │   ├── CitationViewer.tsx # PDF viewer with text highlighting
│   │   ├── ArtifactCard.tsx   # Generated artifact display + download
│   │   ├── TemplatePicker.tsx # Select brand template before generation
│   │   ├── PodcastPlayer.tsx  # Audio player with transcript sync
│   │   ├── MindMapView.tsx    # Interactive mind map (Mermaid)
│   │   ├── FlashcardView.tsx  # Flashcard carousel
│   │   └── QuizView.tsx       # Interactive quiz UI
│   └── hooks/
│       ├── useStudioProject.ts
│       ├── useGroundedChat.ts
│       ├── useArtifacts.ts
│       └── useEntitlement.ts
├── admin/
│   └── templates/
│       ├── page.tsx            # Admin: manage brand templates
│       └── components/
│           └── TemplateUpload.tsx
└── components/
    ├── StudioNavToggle.tsx     # The top-level surface switch component
    ├── UpgradeModal.tsx        # Shown to non-entitled users
    └── SeatManagement.tsx      # Admin: assign/revoke Studio seats

web/src/components/header/
└── SurfaceToggle.tsx           # Reusable toggle: [Search & Chat | Studio]
```

---

## 5. Implementation Strategy

### Phase 1: Foundation & Entitlement (Weeks 1-3)

**Goal:** Studio surface, per-seat entitlement, project CRUD, source management, grounded chat.

1. Add `studio_entitlement`, `studio_seat_assignment`, `studio_project_config` tables and migrations.
2. Build entitlement middleware:
   - API dependency that checks `studio_seat_assignment` for the current user
   - Returns 403 with upgrade payload for non-entitled users
   - Admin endpoints for seat assignment/revocation
3. Create `/studio` API router gated by feature flag + entitlement.
4. Frontend: `SurfaceToggle` component in the app header (always visible). Upgrade modal for non-entitled users.
5. Extend `UserProject` to support Studio mode (detected via `studio_project_config` existence).
6. Build `SourceManager` that aggregates:
   - UserFiles in the project
   - Documents from specified connector document sets
   - URLs scraped on-demand
7. Build `GroundedChatService` that:
   - Scopes search to project sources only (filter by file IDs / document set IDs in Vespa query)
   - Uses existing chat/LLM loop with modified system prompt enforcing source-only grounding
   - Extracts structured citations (source, page, quote) via Pydantic structured output
8. Frontend: Three-panel Studio workspace with project sidebar, source panel, and grounded chat.

### Phase 2: Meeting Content Generators (Weeks 4-6)

**Goal:** One-click generation of meeting deliverables (board deck, one-pager, meeting prep, status update).

1. Add `studio_artifact` table and migration.
2. Implement primary generators (meeting-focused):
   - `board_deck.py`: Generate structured slide content from sources. Output as JSON slide manifest.
   - `one_pager.py`: Single-page executive summary with key metrics, decisions, and next steps.
   - `meeting_prep.py`: Talking points, anticipated questions, background context for a meeting.
   - `status_update.py`: Progress report with accomplishments, blockers, next steps.
3. Implement secondary generators:
   - `study_guide.py`: Structured study guide from all project sources.
   - `flashcards.py`: Q&A pairs grounded in sources.
   - `quiz.py`: Multiple-choice questions with answer keys.
   - `mind_map.py`: Mermaid diagram syntax from source relationships.
4. Celery task for async artifact generation (long-running for large projects).
5. Frontend: GeneratePanel with one-click buttons, artifact cards, interactive viewers.

### Phase 3: Branded Content & Templates (Weeks 7-9)

**Goal:** Admin template management, branded DOCX/PPTX output via shared service layer.

1. Add `brand_template` table and migration.
2. Build shared `TemplateRenderer` service (in `backend/onyx/services/templates/`):
   - DOCX: Use `docxtpl` (Jinja2-in-Word) to fill corporate templates with LLM-generated structured content.
   - PPTX: Use `pptx-cli` manifest system for template-bound slide generation.
   - PDF: Use Pandoc with `--reference-doc` for branded PDF generation.
3. Build admin API for template CRUD:
   - Upload DOCX/PPTX templates with placeholder validation
   - Categorize templates (board_deck, one_pager, status_update, meeting_prep, custom)
   - Set org-wide defaults per category
4. Integrate template selection into all generators (template picker in GeneratePanel).
5. Frontend: Admin template management page, template preview, download buttons for branded exports.
6. Wire shared `TemplateRenderer` so Craft's PPTX skill can also use brand templates.

### Phase 4: Audio Overview / Podcast (Weeks 10-12)

**Goal:** Multi-speaker podcast generation from project content.

1. Add `studio_podcast` table and migration.
2. Build shared `PodcastGenerator` service (in `backend/onyx/services/audio/`):
   - `script_generator.py`: LLM generates dialogue script with speaker tags. Customizable format (interview, panel, monologue).
   - `audio_synthesizer.py`: Orchestrate multi-speaker TTS using existing `VoiceProviderInterface`. Per-speaker voice assignment.
3. Audio mixing: Concatenate per-speaker audio segments into final MP3 (use `pydub` or `ffmpeg`).
4. Celery task for async podcast generation (can take 2-5 minutes).
5. Frontend: PodcastPlayer with waveform, transcript sync, speaker labels.

### Phase 5: Advanced Features (Weeks 13-16)

**Goal:** Deep Research integration, citation viewer, full presentation pipeline, seat management.

1. **Deep Research Integration**: Extend existing `dr_loop.py` to accept project scope constraints. Add "Deep Research" button in Studio that runs multi-cycle research scoped to project sources + optional web.
2. **Citation Viewer**: Build PDF viewer component with highlight overlay. Backend returns highlight coordinates via PyMuPDF text search on source pages.
3. **Full Presentation Pipeline**:
   - LLM generates slide outline from project sources
   - Each slide rendered into corporate template layout via shared TemplateRenderer
   - Images/charts generated where applicable
   - Export as branded PPTX
4. **Sharing & Collaboration**: Projects shareable at team/org level. Shared users can chat but not modify sources.
5. **Seat Management UI**: Admin dashboard showing seat usage, assignment history, per-user generation metrics.

---

## 6. Key Technical Decisions

### 6.1 Studio = Separate Surface, Extended Project

Studio is a distinct UI surface with its own route (`/app/studio/`), but reuses the existing `UserProject` entity extended with `studio_project_config`. This maximizes reuse of:
- File upload/indexing pipeline
- Chat session association
- Access control (RBAC)
- Frontend project patterns

Studio does NOT use the Craft sandbox. It makes direct LLM calls and uses shared generation services. No K8s pod provisioning or agent execution model needed.

### 6.2 Grounding Strategy

- **Strict source scoping**: All Vespa queries include a filter for the project's file IDs / document set IDs. The LLM system prompt explicitly states "answer ONLY from the provided sources."
- **Architectural enforcement**: Source scoping is applied at the retrieval layer (Vespa filter), not just as a prompt instruction. The LLM never sees out-of-scope content.
- **Citation format**: Use Pydantic structured output to extract citations as `[{source_name, page_number, quote, relevance}]` alongside the main answer.
- **Confidence indicator**: If retrieval returns low-relevance chunks, surface a "low confidence" warning.

### 6.3 Template System (Shared Service)

- **Shared location**: `backend/onyx/services/templates/` — consumable by both Studio and Craft.
- **Storage**: Templates stored in MinIO/S3 via existing `file_store` abstraction.
- **Rendering pipeline**: LLM produces structured content (JSON/YAML/Markdown) → Template renderer fills corporate template → Binary file stored and served.
- **Categories**: Templates categorized by purpose (board_deck, one_pager, status_update, meeting_prep, executive_brief, custom).
- **Validation**: Template upload validates placeholder structure matches expected schema.

### 6.4 Audio Architecture (Shared Service)

- **Shared location**: `backend/onyx/services/audio/` — consumable by both Studio and Craft.
- **Reuse existing Voice module**: The `VoiceProviderInterface` already supports OpenAI, ElevenLabs, Azure. Extend with per-segment voice switching.
- **Script format**: `[{speaker: "Host", text: "...", emotion: "curious"}, {speaker: "Expert", text: "...", emotion: "authoritative"}]`
- **Progressive delivery**: Stream individual segments as they're synthesized, show progress in UI.
- **Local TTS option**: For privacy-sensitive deployments, integrate Kokoro/pyKokoro as an additional provider (ONNX, runs on CPU, zero API cost).

### 6.5 Per-Seat Pricing & Entitlement

- **Pricing model**: Per-seat (not per-generation, not per-project). Each seat is a named user who can access Studio.
- **Entitlement check**: API middleware verifies `studio_seat_assignment` for the requesting user. Non-entitled users receive 403 with upgrade payload.
- **UI behavior**:
  - Toggle always visible (awareness/upsell)
  - Non-entitled click → upgrade modal with pricing
  - Team has seats but user unassigned → "Request access from admin" flow
  - Entitled → enters Studio surface
- **Admin controls**: Org admin assigns/revokes seats from team settings.
- **Metering**: Track per-seat usage (projects created, artifacts generated, chat messages) for billing visibility and plan tier enforcement.

### 6.6 Feature Flag & Rollout

- Gate behind PostHog feature flag: `studio-addon-enabled`
- In self-hosted/local mode, controlled by `ENABLE_STUDIO_ADDON` env var (mirrors Craft pattern)
- During beta: flag controls visibility. Post-GA: entitlement controls access, flag used for kill-switch only.
- Plan tiers gate feature depth (e.g., starter = 3 templates, professional = unlimited templates + podcast, enterprise = all + API access)

---

## 7. Dependencies to Add

### Python (backend)

```
docxtpl>=0.20.0        # Jinja2-in-Word template rendering
pptx-cli>=1.2.0       # Template-bound PPTX generation (optional, evaluate vs Craft PPTX skill)
pydub>=0.25.0          # Audio segment concatenation
PyMuPDF>=1.24.0        # PDF text search for citation highlighting (already likely available)
mermaid-py>=0.5.0      # Mermaid diagram rendering (optional, can use frontend rendering)
```

### Node.js (frontend)

```
react-pdf             # PDF viewer with annotation support
mermaid               # Mind map rendering
```

---

## 8. Testing Strategy

| Layer | Type | Scope |
|-------|------|-------|
| **Grounded Chat** | Integration test | Verify chat refuses to answer without sources, citations are accurate |
| **Studio Generators** | External dependency unit test | Mock LLM, verify structured output parsing and artifact creation |
| **Template Renderer** | Unit test | Verify DOCX/PPTX rendering with known inputs produces valid files |
| **Podcast Pipeline** | External dependency unit test | Mock TTS, verify script generation and audio concatenation |
| **Citation Highlighter** | Unit test | Verify text search on known PDF pages returns correct coordinates |
| **E2E** | Playwright | Full notebook workflow: create, upload sources, chat, generate artifact, download |

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| **Large notebooks exceed context window** | Use iterative map-reduce for artifact generation. Chunk sources, generate per-chunk, then synthesize. |
| **PPTX template complexity** | Start with simple placeholder-based templates. Evaluate pptx-cli manifest validation for strict branding. |
| **Podcast generation latency** | Run as async Celery task with progress streaming. Show "generating..." UI with ETA. |
| **Citation accuracy** | Validate citations by re-retrieving the quoted text from the source. Flag unverifiable citations. |
| **Scope creep** | Phased delivery. Each phase is independently valuable. Phase 1+2 alone delivers significant value. |

---

## 10. Success Metrics

### Business Metrics
- **Seat conversion**: % of orgs that purchase Studio seats after seeing the toggle
- **Seat utilization**: % of assigned seats active in a given month
- **Revenue per seat**: MRR contribution per active Studio seat
- **Expansion rate**: Avg seat count growth per org over time

### Product Metrics
- **Adoption**: % of seat holders who create at least one project per month
- **Engagement**: Average artifacts generated per project per week
- **Time to first artifact**: Minutes from project creation to first generated deliverable
- **Grounding quality**: % of citations that can be verified against source text
- **Export usage**: Downloads of branded DOCX/PPTX per week
- **Template adoption**: % of generations that use a brand template vs. plain output
- **Podcast completion**: % of generated audio overviews listened to >50%
- **Surface switching**: How often users toggle between Search & Chat and Studio per session

---

## 11. Resolved Decisions

| # | Question | Decision |
|---|----------|----------|
| 1 | Integrate with Craft or separate surface? | **Separate surface** with shared service layer. Studio has its own UX optimized for meeting content creation; Craft remains the creative/code sandbox. Shared services (templates, audio, PPTX) prevent duplication. |
| 2 | Product name? | **Studio** — signals builder/creator energy, scales beyond meetings, pairs with "Search & Chat" as the other surface. |
| 3 | Navigation? | **Top-level toggle** in app header (top-left, next to logo). Equal weight to main app. Always visible for upsell. |
| 4 | Pricing model? | **Per-seat**. Each named user assigned a Studio seat by their org admin. Not usage-based, not per-project. |
| 5 | UI paradigm? | Purpose-built three-panel layout (sources, chat, generate). One-click structured outputs. No freeform agent sandbox. |

## 12. Open Questions for Product Review

1. Should Studio projects be shareable/collaborative (multiple seat-holders adding sources and chatting in the same project)?
2. What is the maximum source count / token budget per project per plan tier?
3. Should the podcast/audio feature be available on all tiers or reserved for Professional+?
4. Which template types should we support at launch (DOCX only? PPTX? Both)?
5. What are the seat tier limits? (e.g., Starter = 5 seats max, Professional = 50, Enterprise = unlimited?)
6. Should non-seat users be able to view generated artifacts shared by seat holders (read-only access)?
7. Do we need a "Try Studio" free trial experience (limited generations, no templates)?

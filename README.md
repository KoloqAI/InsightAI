<a name="readme-top"></a>

<h1 align="center">
    <img width="128" src="web/public/logo.svg" alt="InsightAI" />
    <br/>
    InsightAI
</h1>

<p align="center">AI-Powered Insight Platform</p>

<p align="center">
    <a href="https://github.com/KoloqAI/InsightAI" target="_blank">
        <img src="https://img.shields.io/badge/repo-KoloqAI%2FInsightAI-blue" alt="Repository" />
    </a>
    <a href="https://github.com/onyx-dot-app/onyx" target="_blank">
        <img src="https://img.shields.io/badge/upstream-onyx--dot--app%2Fonyx-black" alt="Upstream Onyx" />
    </a>
    <a href="https://github.com/KoloqAI/InsightAI/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=blue" alt="License" />
    </a>
</p>

> ### Fork notice
>
> **InsightAI** is a rebranded fork of [Onyx](https://github.com/onyx-dot-app/onyx)
> (formerly Danswer). All core features, connectors, and documentation from the
> upstream project apply here unchanged.
>
> The rebrand is intentionally shallow and upstream-safe: internal package names,
> Docker image names, module paths, and infrastructure identifiers still use
> `onyx`. Only user-visible strings and brand assets have been customized.
> This keeps `git merge upstream/main` low-conflict — see
> [project_documentation.md](project_documentation.md) for the upstream sync
> workflow and the list of branding-patched files.

---

**InsightAI** is the application layer for LLMs — bringing a feature-rich interface that can be easily hosted by anyone.
InsightAI enables LLMs through advanced capabilities like RAG, web search, code execution, file creation, deep research, and more.

Connect your applications with over 50+ indexing based connectors provided out of the box or via MCP.

> [!TIP]
> Most operational documentation still lives at the upstream project's docs
> site: <https://docs.onyx.app>. Substitute "InsightAI" anywhere you see "Onyx"
> in user-facing copy.

![Onyx Chat Silent Demo](https://github.com/onyx-dot-app/onyx/releases/download/v3.0.0/Onyx.gif)

---

## ⭐ Features

- **🔍 Agentic RAG:** Get best in class search and answer quality based on hybrid index + AI Agents for information retrieval
  - Benchmark to release soon!
- **🔬 Deep Research:** Get in depth reports with a multi-step research flow.
  - Top of [leaderboard](https://github.com/onyx-dot-app/onyx_deep_research_bench) as of Feb 2026.
- **🤖 Custom Agents:** Build AI Agents with unique instructions, knowledge, and actions.
- **🌍 Web Search:** Browse the web to get up to date information.
  - Supports Serper, Google PSE, Brave, SearXNG, and others.
  - Comes with an in house web crawler and support for Firecrawl/Exa.
- **📄 Artifacts:** Generate documents, graphics, and other downloadable artifacts.
- **▶️ Actions & MCP:** Let InsightAI agents interact with external applications, comes with flexible Auth options.
- **💻 Code Execution:** Execute code in a sandbox to analyze data, render graphs, or modify files.
- **🎙️ Voice Mode:** Chat with InsightAI via text-to-speech and speech-to-text.
- **🎨 Image Generation:** Generate images based on user prompts.

InsightAI supports all major LLM providers, both self-hosted (like Ollama, LiteLLM, vLLM, etc.) and proprietary (like Anthropic, OpenAI, Gemini, etc.).

To learn more about the features, check out the upstream [Onyx documentation](https://docs.onyx.app/welcome).

---

## 🚀 Deployment Modes

> InsightAI supports deployments in Docker, Kubernetes, Helm/Terraform and provides guides for major cloud providers.
> Detailed deployment guides found [here](https://docs.onyx.app/deployment/overview).

Onyx supports two separate deployment options: standard and lite.

#### Onyx Lite

The Lite mode can be thought of as a lightweight Chat UI. It requires less resources (under 1GB memory) and runs a less complex stack.
It is great for users who want to test out InsightAI quickly or for teams who are only interested in the Chat UI and Agents functionalities.

#### Standard Onyx

The complete feature set which is recommended for serious users and larger teams. Additional components not included in Lite mode:
- Vector + Keyword index for RAG.
- Background containers to run job queues and workers for syncing knowledge from connectors.
- AI model inference servers to run deep learning models used during indexing and inference.
- Performance optimizations for large scale use via in memory cache (Redis) and blob store (MinIO).

## 🏢 InsightAI for Enterprise

InsightAI is built for teams of all sizes, from individual users to the largest global enterprises:
- **Collaboration:** Share chats and agents with other members of your organization.
- **Single Sign On:** SSO via Google OAuth, OIDC, or SAML. Group syncing and user provisioning via SCIM.
- **Role Based Access Control:** RBAC for sensitive resources like access to agents, actions, etc.
- **Analytics:** Usage graphs broken down by teams, LLMs, or agents.
- **Query History:** Audit usage to ensure safe adoption of AI in your organization.
- **Custom code:** Run custom code to remove PII, reject sensitive queries, or to run custom analysis.
- **Whitelabeling:** Customize the look and feel with custom naming, icons, banners, and more.
- **Enterprise Search:** Custom indexing and retrieval that remains performant and accurate for scales of up to tens of millions of documents.
- **Document Permissioning:** Mirrors user access from external apps for RAG use cases.

## 🔄 Upstream sync

This fork pulls changes from [`onyx-dot-app/onyx`](https://github.com/onyx-dot-app/onyx) on a regular cadence. To sync:

```bash
scripts/sync_upstream.sh          # fetch and merge upstream/main
```

Only a small set of files carry InsightAI brand patches; see the "Branding patches" section in [project_documentation.md](project_documentation.md) for the full list. Any merge conflict should be confined to those files and is mechanical to resolve.

## 📚 Licensing
This fork preserves the upstream Onyx licensing model:

- The Community Edition (CE) is available freely under the MIT license.
- The Enterprise Edition (EE) code under `backend/ee/` and related paths remains subject to the upstream Onyx Enterprise License.

See [LICENSE](LICENSE) and [backend/ee/LICENSE](backend/ee/LICENSE).

## 💡 Contributing
Bugs and fixes that are generally applicable should be contributed upstream to [`onyx-dot-app/onyx`](https://github.com/onyx-dot-app/onyx) where appropriate. InsightAI-specific changes (branding, packaging) stay in this fork.

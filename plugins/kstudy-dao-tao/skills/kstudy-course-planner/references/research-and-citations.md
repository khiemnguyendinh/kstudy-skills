# Research and citations

## Research sequence

1. Define the Research Brief from course outcome and decision to be made.
2. Read internal Kstudy material first.
3. Search primary and official sources.
4. Add competitor, platform and public learning references only where they answer a question.
5. Record source metadata before synthesizing findings.
6. Convert findings into curriculum decisions; do not dump links into the course.

## Research tracks

### Market

Use learner evidence, admissions questions, objections, support logs, completed work, job posts and employer requirements. Without Kstudy evidence, label conclusions as hypotheses or market proxies.

### Competitor and course benchmark

Candidate sources may include Run By Linh, Vinalink, CES Global, Skill Bridge, Thái Vân Linh, Udemy and Coursera. Compare public evidence only:

- audience and promise;
- course structure and scope;
- duration and delivery;
- tools/frameworks;
- practice and assessment;
- support and learner experience;
- differentiators and gaps.

Never claim to know a private or paid syllabus from a sales page. Preserve `access_status` such as `PUBLIC`, `LOGIN_REQUIRED`, `PAYWALL`, `BROKEN`, `USER_PROVIDED`.

### Learning content

Use official documentation, books, ebooks, academic or professional sources, case studies and user-provided materials. Paraphrase and synthesize; do not reproduce chapters, long quotations or paid course lessons.

### Tool and trend

For volatile tools record product name, feature, version/date, region or plan limitation, official URL, checked date and fallback. Prefer official release notes or product documentation over third-party claims.

## Source record

Each source should contain:

```json
{
  "source_id": "SRC-001",
  "source_type": "official_web | ebook | textbook | youtube | udemy | coursera | competitor | learner_evidence | job_signal",
  "title": "...",
  "author_or_org": "...",
  "published_or_updated": "unknown",
  "url": "https://...",
  "accessed_at": "YYYY-MM-DD",
  "access_status": "PUBLIC | LOGIN_REQUIRED | PAYWALL | USER_PROVIDED | BROKEN | UNKNOWN",
  "evidence_level": "A_PRIMARY | B_REPUTABLE | C_MARKETING_OR_SECONDARY",
  "supports": ["claim or topic"],
  "citation": "Full citation",
  "notes": "Scope, timestamp, limitation or rights note"
}
```

If author, year, edition or update date is unavailable, use `unknown`; never infer bibliographic details.

## Login-gated sources

When access is required, ask the user to log in directly. Never request credentials. Resume only after the user confirms login. Do not purchase content or extract it in bulk. If login is declined, continue with public evidence and add a research gap.

## Citation formats

- Book/ebook: `Author. (Year). *Title* (edition). Publisher. Chapter/pages if known.`
- Official website: `Organization. (Year or update date). *Page title*. URL. Accessed YYYY-MM-DD.`
- YouTube: `Channel. (Date). *Video title* [Video]. YouTube. URL. Timestamp if used.`
- Udemy/Coursera: `Instructor/organization. (n.d. or date). *Course title*. Platform. URL. Accessed YYYY-MM-DD.`
- Competitor page: `Provider. (Date accessed). *Course/page title*. URL. Public description only.`

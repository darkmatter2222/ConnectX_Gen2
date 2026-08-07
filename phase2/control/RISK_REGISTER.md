# Risk Register — ConnectX Phase 2

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|------------|
| R001 | Repository clutter from prior session makes navigation hard | HIGH | MEDIUM | Focus on new `connectx/` and `tests/` dirs; keep new code clean |
| R002 | No venv means dependency conflicts later | HIGH | LOW | Create venv before first training work; use explicit path |
| R003 | Research documents are outdated or contain incorrect claims | MEDIUM | MEDIUM | Validate techniques against primary sources during implementation |
| R004 | GPU work starts before gym is tested | LOW | HIGH | Do not launch training until engine tests pass and baselines are registered |
| R005 | Time budget exhausted before meaningful progress | MEDIUM | HIGH | Each session focuses on one concrete milestone (engine → tests → baselines → tournament) |
| R006 | Research-only accumulation continues | HIGH | HIGH | Dashboard explicitly tracks engineering milestones; research stops when implementation begins |
| R007 | v2 eval too slow for deep opening book builds | MEDIUM | LOW | Use fallback to original book; build books at lower depth with longer timeout |
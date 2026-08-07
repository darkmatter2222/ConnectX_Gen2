# ConnectX Submissions — Mandatory Release Artifacts

**Root:** `phase2/submissions/`  
**Archives:** `O:\master_model_collection\ConnectX_Gen2_Phase2\submissions\`

## Purpose

Every **completed bot iteration** must produce an immutable, versioned, manually uploadable
`.tar.gz` release artifact. This is part of the definition of done.

## Layout

```
O:\master_model_collection\ConnectX_Gen2_Phase2\submissions\
├── connectx_submission_v0001.tar.gz
├── connectx_submission_v0001.manifest.json
├── connectx_submission_v0001.validation.json
├── LATEST_SUBMISSION.json
```

Git-tracked lightweight metadata:

```
phase2/submissions/
├── README.md
├── SUBMISSION_INDEX.md
├── submission_state.json
├── manifests/
│   ├── v0001.json
│   └── ...
├── build.py            # Packaging utility
├── validate.py         # Validation utility
└── test_submission.py  # Bounded tests
```

## Status Lifecycle

| Status | Description |
|--------|-------------|
| `BUILDING` | Currently being packaged |
| `FAILED_PACKAGING` | `.tar.gz` creation failed |
| `FAILED_VALIDATION` | Clean extraction or runtime test failed |
| `READY_FOR_MANUAL_UPLOAD` | Validated, upload-ready |
| `UPLOADED_MANUALLY` | User confirmed upload to Kaggle |
| `KAGGLE_EVALUATED` | Kaggle result recorded |
| `SUPERSEDED` | Replaced by newer version |
| `RETIRED` | No longer relevant |

## Rules

- **Never reuse a version number.**
- **Never overwrite a previous release.**
- **Never renumber history.**
- **Archive max size:** 1 GiB.
- **Archive must contain only runtime files** (`main.py` at root, model/assets beside it).
- **No enclosing directory, no `.git`, no venv, no tests, no research docs.**

## How to Create a Submission

```bash
cd C:\Users\ryans\source\repos\ConnectX_Gen2
python phase2/submissions/build.py --version v0001 --candidate v2_8x7_5 --source connectx.training.kaggle_self_contained
```

## How to Validate

```bash
python phase2/submissions/validate.py --path O:/master_model_collection/ConnectX_Gen2_Phase2/submissions/connectx_submission_v0001.tar.gz
```
# Limitations

This public repository is designed as a reproducible QSAR workflow demonstration.

## Important limitations

- The included dataset is small and only intended for demonstration.
- Reported demo metrics should not be interpreted as production-level model performance.
- Robust QSAR modeling requires more compounds, better chemical diversity, external validation, and applicability-domain analysis.
- Descriptor-only models can miss 3D, conformational, target-specific, and assay-context effects.
- Client/confidential project data is not included.

## Good practice for real QSAR projects

- Use a larger curated dataset.
- Keep compounds from the same analog series grouped during train/test splitting.
- Add external test-set validation.
- Report applicability domain.
- Avoid overclaiming performance from very small datasets.

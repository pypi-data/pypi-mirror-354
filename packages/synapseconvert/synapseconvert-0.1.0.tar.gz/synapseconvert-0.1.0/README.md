# Synapse Library Tools (Nested Format)

This toolkit provides a two-way converter for nested Synapse-style libraries (collections → categories → items).

## Usage

**Downconvert to Excel**
```bash
python synapse_downconvert.py metadata.json synapse_library.xlsx
```

**Upconvert to JSON**
```bash
python synapse_upconvert.py synapse_library.xlsx metadata.json
```

## Notes

- Tags must be valid JSON lists (e.g., ["Genesis", "Luke"])
- Collection name assumed uniform for now

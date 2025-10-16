# Version Design Document : v0.6.0-move-data-folder-to-root
Technical implementation and design guide for the upcoming version.

## 1. Features Summary
_Overview of features included in this version._

This version reorganizes the project structure by moving JSON data files from `/app/data/` to a new root-level `/data/` folder. This improves maintainability by providing clearer separation between data files (JSON) and data-handling code (Python modules).

**Key Changes:**
- Create new `/data` folder at project root
- Move 3 JSON files: `user_profiles.json`, `insurance_plans.json`, `claims_data.json`
- Keep Python code (`loader.py`, `__init__.py`) in `/app/data/`
- Update path references in `loader.py` to point to new location
- Update documentation to reflect new structure

**Benefits:**
- Easier data file maintenance (all data in one place at root)
- Clear separation: `/app/data/` contains code, `/data/` contains data
- Easier to add new JSON files in the future
- More conventional project structure

## 2. Technical Architecture Overview
_High-level technical structure that supports all features in this version._

**Current Structure:**
```
/app
  /data
    - loader.py (Python module for loading data)
    - __init__.py (Package initialization)
    - user_profiles.json (DATA FILE)
    - insurance_plans.json (DATA FILE)
    - claims_data.json (DATA FILE)
```

**Target Structure:**
```
/app
  /data
    - loader.py (Python module - STAYS HERE)
    - __init__.py (Package initialization - STAYS HERE)
/data  (NEW FOLDER)
  - user_profiles.json (MOVED HERE)
  - insurance_plans.json (MOVED HERE)
  - claims_data.json (MOVED HERE)
```

**Code Changes Required:**
- Update `DATA_DIR` constant in `loader.py` from `Path(__file__).parent` to point to root-level `/data` folder
- The path calculation needs to navigate from `/app/data/loader.py` up to project root, then into `/data`

## 3. Implementation Notes
_Shared technical considerations across all features in this version._

**Path Resolution Strategy:**
The `loader.py` file currently uses `Path(__file__).parent` to get the directory containing the loader module (`/app/data/`). We need to change this to:

```python
# Current (line 29):
DATA_DIR = Path(__file__).parent

# New approach:
DATA_DIR = Path(__file__).parent.parent.parent / "data"
```

This navigates:
1. `Path(__file__)` = `/path/to/project/app/data/loader.py`
2. `.parent` = `/path/to/project/app/data/`
3. `.parent` = `/path/to/project/app/`
4. `.parent` = `/path/to/project/` (project root)
5. `/ "data"` = `/path/to/project/data/`

**Testing Strategy:**
1. After moving files and updating code, test data loading by running the application
2. Verify all three JSON files load successfully
3. Test end-to-end application flow (web interface + agent interactions)
4. Check for any broken imports or file not found errors

**Documentation Updates:**
- Update README.md to show new project structure
- Update any other docs that reference the old data location
- Update code comments in `loader.py` if they mention file locations

## 4. Other Technical Considerations
_Shared any other technical information that might be relevant to building this version._

**No Breaking Changes:**
- The public API of `loader.py` remains unchanged
- All function signatures stay the same
- Only internal path resolution changes
- No changes to JSON file contents or structure

**Version Control:**
- Git will track the file moves properly
- Use `git mv` or ensure files are moved in a way Git recognizes

**Backward Compatibility:**
- This is an internal refactoring; external users won't be affected
- No changes to API endpoints or frontend code needed
- Session management and state remain unchanged

## 5. Open Questions
_Unresolved technical or product questions affecting this version._

**Q1: Should we add a README in the new `/data` folder explaining what goes there?**
- Decision: Not necessary for now, but could be added in future if needed

**Q2: Are there any other files or code that reference the data folder location?**
- Need to search codebase for any hardcoded paths to `/app/data/*.json`
- Need to verify tools and graph nodes don't have direct file references

**Q3: Should we update any environment configuration or deployment scripts?**
- Need to check if any scripts reference data file paths
- Need to verify Docker or deployment configs (if they exist)

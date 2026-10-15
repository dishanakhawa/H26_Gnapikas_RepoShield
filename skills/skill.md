
# RepoMedic AI — Repository Maintenance Skill

## Purpose
Inspect a Python repository and identify dependency maintenance risks.

## Instructions
1. Read the repository's requirements.txt files.
2. Inspect Python imports and compare them with declared dependencies.
3. Identify dependencies that are declared but not imported, when evidence supports the finding.
4. Identify imports that may be missing from dependency declarations.
5. Use Gemma to explain potential maintenance risks and suggest practical fixes.
6. Run available tests when feasible.
7. Never claim a test passed unless it was actually executed successfully.
8. Separate verified observations from AI-generated recommendations.
9. Report errors, limitations, and unresolved risks.

## Output
Create a Dependency Exit Capsule containing:
- Repository inspected
- Dependency findings and evidence
- AI recommendations
- Tests and their actual results
- Unresolved risks
- Suggested next actions
done
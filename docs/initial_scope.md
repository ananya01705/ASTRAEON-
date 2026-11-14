# Initial MVP Scope

## Goal

Prove that the application can query real SPHEREx archive metadata for a selected sky position and identify potential observations for later inspection.

## Included now

- Query IRSA SIA2 for SPHEREx DR1 and QR3.
- Display returned observation metadata.
- Export metadata as CSV.
- Keep archive search results distinct from scientifically comparable observations.

## Not included yet

- Automated transient or moving-object classification.
- Difference imaging or image registration.
- Spectral-temporal fingerprints.
- Candidate confidence scoring.
- Claims of Planet X detection.

## First validation gate

Find a sky region that returns usable SPHEREx observations. Inspect returned columns and product access URLs, then retrieve and inspect at least one real FITS product. Only after this works should temporal image comparison be implemented.

# FateCat Constitution

## Core Purpose

FateCat exists to organize and integrate major prediction traditions, starting with mainstream Chinese systems and effective open-source repositories. Reuse comes before self-built code.

## Engineering Principles

- Glue principle first: use mature libraries, frameworks, public repositories and platform capabilities before writing custom infrastructure.
- Structural migration must not change CLI, API, Bot, Web or pure-analysis behavior.
- Vendor snapshots are read-only supply-chain inputs. Do not patch vendor source in place.
- Domain code belongs in `domains/*/services/*`; contracts, catalog, infra, governance and docs each keep their own truth.
- Secrets, real databases, logs, caches, local raw material and personal paths never enter source or export bundles.
- Every compatibility path must have an owner, risk, expiry condition and removal gate.

## Delivery Rules

- Run local gates before claiming completion.
- Preserve user dirty work and stage only the intended task scope.
- Separate behavior changes from structural refactors.
- Prefer small reversible migration steps over big-bang rewrites.

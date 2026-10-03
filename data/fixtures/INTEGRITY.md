# Fixture integrity manifest

The fixture files are committed and immutable-by-policy. Git blob SHAs at this pre-build revision:

- `data/fixtures/dep_b1.json`: `685f93c9d451ff82d53360c91347b2c1b0681ac9`
- `data/fixtures/dep_load.json`: `666654860238ce444a4a915e507531adae15d15f`
- `data/fixtures/dep_p82.json`: `5b81109e53958e9a66f09edeb0504aa1f93ac788`

The implementation's first test must calculate SHA-256 over the UTF-8 fixture bytes and freeze those SHA-256 values into the release receipt. Git blob SHA and SHA-256 are deliberately not conflated.

Primary PDF SHA-256:
`5ad891010f3e64cef4c319e003eb3a4595e32cc4e872f701a7cbddf82bdcb6f7`

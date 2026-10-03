# Fixture integrity manifest

The fixture files are committed and immutable-by-policy. Git blob SHAs at this pre-build revision:

- `data/fixtures/dep_b1.json`: `685f93c9d451ff82d53360c91347b2c1b0681ac9`
- `data/fixtures/dep_load.json`: `666654860238ce444a4a915e507531adae15d15f`
- `data/fixtures/dep_p82.json`: `5b81109e53958e9a66f09edeb0504aa1f93ac788`

The implementation's first test must calculate SHA-256 over the UTF-8 fixture bytes and freeze those SHA-256 values into the release receipt. Git blob SHA and SHA-256 are deliberately not conflated.

Primary PDF SHA-256:
`5ad891010f3e64cef4c319e003eb3a4595e32cc4e872f701a7cbddf82bdcb6f7`

## E0/E1 canonical SHA-256 freeze — 2026-10-03

After E1 source-integrity PASS, `receipt.json` at the repository root records the accepted canonical file-byte SHA-256 values for use in the release run receipt:

- `data/fixtures/dep_b1.json`: `9ac268e4d96b145b3ef9f82fda71193c43339a103cec4632203f68e3c0ce1e79`
- `data/fixtures/dep_p82.json`: `37de300cd68184cc2315b6fffaf4fa04dbe07127a30514e982b538238359dc09`
- `data/fixtures/dep_load.json`: `7ddde731928ec2df4f8d4d256a75842181fc5ee54b885fb393b92f1a462c3b1b`

The Git blob SHAs above remain historical pre-remediation identifiers; they are not the current SHA-256 values. Approved B1 labels and p.82 source metadata changed bytes, not observations. The bounded E0/E1 receipt does not assert E8, model validation, or release readiness.

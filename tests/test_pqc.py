from pathlib import Path

from qmentor.pqc import scan_paths, scan_text

FIX = Path(__file__).parent / "fixtures" / "pqc"


def cats(findings):
    return {f["category"] for f in findings}


def test_public_key_classified_shor_vulnerable():
    r = scan_paths([str(FIX / "rsa_ecdh.py")])
    assert {"public-key:rsa", "public-key:ecc"} <= cats(r["findings"])
    assert all(f["quantum_exposure"] == "shor-vulnerable" for f in r["findings"] if f["category"].startswith("public-key"))
    assert r["changed_files"] == 0 and r["mode"] == "inventory-only"


def test_symmetric_and_hash_kept_separate():
    r = scan_paths([str(FIX / "aes_sha.py")])
    assert cats(r["findings"]) == {"symmetric", "hash"}
    assert all(f["quantum_exposure"] == "grover-margin-review" for f in r["findings"])


def test_false_positive_fixture_has_no_findings():
    assert scan_paths([str(FIX / "false_positive.py")])["findings"] == []


def test_comment_only_mentions_are_low_confidence():
    f = scan_text("# we used to use RSA here\n")
    assert f and all(x["confidence"] == "low" for x in f)


def test_every_finding_has_next_step():
    r = scan_paths([str(FIX)])
    assert all(f["next_step"] and f["evidence"] for f in r["findings"])

Status: blocked

Result
The PennyLane example fails its energy-equivalence gate: state 101010 gives −9.1225, canonical is −9.3725.

Validation
`python -m pytest -q examples/bond-selection/pennylane` → `test_hamiltonian_matches_canonical_on_all_states` failed; the offset was added twice.

Next
Remove the second offset addition in `adapter.basis_energy` and rerun the test.

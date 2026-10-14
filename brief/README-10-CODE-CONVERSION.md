# Code Conversion and Provider Examples

V3 gives `q-mentor-convert` ownership of verified cross-hardware code and measured optimization quality. `q-mentor-translate` remains a design/comparison skill. Syntax resemblance is irrelevant if the source computation, objective, feasible set, or measurement meaning changes.

The [cross-hardware atlas](README-14-CONVERSION-ATLAS.md) is mandatory for **every** source/target pair, not just Pasqal → Classiq. It groups hardware by execution model, classifies the requested route, supplies current official bridge references, and requires a negative fixture for unsupported semantics. A provider-specific adapter may tighten these rules but may not bypass them.

## Conversion pipeline

Every conversion follows this order:

1. Pin the source SDK version and reproduce the source import or parse result.
2. Extract `CanonicalProblem` and `ProgramIR`: variables, objective, constraints, constants, bit/wire order, Hamiltonians, register geometry, gates or pulses, timing, initial state, measurements, decoding, and backend assumptions.
3. Create a target `CapabilityReport`: `exact`, `approximate`, `unsupported-exact`, or `unknown`.
4. Select the route and its `E`/`C`/`R`/`A`/`U` proof obligation from README-14; build the target plan from a version-matched official example and API reference.
5. Generate complete files, dependency pins, fixture, expected result, and commands.
6. Run syntax, import, local execution, and semantic-equivalence gates in a clean target environment.
7. Emit a `TranslationRecord` with observed validation state and every semantic loss.
8. For optimization tasks, run the bounded `OptimizationRecord` comparison below before using the word `optimized`.

If source code does not parse, repair or reject it before conversion. If the target SDK or credential is unavailable, return complete code only as `syntax-checked` or `unverified`; never claim execution.

## Pasqal/Pulser to Classiq

Pulser describes neutral-atom registers and pulse-driven analog or digital-analog evolution. Classiq/Qmod describes high-level quantum functions synthesized into circuits. Therefore:

- A shared QUBO may be re-expressed as a Classiq QAOA model through `CanonicalProblem`; that is a new implementation of the optimization problem, not a literal conversion of the Pulser sequence.
- Register coordinates, Rydberg interaction strengths, detuning, Rabi waveforms, local addressability, blockade behavior, timing, noise, and measurement semantics must appear in `ProgramIR`.
- Map only semantics supported by the chosen Classiq target. A gate-equivalent digital sequence may be convertible after proof; analog evolution with no circuit equivalent is `unsupported-exact` or an explicitly bounded approximation.
- Never drop a pulse, substitute a generic QAOA ansatz, or change decoding while labeling the result equivalent.

The regression fixture must cover: valid exact digital mapping, shared-QUBO reimplementation, analog-only unsupported mapping, stale source API, missing import, undefined name, credential-required synthesis, and target code that runs but produces a different energy.

## Classiq QAOA optimization regression

Use the [current Classiq QAOA example](https://docs.classiq.io/explore/algorithms/search_and_optimization/grover_mixer_qaoa/gm_qaoa) and [Qmod reference](https://docs.classiq.io/qmod-reference) at a recorded SDK version. The official example factors `cost_layer`, `mixer_layer`, and `qaoa_ansatz`, slices parameters into `gammas` and `betas`, and uses `ExecutionSession.estimate_cost` with SciPy COBYLA. These are strong construction patterns. The example labels its phase-only `cost_layer` with `@qfunc`, while a separate [Classiq oracle example](https://www.classiq.io/insights/quantum-computing-for-finance-how-high-level-quantum-programming-and-gpu-acceleration-are-changing-the-game) uses `@qperm`. Therefore **do not assert that `@qperm` is universally required for every phase layer**. For the pinned SDK, test whether `@qperm` is accepted and improves synthesis or enforces a needed invariant; otherwise use the documented `@qfunc` pattern and record why. Both variants must preserve the phase operator and pass synthesis when that service is available.

The generated target must use named cost, mixer, and ansatz functions, unless a measured alternative is better. Define exactly which angle convention is used: `RX(theta) = exp(-i theta X / 2)` in the usual gate convention, so `RX(beta)` and `RX(2*beta)` parameterize the same family with different beta labels/ranges. Test a one-qubit unitary or statevector and adjust bounds when switching conventions; never silently compare parameter values across conventions. Slicing `gammas=params[:p]` and `betas=params[p:]` is a readability invariant, not an assumed speedup.

Start with a small fixed budget and compare depths `p=1,2,4` where synthesis/resources permit. Four layers are a **candidate**, not a guarantee of the optimum; the winning depth is selected by feasible-sample quality against circuit depth, two-qubit operations, shots, and wall time. For a five-qubit ten-term QUBO, exact enumeration supplies ground truth. Use multiple seeded starts, a stated shot budget and evaluation cap, and at least two target optimizer modes when supported: documented `estimate_cost` + SciPy COBYLA and `variational_minimize` with an explicitly verified objective/quantile definition. Do not describe `quantile=0.7` as “best 30%” without checking the installed API; make the selected tail fraction a tested fixture. Do not compare a CVaR objective with mean energy as though they were the same metric.

Hold the QUBO, penalty, feasible set, initial-state family, decoding, and total budget fixed across variants. Report best feasible energy, gap to exact optimum, feasible-sample probability, expected energy, variability over seeds, shots, objective evaluations, synthesized depth/two-qubit count, elapsed time, and any estimated provider cost. A candidate is `improved` only on a predeclared primary metric without a material regression on the stated resource cap; otherwise report `not-improved` and keep the simpler variant. A first-try compilation is a syntax result, not an optimization result.

## Complete example contract

Each supported target directory contains:

```text
README.md              # version, source links, commands, expected result
requirements.lock      # or ecosystem-equivalent lock
main.py                # complete offline entry point
adapter.py             # canonical-model conversion
test_example.py        # syntax/import, result, decode, equivalence
expected.json          # deterministic fixture and tolerances
```

No hidden notebook state, unexplained generated file, ellipsis, `TODO`, wildcard version, embedded credential, or network call is allowed. Notebooks may accompany—but not replace—the executable example.

## Required examples and gates

| Target | Minimum complete examples | Offline validation |
|---|---|---|
| Qiskit | Canonical `QuadraticProgram`, QUBO/Ising conversion, exact baseline, local QAOA/sampler path, decode | Compile/import; enumerate energy; run pinned local primitive/simulator; compare all toy states |
| Classiq | Python Qmod and native-Qmod form where applicable, synthesis settings, result decode | Compile/import and locally available model validation; credentialed synthesis is separate and visibly gated |
| D-Wave Ocean | BQM from canonical coefficients, `ExactSolver`, local heuristic, guarded QPU adapter | Compile/import; verify offset and all energies with `dimod.ExactSolver`; no Leap call by default |
| Pasqal/Pulser | Register/device capability report, sequence construction, supported QUBO/QAA example, noisy-emulator case | Compile/import; sequence/device validation; local emulator or capability-only gate |
| PennyLane | Explicit `default.qubit`, cost/mixer Hamiltonians, seeded optimization, sampling and decode | Compile/import; inspect circuit/specs; execute locally; compare canonical energy and wire order |
| Cirq | Gate circuit with concrete topology and simulator; optional Google backend profile | Import/run local simulator; verify bit order, unitary/energy, and measurement key |
| pytket | Explicit circuit and compiler pass; Quantinuum backend remains gated | Import/run local simulator; compare pre/post compilation semantics and resource count |
| Bloqade | Native neutral-atom analog program with geometry and schedule | Import/build; local analog simulation or capability-only gate; reject arbitrary dense QUBO |
| Perceval | Discrete-variable photonic circuit, source and detector model | Import/run local processor; account for postselection/loss and decoded event probability |

Use the official documentation, API references, release notes, and maintained example repositories in [README-07](README-07-REFERENCES.md) and [README-12](README-12-SDK-SOURCE-MAP.md). Copy only the smallest relevant pattern, adapt it to the canonical fixture, and cite the exact source. A blog snippet may suggest an approach but cannot be the sole authority for an SDK call.

## Exhaustive coverage without waste

Maintain a sparse source/target **capability graph**, not a quadratic all-pairs promise. For all hardware families in README-11, classify every requested edge as `exact`, `conditional`, `reimplementation`, `approximate`, `unsupported`, or `not-applicable`, with a reason and test from README-14. Prebuild representative gate↔gate, gate→photonic, analog↔analog, BQM→gate/analog, and Pasqal/Pulser→Classiq fixtures. Runnable code is required for every edge claimed exact, conditional, or reimplementation; unsupported edges require a negative fixture, not invented bridge code. Profiled/research-only providers never gain executable edges until a pinned local example passes.

The same six-bond `CanonicalProblem` anchors all nine local targets where the problem is representable. Add one native example per paradigm—gate circuit, Qmod synthesis, BQM/annealing, neutral-atom pulse program, differentiable PennyLane QNode, and photonic sampling—so the plugin learns genuine provider concepts rather than treating APIs as cosmetic wrappers. An unsupported target gets a precise nonrepresentability test instead.

## Definition of complete

A conversion is complete only when all generated files exist, the clean environment installs from locks, syntax/import gates pass, the offline example runs, decoded results satisfy the canonical fixture, exact mappings pass energy equivalence, and the response reports the observed validation state. An optimization claim additionally needs a passing `OptimizationRecord`. Otherwise return the first failure and a repair plan; do not fill the gap with plausible code.

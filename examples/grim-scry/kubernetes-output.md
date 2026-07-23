# Example scry run: `kubernetes`

| Field | Value |
| --- | --- |
| Target | [kubernetes](https://github.com/kubernetes/kubernetes) |
| Model | Composer 2.5 |
| Ran with | Cursor |
| Params | `N = 3`, `K = 12` |

Chat-facing output from a scry of the [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) repository.

## Directory hierarchy

```text
kubernetes/
├─ AGENTS.md
├─ api/ ◀─ OpenAPI spec; API rule violation tracking
│  ├─ api-rules/
│  ├─ discovery/
│  └─ openapi-spec/
│     └─ v3/
├─ build/ ◀─ Containerized build; artifacts under `_output`
│  ├─ build-image/
│  │  └─ cross/
│  ├─ lib/
│  ├─ pause/
│  ├─ root/ ◀─ `Makefile` symlink target
│  └─ server-image/
├─ CHANGELOG/ ◀─ Per-release changelogs (1.37 listed)
├─ cluster/ ◀─ Maintenance mode; no new providers
│  ├─ addons/ ◀─ Legacy cluster add-ons shipped with binaries
│  ├─ gce/
│  ├─ images/
│  ├─ kubemark/
│  ├─ log-dump/ ◀─ Deprecated; superseded by test-infra
│  └─ skeleton/
├─ cmd/ ◀─ Binary entrypoints
│  ├─ kube-apiserver/
│  ├─ kube-controller-manager/
│  ├─ kube-scheduler/
│  ├─ kubelet/
│  ├─ kube-proxy/
│  ├─ kubectl/
│  ├─ kubeadm/
│  ├─ cloud-controller-manager/
│  ├─ kubemark/
│  └─ gen*/ import-boss/ ... ◀─ codegen and repo hygiene tools
├─ docs/
├─ hack/ ◀─ verify/update scripts; codegen; CI helpers
│  ├─ boilerplate/
│  ├─ lib/
│  ├─ make-rules/
│  ├─ jenkins/
│  └─ tools/
├─ pkg/ ◀─ In-tree core implementation
│  ├─ apis/
│  ├─ kubelet/
│  ├─ scheduler/
│  ├─ proxy/
│  ├─ kubectl/
│  ├─ registry/
│  ├─ controller/
│  └─ ...
├─ plugin/
│  └─ pkg/
│     ├─ admission/
│     └─ auth/
├─ staging/ ◀─ Authoritative source for published `k8s.io/*` repos
│  ├─ publishing/
│  └─ src/
│     └─ k8s.io/
├─ test/
│  ├─ cmd/
│  ├─ conformance/
│  ├─ declarative_validation/
│  ├─ e2e/
│  ├─ e2e_node/
│  ├─ integration/
│  ├─ images/
│  └─ kubemark/
├─ third_party/
└─ vendor/
```

## Conceptual hierarchy

```text
Kubernetes ◀─ Container orchestration system (K8s); CNCF-hosted
├─ Control plane
│  ├─ kube-apiserver ─▶ `cmd/kube-apiserver` ─▶ API front door
│  ├─ kube-controller-manager ─▶ `cmd/kube-controller-manager`
│  ├─ kube-scheduler ─▶ `cmd/kube-scheduler`
│  ├─ cloud-controller-manager ─▶ `cmd/cloud-controller-manager` ◀─ extension example only
│  └─ kubeadm ─▶ `cmd/kubeadm` ─▶ cluster bootstrap
├─ Node runtime
│  ├─ kubelet ─▶ `cmd/kubelet` / `pkg/kubelet`
│  └─ kube-proxy ─▶ `cmd/kube-proxy` / `pkg/proxy`
├─ Client surface
│  └─ kubectl ─▶ `cmd/kubectl` / `staging/src/k8s.io/kubectl`
├─ Published libraries ◀─ `staging/` is source of truth
│  ├─ `staging/src/k8s.io/*` ─▶ api, apimachinery, client-go, apiserver, ...
│  └─ go.work + replace ─▶ in-tree resolution; `k8s.io/kubernetes` not a supported library
├─ API layer
│  ├─ `pkg/apis/` + staged `k8s.io/api`
│  ├─ OpenAPI spec ─▶ `api/openapi-spec/`
│  └─ Convention enforcement ─▶ `api/api-rules/violation_exceptions.list`
├─ Build and release
│  ├─ `make` / `build/run.sh` ─▶ `_output/` binaries and images
│  └─ `kubernetes.tar.gz` ─▶ client utils, server binaries, cluster scripts
├─ Quality and verification
│  ├─ `make verify` / `make update`
│  ├─ unit + integration tests ─▶ `make test`, `make test-integration`
│  └─ e2e / conformance / node tests ─▶ `test/`
├─ Legacy cluster ops ◀─ maintenance mode
│  ├─ `cluster/` provider scripts
│  └─ `cluster/addons/` ─▶ reconcile-class vs create-if-missing add-ons
└─ Contributor constraints
   ├─ generated files read-only ─▶ `make update`
   ├─ deps via `hack/pin-dependency.sh` + `hack/update-vendor.sh`
   └─ AGENTS.md
```

## Workflow hierarchy

```text
kubernetes
├─ Bootstrap / build
│  ├─▶ make ◀─ local Go environment
│  ├─▶ make quick-release ◀─ Docker hermetic build
│  └─▶ build/run.sh make [target] ◀─ containerized make (cross, kubectl, test, ...)
├─ Dev hygiene
│  ├─▶ make verify
│  ├─▶ make update ◀─ all generators and formatters
│  ├─▶ hack/verify-all.sh ─▶ redirects to `make verify`
│  └─▶ hack/update-all.sh ─▶ redirects to `make update`
├─ Testing
│  ├─▶ make test WHAT=./pkg/... GOFLAGS=-v
│  ├─▶ make test-integration WHAT=./test/integration/...
│  └─▶ build/run.sh make test / test-integration
├─ Dependencies
│  ├─▶ hack/pin-dependency.sh
│  └─▶ hack/update-vendor.sh ◀─ not `go mod tidy`
├─ Codegen / API rules
│  ├─▶ hack/update-codegen.sh
│  └─▶ UPDATE_API_KNOWN_VIOLATIONS=true ./hack/update-codegen.sh
├─ Release
│  ├─▶ build/release.sh / make release
│  └─▶ _output/release-tars/kubernetes.tar.gz
├─ Legacy cluster (deprecated path)
│  ├─▶ cluster/kube-up.sh / kube-down.sh
│  └─▶ cluster/addons/ ─▶ addon-manager reconcile loop
└─ Primary instruction
   └─▶ AGENTS.md ─▶ `make help`
```

## Summary

Large Go monorepo for Kubernetes itself: control-plane and node binaries under `cmd/`, core logic in `pkg/`, publishable `k8s.io/*` libraries authored in `staging/`, and a heavy `hack/` + `make` toolchain for verify, codegen, build, and test. `AGENTS.md` is the in-repo agent contract; `README.md` points outward for user docs and community contribution.

## Observations

- **Staging-first library model** - `staging/src/k8s.io/` is authoritative; the main module is the integration shell, not a consumer library.
- **Generated-code discipline** - hand-editing `zz_generated.*` / `generated.pb.go` is forbidden; `go.mod`/`go.work` changes go through vendor scripts.
- **Two build paths** - bare `make` vs Dockerized `build/run.sh` / `quick-release`; release artifacts land in `_output/`.
- **Legacy cluster tree** - `cluster/` and `cluster/log-dump/` are explicitly maintenance/deprecated; not the modern install path.
- **CCM is an extension point** - `cmd/cloud-controller-manager` is an example pattern; cloud providers should not vendor or fork it in-tree.
- **Test surface is wide** - `test/` spans cmd, integration, e2e, e2e_node, conformance, declarative validation, and test images; presubmit/release-blocking coverage lives here.
- **API governance is checked in** - OpenAPI lives under `api/openapi-spec/`; known convention violations are tracked in `api/api-rules/`.

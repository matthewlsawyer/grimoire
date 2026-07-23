# Example scry run: `tailscale`

| Field | Value |
| --- | --- |
| Target | [tailscale](https://github.com/tailscale/tailscale) |
| Model | Composer 2.5 |
| Ran with | Cursor |

Chat-facing output from a scry of the [tailscale](https://github.com/tailscale/tailscale) repository.

## Directory hierarchy

```text
tailscale/ ◀─ Open-source Tailscale client; tailscaled daemon and tailscale CLI
├─ cmd/ ◀─ CLI binaries and tools
│  ├─ tailscale/
│  ├─ tailscaled/
│  ├─ derper/
│  ├─ k8s-operator/
│  ├─ k8s-nameserver/
│  ├─ k8s-proxy/
│  └─ tsidp/
├─ client/
├─ derp/ ◀─ DERP packet relay client and server code
├─ feature/ ◀─ Modular feature system; conditionally linkable packages
├─ tsnet/ ◀─ Embed a Tailscale node in a Go program
├─ gokrazy/ ◀─ Gokrazy appliance image (pre-alpha)
├─ docs/
│  └─ k8s/
├─ k8s-operator/
├─ kube/
├─ logtail/ ◀─ Tailscale logs service libraries and examples
├─ licenses/ ◀─ Generated dependency license lists
├─ scripts/
├─ tool/
├─ wgengine/
├─ ipn/
├─ control/
├─ tailcfg/
├─ net/
└─ internal/
```

## Conceptual hierarchy

```text
tailscale
├─ tailscaled ◀─ Background daemon managing the virtual network interface
├─ tailscale CLI ◀─ Command-line tool for configuring and using Tailscale
│  └─▶ tailscaled
├─ DERP ◀─ Packet relay for disco and encrypted WireGuard when UDP or NAT traversal fails
│  ├─ derp/
│  └─ cmd/derper/
├─ tsnet ◀─ Self-contained embedded Tailscale node in a Go process
│  └─ tsnet/
├─ modular features ◀─ Conditionally linkable feature packages via build tags and hooks
│  └─ feature/
├─ Kubernetes operator ◀─ Automated Tailscale resources and cluster integration
│  ├─ k8s-operator/
│  └─ cmd/k8s-operator/
└─ Gokrazy appliance ◀─ Minimal Linux+Tailscale image for VMs and Raspberry Pi
   └─ gokrazy/
```

## Workflow hierarchy

```text
tailscale
├─ Build
│  ├─▶ go install tailscale.com/cmd/tailscale{,d}
│  ├─▶ ./build_dist.sh tailscale.com/cmd/tailscale
│  └─▶ ./build_dist.sh tailscale.com/cmd/tailscaled
├─ Quality
│  ├─▶ make check
│  └─▶ make vet
├─ Lint
│  └─▶ make lint
├─ Generate
│  └─▶ make generate
├─ Kubernetes operator
│  └─▶ make kube-generate-all
│     └─▶ cmd/k8s-operator/
└─ Gokrazy appliance
   └─▶ make qemu ◀─ gokrazy pre-alpha image
```

## Summary

Open-source Tailscale client code: the `tailscaled` daemon and `tailscale` CLI for private WireGuard-based mesh networking on Linux, Windows, macOS, and other platforms. Go monorepo with modular features, DERP relay, embedded `tsnet` library, Kubernetes operator, and appliance images.

## Observations

- Go monorepo; latest Go release required (README cites Go 1.26).
- `./tool/go` wraps the pinned Go toolchain; Makefile targets use it.
- `feature/` is the preferred home for new client functionality; many areas remain half-migrated.
- `cmd/` holds 50+ binaries beyond the core tailscale/tailscaled pair.
- Mobile GUI code lives in separate repos; this tree supplies shared client logic.
- `gokrazy/` appliance work is marked pre-alpha / WIP.

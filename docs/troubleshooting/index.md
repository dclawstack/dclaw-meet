# Troubleshooting

Common issues and solutions for DClaw Meet.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-meet

# Check logs
kubectl logs -n dclaw-meet deployment/dclaw-meet-backend

# Check database
kubectl get clusters -n dclaw-meet
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)

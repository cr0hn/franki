# Traefik as load balancer

This modules allow to enable Traefik as load blancer for an project

## Enable

Traefik LB must be activated in `franki.yaml` file: 

```yaml
version: 1.0.0
type: project

deployment:

  load_balancer:
    traefik:
      domains:
        - my_domain.com
      acme:
        email: my-email@domain.com
```

## Configurations

Traefik module has these options:

- domains: list or domains to claim for ACME
- email: email to configure for ACME

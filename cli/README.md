# CLI

## API Keys Management
Create, list and revoke the API keys for a specific origin.

### create
`$ linka-cli api-keys create ORIGIN`

### list
`$ linka-cli api-keys list`

### revoke
`$ linka-cli api-keys revoke ORIGIN [--all] [--key]`

Either provide `--all` for revoking all the keys associated to a origin or `--key` to revoke a single key.

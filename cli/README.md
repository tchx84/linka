# CLI

## API Keys Management
Create, list and revoke the API keys for a specific source.

### create
`$ linka-cli api-keys create SOURCE`

### list
`$ linka-cli api-keys list`

### revoke
`$ linka-cli api-keys revoke SOURCE [--all] [--key]`

Either provide `--all` for revoking all the keys associated to a source or `--key` to revoke a single key.

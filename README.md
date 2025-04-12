# Seafile Upload Action

A GitHub Action to upload files to a Seafile server.

## Usage

```yaml
steps:
- uses: actions/checkout@v4

- name: Upload to Seafile
  uses: chekoopa/upload-to-seafile@v1
  with:
    server-url: ${{ secrets.SEAFILE_SERVER_URL }}
    username: ${{ secrets.SEAFILE_USERNAME }}
    password: ${{ secrets.SEAFILE_PASSWORD }}
    repo-id: ${{ secrets.SEAFILE_REPO_ID }}
    remote-path: '/uploads'
    local-path: 'dist/*'
    overwrite: 'false'
```

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `server-url` | Yes | Seafile server URL |
| `username` | Yes | Seafile username |
| `password` | Yes | Seafile password |
| `repo-id` | Yes | Seafile repository/library ID |
| `remote-path` | Yes | Destination path in Seafile (default: `/`) |
| `local-path` | Yes | Local file pattern to upload (supports glob) |
| `overwrite` | No | Overwrite existing files (default: false) |
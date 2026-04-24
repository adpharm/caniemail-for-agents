#!/bin/bash
set -e

# install psql (postgresql-client)
sudo apt-get update

echo "Installing Bun"
curl -fsSL https://bun.sh/install | bash

# Install Claude CLI
curl -fsSL https://claude.ai/install.sh | bash

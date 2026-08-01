terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.20"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_ssh_key" "deploy" {
  name       = "zayidni-deploy-key"
  public_key = can(file(var.ssh_public_key_path)) ? file(var.ssh_public_key_path) : var.ssh_public_key
}

resource "digitalocean_droplet" "app" {
  name   = "zayidni-staging"
  region = var.region
  size   = var.size
  image  = "ubuntu-22-04-x64"

  ssh_keys = [digitalocean_ssh_key.deploy.fingerprint]

  user_data = file("${path.module}/cloud-init.yaml")

  tags = ["zayidni", "staging"]
}


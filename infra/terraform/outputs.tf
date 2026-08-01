output "droplet_ip" {
  description = "Public IPv4 address of the staging droplet"
  value       = digitalocean_droplet.app.ipv4_address
}

output "droplet_id" {
  description = "DigitalOcean droplet id"
  value       = digitalocean_droplet.app.id
}

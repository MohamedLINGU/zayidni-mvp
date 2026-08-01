variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key file to add to the droplet (local file)"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "ssh_public_key" {
  description = "Public SSH key content (use this or ssh_public_key_path). Provide via TF_VAR_SSH_PUBLIC_KEY as secret to avoid storing keys in repo."
  type        = string
  default     = ""
}

variable "region" {
  description = "DigitalOcean region"
  type        = string
  default     = "nyc3"
}

variable "size" {
  description = "Droplet size slug"
  type        = string
  default     = "s-1vcpu-2gb"
}

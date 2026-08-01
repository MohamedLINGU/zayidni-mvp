Provision DigitalOcean staging droplet using Terraform

Prerequisites
- Install Terraform (>=1.5)
- Create a DigitalOcean personal access token with write access
- Ensure you have an SSH public key locally (default: ~/.ssh/id_rsa.pub)

Quick steps
1. Copy repo infra files to local machine (already in repo under infra/terraform)
2. Export DO token and (optional) variables:
   export TF_VAR_do_token="<your-do-token>"
   export TF_VAR_ssh_public_key_path="~/.ssh/id_rsa.pub"
   # Optionally set region/size
   export TF_VAR_region="nyc3"
   export TF_VAR_size="s-1vcpu-2gb"

3. Initialize and apply:
   cd infra/terraform
   terraform init
   terraform apply --auto-approve

4. After apply completes, note the droplet_ip output and SSH to it as the 'deploy' user.
   ssh deploy@<droplet_ip>

5. On the droplet, create /home/deploy/.ssh/authorized_keys if your key wasn't set via cloud-init.

6. Run the repo deploy script from your workstation (set STAGING_SSH and STAGING_PATH):
   export STAGING_SSH=deploy@<droplet_ip>
   export STAGING_PATH=/home/deploy/apps/zayidni
   ./scripts/deploy_staging.sh

Notes
- The cloud-init includes a placeholder for the ssh key. Terraform will upload your public key via the digitalocean_ssh_key resource; the cloud-init placeholder is informational in case you edit the file manually.
- For production, prefer managed Postgres and Redis or use DigitalOcean managed services; this terraform example creates only a droplet.
- Clean up with: terraform destroy --auto-approve

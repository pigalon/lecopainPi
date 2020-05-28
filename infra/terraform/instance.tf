provider "aws" {
  profile    = "default"
  region     = "eu-west-3"
}

resource "aws_instance" "lecopain" {
  key_name      = "pigalon"
  ami           = "ami-08c757228751c5335"
  instance_type = "t2.micro"

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/pigalon.pem")
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
        "sudo apt-get update",
        "sudo apt install -y docker.io",
        "sudo usermod -aG docker ubuntu"
        "sudo curl -L \"https://github.com/docker/compose/releases/download/1.26.0-rc4/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
        "sudo chmod +x /usr/local/bin/docker-compose",
        "sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose",
        "sudo mkdir /usr/share/db",
        "sudo mkdir /usr/share/db/lecopain",
        "sudo chown ubuntu:ubuntu /usr/share/db/lecopain",
        "sudo chmod 664 /usr/share/db/lecopain"
      ]
  }
}

# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

provision_script = <<END_OF_LINE
#!/usr/bin/env bash

APTITUDE_UPDATED=/home/vagrant/.aptitude_updated
if [[ ! -e ${APTITUDE_UPDATED} ]]; then
    aptitude update && touch ${APTITUDE_UPDATED}
fi

aptitude --assume-yes install htop python-dev python-pip
pip install --upgrade pip
hash pip
pip install --upgrade setuptools
pip install -r /vagrant/requirements.txt

END_OF_LINE

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  # config.vm.box_check_update = false
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.provision :shell, :inline => provision_script
end

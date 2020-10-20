#!/bin/bash

ansible-galaxy install -r ansible/requirements.yaml
ansible-playbook -i ansible/hosts.ini ansible/main.yaml

import time
import os
import requests
import tomllib
from proxmoxng.models.vms import VM
from proxmoxng import app
from proxmoxng import db

def FaultTolerance(vmID, proxmox, resources, killThread):

    global app
    with open("/etc/proxmoxng/middleware/config.toml", "rb") as f:
        config = tomllib.load(f)
    
    if 'pushover' in config:
        pushover_token = config["pushover"]["token"]
        pushover_user = config["pushover"]["user"]
    else:
        pushover_user = None
        pushover_token = None
        
    keepalivedip = config["keepalived"]["ip"]

    vmHA= []
    nodeHA = []

    id = 1

    vms = resources.vms

    for vm in vms:
        if(vm['id'] == vmID):
            vmHA = vm

    # Get node information
    nodes = resources.nodes
    # Print node names and status
    for node in nodes:
        print(vmHA)
        if(node['node'] == vmHA['node']):
            nodeHA = node

    while not killThread.is_set() and nodeHA['status'] == 'online':

        if(id == 1):
            id = 0
        else:
            id = 1
        
        try:
            for ip in resources.networks:
                if ip == keepalivedip:
                    print(f"[{vmID}] - Node is online, waiting...")
                    proxmox.nodes(vmHA['node']).qemu(vmHA['id'].split('/')[1]).snapshot(f"snapshot_ha_{id}").delete()

            time.sleep(5) 
            for ip in resources.networks:
                if ip == keepalivedip:
                    proxmox.nodes(vmHA['node']).qemu(vmHA['id'].split('/')[1]).snapshot.post(
                        snapname=f"snapshot_ha_{id}",
                        vmstate=1,
                    )


            print(f"[{vmID}] - Snapshot created.")
            time.sleep(20)
        except Exception as e:
            print(f"[{vmID}] - Error managing snapshot: {e}")
            time.sleep(10)
            if(id == 1):
                id = 0
            else:
                id = 1

  
        vms = resources.vms
        for vm in vms:
            if(vm['id'] == vmID):
                vmHA = vm

        # Get node information
        nodes = resources.nodes
        # Print node names and status
        for node in nodes:
            if(node['node'] == vmHA['node']):
                nodeHA = node
        

        print(f"VM ID: {vmHA['id']}, Name: {vmHA['name']}, Status: {vmHA['status']}")
        print(f"Node Name: {nodeHA['node']}, Status: {nodeHA['status']}")

    if killThread.is_set():
        print(f"[{vmID}] - Thread killed.")
        return

    print(f"[{vmID}] - Node is offline, starting migrating...")
    for ip in resources.networks:
        if ip == keepalivedip:
                if pushover_user:
                    requests.post(
                            f"https://api.pushover.net/1/messages.json",
                            data={
                                "token": pushover_token,
                                "user": pushover_user,
                                "title": f"Fault Tolerance - Node {nodeHA['node']} offline - VM {vmID}",
                            "message": f"[{vmID}] - Node is offline. Starting migrating to another node.",
                            },
                        )

       
    vms = resources.vms
    for vm in vms:
        if(vm['id'] ==  vmID):
            vmHA = vm
    
    originalNode = ''

    nodes = resources.nodes
        # Print node names and status
    for node in nodes:
        if(node['node'] == vmHA['node']):
            originalNode = node

    while vmHA['node'] == nodeHA['node'] and originalNode['status'] != 'running':
        time.sleep(10)
        print(f"[{vmID}] - Waiting for VM to migrate...")
        vms = resources.vms
        for vm in vms:
            if(vm['id'] ==  vmID):
                vmHA = vm
                
        nodes = resources.nodes
        # Print node names and status
        for node in nodes:
            if(node['node'] == vmHA['node']):
                originalNode = node

        
    for ip in resources.networks:
        if ip == keepalivedip:
            if 'snapstate' in proxmox.nodes(vmHA['node']).qemu(vmHA['id'].split('/')[1]).snapshot(f"snapshot_ha_{id}").config.get().keys():
                print(f"[{vmID}] - VM is in prepare state, not good...")
                proxmox.nodes(vmHA['node']).qemu(vmHA['id'].split('/')[1]).snapshot(f"snapshot_ha_{id}").delete(
                    force=1,
                )
                print(f"[{vmID}] - Snapshot deleted.")
                time.sleep(3)
                if(id == 1):
                    id = 0
                else:
                    id = 1

            proxmox.nodes(vmHA['node']).qemu(vmHA['id'].split('/')[1]).snapshot(f"snapshot_ha_{id}").rollback.post()
            print(f"[{vmID}] - Rollback completed.")
            requests.post(
                    f"https://api.pushover.net/1/messages.json",
                    data={
                        "token": pushover_token,
                        "user": pushover_user,
                        "title": f"Fault Tolerance - Rollback - VM {vmID}",
                        "message": f"[{vmID}] - Vm assigned to node {vmHA['node']} - Rollback completed.",
                    },
                )
            with app.app_context():
                VM.query.filter_by(name=vmID).delete()
                db.session.commit()


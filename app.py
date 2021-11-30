import time
from flask import Flask

#Nova usage (Computing resources)
from novaclient import client 
#Keystone usage (Authentication)
from keystoneauth1 import loading 
from keystoneauth1 import session
#Glance usage (Images)
from glanceclient import Client
#Neutron usage (Networks)
from neutronclient.v2_0 import client as NetClient

app = Flask(__name__)

VERSION='2'
AUTH_URL="https://api-acloud.ormuco.com:5000/v3"
USERNAME="utb@ormuco.com"
PASSWORD="ILOVEUTB2021"
PROJECT_ID="2ee7b627f154414f83ffdbbf6c78999f"

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=AUTH_URL,username=USERNAME,password=PASSWORD,project_id=PROJECT_ID)
sess = session.Session(auth=auth)
nova = client.Client(VERSION, session=sess)
glance = Client(VERSION,session=sess)
neutron = NetClient.Client(session=sess)

@app.route("/servers")
def serverlist():
    servers=nova.servers.list()
    for server in servers:
        print(server.name)
    return("<h1>Openstack Server List</h1>")   

@app.route("/servercreate")
def servercreate():
    flavors=nova.flavors.list()
    images=glance.images.list()
    networks=neutron.list_networks()
    servers=nova.servers.list()

    print("\nServer list")
    for server in servers:
        print(server.name)
    
    print("\nFlavor list")
    for flavor in flavors:
        print(flavor.id, flavor.name)

    print("\nImage list")
    for image in images:
        print(image.id, image.name)

    print("\nNetwork list")
    print(networks)

    server_name=input("\nEnter server name: ")
    user_flavor=input("\nEnter flavor ID: ")
    user_image=input("\nEnter image ID: ")
    user_keypair=input("\nEnter a key-pair name: ")

    #Creation of instance
    image = user_image
    flavor = nova.flavors.find(id=user_flavor)
    key_name=user_keypair
    intance = nova.servers.create(name=server_name, image=image, flavor=flavor, key_name=key_name)

    print("\nStarting server...")
    time.sleep(5)
    print("\nServer list:")
    for server in nova.servers.list():
        print(server.name)

    return(
        "<h1>Openstack Server Create</h1>"
        "<p/>"
        "<p/>"
        "<h2>Flavor List</h2>"
        "<p/>"
        "<p/>"
        "<h2>Image List</h2>"
    )

@app.route("/")
def hello_world():
    return "<h1>Main page</h1>"







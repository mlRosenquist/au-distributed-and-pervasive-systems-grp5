import os
from platform import node
node_id = os.environ['NODE_ID']
no_nodes = os.environ['NO_NODES']
print("NODE ID: %s" % node_id)
print("NO. NODES: %s" % no_nodes)
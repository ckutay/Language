import re

class Sheet:

    regex = re.compile('\{\d+x\d+\}')

    class Node:
        def __init__(self,name):
            self.name=name
            self.value=''
            self.computed_value=''
            self.incoming={}
            self.outcoming={}
            self.changed=False
            self.count=0

    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        names=['{%sx%s}'%(k/cols,k%cols) for k in xrange(rows*cols)]
        self.nodes=dict([(name,Sheet.Node(name)) for name in names])
        print self.nodes

    def delete_from(self,other_list):
        indices = [k for (k,node) in enumerate(other_list) if k==node] 
        if indices: del other_list[indices[0]]

    def changed(self,node,changed_nodes=[]):
        for other_node in node.outcoming:
            if not other_node in changed_nodes:
                changed_nodes.append(other_node)
                self.changed(other_node,changed_nodes)
        return changed_nodes

    def set(self,key,value):
        node=self.nodes[key]
        node.value=value
        if value[:1]=='=':
            # clear all edges involving current node
            for other_node in node.incoming:
                del node.outcoming[me]
            node.incoming.clear()
            # build new edges
            for match in self.regex.finditer(value[1:]):
                other_key=match.group()
                other_node=self.nodes[other_key]           
                other_node.outcoming[node]=True
                node.incoming[other_node]=True
            self.calculate(node)
        else:
            try:
                node.computed_value=int(node.value)                
            except:
                try:
                    node.computed_value=float(node.value)
                except:
                    node.computed_value=node.value
        return self.iterate(node)

    def calculate(self,node):
        if node.value[:1]=='=':
            command=node.value[1:]
            for match in self.regex.finditer(command):
                other_key=match.group()
                other_value=self.nodes[other_key].computed_value or 0.0
                command=command.replace(other_key,repr(other_value))
            print 'computing',node.name,command
            try:
                node.computed_value=eval(command)
            except:
                node.computed_value='ERROR'
            print node.name,node.computed_value

    def iterate(self,node):
        output={node.name:node.computed_value}
        changed_nodes = self.changed(node)
        while changed_nodes:
            ok=False
            for (k,other_node) in enumerate(changed_nodes):
                if not set(other_node.incoming.keys()).intersection(set(changed_nodes)):
                    self.calculate(other_node)
                    output[other_node.name]=other_node.computed_value
                    del changed_nodes[k]
                    ok=True
                    break
            if not ok: raise SynataxError
        return output

            

"""
L = Empty list that will contain the sorted elements
S = Set of all nodes with no incoming edges
while S is non-empty do
    remove a node n from S
    insert n into L
    for each node m with an edge e from n to m do
        remove edge e from the graph
        if m has no other incoming edges then
            insert m into S
if graph has edges then
    output error message (graph has at least one cycle)
else 
    output message (proposed topologically sorted order: L)

"""            

s=Sheet(4,4)
s.set('{1x2}','={0x0}')
s.set('{0x0}','=5+{1x1}+{2x2}')
s.set('{1x1}','6')
print s.set('{2x2}',"3")


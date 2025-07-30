from typed_graph.typed_graph import N, E, NK, EK, NT, ET, S, EdgeCls, TypedGraphCls, TypedGraph, NodeIdCollision, EdgeIdCollision
from pydantic import BaseModel
from typing import Generic, Dict, Tuple
from typed_graph.typed_traits import *
from typed_graph.typed_error import *
from typed_graph.dependency_traits import RustModel
from typing import Dict, Generic, Callable, Any
from pydantic import model_validator, model_serializer, BaseModel
from pydantic_core import core_schema

from pydantic import BaseModel, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
import json


class PartialTypedGraph(BaseModel, Generic[N, E, NK, EK, NT, ET, S]):
    """
    Typedraph[N, E, NK, EK, NT, ET, S]

    Generic graph with customizable types
    """
    graph_schema: S
    nodes: Dict[NK, N]
    edges: Dict[EK, Tuple[NK, NK, E]]

    def __init__(self, schema: S, nodes: Dict[NK, N], edges: Dict[EK, Tuple[NK, NK, E]]):
        if isinstance(schema, str):
            super().__init__(graph_schema=json.loads(schema), nodes = nodes, edges = edges)
        else:
            super().__init__(graph_schema=schema, nodes = nodes, edges = edges)

    def get_schema(self) -> S:
        return self.graph_schema
    
    def add_file(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            g = self.model_validate_json(f.read())
            self.append(g)

    def save_file(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.model_dump_json(indent=4))

    def add_node(self, node: N):
        """
        Add a node to the partial graph  
        WARNING: This does not perform any validation checks  
        All checks are performed on completion
        """
        self.nodes[node.get_id()] = node

    def add_edge(self, source: NK, target: NK, edge: E):
        """
        Add an edge to the partial graph  
        WARNING: This does not perform any validation checks
        All checks are performed on completion
        """
        self.edges[edge.get_id()] = (source, target, edge)

    def append(self, other: 'PartialTypedGraph[N, E, NK, EK, NT, ET, S]'):
        for node_id, node in other.nodes.items():
            if node_id in self.nodes:
                raise NodeIdCollision(node_id)
            self.nodes[node_id] = node

        for edge_id, edge in other.edges.items():
            if edge_id in self.edges:
                raise EdgeIdCollision(edge_id)
            self.edges[edge_id] = edge

    def finish(self) -> TypedGraph[N, E, NK, EK, NT, ET, S]:
        N, E, NK, EK, NT, ET, S = PartialTypedGraph._get_generics(type(self))
        g = TypedGraph[N, E, NK, EK, NT, ET, S](schema=self.graph_schema)
        for node in self.nodes.values():
            g.add_node(node)

        for source, target, edge in self.edges.values():
            g.add_edge(source, target, edge)

        return g
        
    
    @model_serializer(mode='plain')
    def _serialize(self, *args, **kwarg) -> dict[str, Any]:
        """
        Parse the graph to json
        """

        nodes = list(self.nodes.values())
        edges = list()
        for source, target, weight in self.edges.values():
            edges.append(EdgeCls(
                weight = weight,
                source = source,
                target = target,
            ))

        kwarg['by_alias'] = True

        return TypedGraphCls[N, E, NK, S](
            schema = self.graph_schema,
            nodes = nodes,
            edges = edges
        ).model_dump(*args, **kwarg)
    
    @staticmethod
    def _get_generics(cls):
        """
        Retrieve the generics types from the class
        We use __pydantic_generic_metadata__ as the generics are eaten by the BaseModel
        """
        
        args = cls.__pydantic_generic_metadata__['args']

        if not isinstance(args, tuple) or len(args) != 7:
            raise AttributeError(f'Failed to find generics for {cls}')

        N, E, NK, EK, NT, ET, S = args
        return N, E, NK, EK, NT, ET, S

    # We use staticmethod instead of classmethods
    # because classmethod for some reason does not include the actual type of the generics
    # if a solution is found to this. It would be great, however for now this is what we have
    @model_validator(mode='wrap')
    def _deserialize(
        cls, 
        d: dict[str, Any], 
        default: Callable[[dict[str, Any]], 'PartialTypedGraph[N, E, NK, EK, NT,ET, S]'],
        *args,
        **kwarg
    ) -> 'TypedGraph[S]':
        """
        First Parse TypedGraphCls and then use it to construct the TypedGraph
        """

        if isinstance(d, cls):
            return d
        
        if isinstance(d, dict):
            if 'graph_schema' in d:
                return default(d)
            
        N, E, NK, EK, NT, ET, S = PartialTypedGraph._get_generics(cls)

        if isinstance(d, dict):
            cls_g = TypedGraphCls[N, E, NK, S].model_validate(d)
        elif isinstance(d, TypedGraphCls[N, E, NK, S]):
            cls_g = d
        else:
            raise ValueError('expected dict')
        
        # Create the graph
        g = cls(schema = cls_g.graph_schema, nodes={}, edges={})
        
        # Add all the nodes
        for node in cls_g.nodes:
            g.add_node(node)
        
        # Add all the edges between the nodes
        for edge in cls_g.edges:
            g.add_edge(
                edge.source,
                edge.target,
                edge.weight
            )
        
        return g

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """
        Use all the properties from TypedGraphCls instead of TypedGraph
        """
        # If this breaks i am very sorry
        # I have spend countless hours trying to come up with a way to serialize/deserialize using TypedGraphCls
        # but none of them has worked
        # So now i just hardcode TypedGraphCls schema into TypeGraph

        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        
        N, E, NK, EK, NT, ET, S = TypedGraph._get_generics(cls)
        cls_schema = TypedGraphCls[N, E, NK, S].model_json_schema()

        def find_ref_replacement(ref):
            if not isinstance(ref, dict):
                return None
            
            if '$ref' in ref:
                ref_key = ref['$ref'].split('/')[-1]
                if ref_key in cls_schema['$defs']:
                    return cls_schema['$defs'][ref_key]
            return None

        def dereference_refs(d: Any):
            if isinstance(d, list):
                for i in range(0, len(d)):
                    new_ref = find_ref_replacement(d[i])
                    if new_ref:
                        d[i] = new_ref
                        
                    dereference_refs(d[i])
            elif isinstance(d, dict):
                for k, v in list(d.items()):
                    if k == '$defs':
                        continue
                    
                    new_ref = find_ref_replacement(v)
                    if new_ref:
                        d[k] = new_ref

                    dereference_refs(d[k])

        # Since EdgeCls is not used by TypedGraph, any reference to it will cause an error
        # So instead of figuring out how to add EdgeCls into $defs we just dereference all references
        dereference_refs(cls_schema)

        json_schema['properties'] = cls_schema['properties']
        if '$defs' in json_schema:
            del json_schema['$defs']

        return json_schema
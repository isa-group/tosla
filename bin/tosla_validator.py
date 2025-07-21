from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, DCTERMS
from pyshacl import validate
from collections import defaultdict
import time
from rdflib.term import BNode
from collections import defaultdict

# Namespaces
SH = Namespace("http://www.w3.org/ns/shacl#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
TOSL = Namespace("https://w3id.org/tosl/")
TOSLA = Namespace("https://w3id.org/tosla/")

DATA_PATH = ""
SHACL_PATH = "agreement_shape.ttl"

generated_labels = {}
generated_names = defaultdict(int)

def get_label(graph, node):
    if node is None:
        return "None"
    # Si ya lo tenemos nombrado
    if node in generated_labels:
        return generated_labels[node]

    # Si tiene rdfs:label o odrl:uid
    label = graph.value(node, RDFS.label) or graph.value(node, ODRL.uid)
    if label:
        return str(label)

    # Si es un URI, extraer el fragmento o el último segmento
    if hasattr(node, 'split'):
        uri = str(node)
        if '#' in uri:
            return uri.split('#')[-1]
        elif '/' in uri:
            return uri.rstrip('/').split('/')[-1]

    # Si es un nodo anónimo o muy largo (e.g., hash)
    if isinstance(node, BNode) or (str(node).startswith("n") and len(str(node)) > 30):
        rdf_types = list(graph.objects(node, RDF.type))
        typename = "Anonymous"
        if rdf_types:
            for t in rdf_types:
                if str(t).startswith(str(ODRL)):
                    typename = str(t).replace(str(ODRL), "")
                elif str(t).startswith(str(TOSL)):
                    typename = str(t).replace(str(TOSL), "")
        generated_names[typename] += 1
        name = f"{typename}_{generated_names[typename]}"
        generated_labels[node] = name
        return name

    return str(node)


def parse_validation_results(results_graph_data):
    graph = Graph()
    graph.parse(data=results_graph_data, format="turtle")

    edges = []
    nodes = set()

    for result in graph.subjects(RDF.type, SH.ValidationResult):
        subject = graph.value(result, SH.focusNode)
        predicate = graph.value(result, SH.resultPath)
        obj = graph.value(result, SH.value)

        if subject and predicate is not None:
            edges.append((subject, predicate, obj))
            nodes.update([subject, obj])

    return edges, nodes, graph

def build_tree(edges):
    tree = defaultdict(list)
    for subj, pred, obj in edges:
        tree[subj].append((pred, obj))
    return tree

def collect_paths(node, tree, all_paths, path=None):
    if path is None:
        path = []
    extended = False
    for pred, child in tree.get(node, []):
        extended = True
        collect_paths(child, tree, all_paths, path + [(node, pred)])
    if not extended:
        all_paths.add(tuple(path + [(node, None)]))  # leaf node

def filter_unique_paths(all_paths):
    return {
        path for path in all_paths
        if not any(other != path and path == other[:len(path)] for other in all_paths)
    }

def validate_tosla_ttl(ttl_content, shacl_path):
    g = Graph()
    try:
        g.parse(data=ttl_content, format='turtle')
    except Exception as e:
        return {
            "syntax_valid": False,
            "syntax_error": str(e)
        }
    
    # Si llegamos aquí, sintaxis OK
    result = {
        "syntax_valid": True,
        "syntax_error": None
    }

    start = time.time()
    conforms, results_graph, _ = validate(
        data_graph=g,
        shacl_graph=shacl_path,
        inference='rdfs',
        serialize_report_graph=True,
        advanced=True,
        abort_on_first=False,
        meta_shacl=False,
        js=False,
        max_recursion_depth=10
    )
    duration = time.time() - start

    result = {
        "conforms": conforms,
        "validation_time": duration,
        "violations": []
    }

    if not conforms:
        # parse violations
        edges, nodes, graph = parse_validation_results(results_graph)
        tree = build_tree(edges)
        child_nodes = {obj for _, _, obj in edges}
        roots = [n for n in nodes if n not in child_nodes]

        all_paths = set()
        for root in roots:
            collect_paths(root, tree, all_paths)

        unique_paths = filter_unique_paths(all_paths)

        for path in sorted(unique_paths):
            readable_path = []
            for node, pred in path:
                if pred is None:
                    readable_path.append(get_label(graph, node))
                else:
                    readable_path.append(get_label(graph, node))
                    readable_path.append(get_label(graph, pred))
            result["violations"].append({
                "path": readable_path
            })

    return result

if __name__ == "__main__":
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        ttl_content = f.read()
    result = validate_tosla_ttl(ttl_content, SHACL_PATH)
    print(result)
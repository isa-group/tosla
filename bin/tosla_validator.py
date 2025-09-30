from rdflib import Graph, Namespace
from rdflib.namespace import RDF
from pyshacl import validate
import time
import json

SH = Namespace("http://www.w3.org/ns/shacl#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
TOSL = Namespace("https://w3id.org/tosl/")
TOSLA = Namespace("https://w3id.org/tosla/")

DATA_PATH = ""
SHACL_PATH = "../validator/agreement_shape.ttl"


def iter_results_from_roots(rep_graph: Graph):
    all_results = set(rep_graph.subjects(RDF.type, SH.ValidationResult))
    detailed = set(rep_graph.objects(None, SH.detail))
    roots = [r for r in all_results if r not in detailed]
    visited = set()

    def walk(r):
        if r in visited:
            return
        visited.add(r)
        yield r
        for d in rep_graph.objects(r, SH.detail):
            yield from walk(d)

    for r in roots:
        yield from walk(r)


def extract_flat_violations(results_graph_data: str):
    g = Graph()
    g.parse(data=results_graph_data, format="turtle")

    def val(res, p):
        v = g.value(res, p)
        return str(v) if v is not None else ""

    out = []
    seen_keys = set()

    for r in iter_results_from_roots(g):
        item = {
            "severity": val(r, SH.resultSeverity),
            "sourceShape": val(r, SH.sourceShape),
            "sourceConstraintComponent": val(r, SH.sourceConstraintComponent),
            "focusNode": val(r, SH.focusNode),
            "valueNode": val(r, SH.value),
            "resultPath": val(r, SH.resultPath),
            "message": val(r, SH.resultMessage),
        }
        key = (
            item["severity"],
            item["sourceShape"],
            item["sourceConstraintComponent"],
            item["focusNode"],
            item["valueNode"],
            item["resultPath"],
            item["message"],
        )
        if key not in seen_keys:
            seen_keys.add(key)
            out.append(item)
    return out


def validate_tosla_ttl(ttl_content: str, shacl_path: str):
    """Valida el TTL contra el SHACL y devuelve dict con JSON de resultados."""
    g = Graph()
    try:
        g.parse(data=ttl_content, format="turtle")
    except Exception as e:
        return {
            "syntax_valid": False,
            "syntax_error": str(e),
        }

    start = time.time()
    conforms, report_graph, _ = validate(
        data_graph=g,
        shacl_graph=shacl_path,
        shacl_graph_format="turtle",
        inference="rdfs",
        serialize_report_graph=True,
        advanced=True,
        abort_on_first=False,
        meta_shacl=False,
        js=False,
        max_recursion_depth=10,
    )
    duration = time.time() - start

    result = {
        "syntax_valid": True,
        "conforms": bool(conforms),
        "validation_time_sec": duration,
        "violations": [],
    }

    if not conforms:
        result["violations"] = extract_flat_violations(report_graph)

    return result


if __name__ == "__main__":
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        ttl_content = f.read()
    result = validate_tosla_ttl(ttl_content, SHACL_PATH)
    print(json.dumps(result, ensure_ascii=False, indent=2))
from app.graph.builder import build_graph

graph = build_graph()

input_data = {
    "paragraph": "John is a software engineer from Bangalore.",
    "schema": {
        "name": {},
        "age": {},
        "city": {},
        "profession": {},
        "salary": {}
    }
}

result = graph.invoke(input_data)

print("\nFinal Table:\n")
print(result["final_table"])
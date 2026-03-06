from fastmcp import Client

client = Client("http://localhost:8003")

print(client.tools())

# result = client.call_tool("add", {"a": 2, "b": 3})
result = client.call_tool("search_documents", {
    "query": "voltage range"
})

print(result)
print("Add result:", result)
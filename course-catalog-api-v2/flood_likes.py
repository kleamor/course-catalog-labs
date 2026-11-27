"""Dangerous demonstration: executes 12 like mutations and changes the database."""
import httpx

query = 'mutation { ' + ' '.join(f'a{i}: likeCourse(id: "api-design") {{ course {{ likes }} }}' for i in range(12)) + ' }'
response = httpx.post("http://127.0.0.1:8000/graphql", json={"query": query})
print(response.status_code, response.json())

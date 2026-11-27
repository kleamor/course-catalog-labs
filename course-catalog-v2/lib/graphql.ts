const API_URL = process.env.API_URL ?? "http://127.0.0.1:8000";

export async function gql<T>(query: string, variables: Record<string, unknown>): Promise<T> {
  const response = await fetch(`${API_URL}/graphql`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, variables }),
    cache: "no-store",
  });
  if (!response.ok) throw new Error(`GraphQL HTTP request failed: ${response.status}`);
  const result = (await response.json()) as { data?: T; errors?: { message: string }[] };
  if (result.errors?.length) throw new Error(`GraphQL request failed: ${result.errors[0].message}`);
  if (!result.data) throw new Error("GraphQL response contains no data");
  return result.data;
}

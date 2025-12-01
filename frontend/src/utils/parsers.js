export async function safeParseJson(res) {
  try {
    return await res.json();
  } catch {
    return null;
  }
}

export function extractMessage(json, res, defaultMsg) {
  if (!json) return res?.statusText || defaultMsg;
  if (typeof json === "string") return json;
  return json.msg || json.message || res?.statusText || defaultMsg;
}

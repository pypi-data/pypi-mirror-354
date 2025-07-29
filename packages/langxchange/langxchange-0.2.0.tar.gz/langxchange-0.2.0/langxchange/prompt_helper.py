# langxchange/prompt_helper.py

from typing import Any, Dict, List, Optional

class PromptHelper:
    """
    Builds prompts for LLMs and provides an interface to call injected tools.
    """

    def __init__(
        self,
        llm: Any,
        system_prompt: str,
        tools: Optional[Dict[str, Any]] = None
    ):
        """
        :param llm: an object with .chat(messages, **kwargs) -> str
        :param system_prompt: the initial system-level instruction
        :param tools: a dict mapping tool names to tool instances
        """
        self.llm = llm
        self.system_prompt = system_prompt
        self.tools = tools or {}

    def call_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """
        Invoke a named tool that was injected at init.
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")
        tool = self.tools[tool_name]
        # we assume each tool has a `query()` method, adjust as needed
        return tool.query(*args, **kwargs)

    def run(
        self,
        user_query: str,
        retrieval_results: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> str:
        """
        Build the full chat context and call the LLM.
        If the user_query starts with "TOOL:<tool_name>:", we will
        route it to the appropriate tool instead of the LLM.
        """
        # Tool‐invocation syntax:  TOOL:<tool_name>:rest of query
        if user_query.startswith("TOOL:"):
            _, tool_name, tool_q = user_query.split(":", 2)
            return self.call_tool(tool_name, tool_q.strip())

        # otherwise build a normal chat
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]

        if retrieval_results:
            # include retrieved snippets as assistant messages
            for hit in retrieval_results:
                doc = hit.get("text") or hit.get("document", "")
                if isinstance(doc, list):
                    doc = "\n".join(doc)
                meta = hit.get("metadata", {})
                tag = ", ".join(f"{k}={v}" for k, v in meta.items())
                messages.append({
                    "role": "assistant",
                    "content": f"[Snippet] {tag}:\n{doc}"
                })

        messages.append({"role": "user", "content": user_query})

        return self.llm.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

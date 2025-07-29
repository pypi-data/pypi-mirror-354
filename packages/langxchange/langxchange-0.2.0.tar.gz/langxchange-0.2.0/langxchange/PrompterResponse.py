# langxchange/PrompterResponse.py

import json
from typing import Any, Dict, List, Optional


class PrompterResponse:
    """
    A simple prompt‐builder that can accept “tools” (like DbTool) for the LLM to invoke.
    When one of the messages has role="tool_request", this code will:
      1) Look up self.tools[tool_name], call its .query(...) (or .run(...) / __call__).  
      2) Append a single message with role="tool", name=tool_name, content=<the result>.  
      3) Finally send the entire expanded message list into llm.chat(...) and return the LLM’s reply.
    """

    def __init__(
        self,
        llm: Any,
        system_prompt: str = "",
        tools: Optional[Dict[str, Any]] = None
    ):
        """
        :param llm: any object with a .chat(messages:List[Dict], temperature, max_tokens) → str interface
        :param system_prompt: the “system” message to send first
        :param tools: a dict mapping tool_name → tool_instance.  E.g. {"dbtool": DbTool(...)}
        """
        self.llm = llm
        self.system_prompt = system_prompt
        self.tools = tools or {}

    def run(
        self,
        user_messages: List[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> str:
        """
        Send a sequence of messages. Each message is a dict with:
          - role: one of "system", "user", "assistant", "tool_request"
          - content: string (for "system"/"user"/"assistant")
          - tool_name & tool_input: for "tool_request" messages only.

        Flow:
          1) Prepend the system prompt (if any) as a {"role":"system"} message.
          2) Walk through user_messages in order:
             - If role=="tool_request": invoke the named tool and append exactly one
               {"role":"tool","name":<tool_name>,"content":<tool_output>} to the pipeline.
             - Otherwise ("user" or "assistant"), pass the message through unchanged.
          3) Finally send the entire expanded list to llm.chat(...) and return the LLM’s reply.
        """
        full_msgs: List[Dict[str, Any]] = []

        # 1) Add system prompt if provided
        if self.system_prompt:
            full_msgs.append({"role": "system", "content": self.system_prompt})

        # 2) Process each incoming message
        for msg in user_messages:
            role = msg.get("role")
            if role == "tool_request":
                # Expect these keys: "tool_name" (str), "tool_input" (any)
                tool_name = msg.get("tool_name")
                tool_input = msg.get("tool_input")

                if tool_name not in self.tools:
                    # Unknown tool: report as an assistant message
                    full_msgs.append({
                        "role": "assistant",
                        "content": f"[❌ ERROR] Requested tool '{tool_name}' is not available."
                    })
                    continue

                # 2.a) Invoke the tool
                try:
                    tool_instance = self.tools[tool_name]
                    if hasattr(tool_instance, "query"):
                        # If tool_input is a dict, expand it as kwargs; else pass as single argument
                        result = (
                            tool_instance.query(**tool_input)
                            if isinstance(tool_input, dict)
                            else tool_instance.query(tool_input)
                        )
                    elif hasattr(tool_instance, "__call__"):
                        result = tool_instance(tool_input)
                    elif hasattr(tool_instance, "run"):
                        result = tool_instance.run(tool_input)
                    else:
                        raise AttributeError(
                            f"Tool '{tool_name}' has no 'query', '__call__', or 'run' method."
                        )
                except Exception as e:
                    result = f"[❌ ERROR] Tool '{tool_name}' failed: {e}"

                # 2.b) Append a single message with role="tool"
                # According to OpenAI API, "tool" is a valid role; include "name" for reference.
                content_str = (
                    json.dumps(result, indent=2)
                    if not isinstance(result, str)
                    else result
                )
                full_msgs.append({
                    "role": "tool",
                    "name": tool_name,
                    "content": content_str
                })

            else:
                # Regular "user" or "assistant" message: pass through unchanged
                full_msgs.append(msg)

        # 3) Call the LLM
        llm_reply = self.llm.chat(
            messages=full_msgs,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return llm_reply

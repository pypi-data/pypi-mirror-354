import logging
import sys
import requests
from typing import List, Dict, Any
from urllib.parse import urljoin
import random
import string

# 设置默认日志格式
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class AgentSDK:
    """Agent SDK for interacting with Agent services."""

    def __init__(self, base_url: str, agent_id: int):
        """Initialize SDK.

        Args:
            base_url: API base URL
            agent_id: Agent ID
        """
        self.base_url = base_url.rstrip("/")
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"{__name__}.AgentSDK_{agent_id}")

    def _make_url(self, path: str) -> str:
        """Build complete API URL.

        Args:
            path: API path

        Returns:
            Complete API URL
        """
        return urljoin(f"{self.base_url}/", path.lstrip("/"))

    def think(self, content: str) -> str:
        """Send a thought to the Agent.

        Args:
            content: Thought content

        Returns:
            Agent's response
        """
        url = self._make_url("/v1/agents/python/think")
        data = {"agent_id": self.agent_id, "content": content}

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            if "result" in result:
                return result["result"]
            raise Exception(f"Unexpected response: {result}")
        except Exception as e:
            self.logger.error(f"Think failed: {e}")
            raise

    def look(self, query: str, img_urls: List[str]) -> str:
        """Have the Agent process images.

        Args:
            query: Query content
            img_urls: List of image URLs

        Returns:
            Processing result
        """
        url = self._make_url("/v1/agents/python/look")
        data = {"agent_id": self.agent_id, "query": query, "image_urls": img_urls}

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            if "result" in result:
                return result["result"]
            raise Exception(f"Unexpected response: {result}")
        except Exception as e:
            self.logger.error(f"Look failed: {e}")
            raise

    def call_mcp_server(self, server_name: str, method: str, *args: Any) -> Any:
        """Call an Agent ability.

        Args:
            namespace: Ability namespace
            name: Ability name
            args: Ability arguments

        Returns:
            Ability execution result
        """
        url = self._make_url("/v1/mcp/servers/call_tool")
        data = {
            "server_name": server_name,
            "tool_name": method,
            "args": args,
        }

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            if "result" in result:
                return result["result"]
            raise Exception(f"Unexpected response: {result}")
        except Exception as e:
            self.logger.error(f"Call ability failed: {e}")
            raise

    def clear_memory(self, session_id: str = None) -> Dict[str, Any]:
        """Clear agent's memory.

        Args:
            session_id: Optional session ID to clear specific session memory

        Returns:
            Response containing code, message and data
        """
        url = self._make_url("/v1/memory/clear")
        params = {"agent_id": self.agent_id}
        if session_id:
            params["session_id"] = session_id

        try:
            response = requests.delete(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Clear memory failed: {e}")
            raise


def create_memory_agent(agent_info: Dict[str, Any], base_url: str) -> Dict[str, Any]:
    """Create a memory agent."""
    url = base_url + "/v1/agents/create_memory_agent"
    response = requests.post(url, json=agent_info)
    response.raise_for_status()
    return response.json()


def destroy_memory_agent(agent_id: int, base_url: str) -> Dict[str, Any]:
    """Destroy a memory agent."""
    url = base_url + "/v1/agents/destroy_memory_agent"
    response = requests.get(url, params={"agentId": agent_id})
    response.raise_for_status()
    return response.json()


# 获取所有可用的 mcp servers
def get_all_mcp_servers(base_url: str) -> List[Dict[str, Any]]:
    """Get all available mcp servers."""
    url = base_url + "/v1/mcp/servers/list"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class AgentContext:
    """Agent context manager."""

    def __init__(
        self,
        agent_info: Dict[str, Any] = dict(),
        base_url: str = "http://127.0.0.1:8086",
    ):
        """Initialize context.

        Args:
            agent_info: Agent information dictionary with at least 'id' field.
                      In platform environment, this will be automatically injected.
                      Optional keys include:
                      - name: Agent's name
                      - role: Agent's role
                      - responsibilities: Agent's responsibilities
                      - backgroundKnowledge: Agent's background knowledge
                      - mcp_servers: Agent's MCP servers
            base_url: API base URL (defaults to http://127.0.0.1:8086)
        """
        if not isinstance(agent_info, dict):
            raise ValueError(
                "agent_info must be a dictionary! you can add optional keys: name, role, responsibilities, backgroundKnowledge to enhance agent_info"
            )

        if not all(
            map(
                lambda x: x in agent_info,
                [
                    "name",
                    "role",
                    "responsibilities",
                    "backgroundKnowledge",
                    "mcp_servers",
                ],
            )
        ):
            logger.info(
                "You can enhance agent_info by adding optional keys: name, role, responsibilities, backgroundKnowledge. "
                "For mcp_servers, you need to provide a list of server IDs which can be obtained from get_all_mcp_servers()"
            )

        self.base_url = base_url
        self.agent_info = agent_info
        # self.sdk = AgentSDK(base_url, agent_info["id"])
        self.logger = logger

    def __enter__(self):
        """Enter context."""

        name = self.agent_info.get(
            "name", "".join(random.choices(string.ascii_letters + string.digits, k=16))
        )
        self.logger.info(f"Starting execution: {name}")

        if "id" not in self.agent_info:
            ins = create_memory_agent(self.agent_info, self.base_url)
            print(ins)
            self.sdk = AgentSDK(self.base_url, ins["id"])
        else:
            self.sdk = AgentSDK(self.base_url, self.agent_info["id"])

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        if "id" not in self.agent_info:
            destroy_memory_agent(self.sdk.agent_id, self.base_url)
        if exc_type:
            self.logger.error(f"Execution error: {exc_val}")
        else:
            self.logger.info("Execution complete")
        return False

    def get_all_mcp_servers(self) -> List[Dict[str, Any]]:
        """Get all available mcp servers."""
        return get_all_mcp_servers(self.base_url)

    def think(self, content: str) -> str:
        """Send a thought to the Agent."""
        return self.sdk.think(content)

    def look(self, query: str, img_urls: List[str]) -> str:
        """Have the Agent process images."""
        return self.sdk.look(query, img_urls)

    def call_mcp_server(self, server_name: str, method: str, *args: Any) -> Any:
        """Call an MCP server."""
        return self.sdk.call_mcp_server(server_name, method, *args)

    def clear_memory(self, session_id: str = None) -> Dict[str, Any]:
        """Clear agent's memory.

        Args:
            session_id: Optional session ID to clear specific session memory

        Returns:
            Response containing code, message and data
        """
        return self.sdk.clear_memory(session_id)

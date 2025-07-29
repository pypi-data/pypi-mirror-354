# coding: utf-8
# Copyright (c) 2025 inclusionAI.

from typing import Any, Dict, Tuple, Union

from aworld.core.event.base import Message

from aworld.config.conf import ToolConfig, ConfigDict
from aworld.core.agent.base import AgentFactory
from aworld.core.common import ActionModel, Observation
from aworld.core.tool.base import ToolFactory, AsyncTool
from aworld.logs.util import logger
from aworld.tools.mcp_tool.executor import MCPToolExecutor
from aworld.tools.utils import build_observation


@ToolFactory.register(name="mcp",
                      desc="mcp execute tool",
                      asyn=True)
class McpTool(AsyncTool):
    def __init__(self, conf: Union[Dict[str, Any], ConfigDict, ToolConfig], **kwargs) -> None:
        """Initialize the McpTool.

        Args:
            conf: tool config
        """
        super(McpTool, self).__init__(conf, **kwargs)
        self.action_executor = MCPToolExecutor(self)

    async def reset(self, *, seed: int | None = None, options: Dict[str, str] | None = None) -> Tuple[
        Observation, dict[str, Any]]:
        self._finished = False
        return build_observation(observer=self.name(), ability=""), {}

    async def close(self) -> None:
        self._finished = True
        # default only close playwright
        await self.action_executor.close(self.conf.get('close_servers', ['ms-playwright']))

    async def do_step(self,
             actions: list[ActionModel],
             **kwargs) -> Tuple[Observation, float, bool, bool, dict[str, Any]]:
        """Step of tool.

        Args:
            actions: actions
            **kwargs: -
        Returns:
            Observation, float, bool, bool, dict[str, Any]: -
        """
        self._finished = False
        reward = 0
        fail_error = ""
        terminated = kwargs.get("terminated", False)
        # todo sandbox
        agent = AgentFactory.agent_instance(actions[0].agent_name)
        if not actions:
            self._finished = True
            observation = build_observation(observer=self.name(),
                                            content="raw actions is empty",
                                            ability="")
            return (observation,
                    reward,
                    terminated,
                    kwargs.get("truncated", False),
                    {"exception": "actions is empty"})

        mcp_actions = []
        for action in actions:
            tool_name = action.tool_name
            if 'mcp' != tool_name:
                logger.warning(f"Unsupported tool: {tool_name}")
                continue
            full_tool_name = action.action_name
            names = full_tool_name.split("__")
            if len(names) < 2:
                logger.warning(f"{full_tool_name} illegal format")
                continue
            action.action_name = names[1]
            action.tool_name = names[0]
            mcp_actions.append(action)
        if not mcp_actions:
            self._finished = True
            observation = build_observation(observer=self.name(),
                                            content="no valid mcp actions",
                                            ability=actions[-1].action_name)
            return (observation, reward,
                    terminated,
                    kwargs.get("truncated", False),
                    {"exception": "no valid mcp actions"})

        action_results = None
        try:
            # todo sandbox
            if agent and agent.sandbox:
                sand_box = agent.sandbox
                action_results = await sand_box.mcpservers.call_tool(action_list=mcp_actions)
                message = Message()
                message.payload= action_results
            else:
                action_results, ignore = await self.action_executor.async_execute_action(mcp_actions)
            reward = 1
        except Exception as e:
            fail_error = str(e)
        finally:
            self._finished = True

        observation = build_observation(observer=self.name(),
                                        ability=actions[-1].action_name)
        if action_results:
            for res in action_results:
                if res.is_done:
                    terminated = res.is_done
                if res.error:
                    fail_error += res.error

            observation.action_result = action_results
            observation.content = action_results[-1].content

        info = {"exception": fail_error, **kwargs}
        return (observation,
                reward,
                terminated,
                kwargs.get("truncated", False),
                info)

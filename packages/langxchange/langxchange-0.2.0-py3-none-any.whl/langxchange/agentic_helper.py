# langxchange/agentic_helper.py

import yaml
import uuid  # for unique agent IDs
import time
import difflib
import random
from datetime import datetime
from typing import Any, Dict, List, Optional

from langxchange.agent_memory_helper import AgentMemoryHelper


class HierarchicalGoal:
    def __init__(
        self,
        description: str,
        subgoals: Optional[List['HierarchicalGoal']] = None
    ):
        self.description = description
        self.subgoals = subgoals or []
        self.completed = False
        self.parent: Optional['HierarchicalGoal'] = None
        for sg in self.subgoals:
            sg.parent = self

    def add_subgoal(self, subgoal: 'HierarchicalGoal') -> None:
        subgoal.parent = self
        self.subgoals.append(subgoal)

    def mark_completed(self) -> None:
        self.completed = True
        if self.parent and all(sg.completed for sg in self.parent.subgoals):
            self.parent.mark_completed()

    def is_fully_completed(self) -> bool:
        if not self.completed:
            return False
        return all(sg.is_fully_completed() for sg in self.subgoals)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'description': self.description,
            'completed': self.completed,
            'subgoals': [sg.to_dict() for sg in self.subgoals]
        }

    def __repr__(self) -> str:
        status = '✅' if self.completed else '❌'
        return f"{status} {self.description!r} ({len(self.subgoals)} subgoals)"


class LLMAgentHelper:
    """
    LLM-driven agent: sense -> think -> decide -> act -> perceive,
    supports internal memory and optional external memory offload.
    """
    def __init__(
        self,
        llm,
        action_space: List[str],
        agent_id: Optional[str] = None,
        memory: Optional[List[str]] = None,
        config_path: Optional[str] = None,
        external_memory_helper: Optional[AgentMemoryHelper] = None
    ):
        self.llm = llm
        # assign a unique agent ID if not provided
        self.agent_id = agent_id if agent_id is not None else uuid.uuid4().hex
        self.action_space = action_space
        self.memory = memory or []
        self.observation_log: List[str] = []
        self.current_goal: Optional[str] = None
        self.config: Dict[str, Any] = {}
        if config_path:
            with open(config_path) as f:
                self.config = yaml.safe_load(f)

        self.external_memory = external_memory_helper
        self.use_external = external_memory_helper is not None
        # max internal memory capacity
        self._max_memory = 5000
        self._offload_size = 2000

    def set_goal(self, goal: str) -> None:
        self.current_goal = goal

    def perceive(self, observation: str) -> None:
        """Capture a new observation, manage internal/external memory cap."""
        timestamp = datetime.utcnow().isoformat()
        entry = f"[{timestamp}] {observation}"
        self.memory.append(entry)
        if len(self.memory) > self._max_memory:
            chunk = self.memory[-self._offload_size:]
            if self.use_external:
                for obs in chunk:
                    text = obs.split('] ', 1)[1]
                    self.external_memory.add_memory(
                        agent_id=self.agent_id,
                        role='observation',
                        text=text
                    )
            else:
                self.observation_log.extend(chunk)
            self.memory = self.memory[:-self._offload_size]
        if self.use_external:
            self.external_memory.add_memory(
                agent_id=self.agent_id,
                role='observation',
                text=observation
            )

    def think(self) -> str:
        if not self.current_goal:
            raise RuntimeError("No goal set. Call set_goal() first.")
        if self.use_external:
            recent = self.external_memory.get_recent(self.agent_id, n=5)
            obs = [text for _, _, text in recent]
        else:
            obs = self.memory[-5:]
        messages = [
            {'role': 'system', 'content': 'You are an intelligent assistant.'},
            {'role': 'user', 'content': (
                f"Goal: {self.current_goal}\n"
                "Recent obs:\n" + "\n".join(obs) + "\n\nAnalysis?"
            )}
        ]
        return self.llm.chat(messages=messages).strip()

    def decide(self, thought: str) -> str:
        options = ''.join(f'- {a}' for a in self.action_space)
        messages = [
            {'role': 'system', 'content': 'You are a decision maker.'},
            {'role': 'user', 'content': (f"Thought: {thought} Choose one action from: {options} Reply with the action name.")}
        ]
        raw = self.llm.chat(messages=messages).strip()
        # direct match
        if raw in self.action_space:
            return raw
        # extract quoted action if present
        import re
        m = re.search(r'"([^"]+)"', raw)
        if m:
            candidate = m.group(1).strip()
            if candidate in self.action_space:
                return candidate
        # fuzzy match fallback
        matches = difflib.get_close_matches(raw, self.action_space, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        # final error
        raise ValueError(f"Invalid action: {raw}")

    def act(self, action: str) -> str:
        outcomes = [
            f"Action '{action}' succeeded.",
            f"Action '{action}' failed.",
            f"Action '{action}' unexpected."
        ]
        return random.choice(outcomes)

    def run_cycle(self) -> Dict[str, str]:
        thought = self.think()
        action = self.decide(thought)
        outcome = self.act(action)
        self.perceive(outcome)
        return {'thought': thought, 'action': action, 'outcome': outcome}

    def get_agent_id(self) -> str:
        """
        Return the unique identifier for this agent.
        """
        return self.agent_id


class PlanningAgent(LLMAgentHelper):
    """Adds hierarchical goals and planning on top of LLMAgentHelper."""
    def __init__(
        self,
        llm,
        action_space: List[str],
        agent_id: str,
        memory: Optional[List[str]] = None,
        config_path: Optional[str] = None,
        external_memory_helper: Optional[AgentMemoryHelper] = None
    ):
        super().__init__(
            llm, action_space, agent_id,
            memory=memory,
            config_path=config_path,
            external_memory_helper=external_memory_helper
        )
        self.goal_stack: List[HierarchicalGoal] = []
        self.current_plan: List[str] = []

    def set_hierarchical_goal(self, goal: HierarchicalGoal) -> None:
        self.goal_stack = [goal]
        self.current_plan = []

    def create_plan(self) -> None:
        top = self.goal_stack[-1]
        prompt = (
            f"Goal: {top.description}\n\n"
            "Create a numbered plan with actions from:\n"
            f"{', '.join(self.action_space)}\n\nPlan:"
        )
        plan_text = self.llm.chat(messages=[
            {'role':'system','content':'Expert planner.'},
            {'role':'user','content':prompt}
        ])
        lines = [ln.strip() for ln in plan_text.splitlines() if ln.strip()]
        self.current_plan = []
        for ln in lines:
            cleaned = ln.lstrip('0123456789. ').strip()
            if cleaned in self.action_space:
                self.current_plan.append(cleaned)

    def think(self) -> str:
        if not self.current_plan:
            self.create_plan()
        top = self.goal_stack[-1]
        if self.use_external:
            recent = self.external_memory.get_recent(self.agent_id, n=5)
            obs = [t for _,_,t in recent]
        else:
            obs = self.memory[-5:]
        msg = (
            f"Current goal: {top.description}\n\n"
            "Plan:\n" + "\n".join(f"- {s}" for s in self.current_plan)
            + "\n\nRecent obs:\n" + "\n".join(obs)
            + "\n\nNext action?"
        )
        return self.llm.chat(messages=[
            {'role':'system','content':'Planner assistant.'},
            {'role':'user','content':msg}
        ]).strip()

    def update_goals(self) -> None:
        if not self.goal_stack:
            return
        top = self.goal_stack[-1]
        if top.completed:
            self.goal_stack.pop()
            self.current_plan = []
            for sg in top.subgoals:
                if not sg.completed:
                    self.goal_stack.append(sg)
                    break

    def run_cycle(self) -> Dict[str, str]:
        thought = self.think()
        action = self.decide(thought)
        outcome = self.act(action)
        self.perceive(outcome)
        if self.current_plan and action == self.current_plan[0]:
            self.current_plan.pop(0)
            if not self.current_plan:
                self.goal_stack[-1].mark_completed()
        self.update_goals()
        return {'thought':thought,'action':action,'outcome':outcome}


class MemoryAwareAgent(PlanningAgent):
    """Wrapper that ensures all observations also tagged by role and uses external memory."""
    def __init__(
        self,
        llm,
        action_space: List[str],
        agent_id: Optional[str] = None,
        role: str = 'agent',
        memory: Optional[List[str]] = None,
        config_path: Optional[str] = None,
        sqlite_path: str = "agent_memory.db",
        useext_ram: bool = False
    ):
        # pass agent_id through; helper assigns if None
        ext = AgentMemoryHelper(
            llm_helper=llm,
            sqlite_path=sqlite_path
        ) if useext_ram else None
        super().__init__(
            llm,
            action_space,
            agent_id,
            memory=memory,
            config_path=config_path,
            external_memory_helper=ext
        )
        self.role = role

    def perceive(self, observation: str) -> None:
        super().perceive(observation)
        # additional tagging if needed

    def think(self) -> str:
        return super().think()

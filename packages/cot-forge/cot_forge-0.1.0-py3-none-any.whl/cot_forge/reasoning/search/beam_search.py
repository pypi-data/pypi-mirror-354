"""
Beam search implementation for generating reasoning chains.

This search algorithm explores multiple reasoning paths in parallel, 
maintaining a "beam" (chain) of the most promising candidates at each step.
It expands the reasoning chain by applying different strategies and selecting 
the most promising ones based on a scoring mechanism.

The algorithm begins with an initial chain-of-thought (CoT) and iteratively expands it.
At each step, it considers multiple strategies to extend each beam,
evaluates the resulting paths using a scorer, 
and keeps only the top `beam_width` paths for further exploration.

The search continues until a termination condition is met 
(e.g., a solution is found or the maximum depth is reached).

Key aspects:
    - Parallel Exploration: Explores multiple reasoning paths simultaneously.
    - Strategy-Driven Expansion: Uses a variety of strategies to generate next steps in reasoning chains.
    - Scoring Mechanism: Evaluates the generated strategies and selects the most promising paths.
    - Verification: Checks the validity of the generated chain using a verifier.

Logical flow:
    1. Initialization: Start with an initial CoT.
    2. Beam Initialization: Create initial beams, each employing a distinct strategy 
        (reusing strategies if `beam_width` exceeds the number of available strategies).
    3. Iterative Expansion:
        a. Strategy Selection: For each beam, select the best strategy to extend the reasoning chain.
        b. Scoring: Evaluate the expanded beams using a scoring mechanism.
        c. Beam Pruning: Keep only the top `beam_width` beams.
        d. Verification: Check if the generated chain is valid using a verifier; if valid, mark it as final.
    4. Termination: Continue until a termination condition is met (e.g., maximum depth reached).
    5. Result: Return all beams.
"""
# TODO: Multithread the beam search

import logging
from typing import Any

from cot_forge.llm import LLMProvider
from cot_forge.reasoning.scorers import BaseScorer
from cot_forge.reasoning.strategies import (
    InitializeCoT,
    ScoredStrategySelector,
    StrategyRegistry,
    default_strategy_registry,
)
from cot_forge.reasoning.types import ReasoningNode, SearchResult
from cot_forge.reasoning.verifiers import BaseVerifier
from cot_forge.utils.search_utils import generate_and_parse_cot

from .search_algorithm import BaseSearch

logger = logging.getLogger(__name__)


class BeamSearch(BaseSearch):
  """
  Simple beam search to produce multiple parallel reasoning chains.

  This class implements a beam search algorithm to generate multiple reasoning chains
  in parallel. It uses a scoring mechanism to evaluate the generated strategies and selects the
  most promising paths for further exploration.

  Attributes:
      beam_width (int): Number of beams to be explored.
      branching_factor (int): Number of strategies to consider at each node when extending each beam.
      max_depth (int): Maximum depth for the search.
      name (str): Name of the search algorithm.
      description (str): Description of the search algorithm.
      strategy_selector (ScoredStrategySelector): Strategy selector for scoring strategies.

  Usage:
      To use this class, create an instance of `BeamSearch` and call its `_search` method
      with the required arguments. For example:

      ```python
      search = BeamSearch(beam_width=3, max_depth=5)
      result = search._search(
          question="What is the capital of France?",
          ground_truth_answer="Paris",
          search_llm=my_llm_provider,
          scorer=my_scorer,
          verifier=my_verifier
      )
      print(result.success)
      ```
  """

  def __init__(self,
               beam_width: int = 2,
               branching_factor: int = 3,
               max_depth: int = 3,
               ):
    self.beam_width = beam_width
    self.branching_factor = branching_factor
    self.max_depth = max_depth
    self.name = "beam_search"
    self.description = ("A search algorithm that explores multiple parallel "
                        "reasoning chains using beam search, "
                        "maintaining and expanding the most promising paths based on scoring.")
    self.strategy_selector = ScoredStrategySelector()

  def to_dict(self):
    """
    Convert the search algorithm to a dictionary representation.

    Returns:
        dict: Dictionary representation of the search algorithm.
    """
    return {
        "class_name": self.__class__.__name__,
        "name": self.name,
        "description": self.description,
        "beam_width": self.beam_width,
        "branching_factor": self.branching_factor,
        "max_depth": self.max_depth,
    }

  @classmethod
  def from_dict(cls, data: dict):
    """
    Create a search algorithm instance from a dictionary representation.

    Args:
        data (dict): Dictionary representation of the search algorithm.

    Returns:
        BeamSearch: Instance of the search algorithm.
    """
    return cls(
        beam_width=data.get("beam_width"),
        branching_factor=data.get("branching_factor"),
        max_depth=data.get("max_depth"),
    )

  def initialize_cot(
      self,
      question: str,
      ground_truth_answer: str,
      verifier: BaseVerifier,
      search_llm: LLMProvider,
      llm_kwargs: dict[str, Any] = None
  ) -> ReasoningNode:
    """
    Initialize the chain of thought (CoT) with the initial question and response.

    This method generates the initial reasoning node by applying the 
    [InitializeCoT] strategy and verifying the generated response.

    Args:
        question (str): The question to answer.
        ground_truth_answer (str): The true answer to the question.
        verifier (BaseVerifier): The verifier used to check the correctness of the initial response.
        search_llm (LLMProvider): The LLM provider used to generate the initial CoT.
        llm_kwargs (dict[str, Any], optional): Additional keyword arguments for the LLM provider.

    Returns:
        ReasoningNode: The initial reasoning node containing the generated CoT.

    Raises:
        Exception: If an error occurs during the generation or verification process.

    See Also:
        cot_forge.reasoning.strategies.InitializeCoT: Strategy for initializing CoT
    """
    strategy = InitializeCoT
    prompt = strategy.build_prompt(question)

    response, cot = generate_and_parse_cot(
        llm_provider=search_llm,
        prompt=prompt,
        llm_kwargs=llm_kwargs,
        logger=logger,
        on_error="retry",
        max_retries=3
    )

    initial_node = self.create_node(
        strategy=strategy,
        prompt=prompt,
        response=response,
        cot=cot,
        metadata={"is_initial": True}
    )

    self.verify_node(
        node=initial_node,
        question=question,
        ground_truth_answer=ground_truth_answer,
        verifier=verifier,
        on_error='continue',
        logger=logger
    )

    return initial_node

  def initialize_beams(
      self,
      initial_node: ReasoningNode,
      strategy_registry: StrategyRegistry,
      scorer: BaseScorer,
      depth: int,
      search_llm: LLMProvider,
      question: str,
      ground_truth_answer: str,
      verifier: BaseVerifier,
      llm_kwargs: dict[str, Any] = None,
  ) -> list[ReasoningNode]:
    """
    Initialize the beams for the beam search by creating multiple reasoning nodes.

    This method generates a list of reasoning nodes (beams) starting from the given initial node.
    Each beam is created by applying a distinct strategy selected from the strategy registry.
    The strategies are scored using the provided scorer, and the resulting nodes are verified
    for correctness using the verifier.

    Args:
        initial_node (ReasoningNode): The starting node for the beam search.
        strategy_registry (StrategyRegistry): The registry containing available reasoning strategies.
        scorer (BaseScorer): The scorer used to evaluate and rank the strategies.
        depth (int): The current depth in the search process.
        search_llm (LLMProvider): The LLM provider used to generate reasoning steps.
        question (str): The question being answered.
        ground_truth_answer (str): The true answer to the question for verification/scoring purposes.
        verifier (BaseVerifier): The verifier used to check correctness of the generated reasoning nodes.
        llm_kwargs (dict[str, Any], optional): Additional keyword arguments for the LLM provider.

    Returns:
        list[ReasoningNode]: A list of initialized reasoning nodes (beams) created from the initial node.

    Raises:
        ValueError: If an error occurs during strategy selection or node creation.

    Example:
        ```python
        beams = search_instance.initialize_beams(
            initial_node=initial_node,
            strategy_registry=strategy_registry,
            scorer=scorer,
            depth=1,
            search_llm=search_llm,
            question="What is the capital of France?",
            ground_truth_answer="Paris",
            verifier=verifier,
            llm_kwargs={"temperature": 0.7}
        )
        print(f"Initialized {len(beams)} beams.")
        ```
    """

    llm_kwargs = llm_kwargs or {}
    # Set the number of strategies to consider as the maximum of the branching factor and beam width
    # This ensures that we consider enough strategies to fulfill the beam width
    # If the number of strategies is less than the beam width, we can reuse strategies
    num_considered_strategies = max(self.branching_factor, self.beam_width)

    # Create a list to hold the beams
    # This will be a list of ReasoningNode objects
    beams = []

    try:
      scored_strategies = self.strategy_selector.select(
          search_llm=search_llm,
          registry=strategy_registry,
          depth=depth,
          num_strategies=self.beam_width,
          num_considered=num_considered_strategies,
          nodes=[initial_node],
          question=question,
          ground_truth_answer=ground_truth_answer,
          scorer=scorer,
          llm_kwargs=llm_kwargs,
          logger=logger
      )
    except Exception as e:
      # logger.error("Error in selecting strategies")
      raise ValueError("Failed to select strategies") from e

    # Unpack the search data. Should be a list of length 1 for the initial node.
    scored_strategies = scored_strategies[0]
    # scored_strategies is a dictionary of dictionaries. Key is irrelevant.
    for search_data in scored_strategies.values():
      selection_count = search_data['selection_count']
      # If selection count is 0, create a new pruned node out of it
      if selection_count == 0:
        self.create_node(
            strategy=search_data['strategy'],
            prompt=search_data['prompt'],
            response=search_data['response'],
            cot=search_data['cot'],
            parent=initial_node,
            pruned=True,
            metadata={"is_initial": False, "score": search_data['score']}
        )
      # Otherwise, create `count_value` new nodes for the selected strategy
      # Add to the beams list
      else:
        for _ in range(selection_count):
          new_beam = self.create_node(
              strategy=search_data['strategy'],
              prompt=search_data['prompt'],
              response=search_data['response'],
              cot=search_data['cot'],
              parent=initial_node,
              metadata={"is_initial": False, "score": search_data['score']}
          )
          beams.append(new_beam)

    # Check if the new node is a terminal node with verifier
    for beam in beams:
      self.verify_node(
          node=beam,
          question=question,
          ground_truth_answer=ground_truth_answer,
          verifier=verifier,
          on_error="retry",
          logger=logger
      )

    return beams

  def _search(
      self,
      question: str,
      ground_truth_answer: str,
      search_llm: LLMProvider,
      scorer: BaseScorer,
      verifier: BaseVerifier,
      strategy_registry: StrategyRegistry = default_strategy_registry,
      llm_kwargs: dict[str, Any] = None,
  ) -> SearchResult:
    """
    Perform a beam search to generate possible chains of thought.

    This method explores multiple reasoning paths in parallel, maintaining a beam of the most
    promising candidates at each step. It iteratively expands the reasoning chains, evaluates
    them using a scoring mechanism, and prunes the beam to keep only the top candidates.

    Args:
        question (str): The question to answer.
        ground_truth_answer (str): The true answer to the question.
        search_llm (LLMProvider): The LLM provider used to generate reasoning steps.
        scorer (BaseScorer): The scorer used to evaluate different beam options.
        verifier (BaseVerifier): The verifier used to check the correctness of final answers.
        strategy_registry (StrategyRegistry, optional): The registry of available strategies.
        llm_kwargs (dict[str, Any], optional): Additional keyword arguments for reasoning LLM calls.

    Returns:
        SearchResult: An object containing the terminal nodes of the beams, success status, and metadata.

    Raises:
        ValueError: If an error occurs during strategy selection or beam initialization.
    """
    # Assert that scorer is provided
    if scorer is None:
      raise ValueError("Scorer must be provided for beam search.")

    # Create initial node
    try:
      initial_node = self.initialize_cot(
          question=question,
          ground_truth_answer=ground_truth_answer,
          verifier=verifier,
          search_llm=search_llm,
          llm_kwargs=llm_kwargs
      )
    except Exception:
      # logger.error(f"Error in initializing CoT: {e}")
      return SearchResult(terminal_nodes=None,
                          question=question,
                          ground_truth_answer=ground_truth_answer,
                          success=False,
                          metadata={"depth": -1, "reason": "Failed to initialize CoT"})

    # Check if initial node is already successful
    if initial_node.success:
      return SearchResult(
          question=question,
          ground_truth_answer=ground_truth_answer,
          terminal_nodes=[initial_node],
          success=True,
          metadata={"depth": 0, "reason": "Initial node is already successful"}
      )

    # Initialize the beams
    try:
      beams = self.initialize_beams(
          initial_node=initial_node,
          strategy_registry=strategy_registry,
          scorer=scorer,
          depth=1,
          search_llm=search_llm,
          question=question,
          ground_truth_answer=ground_truth_answer,
          verifier=verifier,
          llm_kwargs=llm_kwargs,
      )
    except Exception:
      # logger.error(f"Error in initializing beams: {e}")
      return SearchResult(
          terminal_nodes=None,
          question=question,
          ground_truth_answer=ground_truth_answer,
          success=False,
          metadata={
              "depth": 0,
              "reason": "Failed to initialize beams"
          }
      )

    # Check if all beams are already successful
    if all(beam.success for beam in beams):
      return SearchResult(
          question=question,
          ground_truth_answer=ground_truth_answer,
          terminal_nodes=beams,
          success=True,
          metadata={"depth": 1,
                    "reason": "All beams successful at initialization"}
      )

    depth = 1
    # Range starts at 2 because we already have the initial node and beams, zero based indexing
    for depth in range(2, self.max_depth+1):
      # Get number of activte beams to pass as number of strategies to select
      num_active_beams = len([beam for beam in beams if not beam.is_final])
      # Track new beams
      new_beams = []
      try:
        scored_strategies = self.strategy_selector.select(
            search_llm=search_llm,
            registry=strategy_registry,
            depth=depth,
            question=question,
            ground_truth_answer=ground_truth_answer,
            num_strategies=num_active_beams,
            num_considered=self.branching_factor,
            nodes=beams,
            scorer=scorer,
            llm_kwargs=llm_kwargs,
            logger=logger
        )
      except Exception as e:
        # logger.error("Error in selecting strategies")
        raise ValueError("Failed to select strategies") from e

      for idx, strat_dict in enumerate(scored_strategies):
        # If beam is already final, skip it
        if beams[idx].is_final:
          # Add the beam to the new beams list to continue tracking it
          new_beams.append(beams[idx])
          continue
        # Unpack the search data
        for search_data in strat_dict.values():
          # If selection count is 0, create a new pruned node out of it
          if search_data['selection_count'] == 0:
            self.create_node(
                strategy=search_data['strategy'],
                prompt=search_data['prompt'],
                response=search_data['response'],
                cot=search_data['cot'],
                parent=beams[idx],
                pruned=True,
                metadata={"is_initial": False, "score": search_data['score']}
            )
          # Otherwise, create `count_value` new nodes for the selected strategy
          # Add to the beams list
          else:
            for _ in range(search_data['selection_count']):
              new_beam = self.create_node(
                  strategy=search_data['strategy'],
                  prompt=search_data['prompt'],
                  response=search_data['response'],
                  cot=search_data['cot'],
                  parent=beams[idx],
                  metadata={"is_initial": False, "score": search_data['score']}
              )
              new_beams.append(new_beam)

      # Update the beams list with the new beams
      beams = new_beams

      # Verify the new beams
      for new_node in beams:
        # If the node is already final, skip it
        if new_node.is_final:
          continue
        # Verify the node
        self.verify_node(
            node=new_node,
            question=question,
            ground_truth_answer=ground_truth_answer,
            verifier=verifier,
            on_error='continue',
            logger=logger
        )

      # Check if all beams are final, if so, break the loop
      if all(beam.is_final for beam in beams):
        break

    # Set each terminal node as final once loop is complete
    for beam in beams:
      beam.is_final = True

    reason = "Max depth reached" if depth == self.max_depth else "All beams successful"
    result = SearchResult(
        question=question,
        ground_truth_answer=ground_truth_answer,
        terminal_nodes=beams,
        success=any(node.success for node in beams),
        metadata={
            "depth": depth,
            "reason": reason
        }
    )

    return result

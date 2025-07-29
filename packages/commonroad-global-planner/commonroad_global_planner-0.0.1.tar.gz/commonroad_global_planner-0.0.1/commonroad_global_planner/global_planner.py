from commonroad.planning.planning_problem import PlanningProblem
from commonroad.scenario.scenario import Scenario

# commonroad
import commonroad_velocity_planner.fast_api as velocity_api
from commonroad_route_planner.route_planner import RoutePlanner, LaneletSequence
from commonroad_route_planner.reference_path_planner import ReferencePathPlanner
from commonroad_route_planner.reference_path import ReferencePath
from commonroad_velocity_planner.global_trajectory import GlobalTrajectory

from typing import List

from commonroad_velocity_planner.velocity_planner_interface import ImplementedPlanners


class GlobalPlanner:
    """
    Global Planner for CommonRoad scenarios. This is essentially a small wrapper around the commonroad-route-planner
    for route and reference path planning and the commonroad velocity planner for velocity profile planning.
    """

    def __init__(
        self,
        scenario: Scenario,
        planning_problem: PlanningProblem,
    ) -> None:
        """
        CommonRoad global planner. The global planner can generate a route, reference path and velocity profile.
        It is essentially a wrapper for the commonroad-route-planner and the commonroad-velocity-planner.
        :param scenario: cr scenario object
        :param planning_problem: cr planning problem
        """
        self._scenario: Scenario = scenario
        self._planning_problem: PlanningProblem = planning_problem

    @property
    def scenario(self) -> Scenario:
        """
        :return: cr scenario
        """
        return self._scenario

    @scenario.setter
    def scenario(self, scenario: Scenario) -> None:
        """
        :param scenario: cr scenario
        """
        self._scenario = scenario

    @property
    def planning_problem(self) -> PlanningProblem:
        """
        :return: cr planning problem
        """
        return self._planning_problem

    @planning_problem.setter
    def planning_problem(self, planning_problem: PlanningProblem) -> None:
        """
        :param planning_problem: cr planning problem
        """
        self._planning_problem = planning_problem

    def plan_global_trajectory(
        self,
        retrieve_shortest: bool = True,
        consider_least_lance_changes: bool = True,
        velocity_planner: ImplementedPlanners = ImplementedPlanners.QPPlanner,
        use_regulatory_stop_elements: bool = False,
        regulatory_elements_time_step: int = 0,
    ) -> GlobalTrajectory:
        """
        Plans reference path considering one or more route options
        :param retrieve_shortest: if true, shortest route will be used
        :param consider_least_lance_changes: if true, fewer lane changes will be preferred.
        :param velocity_planner: velocity planner to be used
        :param use_regulatory_stop_elements: if true, traffic lights and stop lines will be considered
        :param regulatory_elements_time_step: if use_regulatory_stop_elements, this time step will be used for
        :return: global trajectory
        """
        routes: List[LaneletSequence] = self.plan_routes()
        reference_path: ReferencePath = self.plan_reference_path(
            routes=routes,
            retrieve_shortest=retrieve_shortest,
            consider_least_lance_changes=consider_least_lance_changes,
        )
        return self.plan_velocity_profile(
            reference_path=reference_path,
            velocity_planner=velocity_planner,
            use_regulatory_stop_elements=use_regulatory_stop_elements,
            regulatory_elements_time_step=regulatory_elements_time_step,
        )

    def plan_routes(self) -> List[LaneletSequence]:
        """
        Plan routes, defined as sequence of lanelets
        :return: list of different routes, aka lanelet sequences
        """
        route_planner = RoutePlanner(
            lanelet_network=self._scenario.lanelet_network,
            planning_problem=self._planning_problem,
        )
        return route_planner.plan_routes()

    def plan_reference_path(
        self,
        routes: List[LaneletSequence],
        retrieve_shortest: bool = True,
        consider_least_lance_changes: bool = True,
    ) -> ReferencePath:
        """
        Plans reference path considering one or more route options
        :param routes: route options
        :param retrieve_shortest: if true, will return shortest reference path
        :param consider_least_lance_changes: if true, will return reference path with leas lane changes
        :return: reference path
        """

        ref_path_planner: ReferencePathPlanner = ReferencePathPlanner(
            lanelet_network=self._scenario.lanelet_network,
            planning_problem=self._planning_problem,
            routes=routes,
        )

        return ref_path_planner.plan_shortest_reference_path(
            retrieve_shortest=retrieve_shortest,
            consider_least_lance_changes=consider_least_lance_changes,
        )

    def plan_velocity_profile(
        self,
        reference_path: ReferencePath,
        velocity_planner: ImplementedPlanners = ImplementedPlanners.QPPlanner,
        use_regulatory_stop_elements: bool = False,
        regulatory_elements_time_step: int = 0,
    ) -> GlobalTrajectory:
        """
        Plan velocity profile given a reference path
        :param reference_path: cr reference path
        :param velocity_planner: velocity planner to be used
        :param use_regulatory_stop_elements: if true, traffic lights and stop lines will be considered
        :param regulatory_elements_time_step: if use_regulatory_stop_elements, this time step will be used for
        traffic lights
        :return: global trajectory
        """
        return (
            velocity_api.global_trajectory_from_cr_reference_path_and_planning_problem(
                cr_reference_path=reference_path,
                planning_problem=self._planning_problem,
                lanelet_network=self._scenario.lanelet_network,
                velocity_planner=velocity_planner,
                use_regulatory_elements=use_regulatory_stop_elements,
                regulatory_elements_time_step=regulatory_elements_time_step,
            )
        )

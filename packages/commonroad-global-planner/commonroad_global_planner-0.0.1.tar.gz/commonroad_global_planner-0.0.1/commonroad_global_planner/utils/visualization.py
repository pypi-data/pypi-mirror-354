from dataclasses import dataclass

# commonroad
from commonroad.planning.planning_problem import PlanningProblem
from commonroad.scenario.scenario import Scenario
from commonroad_velocity_planner.global_trajectory import GlobalTrajectory
from commonroad_velocity_planner.utils.visualization.visualize_velocity_planner import (
    visualize_global_trajectory as vgt,
)


@dataclass
class VppWrapper:
    """
    Small wrapper so visualize global trajectory can be used from cr velocity planner
    """

    planning_problem: PlanningProblem


def visualize_global_trajectory(
    scenario: Scenario,
    planning_problem: PlanningProblem,
    global_trajectory: GlobalTrajectory,
    save_path: str,
    size_x: float = 10.0,
    save_img: bool = False,
    saving_format: str = "png",
    test: bool = False,
) -> None:
    """
    Visualizes global trajectory
    :param scenario: cr scenario
    :param planning_problem: planning problem object
    :param global_trajectory: global trajectory object
    :param save_path: path to save image to
    :param size_x: fig size
    :param save_img: if true, saves image, otherwise displays it
    :param saving_format: saving format
    :param test: if true, neither displays nor saves iamge
    """
    vgt(
        scenario=scenario,
        velocity_planning_problem=VppWrapper(planning_problem),
        global_trajectory=global_trajectory,
        save_path=save_path,
        size_x=size_x,
        save_img=save_img,
        saving_format=saving_format,
        test=test,
    )

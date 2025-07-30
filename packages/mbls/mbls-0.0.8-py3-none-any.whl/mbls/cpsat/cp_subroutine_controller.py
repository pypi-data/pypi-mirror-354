from abc import abstractmethod
from datetime import datetime
from typing import Generic, Optional, TypeVar

from routix import (
    DynamicDataObject,
    ElapsedTimer,
    SolverOutputSummary,
    SubroutineController,
)

from .custom_cp_model import CustomCpModel

ProblemT = TypeVar("ProblemT")  # Type for the problem instance
CpModelT = TypeVar("CpModelT", bound=CustomCpModel)
StoppingCriteriaT = TypeVar("StoppingCriteriaT", bound=DynamicDataObject)


class CpSubroutineController(
    SubroutineController, Generic[ProblemT, CpModelT, StoppingCriteriaT]
):
    """
    Subroutine controller utilizing OR-Tools CP model.
    This controller manages the execution of a CP model subroutine,
    including the creation of the model, solving it, and logging results.
    """

    def __init__(
        self,
        instance: ProblemT,
        shared_param_dict: dict,
        cp_model_class: type[CpModelT],
        subroutine_flow: DynamicDataObject,
        stopping_criteria: StoppingCriteriaT,
        start_dt: Optional[datetime] = None,
        expr_name: Optional[str] = None,
    ):
        """
        Initialize the CpSubroutineController.
        - Set up the subroutine controller with algorithm data.
        - Create an instance of base CP model using the provided instance and shared parameters.
        - Set the number of base constraints of the CP model.

        Args:
            instance (ProblemT): Instance-specific parameters for the CP model.
            shared_param_dict (dict): Shared parameters for the CP model.
            cp_model_class (type[CpModelT]): The class of the CP model to be used.
            subroutine_flow (DynamicDataObject): The flow of the subroutine to be executed.
            stopping_criteria (StoppingCriteriaT): Stopping criteria for the controller.
            start_dt (Optional[datetime], optional): Start date and time for the controller. Defaults to None.
            expr_name (Optional[str], optional): Name of the experiment. Defaults to None.
        """
        _expr_name = expr_name or str(
            getattr(instance, "name", "CP Subroutine Controller")
        )
        super().__init__(
            name=_expr_name,
            subroutine_flow=subroutine_flow,
            stopping_criteria=stopping_criteria,
            start_dt=start_dt,
        )

        self.instance = instance
        """Instance-specific parameters for the CP model."""
        self.shared_param_dict = shared_param_dict
        """Shared parameters for the CP model."""
        self.cp_model_class = cp_model_class
        """The class of the CP model to be used."""

        self._obj_value_log: list[tuple[float, float]] = []
        """
        Log of objective values during the solving process.
        Each entry is a tuple of (elapsed time, objective value).
        """
        self._obj_bound_log: list[tuple[float, float]] = []
        """
        Log of known lower (upper) bound found when min(max)imizing.
        Each entry is a tuple of (elapsed time, best bound).
        """

        self.cp_model = self.create_base_cp_model()
        self.cp_model.set_num_base_constraints()

    @property
    def obj_value_log(self) -> list[tuple[float, float]]:
        """Get the objective value log.

        Returns:
            list[tuple[float, float]]: List of tuples containing (elapsed time, objective value).
        """
        return self._obj_value_log.copy()

    @property
    def obj_bound_log(self) -> list[tuple[float, float]]:
        """Get the objective bound log.

        Returns:
            list[tuple[float, float]]: List of tuples containing (elapsed time, best bound).
        """
        return self._obj_bound_log.copy()

    @abstractmethod
    def create_base_cp_model(self) -> CpModelT:
        """Create and return a CP model instance."""
        pass

    @staticmethod
    def add_obj_value_log(
        log_entry: tuple[float, float],
        obj_value_log: list[tuple[float, float]],
        is_maximize: bool = False,
    ) -> None:
        """Update the objective value log with a single tuple.

        Args:
            log_entry (tuple[float, float]): (elapsed time, objective value)
            obj_value_log (list[tuple[float, float]]): List to append objective value logs.
        """
        latest_obj_value = obj_value_log[-1][1] if obj_value_log else None
        if latest_obj_value is None or (
            (is_maximize and log_entry[1] > latest_obj_value)
            or (not is_maximize and log_entry[1] < latest_obj_value)
        ):
            # Only append if the new objective value is better than the last one
            # (or if it's the first entry in the log)
            # This ensures that we only log improvements in the objective value.
            obj_value_log.append((log_entry[0], log_entry[1]))
        else:
            # If the new objective value is not better, we do not log it.
            # This avoids cluttering the log with non-improving values.
            pass

    @staticmethod
    def add_obj_bound_log(
        log_entry: tuple[float, float],
        obj_bound_log: list[tuple[float, float]],
        is_maximize: bool = False,
    ) -> None:
        """Update the objective bound log with a single tuple.

        Args:
            log_entry (tuple[float, float]): (elapsed time, objective bound)
            obj_bound_log (list[tuple[float, float]]): List to append objective bound logs.
        """
        latest_obj_bound = obj_bound_log[-1][1] if obj_bound_log else None
        if latest_obj_bound is None or (
            (is_maximize and log_entry[1] < latest_obj_bound)
            or (not is_maximize and log_entry[1] > latest_obj_bound)
        ):
            # Only append if the new bound is better than the last one
            # (or if it's the first entry in the log)
            # This ensures that we only log improvements in the objective bound.
            obj_bound_log.append((log_entry[0], log_entry[1]))
        else:
            # If the new bound is not better, we do not log it.
            # This avoids cluttering the log with non-improving bounds.
            pass

    @staticmethod
    def add_to_obj_log(
        log_entry: tuple[float, float, float],
        obj_value_log: list[tuple[float, float]],
        obj_bound_log: list[tuple[float, float]],
        is_maximize: bool = False,
        obj_value_is_valid: bool = False,
        obj_bound_is_valid: bool = False,
    ) -> None:
        """Update the objective value and bound logs with a single tuple.

        Args:
            log_entry (tuple[float, float, float]): (elapsed time, objective value, best bound)
            obj_value_log (list[tuple[float, float]]): List to append objective value logs.
            obj_bound_log (list[tuple[float, float]]): List to append objective bound logs.
            obj_value_is_valid (bool, optional): If True, adds the objective value log.
                Defaults to False.
            obj_bound_is_valid (bool, optional): If True, adds the objective bound log.
                Defaults to False.
        """
        if obj_value_is_valid:
            CpSubroutineController.add_obj_value_log(
                (log_entry[0], log_entry[1]), obj_value_log, is_maximize=is_maximize
            )
        if obj_bound_is_valid:
            CpSubroutineController.add_obj_bound_log(
                (log_entry[0], log_entry[2]), obj_bound_log, is_maximize=is_maximize
            )

    def add_obj_log(
        self,
        log_entry: tuple[float, float, float],
        is_maximize: bool = False,
        obj_value_is_valid: bool = False,
        obj_bound_is_valid: bool = False,
    ) -> None:
        """Update the objective value and bound logs with a single tuple.

        Args:
            log_entry (tuple[float, float, float]): (elapsed time, objective value, best bound)
            is_maximize (bool, optional): If True, indicates maximization problem.
                Defaults to False.
            obj_value_is_valid (bool, optional): If True, adds the objective value log.
                Defaults to False.
            obj_bound_is_valid (bool, optional): If True, adds the objective bound log.
                Defaults to False.
        """
        self.add_to_obj_log(
            log_entry=log_entry,
            obj_value_log=self._obj_value_log,
            obj_bound_log=self._obj_bound_log,
            is_maximize=is_maximize,
            obj_value_is_valid=obj_value_is_valid,
            obj_bound_is_valid=obj_bound_is_valid,
        )

    @staticmethod
    def append_to_obj_log(
        log_list: list[tuple[float, float, float]],
        obj_value_log: list[tuple[float, float]],
        obj_bound_log: list[tuple[float, float]],
        is_maximize: bool = False,
        obj_value_is_valid: bool = False,
        obj_bound_is_valid: bool = False,
    ) -> None:
        """Update the objective value and bound logs with a list of tuples.

        Args:
            log_list (list[tuple[float, float, float]]): List of tuples containing
                (elapsed time, objective value, best bound).
            obj_value_log (list[tuple[float, float]]): List to append objective value logs.
            obj_bound_log (list[tuple[float, float]]): List to append objective bound logs.
            is_maximize (bool, optional): If True, indicates maximization problem.
                Defaults to False.
            obj_value_is_valid (bool, optional): If True, adds the objective value log.
                Defaults to False.
            obj_bound_is_valid (bool, optional): If True, adds the objective bound log.
                Defaults to False.
        """
        if obj_value_is_valid or obj_bound_is_valid:
            for log_entry in log_list:
                CpSubroutineController.add_to_obj_log(
                    log_entry,
                    obj_value_log,
                    obj_bound_log,
                    is_maximize=is_maximize,
                    obj_value_is_valid=obj_value_is_valid,
                    obj_bound_is_valid=obj_bound_is_valid,
                )

    def append_obj_log(
        self,
        log_list: list[tuple[float, float, float]],
        is_maximize: bool = False,
        obj_value_is_valid: bool = False,
        obj_bound_is_valid: bool = False,
    ) -> None:
        """Update the objective value and bound logs with a list of tuples.

        Args:
            log_list (list[tuple[float, float, float]]): List of tuples containing
                (elapsed time, objective value, best bound).
            is_maximize (bool, optional): If True, indicates maximization problem.
                Defaults to False.
            obj_value_is_valid (bool, optional): If True, adds the objective value log.
                Defaults to False.
            obj_bound_is_valid (bool, optional): If True, adds the objective bound log.
                Defaults to False.
        """
        self.append_to_obj_log(
            log_list,
            self._obj_value_log,
            self._obj_bound_log,
            is_maximize=is_maximize,
            obj_value_is_valid=obj_value_is_valid,
            obj_bound_is_valid=obj_bound_is_valid,
        )

    def solve_cp_model(
        self,
        cp_model: CpModelT,
        computational_time: float,
        num_workers: int,
        random_seed: Optional[int] = None,
        timer: Optional[ElapsedTimer] = None,
        obj_value_is_valid: bool = False,
        obj_bound_is_valid: bool = False,
    ) -> SolverOutputSummary:
        """Solve the given CP model.

        Args:
            cp_model (CpModelT): The CP model to be solved.
            computational_time (float): The maximum computational time in seconds.
            num_workers (int): The number of parallel workers (i.e. threads) to use during search.
            random_seed (Optional[int], optional): Random seed for reproducibility. Defaults to None.
            timer (Optional[ElapsedTimer], optional): Timer to be passed to solver callback. Defaults to None.
            obj_value_is_valid (bool, optional): If True, adds the objective value log.
                Defaults to False.
            obj_bound_is_valid (bool, optional): If True, adds the objective bound log.
                Defaults to False.

        Raises:
            AttributeError: If self.cp_model is not initialized.

        Returns:
            SolverOutputSummary: A summary of the solver output, including status,
                elapsed time, objective value, best objective bound, and progress log.
        """
        (solver_status, elapsed_time, obj_value, obj_bound) = (
            cp_model.solve_with_prog_logger(
                computational_time=computational_time,
                num_workers=num_workers,
                random_seed=random_seed,
                timer=timer,
            )
        )
        progress_log = cp_model.get_progress_log()
        self.append_obj_log(
            log_list=progress_log,
            is_maximize=cp_model.is_maximize(),
            obj_value_is_valid=obj_value_is_valid,
            obj_bound_is_valid=obj_bound_is_valid,
        )

        return SolverOutputSummary(
            status=solver_status,
            elapsed_time=elapsed_time,
            objective_value=obj_value,
            best_objective_bound=obj_bound,
            progress_log=progress_log,
        )

    def solve_current_cp_model(
        self,
        computational_time: float,
        num_workers: int,
        random_seed: Optional[int] = None,
        timer: Optional[ElapsedTimer] = None,
        obj_value_is_valid: bool = False,
        obj_bound_is_valid: bool = False,
    ) -> SolverOutputSummary:
        """Solve the current CP model.

        Args:
            computational_time (float): The maximum computational time in seconds.
            num_workers (int): The number of parallel workers (i.e. threads) to use during search.
            random_seed (Optional[int], optional): Random seed for reproducibility. Defaults to None.
            timer (Optional[ElapsedTimer], optional): Timer to be passed to solver callback. Defaults to None.
            obj_value_is_valid (bool, optional): If True, adds the objective value log.
                Defaults to False.
            obj_bound_is_valid (bool, optional): If True, adds the objective bound log.
                Defaults to False.

        Raises:
            AttributeError: If self.cp_model is not initialized.

        Returns:
            SolverOutputSummary: A summary of the solver output, including status,
                elapsed time, objective value, best objective bound, and progress log.
        """
        if not hasattr(self, "cp_model"):
            raise AttributeError("CP model is not initialized.")
        return self.solve_cp_model(
            cp_model=self.cp_model,
            computational_time=computational_time,
            num_workers=num_workers,
            random_seed=random_seed,
            timer=timer,
            obj_value_is_valid=obj_value_is_valid,
            obj_bound_is_valid=obj_bound_is_valid,
        )

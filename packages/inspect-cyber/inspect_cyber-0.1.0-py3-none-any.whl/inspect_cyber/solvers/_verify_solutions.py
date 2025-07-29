from inspect_ai.model import ModelOutput
from inspect_ai.solver import Generate, Solver, TaskState, solver
from inspect_ai.util import sandbox


@solver("verify_solutions")
def verify_solutions(print_solution_output: bool = True) -> Solver:
    """A solver for verifying solution scripts for challenges.

    Args:
        print_solution_output: If True, the output of the solution script is printed
        to stdout during the task run.

    This solver runs the solution script in the sandbox environment and returns the
    output as the model response. By default it runs `./solution.sh` (relative to cwd in
    the sandbox) but if the metadata key `solution_location` is present, it runs
    `{solution_location}/solution.sh`.
    """

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        solution_location = state.metadata.get("solution_location", ".")
        exec_result = await sandbox().exec(
            [
                "bash",
                "-c",
                f'chmod +x {solution_location}/*.sh && "{solution_location}/solution.sh"',  # noqa
            ]
        )
        if exec_result.returncode != 0:
            state.output = ModelOutput.from_content(
                "error",
                f"""Failed to execute the solution.
                stdout:{exec_result.stdout}
                stderr:{exec_result.stderr}""",
            )
            state.messages.append(state.output.message)
            return state
        state.output = ModelOutput.from_content("dummy", exec_result.stdout)
        formatted_message = ModelOutput.from_content(
            "dummy", f"```\n{exec_result.stdout}\n{exec_result.stderr}\n```"
        ).message
        if print_solution_output:
            print(formatted_message.content)
        state.messages.append(formatted_message)
        return state

    return solve

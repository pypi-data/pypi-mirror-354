# ruff: noqa: D100

# Standard
import argparse
from pathlib import Path

# First party
from .logger import logger
from .workflow import Workflow

def gen_workflow(args: argparse.Namespace) -> None:
    """Generate a workflow from a YAML description."""
    logger.debug("gen_workflow() START")
    
    # Load workflow from YAML file
    w = Workflow.from_yaml(Path(args.input_yaml))
    if len(w) == 0:
        msg = f"No workflow in {args.input_yaml}"
        raise ValueError(msg)
    if len(w) > 1:
        msg = f"Multiple workflows in {args.input_yaml}"
        raise ValueError(msg)

    # Generate output
    match args.output_type:
        case "bash":
            w[0].to_bash(Path(args.output_file), tagline=not args.no_tagline)
        case "pegasus":
            w[0].to_pegasus_dag(Path(args.output_file),
                                tagline=not args.no_tagline)
        case _:
            msg = f"Unknown output type: {args.output_type}"
            raise ValueError(msg)

def add_gen_workflow_subcmd(p: argparse.ArgumentParser) -> None:
    """Add subcmd gen-workflow."""
    p.set_defaults(func = gen_workflow)

    # Tag line
    p.add_argument("--no-tagline", action="store_true",
                   help = "Do not add tagline to the output script.")

    # YAML input file
    p.add_argument("-i", "--input-yaml",
                   help = ("Path to the YAML file containing the workflow"
                           " description."))

    # Output file
    p.add_argument("-o", "--output-file",
                   help = "Path to the output file")

    # Output type
    p.add_argument("-t", "--output-type", choices = ["bash", "pegasus"],
                   help = "Set the output type.")

#!/usr/bin/env python

import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from typing import Iterator

import relab
import torch
from relab import agents
from relab.helpers.Typing import Parameter
from torch import nn


def describe(
    network_name: str, parameters: Iterator[Parameter], memory_unit: str = "GB"
) -> None:
    """
    Describe the parameters passed as arguments.
    :param network_name: the name of the neural network whose parameters are passed as arguments
    :param parameters: the parameters to describe
    :param memory_unit: the unit to use describe the model size (B, KB, MB or GB)
    """

    # The size of one parameter in bits for each data type.
    dtype_sizes = {
        torch.complex128: 128,
        torch.cdouble: 128,
        torch.float64: 64,
        torch.double: 64,
        torch.complex64: 64,
        torch.cfloat: 64,
        torch.int64: 64,
        torch.long: 64,
        torch.float32: 32,
        torch.float: 32,
        torch.int32: 32,
        torch.int: 32,
        torch.float16: 16,
        torch.half: 16,
        torch.bfloat16: 16,
        torch.int16: 16,
        torch.short: 16,
        torch.uint8: 8,
        torch.int8: 8,
    }

    # The number of bytes for each memory unit.
    memory_units = {
        "B": 1,
        "KB": 1e3,
        "MB": 1e6,
        "GB": 1e9,
    }

    # Count the number of parameters, keep track of their types, and memory usage.
    dtypes = []
    memory_usage = 0
    total_n_params = 0
    for params in parameters:
        dtype = params.dtype
        dtypes.append(dtype)
        n_params = params.numel()
        total_n_params += n_params
        memory_usage += n_params * dtype_sizes[dtype] / (8 * memory_units[memory_unit])

    # Display the parameter summary on the standard output.
    if all([dtype == dtypes[0] for dtype in dtypes]) is True:
        dtypes = dtypes[0]
    logging.info(f"- Network: {network_name}")
    logging.info(f"  Parameter type: {dtypes}.")
    logging.info(f"  Number of parameters: {total_n_params}.")
    logging.info(f"  Parameters memory size: {memory_usage:0.3f} {memory_unit}.")


def describe_params(agent: str, env: str, seed: int) -> None:
    """
    Describe the agent's parameters.
    :param agent: the agent name
    :param env: the environment name
    :param seed: the random seed
    """

    # Initialize the benchmark.
    relab.initialize(agent, env, seed)

    # Create the requested agent.
    logging.info(f"Describing the {agent} parameters:")
    agent = agents.make(agent, training=True)

    # Describe the agent parameters.
    for i, attribute_name in enumerate(dir(agent)):
        attribute = getattr(agent, attribute_name)
        if isinstance(attribute, nn.Module):
            describe(attribute_name, attribute.parameters())


def main():
    """
    Entry point of the describe_params.py script.
    """

    # Parse the script arguments.
    parser = ArgumentParser(
        prog="describe_params.py", formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--agent",
        type=str,
        default="DuelingDDQN",
        help="name of the agent whose policy needs to be demonstrated",
    )
    parser.add_argument(
        "--env",
        type=str,
        default="ALE/Pong-v5",
        help="name of the environment on which to demonstrate the agent's policy",
    )
    parser.add_argument("--seed", type=int, default=0, help="random seed to use")
    args = parser.parse_args()

    # Describe the agent's parameters.
    describe_params(agent=args.agent, env=args.env, seed=args.seed)


if __name__ == "__main__":
    main()

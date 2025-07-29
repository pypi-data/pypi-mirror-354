from typing import Tuple

import torch
from relab.agents.networks.layers.Categorical import Categorical
from relab.agents.networks.layers.DiagonalGaussian import DiagonalGaussian
from torch import Tensor, nn


class ContinuousTransitionNetwork(nn.Module):
    """!
    Class implementing a transition network with continuous latent variables.
    """

    def __init__(self, n_actions: int = 18, n_continuous_vars: int = 10) -> None:
        """!
        Constructor.
        @param n_actions: the number of allowable actions
        @param n_continuous_vars: the number of continuous latent variables
        """

        # Call the parent constructor.
        super().__init__()

        # @var net
        # Transition network that predicts the next state distribution.
        self.net = nn.Sequential(
            nn.Linear(n_continuous_vars + n_actions, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            DiagonalGaussian(512, n_continuous_vars),
        )

        # @var n_actions
        # Number of allowable actions in the environment.
        self.n_actions = n_actions

    def forward(self, states: Tensor, actions: Tensor) -> Tensor:
        """!
        Perform the forward pass through the network.
        @param states: the input states
        @param actions: the input actions
        @return the mean and the log of the variance of the diagonal Gaussian
        """
        actions = torch.one_hot(actions.to(torch.int64), self.n_actions)
        x = torch.cat((states, actions), dim=1)
        return self.net(x)


class DiscreteTransitionNetwork(nn.Module):
    """!
    Class implementing a transition network with discrete latent variables.
    """

    def __init__(
        self, n_actions: int = 18, n_discrete_vars: int = 20, n_discrete_vals: int = 10
    ) -> None:
        """!
        Constructor.
        @param n_actions: the number of actions available to the agent
        @param n_discrete_vars: the number of discrete latent variables
        @param n_discrete_vals: the number of values taken by all the discrete latent variables,
            or a list describing the number of values taken by each discrete latent variable
        """

        # Call the parent constructor.
        super().__init__()

        # @var net
        # Transition network that predicts the next state distribution.
        self.net = nn.Sequential(
            nn.Linear(n_discrete_vars * n_discrete_vals + n_actions, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            Categorical(512, n_discrete_vars, n_discrete_vals),
        )

        # @var n_actions
        # Number of allowable actions in the environment.
        self.n_actions = n_actions

    def forward(self, states: Tensor, actions: Tensor) -> Tensor:
        """!
        Perform the forward pass through the network.
        @param states: the input states
        @param actions: the input actions
        @return the log-probabilities of the categorical
        """
        actions = torch.one_hot(actions.to(torch.int64), self.n_actions)
        x = torch.cat((states, actions), dim=1)
        return self.net(x)


class MixedTransitionNetwork(nn.Module):
    """!
    Class implementing a transition network with discrete and continuous latent variables.
    """

    def __init__(
        self,
        n_actions: int = 18,
        n_continuous_vars: int = 10,
        n_discrete_vars: int = 20,
        n_discrete_vals: int = 10,
    ) -> None:
        """!
        Constructor.
        @param n_actions: the number of actions available to the agent
        @param n_continuous_vars: the number of continuous latent variables
        @param n_discrete_vars: the number of discrete latent variables
        @param n_discrete_vals: the number of values taken by all the discrete latent variables,
            or a list describing the number of values taken by each discrete latent variable
        """

        # Call the parent constructor.
        super().__init__()

        # @var net
        # Transition network that predicts the next state distribution.
        n_latent_vars = n_continuous_vars + n_discrete_vars * n_discrete_vals
        self.net = nn.Sequential(
            nn.Linear(n_latent_vars + n_actions, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
        )

        # @var gaussian_head
        # Network head that outputs the mean and log variance of the continuous
        # latent variables.
        self.gaussian_head = DiagonalGaussian(512, n_continuous_vars)

        # @var categorical_head
        # Network head that outputs the log-probabilities of the discrete
        # latent variables.
        self.categorical_head = Categorical(512, n_discrete_vars, n_discrete_vals)

        # @var n_actions
        # Number of allowable actions in the environment.
        self.n_actions = n_actions

    def forward(self, states: Tensor, actions: Tensor) -> Tuple[Tensor, Tensor]:
        """!
        Perform the forward pass through the network.
        @param states: the input states
        @param actions: the input actions
        @return the mean and the log-variance of the diagonal Gaussian, and the log-probabilities of the categorical
        """
        actions = torch.one_hot(actions.to(torch.int64), self.n_actions)
        x = torch.cat((states, actions), dim=1)
        x = self.net(x)
        return self.gaussian_head(x), self.categorical_head(x)

import torch
from library.cpp.agents.memory import FastReplayBuffer


class ReplayBuffer:
    """!
    @brief Python wrapper around replay buffer implemented in C++.

    @details
    The implementation is based on the following papers:

    <b>Prioritized experience replay</b>,
    published on arXiv, 2015.

    Authors:
    - Tom Schaul

    <b>Learning to predict by the methods of temporal differences</b>,
    published in Machine learning, 3:9–44, 1988.

    Authors:
    - Richard S. Sutton

    More precisely, the replay buffer supports multistep Q-learning and
    prioritization of experiences according to their associated loss.
    """

    def __init__(self) -> None:
        """!
        Create a replay buffer.
        """

        # @var buffer
        # The C++ implementation of the replay buffer.
        self.buffer = FastReplayBuffer()

    def append(self, experience: torch.Tensor) -> None:
        """!
        Add a new experience to the buffer.
        @param experience: the experience to add
        """
        self.buffer.append(experience)

    def __len__(self) -> int:
        """!
        Retrieve the number of elements in the buffer.
        @return the number of elements contained in the replay buffer
        """
        return self.buffer.length()

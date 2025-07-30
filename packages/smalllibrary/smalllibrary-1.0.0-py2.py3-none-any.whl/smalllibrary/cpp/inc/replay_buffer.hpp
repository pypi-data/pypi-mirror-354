// Copyright 2025 Theophile Champion. No Rights Reserved.
/**
 * @file replay_buffer.hpp
 * @brief Declaration of the replay buffer class.
 */

#ifndef RELAB_CPP_INC_AGENTS_MEMORY_REPLAY_BUFFER_HPP_
#define RELAB_CPP_INC_AGENTS_MEMORY_REPLAY_BUFFER_HPP_

#include <torch/extension.h>

#include <experimental/filesystem>
#include <map>
#include <memory>
#include <string>

namespace relab::agents::memory {

/**
 * @brief Class implementing a replay buffer.
 *
 * @details
 * For more information about the original papers, please refer to the
 * documentation of MDQN and PrioritizedDQN.
 */
class ReplayBuffer {
 private:
  // The buffer storing the observations.
  std::vector<torch::Tensor> observations;

 public:
  /**
   * Create a replay buffer.
   * @param capacity the number of experience the buffer can store
   * @param batch_size the size of the batch to sample
   * @param frame_skip the number of times each action is repeated in the
   * environment, if None use the configuration
   * @param stack_size the number of stacked frame in each observation, if None
   * use the configuration
   * @param screen_size: the size of the images used by the agent to learn
   * @param type the type of compression to use
   * @param args the prioritization and multistep arguments composed of:
   *     - initial_priority: the maximum experience priority given to new transitions
   *     - omega: the prioritization exponent
   *     - omega_is: the important sampling exponent
   *     - n_children: the maximum number of children each node of the priority-tree can have
   *     - n_steps: the number of steps for which rewards are accumulated in multistep Q-learning
   *     - gamma: the discount factor
   */
  ReplayBuffer();

  /**
   * Add a new experience to the buffer.
   * @param obs the experience to add
   */
  void append(const torch::Tensor &obs);

  /**
   * Retrieve the number of elements in the buffer.
   * @return the number of elements contained in the replay buffer
   */
  int size();
};
}  // namespace relab::agents::memory

#endif  // RELAB_CPP_INC_AGENTS_MEMORY_REPLAY_BUFFER_HPP_

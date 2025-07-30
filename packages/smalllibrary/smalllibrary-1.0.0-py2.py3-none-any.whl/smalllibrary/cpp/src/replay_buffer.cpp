// Copyright 2025 Theophile Champion. No Rights Reserved.

#include "agents/memory/replay_buffer.hpp"

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <map>
#include <memory>
#include <random>
#include <string>

#include "helpers/debug.hpp"
#include "helpers/serialize.hpp"
#include "helpers/torch.hpp"

namespace relab::agents::memory {

ReplayBuffer::ReplayBuffer() {}

void ReplayBuffer::append(const torch::Tensor &obs) {
  this->observations->append(obs);
}

int ReplayBuffer::size() { return this->observations->size(); }

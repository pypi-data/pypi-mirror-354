// Copyright 2025 Theophile Champion. No Rights Reserved.

#include <pybind11/pybind11.h>

#include "agents/memory/replay_buffer.hpp"

namespace py = pybind11;
using relab::agents::memory::ReplayBuffer;

PYBIND11_MODULE(cpp, m) {
  m.doc() = "A module providing C++ acceleration for ReLab.";

  py::class_<ReplayBuffer>(m, "FastReplayBuffer")
      .def(py::init<>())
      .def("append", &ReplayBuffer::append, "Add an experience to the replay buffer.")

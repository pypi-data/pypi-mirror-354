// Copyright 2025 Theophile Champion. No Rights Reserved.
/**
 * @file priority_tree.hpp
 * @brief Declaration of the priority tree class.
 */

#ifndef RELAB_CPP_INC_AGENTS_MEMORY_PRIORITY_TREE_HPP_
#define RELAB_CPP_INC_AGENTS_MEMORY_PRIORITY_TREE_HPP_

#include <torch/extension.h>

#include <string>
#include <vector>

namespace relab::agents::memory::impl {

// Alias for a sum-tree.
using SumTree = std::vector<std::vector<double>>;

// Alias for a max-tree.
using MaxTree = std::vector<torch::Tensor>;

/**
 * @brief A class storing the experience priorities.
 */
class PriorityTree {
 private:
  // Store the priority tree parameters.
  float initial_priority;
  int capacity;
  int n_children;

  // The trees' depth, and the current index.
  int depth;
  int current_id;

  // Boolean keeping track of whether the sum-tree needs to be refreshed
  bool need_refresh_all;

  // Create a tensor of priorities, an empty sum-tree and an empty max-tree.
  torch::Tensor priorities;
  SumTree sum_tree;
  MaxTree max_tree;

 public:
  /**
   * Create a priority tree.
   * @param capacity the tree's capacity
   * @param initial_priority the initial priority given to first elements
   * @param n_children the number of children each node has
   */
  PriorityTree(int capacity, float initial_priority, int n_children);

  /**
   * Create a sum-tree.
   * Importantly, tree elements must be double to avoid numerical precision
   * error of torch tensors.
   * @param depth the tree's depth
   * @param n_children the number of children each node has
   * @return the tree
   */
  static SumTree createSumTree(int depth, int n_children);

  /**
   * Create a max-tree.
   * Importantly, tree elements must be double to avoid numerical precision
   * error of torch tensors.
   * @param depth the tree's depth
   * @param n_children the number of children each node has
   * @return the tree
   */
  static MaxTree createMaxTree(int depth, int n_children);

  /**
   * Compute the sum of all priorities.
   * @return the sum of all priorities
   */
  double sum();

  /**
   * Find the largest priority.
   * @return the largest priority
   */
  float max();

  /**
   * Empty the priority tree.
   */
  void clear();

  /**
   * Retrieve the number of priorities stored in the priority tree.
   * @return the number of priorities stored in the priority tree
   */
  int size();

  /**
   * Add a priority in the priority tree.
   * @param priority the new priority
   */
  void append(float priority);

  /**
   * Retrieve a priority from the priority tree.
   * @param index the index of the experience whose priority must be retrieved
   * @return the priority
   */
  float get(int index);

  /**
   * Replace a priority in the priority tree.
   * @param index the index of the experience whose priority must be replaced
   * @param priority the new priority
   */
  void set(int index, float priority);

  /**
   * Transform an experience index to its internal index.
   * @param index the experience index
   * @return the internal index
   */
  int internalIndex(int index);

  /**
   * Transform an internal index to its experience index.
   * @param index the internal index
   * @return the experience index
   */
  int externalIndex(int index);

  /**
   * Sample indices of buffer elements proportionally to their priorities.
   * @param n the number of indices to sample
   * @return the sampled indices
   */
  torch::Tensor sampleIndices(int n);

  /**
   * Compute the experience index associated to the sampled priority using
   * inverse transform sampling (tower sampling).
   * @param priority the sampled priority
   * @return the experience index
   */
  int towerSampling(float priority);

  /**
   * Compute the index of the parent element.
   * @param idx the index of the element whose parent index must be computed
   * @return the parent index
   */
  int parentIndex(int idx);

  /**
   * Update the sum-tree to reflect an element being set to a new priority.
   * @param index the internal index of the element
   * @param old_priority the old priority
   */
  void updateSumTree(int index, float old_priority);

  /**
   * Refresh the entire sum-tree.
   */
  void refreshAllSumTree();

  /**
   * Update the max-tree to reflect an element being set to a new priority.
   * @param index the internal index of the element
   * @param old_priority the old priority
   */
  void updateMaxTree(int index, float old_priority);

  /**
   * Compute the maximum value among the child nodes.
   * @param depth the depth of the parent node
   * @param parent_index the internal index of the parent node
   * @param index the internal index of the node whose value is being set to a
   * new priority
   * @param old_priority the old priority
   * @param new_priority the new priority
   * @return the maximum value
   */
  float maxChildValue(int depth, int parent_index, int index, float old_priority, float new_priority);

  /**
   * Create a string representation of the max-tree.
   * @param max_n_elements the maximum number of elements to display, by default
   * all elements are displayed
   * @return a string representing the tree
   */
  std::string maxTreeToStr(int max_n_elements = -1);

  /**
   * Create a string representation of the sum-tree.
   * @param max_n_elements the maximum number of elements to display, by default
   * all elements are displayed
   * @return a string representing the tree
   */
  std::string sumTreeToStr(int max_n_elements = -1);

  /**
   * Create a string representation of a tree.
   * @param tree the tree to convert into a string
   * @param get a function returning the j-th element of the i-th row in the
   * tree
   * @param max_n_elements the maximum number of elements to display, by default
   * all elements are displayed
   * @param precision the number of decimal digits used to display the tree
   * elements
   * @return a string representing the tree
   */
  template <class Tree, class T>
  std::string treeToStr(Tree tree, T (*get)(Tree, int, int), int max_n_elements = -1, int precision = 1);

  /**
   * Load the priority tree from the checkpoint.
   * @param checkpoint a stream reading from the checkpoint file
   */
  void load(std::istream &checkpoint);

  /**
   * Save the priority tree in the checkpoint.
   * @param checkpoint a stream writing into the checkpoint file
   */
  void save(std::ostream &checkpoint);

  /**
   * Print the priority tree on the standard output.
   * @param verbose true if the full priority tree should be displayed, false
   * otherwise
   * @param prefix the prefix to add an front of the optional information
   */
  void print(bool verbose = false, const std::string &prefix = "");

  /**
   * Compare two priority trees.
   * @param lhs the priority tree on the left-hand-side of the equal sign
   * @param rhs the priority tree on the right-hand-side of the equal sign
   * @return true if the priority trees are identical, false otherwise
   */
  friend bool operator==(const PriorityTree &lhs, const PriorityTree &rhs);
};
}  // namespace relab::agents::memory::impl

namespace relab::agents::memory {
using impl::PriorityTree;
}  // namespace relab::agents::memory

#endif  // RELAB_CPP_INC_AGENTS_MEMORY_PRIORITY_TREE_HPP_

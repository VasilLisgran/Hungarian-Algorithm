# Hungarian Method for the Assignment Problem

An elegant and robust implementation of the **Hungarian Method** (Kuhn-Munkres algorithm) developed in **Wolfram Mathematica** and **Python**. This project was created as part of a university research project ("Computer Mathematica Systems") at Saint Petersburg State University of Economics (UNECON).

The algorithm solves the classical maximum-weight assignment problem (and can be adapted for minimum-cost) using linear programming duality, alternating paths, and potential adjustments based on the theorems of König and Egerváry.

---

## 📌 Project Overview

In management, planning, and optimization problems, it is frequently necessary to distribute limited resources among tasks or jobs to achieve maximum efficiency.
* **Scenario:** Assign $n$ individuals to $n$ jobs, where each individual has a specific qualification rating or efficiency value for each job.
* **Objective:** Find a bijective mapping (one-to-one assignment) that **maximizes the total rating** (or minimizes total costs).
* **Complexity:** While a naive brute-force approach requires $O(n!)$ operations, the Hungarian method systematically converges in polynomial time ($O(n^3)$).

---

## 📐 Mathematical Formulation

### 1. The Matrix & Assignment Permutation
Let $R = [r_{ij}]$ be an $n \times n$ rating matrix with positive real entries ($r_{ij} > 0$), where $r_{ij}$ represents the performance score of worker $i$ on job $j$. An assignment is a permutation of indices:

$$\begin{pmatrix} 1 & 2 & \dots & n \\ j_1 & j_2 & \dots & j_n \end{pmatrix}$$

The primary primal objective is to find a permutation that maximizes:
$$\max \sum_{i=1}^{n} r_{i, j_i}$$

### 2. Dual Problem & Adequate Budget
The dual optimization model introduces a set of potentials (budgets) $u_i$ for each individual and $v_j$ for each job. A budget configuration is defined as **adequate** (or valid coverage) if:

$$u_i + v_j \ge r_{ij}, \quad \forall i,j \in \{1, \dots, n\}$$

The dual objective minimizes the total budget allocation:
$$\min \sum_{i=1}^{n} u_i + \sum_{j=1}^{n} v_j$$

According to the **Duality Theorems**, if we find an adequate budget and a complete assignment such that the total rating equals the dual budget sum ($u_i + v_j = r_{ij}$ for all chosen pairs), both the assignment and the budget are globally optimal.

---

## 🔬 Theoretical Foundations

The algorithm relies on several foundational lemmas and theorems regarding transfers and structural properties of bipartite graphs:

* **Transfers & Alternating Paths:** If a partial matching exists, it can be expanded dynamically. A *transfer* shifts $r$ individuals across jobs, reassigning them onto available or newly vacated positions.
* **König's Theorem:** In any bipartite graph, the size of a maximum matching is equal to the size of a minimum vertex cover. In matrix terms, the maximum number of independent 1s in the qualification matrix $Q$ equals the minimum number of lines (rows/columns) required to cover all 1s.
* **Theorem 7 (Potential Shift):** If a maximum matching in the qualified matrix $Q$ yields $m < n$ pairs, the dual budget can always be strictly decremented by a positive integer $\Delta = n - m > 0$, exposing new valid edges without breaking feasibility.

---

## 💻 Algorithmic Workflow & Code Structure

The program alternates between two core procedures until a complete matching is constructed.

### 1. Initial Potentials Setup
To optimize convergence, the implementation evaluates raw matrix bounds:
* Calculates row maximums ($a_i = \max_j r_{ij}$) and column maximums ($b_j = \max_i r_{ij}$).
* If $\sum a_i \le \sum b_j$, it initializes $u_i = a_i$ and $v_j = 0$. Otherwise, it sets $u_i = 0$ and $v_j = b_j$.

### 2. Routine I: Augmented Path Search (Max Matching)
For a fixed potential state, a binary **Qualification Matrix** $Q$ is computed where $q_{ij} = 1$ if $u_i + v_j = r_{ij}$, and $0$ otherwise.
* A recursive depth-first search (`constructSequence`) traverses unassigned columns to detect alternating augmenting paths.
* When an augmenting path is found, the chain of assignments updates (`matchRow` and `matchCol`), increasing the matching size by 1.

### 3. Routine II: Dual Potential Adjustments
Activated when Routine I stalls with a maximal matching $m < n$.
* Rows are categorized into *reachable* (essential) and *unreachable* (inessential) via alternating trees starting from unassigned columns.
* Columns are classified similarly based on existing match links.
* A boundary value $d$ is determined:
  $$d = \min_{r \in \text{inessRows}, c \in \text{inessCols}} (u_r + v_c - R_{rc})$$
* Potentials are adjusted by $d$ (subtracting from unreachable rows, adding to reachable columns), which systematically preserves feasibility while bringing new zero-reduced-cost edges into $Q$.

---

## 📊 Evaluation Example

The implementation includes a benchmark evaluation on a complex $8 \times 8$ matrix:

```wolfram
R = {
  {92, 64, 17, 83, 45, 71, 38, 56},
  {23, 88, 45, 12, 67, 34, 89, 41},
  {77, 35, 91, 28, 54, 66, 19, 73},
  {44, 59, 12, 87, 33, 68, 92, 27},
  {81, 16, 74, 45, 90, 22, 55, 68},
  {33, 77, 54, 69, 28, 83, 41, 95},
  {66, 43, 88, 31, 76, 59, 27, 84},
  {50, 92, 35, 77, 43, 68, 71, 19}
};

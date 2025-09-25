# Define CPTs as Python dictionaries

# Prior probabilities
P_B = {True: 0.001, False: 0.999}
P_E = {True: 0.002, False: 0.998}

# Conditional probabilities for Alarm given Burglary and Earthquake
P_A_given_BE = {
    (True, True): 0.95,
    (True, False): 0.94,
    (False, True): 0.29,
    (False, False): 0.001
}

# Conditional probabilities for JohnCalls given Alarm
P_J_given_A = {True: 0.90, False: 0.05}

# Conditional probabilities for MaryCalls given Alarm
P_M_given_A = {True: 0.70, False: 0.01}

# Variables order
variables = ['B', 'E', 'A', 'J', 'M']


def joint_probability(assignment):
    """
    Compute the joint probability of a full assignment.
    assignment: dict like {'B': True, 'E': False, 'A': True, 'J': False, 'M': True}
    """
    B = assignment['B']
    E = assignment['E']
    A = assignment['A']
    J = assignment['J']
    M = assignment['M']

    p_B = P_B[B]
    p_E = P_E[E]
    p_A = P_A_given_BE[(B, E)] if A else 1 - P_A_given_BE[(B, E)]
    p_J = P_J_given_A[A] if J else 1 - P_J_given_A[A]
    p_M = P_M_given_A[A] if M else 1 - P_M_given_A[A]

    return p_B * p_E * p_A * p_J * p_M


def all_assignments(vars_list):
    """
    Generate all possible True/False assignments for given variables.
    """
    if not vars_list:
        yield {}
    else:
        first, *rest = vars_list
        for rest_assignment in all_assignments(rest):
            for val in [True, False]:
                assignment = rest_assignment.copy()
                assignment[first] = val
                yield assignment


def marginalize(query_vars, evidence):
    """
    Compute the marginal probability of query_vars given evidence,
    summing over all other variables.
    query_vars: list of variable names to keep (e.g. ['B'])
    evidence: dict of observed variables (e.g. {'J': True, 'M': True})
    Returns a dictionary mapping assignments of query_vars to probabilities.
    """
    hidden_vars = [v for v in variables if v not in query_vars and v not in evidence]

    probs = {}
    for q_assignment in all_assignments(query_vars):
        total = 0.0
        # Merge q_assignment and evidence
        partial_assignment = {**q_assignment, **evidence}

        # Sum over hidden vars
        for h_assignment in all_assignments(hidden_vars):
            full_assignment = {**partial_assignment, **h_assignment}
            total += joint_probability(full_assignment)

        probs[tuple(q_assignment[var] for var in query_vars)] = total

    return probs


def normalize(dist):
    """
    Normalize a probability distribution dictionary so values sum to 1.
    """
    total = sum(dist.values())
    return {k: v / total for k, v in dist.items()}


def query(query_vars, evidence):
    """
    Compute the posterior distribution P(query_vars | evidence).
    Returns normalized distribution over query_vars.
    """
    marginal = marginalize(query_vars, evidence)
    normalized = normalize(marginal)
    return normalized


# Example usage:

if __name__ == "__main__":
    # Query: P(Burglary | JohnCalls=True, MaryCalls=True)
    evidence = {'J': True, 'M': True}
    query_vars = ['B']

    result = query(query_vars, evidence)
    print("P(Burglary | JohnCalls=True, MaryCalls=True):")
    for assignment, prob in result.items():
        print(f"B={assignment[0]}: {prob:.5f}")

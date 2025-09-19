# =============================================================================
# Imports
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, make_blobs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from collections import Counter
import time

# =============================================================================
# Helper Class for LVQ (Questions 1 & 2)
# =============================================================================
class LVQ:
    """A simple from-scratch implementation of Learning Vector Quantization."""
    def __init__(self, n_prototypes_per_class=1, learning_rate=0.3, epochs=100):
        self.n_prototypes_per_class = n_prototypes_per_class
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.prototypes = None
        self.prototype_labels = None

    def fit(self, X, y):
        n_features = X.shape[1]
        classes = np.unique(y)
        
        # Initialize prototypes by picking random samples from each class
        self.prototypes = []
        self.prototype_labels = []
        for c in classes:
            class_samples = X[y == c]
            indices = np.random.choice(len(class_samples), self.n_prototypes_per_class, replace=False)
            for i in indices:
                self.prototypes.append(class_samples[i])
                self.prototype_labels.append(c)
        self.prototypes = np.array(self.prototypes)
        
        for epoch in range(self.epochs):
            rate = self.learning_rate * (1.0 - (epoch / float(self.epochs)))
            
            # Select a random training sample
            i = np.random.randint(0, len(X))
            sample_X, sample_y = X[i], y[i]
            
            # Find Best Matching Unit (BMU)
            distances = [np.linalg.norm(sample_X - p) for p in self.prototypes]
            bmu_index = np.argmin(distances)
            
            # Update prototype
            if self.prototype_labels[bmu_index] == sample_y:
                self.prototypes[bmu_index] += rate * (sample_X - self.prototypes[bmu_index])
            else:
                self.prototypes[bmu_index] -= rate * (sample_X - self.prototypes[bmu_index])
    
    def predict(self, X):
        predictions = []
        for x in X:
            distances = [np.linalg.norm(x - p) for p in self.prototypes]
            bmu_index = np.argmin(distances)
            predictions.append(self.prototype_labels[bmu_index])
        return np.array(predictions)

# =============================================================================
# Question 1: Train an LVQ on the Iris dataset
# =============================================================================
def run_question_1():
    print("--- Question 1: LVQ on Iris Dataset ---")
    
    # 1. Load and prepare data
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Scale features for better performance with distance-based algorithms
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. Split into training (70%) and testing (30%)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)
    
    # 3. Train the LVQ model
    lvq = LVQ(n_prototypes_per_class=2, learning_rate=0.5, epochs=200)
    lvq.fit(X_train, y_train)
    
    # 4. Report classification accuracy
    predictions = lvq.predict(X_test)
    accuracy = np.mean(predictions == y_test)
    
    print(f"LVQ model trained on the Iris dataset.")
    print(f"Classification Accuracy on Test Set: {accuracy * 100:.2f}%\n")

# =============================================================================
# Question 2: Visualize LVQ decision boundaries
# =============================================================================
def run_question_2():
    print("--- Question 2: Visualizing LVQ Decision Boundaries ---")
    
    # 1. Generate a synthetic dataset with 3 classes
    X_synth, y_synth = make_blobs(n_samples=300, centers=3, n_features=2, random_state=42, cluster_std=1.5)
    
    # 2. Train an LVQ model
    lvq_viz = LVQ(n_prototypes_per_class=2, learning_rate=0.5, epochs=500)
    lvq_viz.fit(X_synth, y_synth)
    
    # 3. Create a mesh grid for plotting decision boundaries
    x_min, x_max = X_synth[:, 0].min() - 1, X_synth[:, 0].max() + 1
    y_min, y_max = X_synth[:, 1].min() - 1, X_synth[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.05),
                         np.arange(y_min, y_max, 0.05))

    # 4. Predict the class for each point in the grid
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    Z = lvq_viz.predict(grid_points)
    Z = Z.reshape(xx.shape)

    # 5. Plot the results
    plt.figure(figsize=(10, 7))
    plt.contourf(xx, yy, Z, alpha=0.4, cmap=plt.cm.RdYlBu)
    plt.scatter(X_synth[:, 0], X_synth[:, 1], c=y_synth, s=30, edgecolor='k', cmap=plt.cm.RdYlBu)
    plt.scatter(lvq_viz.prototypes[:, 0], lvq_viz.prototypes[:, 1], c='white', marker='X', s=250, 
                edgecolor='black', linewidth=2, label='Prototypes')
    
    plt.title("Question 2: LVQ Decision Boundaries")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    print("Displaying the plot for LVQ decision boundaries...")
    plt.show()
    print("Plot closed.\n")

# =============================================================================
# Question 3: Implement a SOM and visualize neuron movement
# =============================================================================
def run_question_3():
    print("--- Question 3: Visualizing SOM Neuron Movement ---")
    
    # 1. Define the dataset
    data = np.array([
        [0.1, 0.2], [0.15, 0.25], [0.2, 0.3],  # Class A
        [0.9, 0.8], [0.85, 0.75], [0.8, 0.7]   # Class B
    ])
    
    # 2. SOM Parameters
    n_neurons = 2
    n_epochs = 100
    learning_rate = 0.6
    
    # Initialize neurons randomly
    neurons = np.random.rand(n_neurons, 2)
    initial_neurons = neurons.copy()
    history = [initial_neurons.copy()]

    # 3. Train the SOM
    for epoch in range(n_epochs):
        rate = learning_rate * (1.0 - (epoch / float(n_epochs)))
        sample = data[np.random.randint(0, len(data))]
        
        # Find BMU
        distances = np.linalg.norm(neurons - sample, axis=1)
        bmu_index = np.argmin(distances)
        
        # Update neurons (BMU and its neighbors)
        for i in range(n_neurons):
            # In a 1D SOM of 2 neurons, they are always neighbors
            influence = np.exp(-np.linalg.norm(i - bmu_index)**2 / (2 * (rate**2)))
            neurons[i] += rate * influence * (sample - neurons[i])
        
        if epoch % 10 == 0:
            history.append(neurons.copy())
    
    # 4. Visualize the movement
    history = np.array(history)
    plt.figure(figsize=(10, 7))
    
    # Plot data points
    plt.scatter(data[:3, 0], data[:3, 1], c='blue', label='Class A')
    plt.scatter(data[3:, 0], data[3:, 1], c='red', label='Class B')
    
    # Plot initial neuron positions
    plt.scatter(initial_neurons[:, 0], initial_neurons[:, 1], c='gray', marker='s', s=150, label='Initial Neurons')
    
    # Plot final neuron positions
    plt.scatter(neurons[:, 0], neurons[:, 1], c='black', marker='X', s=250, label='Final Neurons')
    
    # Plot the path of each neuron
    for i in range(n_neurons):
        plt.plot(history[:, i, 0], history[:, i, 1], 'k--', alpha=0.5)

    plt.title("Question 3: SOM Neuron Movement During Training")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.grid(True)
    print("Displaying the plot for SOM neuron movement...")
    plt.show()
    print("Plot closed.\n")


# =============================================================================
# Question 4: Implement an ART network
# =============================================================================
class ART1:
    """A simple from-scratch implementation of ART1 for binary patterns."""
    def __init__(self, vigilance=0.7):
        self.vigilance = vigilance
        self.prototypes = []

    def process_patterns(self, patterns):
        print(f"Initializing ART1 with vigilance ρ = {self.vigilance}\n")
        
        for i, P in enumerate(patterns):
            print(f"--- Presenting Pattern P{i+1}: {P} ---")
            
            if not self.prototypes:
                print("No categories exist. Creating Category 1.")
                self.prototypes.append(P)
                print(f"  - P{i+1} assigned to new Category 1.")
                print(f"  - Prototype for C1 is now: {self.prototypes[0]}\n")
                continue

            # Competition Phase
            match_scores = []
            for T in self.prototypes:
                # Bitwise AND for intersection
                intersection = np.logical_and(P, T).sum()
                match_scores.append(intersection)
            
            # Find best matching units in descending order of match score
            sorted_indices = np.argsort(match_scores)[::-1]
            
            assigned = False
            for j in sorted_indices:
                T = self.prototypes[j]
                intersection_size = match_scores[j]
                pattern_size = P.sum()
                
                print(f"  - Testing against Category {j+1} (Prototype: {T})")
                print(f"    - Match Score = |P ∩ T| = {intersection_size}")
                
                # Vigilance Test
                vigilance_score = intersection_size / pattern_size
                print(f"    - Vigilance Check: {vigilance_score:.3f} >= {self.vigilance}?")
                
                if vigilance_score >= self.vigilance:
                    print("    - Vigilance Test: PASSED.")
                    # Update prototype
                    self.prototypes[j] = np.logical_and(P, T)
                    print(f"  - P{i+1} assigned to existing Category {j+1}.")
                    print(f"  - Prototype for C{j+1} updated to: {self.prototypes[j]}\n")
                    assigned = True
                    break
                else:
                    print("    - Vigilance Test: FAILED.")

            if not assigned:
                print("  - Pattern failed vigilance test for all existing categories.")
                self.prototypes.append(P)
                new_category_idx = len(self.prototypes)
                print(f"  - P{i+1} assigned to new Category {new_category_idx}.")
                print(f"  - Prototype for C{new_category_idx} is: {P}\n")

def run_question_4():
    print("--- Question 4: ART Network for Binary Patterns ---")
    
    # 1. Define patterns and vigilance
    patterns = [
        np.array([1, 0, 1, 0, 1, 0]),
        np.array([1, 1, 0, 0, 1, 0]),
        np.array([0, 1, 0, 1, 0, 1]),
        np.array([1, 0, 0, 1, 1, 0])
    ]
    vigilance = 0.7
    
    # 2. Process patterns
    art = ART1(vigilance=vigilance)
    art.process_patterns(patterns)
    
    # 3. Show final category formation
    print("--- Final Category Formation ---")
    for i, proto in enumerate(art.prototypes):
        print(f"Category {i+1} Prototype: {proto}")
    print()

# =============================================================================
# Main execution block
# =============================================================================
if __name__ == "__main__":
    run_question_1()
    run_question_2()
    run_question_3()
    run_question_4()
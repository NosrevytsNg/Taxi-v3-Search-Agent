
from taxi_env import TaxiRouteSolver

if __name__ == "__main__":
    # Initialize the Taxi Route Solver
    solver = TaxiRouteSolver()

    # Run A* Search
    solver.a_star_search()

    # Run Depth-First Search
    solver.depth_first_search()

    # Run Breadth-First Search
    solver.breadth_first_search()


import gymnasium as gym
from copy import deepcopy
from queue import PriorityQueue, LifoQueue, Queue
import time


class TaxiRouteSolver:
    def __init__(self, env_name="Taxi-v3", render_mode="ansi"):
        try:
            self.env = gym.make(env_name, render_mode=render_mode)
            self.env.reset()
            self.no_of_actions = self.env.action_space.n

            print(f"✅ Environment '{env_name}' initialized successfully.")
            print(f"🎮 Render Mode: {render_mode}")
            print(f"🔢 Action Space Size: {self.no_of_actions}")

        except gym.error.Error as gym_error:
            raise RuntimeError(f"Gym environment error: {gym_error}")

        except Exception as error:
            raise RuntimeError(f"An unexpected error occurred: {error}")

    def results(self, actions_taken=[], reward=0, steps=0, time=0, algo_name="undefined", separator=False):
        print("=" * 50)
        print("📚 Algorithm: {}".format(algo_name))
        print("⏱️ Duration: {:.5f} ms".format(time))
        print("👣 Total Steps: {}".format(steps))
        print("🚕 Actions Taken by Taxi: {}".format(actions_taken))
        print("💰 Total Reward: {}".format(reward))
        print("=" * 50)

        if separator:
            print("\n")

    def heuristic(self, done):
        return {True: 0, False: 1}[done]

    def reconstruct_path(self, predecessors, initial_state, goal_state):
        path = []
        current_state = goal_state
        while current_state != initial_state:
            prev_state, prev_action = predecessors[current_state]
            path.append(prev_action)
            current_state = prev_state
        return path[::-1]

    def a_star_search(self):
        begin_timer = time.time()
        total_no_of_steps = 0
        total_reward = 0

        copy_env = deepcopy(self.env)
        initial_state, _ = copy_env.reset()

        queue = PriorityQueue()
        queue.put((0, initial_state, []))
        visited = set()
        predecessors = {}
        visited.add(initial_state)
        cost = {initial_state: 0}

        while not queue.empty():
            _, state, path = queue.get()

            actions = list(range(self.env.action_space.n))
            while actions:
                action = actions.pop(0)
                copy_env.unwrapped.s = state
                new_state, reward, done, _, _ = copy_env.step(action)
                new_cost = cost[state] + 1

                if new_state not in visited or cost.get(new_state, float('inf')) > new_cost:
                    total_no_of_steps += 1
                    cost[new_state] = new_cost
                    visited.add(new_state)
                    predecessors[new_state] = (state, action)

                    priority = new_cost + self.heuristic(done)
                    queue.put((priority, new_state, path + [action]))
                    total_reward += reward

                if done:
                    final_path = self.reconstruct_path(predecessors, initial_state, new_state)
                    self.results(
                        actions_taken=final_path,
                        reward=total_reward,
                        steps=total_no_of_steps,
                        time=time.time() - begin_timer,
                        algo_name="A* Search",
                        separator=True
                    )
                    return
        print("No solution found")

    def depth_first_search(self):
        begin_timer = time.time()
        total_no_of_steps = 0
        total_reward = 0

        copy_env = deepcopy(self.env)
        initial_state, _ = copy_env.reset()

        stack = LifoQueue()
        stack.put((initial_state, []))
        visited = set()
        predecessors = {}
        visited.add(initial_state)

        while not stack.empty():
            state, path = stack.get()

            actions = list(range(self.env.action_space.n))
            while actions:
                action = actions.pop(0)
                copy_env.unwrapped.s = state
                new_state, reward, done, _, _ = copy_env.step(action)
                total_no_of_steps += 1
                total_reward += reward

                if new_state not in visited:
                    visited.add(new_state)
                    predecessors[new_state] = (state, action)
                    stack.put((new_state, path + [action]))

                if done:
                    final_path = self.reconstruct_path(predecessors, initial_state, new_state)
                    self.results(
                        actions_taken=final_path,
                        reward=total_reward,
                        steps=total_no_of_steps,
                        time=time.time() - begin_timer,
                        algo_name="Depth First Search",
                        separator=True
                    )
                    return
        print("No solution found")

    def breadth_first_search(self):
        begin_timer = time.time()
        total_no_of_steps = 0
        total_reward = 0

        copy_env = deepcopy(self.env)
        initial_state, _ = copy_env.reset()

        queue = Queue()
        queue.put((initial_state, []))
        visited = set()
        predecessors = {}
        visited.add(initial_state)

        while not queue.empty():
            state, path = queue.get()

            actions = list(range(self.env.action_space.n))
            while actions:
                action = actions.pop(0)
                copy_env.unwrapped.s = state
                total_no_of_steps += 1

                new_state, reward, done, _, _ = copy_env.step(action)

                if new_state not in visited:
                    visited.add(new_state)
                    queue.put((new_state, path + [action]))
                    predecessors[new_state] = (state, action)
                    total_reward += reward

                if done:
                    final_path = self.reconstruct_path(predecessors, initial_state, new_state)
                    self.results(
                        actions_taken=final_path,
                        reward=total_reward,
                        steps=total_no_of_steps,
                        time=time.time() - begin_timer,
                        algo_name="Breadth First Search",
                        separator=True
                    )
                    return
        print("No solution found")

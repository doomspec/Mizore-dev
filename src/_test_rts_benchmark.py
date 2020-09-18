from CircuitConstructor._time_evolution_contructor import generate_benchmark_from_file,generate_trotter_benchmark_from_file

if __name__ == "__main__":
    path="mizore_results/adaptive_evolution/Untitled_09-18-02h20m02s"
    print(generate_trotter_benchmark_from_file(path,1))
    print(generate_benchmark_from_file(path))
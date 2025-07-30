"""
Performance Tests for Free Fermion Library

This module contains performance benchmarks and stress tests for the Free Fermion Library,
measuring execution time, memory usage, and scalability of key algorithms.

Test categories:
- Algorithm performance benchmarks
- Scalability tests
- Memory usage tests
- Comparison benchmarks
- Stress tests
"""

import pytest
import numpy as np
import networkx as nx
import time
import gc
import sys
import os
import psutil
from functools import wraps

# Import the library
import ff


def benchmark(func):
    """Decorator to measure execution time of test functions"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"{func.__name__}: {elapsed:.4f} seconds")
        return result

    return wrapper


def memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


class TestAlgorithmPerformance:
    """Test performance of core algorithms"""

    @benchmark
    def test_pfaffian_performance(self):
        """Benchmark pfaffian calculation performance"""
        sizes = [10, 20, 30, 40]
        times = []

        for n in sizes:
            # Create random skew-symmetric matrix
            A_random = np.random.randn(n, n)
            A = A_random - A_random.T

            start_time = time.time()
            pf_val = ff.pf(A)
            end_time = time.time()

            elapsed = end_time - start_time
            times.append(elapsed)

            # Verify result is finite
            assert np.isfinite(pf_val), f"Pfaffian should be finite for {n}x{n} matrix"

        # Performance should scale reasonably (not exponentially)
        for i in range(1, len(times)):
            ratio = times[i] / times[i - 1]
            size_ratio = sizes[i] / sizes[i - 1]

            # Should not scale worse than O(n^4)
            assert ratio <= size_ratio**4 * 2, f"Pfaffian scaling should be reasonable"

    @benchmark
    @pytest.mark.slow
    def test_hafnian_performance(self):
        """Benchmark hafnian calculation performance"""
        sizes = [8, 12, 16, 20]  # Smaller sizes due to exponential complexity
        times = []

        for n in sizes:
            # Create random symmetric matrix
            A_random = np.random.randn(n, n)
            A = A_random + A_random.T

            start_time = time.time()
            hf_val = ff.hf(A)
            end_time = time.time()

            elapsed = end_time - start_time
            times.append(elapsed)

            # Verify result is finite
            assert np.isfinite(hf_val), f"Hafnian should be finite for {n}x{n} matrix"

        # Hafnian is exponential, but should complete in reasonable time
        assert all(t < 60.0 for t in times), "Hafnian should complete within 60 seconds"

    @benchmark
    def test_perfect_matching_performance(self):
        """Benchmark perfect matching counting performance"""
        sizes = [10, 15, 20, 25]
        times = []

        for n in sizes:
            # Create grid graph
            side = int(np.sqrt(n))
            if side * side != n:
                side = int(np.sqrt(n)) + 1
                n = side * side

            G = nx.grid_2d_graph(side, side)

            start_time = time.time()
            count = ff.count_perfect_matchings(G)
            end_time = time.time()

            elapsed = end_time - start_time
            times.append(elapsed)

            # Verify result is non-negative
            assert count >= 0, f"Perfect matching count should be non-negative"

        # Should complete in reasonable time
        assert all(
            t < 30.0 for t in times
        ), "Perfect matching should complete within 30 seconds"

    @benchmark
    def test_symplectic_diagonalization_performance(self):
        """Benchmark symplectic diagonalization performance"""
        sizes = [20, 40, 60, 80]
        times = []

        for n in sizes:
            # Create random skew-symmetric matrix
            A_random = np.random.randn(n, n) + 1j * np.random.randn(n, n)
            A = A_random + A_random.conj().T

            Z_random = np.random.randn(n, n) + 1j * np.random.randn(n, n)
            Z = Z_random - Z_random.T

            H = ff.build_H(n, A, Z)

            start_time = time.time()
            eigenvals, eigenvecs = ff.eigh_sp(H)
            end_time = time.time()

            elapsed = end_time - start_time
            times.append(elapsed)

            # Verify results
            assert len(eigenvals) == n, f"Should have {n} eigenvalues"
            assert eigenvecs.shape == (n, n), f"Eigenvectors should be {n}x{n}"

        # Should scale polynomially
        for i in range(1, len(times)):
            ratio = times[i] / times[i - 1]
            size_ratio = sizes[i] / sizes[i - 1]

            # Should not scale worse than O(n^3)
            assert (
                ratio <= size_ratio**3 * 2
            ), "Symplectic diagonalization should scale polynomially"

    @benchmark
    def test_correlation_matrix_performance(self):
        """Benchmark correlation matrix computation performance"""
        sizes = [50, 100, 150, 200]
        times = []

        for n in sizes:
            # Create random Hamiltonian
            H = np.random.randn(n, n)
            H = H + H.T

            start_time = time.time()
            gamma = ff.correlation_matrix(H)
            end_time = time.time()

            elapsed = end_time - start_time
            times.append(elapsed)

            # Verify result
            assert gamma.shape == (n, n), f"Correlation matrix should be {n}x{n}"
            assert np.allclose(gamma, gamma.T.conj()), "Should be Hermitian"

        # Should scale with matrix diagonalization (O(n^3))
        for i in range(1, len(times)):
            ratio = times[i] / times[i - 1]
            size_ratio = sizes[i] / sizes[i - 1]

            # Should scale roughly as O(n^3)
            assert (
                ratio <= size_ratio**3 * 3
            ), "Correlation matrix should scale as O(n^3)"


class TestScalabilityTests:
    """Test scalability with increasing system size"""

    @pytest.mark.slow
    def test_matrix_operations_scalability(self):
        """Test scalability of basic matrix operations"""
        sizes = np.array([10, 20, 40, 80])

        # Test determinant calculation
        det_times = []
        for n in sizes:
            A = np.random.randn(n, n)

            start_time = time.time()
            det_val = ff.dt(A)
            end_time = time.time()

            det_times.append(end_time - start_time)
            assert np.isfinite(det_val), "Determinant should be finite"

        # Test permanent calculation (smaller sizes due to complexity)
        perm_sizes = sizes[sizes <= 20]  # Limit to smaller sizes
        perm_times = []
        for n in perm_sizes:
            A = np.random.randn(n, n)

            start_time = time.time()
            perm_val = ff.pt(A)
            end_time = time.time()

            perm_times.append(end_time - start_time)
            assert np.isfinite(perm_val), "Permanent should be finite"

        # Verify reasonable scaling
        assert all(t < 10.0 for t in det_times), "Determinant should be fast"
        assert all(t < 60.0 for t in perm_times), "Permanent should complete reasonably"

    def test_graph_algorithms_scalability(self):
        """Test scalability of graph algorithms"""
        node_counts = [16, 25, 36, 49]  # Perfect squares for grid graphs

        planarity_times = []
        matching_times = []

        for n_nodes in node_counts:
            side = int(np.sqrt(n_nodes))
            G = nx.grid_2d_graph(side, side)

            # Test planarity checking
            start_time = time.time()
            is_planar = nx.is_planar(G)
            planarity_time = time.time() - start_time
            planarity_times.append(planarity_time)

            assert is_planar, "Grid graphs should be planar"

            # Test perfect matching (if even number of nodes)
            if n_nodes % 2 == 0:
                start_time = time.time()
                count = ff.count_perfect_matchings(G)
                matching_time = time.time() - start_time
                matching_times.append(matching_time)

                assert count >= 0, "Perfect matching count should be non-negative"

        # Should complete in reasonable time
        assert all(
            t < 5.0 for t in planarity_times
        ), "Planarity checking should be fast"
        assert all(
            t < 30.0 for t in matching_times
        ), "Perfect matching should be reasonable"

    def test_quantum_system_scalability(self):
        """Test scalability of quantum system simulations"""
        system_sizes = [2, 4, 8]

        diagonalization_times = []
        correlation_times = []

        for n in system_sizes:

            rho, H = ff.random_FF_state(n, returnH=True)

            # Test diagonalization
            start_time = time.time()
            eigenvals, eigenvecs = ff.eigh_sp(H)
            diag_time = time.time() - start_time
            diagonalization_times.append(diag_time)

            # Test correlation matrix computation
            start_time = time.time()
            gamma = ff.compute_2corr_matrix(rho, n)
            corr_time = time.time() - start_time
            correlation_times.append(corr_time)

            # Verify results
            assert len(eigenvals) == 2 * n, "Should have correct number of eigenvalues"
            assert gamma.shape == (
                2 * n,
                2 * n,
            ), "Correlation matrix should have correct shape"

        # Should scale polynomially
        for i in range(1, len(diagonalization_times)):
            ratio = diagonalization_times[i] / diagonalization_times[i - 1]
            size_ratio = system_sizes[i] / system_sizes[i - 1]

            # Diagonalization should scale as O(n^3)
            assert (
                ratio <= size_ratio**3 * 3
            ), "Diagonalization should scale polynomially"


class TestMemoryUsage:
    """Test memory usage and efficiency"""

    @pytest.mark.slow
    def test_matrix_memory_usage(self):
        """Test memory usage of matrix operations"""
        initial_memory = memory_usage()

        # Create large matrices and perform operations
        n = 200
        A = np.random.randn(n, n)
        B = np.random.randn(n, n)

        # Matrix multiplication
        C = A @ B

        # Determinant
        det_A = ff.dt(A)

        # Clean up
        del A, B, C
        gc.collect()

        final_memory = memory_usage()
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable
        assert (
            memory_increase < 500
        ), "Memory usage should be reasonable"  # Less than 500 MB

    def test_memory_cleanup(self):
        """Test that memory is properly cleaned up"""
        initial_memory = memory_usage()

        # Perform multiple operations
        for i in range(10):
            n = 5
            rho = ff.random_FF_state(n)

            eigenvals = np.linalg.eigvals(rho)
            gamma = ff.correlation_matrix(rho)

            # Explicit cleanup
            del rho, eigenvals, gamma

        gc.collect()
        final_memory = memory_usage()

        # Memory should not grow significantly
        memory_growth = final_memory - initial_memory
        assert memory_growth < 100, "Memory should be cleaned up properly"

    def test_large_system_memory(self):
        """Test memory usage with large systems"""
        # Test with largest system that should fit in memory
        try:
            n = 500
            H = np.random.randn(n, n)
            H = H + H.T

            memory_before = memory_usage()

            # Perform computation
            eigenvals = np.linalg.eigvals(H)

            memory_after = memory_usage()
            memory_used = memory_after - memory_before

            # Should use reasonable amount of memory
            expected_memory = n * n * 8 / 1024 / 1024 * 3  # Rough estimate in MB
            assert (
                memory_used < expected_memory * 2
            ), "Memory usage should be reasonable"

            # Clean up
            del H, eigenvals
            gc.collect()

        except MemoryError:
            # Acceptable if system doesn't have enough memory
            pytest.skip("Not enough memory for large system test")


class TestComparisonBenchmarks:
    """Compare performance with reference implementations"""

    def test_determinant_vs_numpy(self):
        """Compare determinant performance with NumPy"""
        sizes = [50, 100, 150]

        for n in sizes:
            A = np.random.randn(n, n)

            # Time our implementation
            start_time = time.time()
            det_ours = ff.dt_eigen(A)
            our_time = time.time() - start_time

            # Time NumPy implementation
            start_time = time.time()
            det_numpy = np.linalg.det(A)
            numpy_time = time.time() - start_time

            # Results should be close
            assert np.allclose(det_ours, det_numpy), "Results should match NumPy"

            # Our implementation should be reasonably competitive
            # (Allow up to 100x slower, as we might have additional features)
            assert (
                our_time < numpy_time * 100
            ), "Should be reasonably competitive with NumPy"

    def test_matrix_operations_vs_numpy(self):
        """Compare basic matrix operations with NumPy"""
        n = 100
        A = np.random.randn(n, n)
        B = np.random.randn(n, n)

        # Matrix multiplication
        start_time = time.time()
        C_numpy = A @ B
        numpy_time = time.time() - start_time

        # Our implementation (if available)
        try:
            start_time = time.time()
            C_ours = ff.matrix_multiply(A, B)
            our_time = time.time() - start_time

            assert np.allclose(C_ours, C_numpy), "Matrix multiplication should match"
            assert our_time < numpy_time * 5, "Should be reasonably fast"

        except AttributeError:
            # Custom implementation might not exist
            pass


class TestStressTests:
    """Stress tests for robustness and stability"""

    @pytest.mark.slow
    def test_repeated_operations_stress(self):
        """Test stability under repeated operations"""
        n_iterations = 100
        n = 20

        for i in range(n_iterations):
            # Create random matrix
            A = np.random.randn(n, n)
            A = A + A.T

            # Perform operations
            det_val = ff.dt(A)
            eigenvals = np.linalg.eigvals(A)

            # Results should always be finite
            assert np.isfinite(
                det_val
            ), f"Determinant should be finite at iteration {i}"
            assert np.all(
                np.isfinite(eigenvals)
            ), f"Eigenvalues should be finite at iteration {i}"

    @pytest.mark.slow
    def test_edge_case_stress(self):
        """Test with edge cases and extreme values"""
        # Very small matrices
        A_small = np.array([[1e-10]])
        det_small = ff.dt(A_small)
        assert np.isfinite(det_small), "Should handle very small values"

        # Very large matrices (if memory allows)
        try:
            A_large = np.random.randn(300, 300)
            det_large = ff.dt(A_large)
            assert np.isfinite(det_large), "Should handle large matrices"
        except MemoryError:
            pytest.skip("Not enough memory for large matrix test")

        # Nearly singular matrices
        A_singular = np.random.randn(10, 10)
        A_singular[0, :] = A_singular[1, :] * (1 + 1e-15)  # Make nearly singular

        try:
            det_singular = ff.dt(A_singular)
            # Should either be very small or raise appropriate error
            assert (
                np.isfinite(det_singular) or abs(det_singular) < 1e-10
            ), "Should handle nearly singular matrices"
        except np.linalg.LinAlgError:
            # Acceptable to fail on singular matrices
            pass

    @pytest.mark.slow
    def test_numerical_stability_stress(self):
        """Test numerical stability under various conditions"""
        # Test with ill-conditioned matrices
        for cond_num in [1e6, 1e9, 1e12]:
            try:
                # Create matrix with specific condition number
                n = 20
                U, _, Vt = np.linalg.svd(np.random.randn(n, n))
                s = np.logspace(0, -np.log10(cond_num), n)
                A = U @ np.diag(s) @ Vt

                # Test operations
                det_val = ff.dt(A)

                # Should either succeed or fail gracefully
                assert (
                    np.isfinite(det_val) or abs(det_val) < 1e-15
                ), f"Should handle condition number {cond_num}"

            except np.linalg.LinAlgError:
                # Acceptable to fail on very ill-conditioned matrices
                pass

    @pytest.mark.slow
    def test_concurrent_operations_stress(self):
        """Test stability under concurrent operations"""
        import threading
        import queue

        results = queue.Queue()
        errors = queue.Queue()

        def worker():
            try:
                for i in range(10):
                    n = 20
                    A = np.random.randn(n, n)
                    det_val = ff.dt(A)
                    results.put(det_val)
            except Exception as e:
                errors.put(e)

        # Start multiple threads
        threads = []
        for i in range(4):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        # Wait for completion
        for t in threads:
            t.join()

        # Check results
        assert errors.empty(), "No errors should occur in concurrent operations"

        # Collect results
        result_list = []
        while not results.empty():
            result_list.append(results.get())

        # All results should be finite
        assert all(
            np.isfinite(r) for r in result_list
        ), "All concurrent results should be finite"


class TestPerformanceRegression:
    """Test for performance regressions"""

    def test_baseline_performance(self):
        """Establish baseline performance metrics"""
        # Standard test case
        n = 50
        A = np.random.randn(n, n)
        A = A + A.T

        # Measure key operations
        operations = {}

        # Determinant
        start_time = time.time()
        det_val = ff.dt(A)
        operations["determinant"] = time.time() - start_time

        # Eigenvalues
        start_time = time.time()
        eigenvals = np.linalg.eigvals(A)
        operations["eigenvalues"] = time.time() - start_time

        # Correlation matrix
        start_time = time.time()
        gamma = ff.correlation_matrix(A)
        operations["correlation_matrix"] = time.time() - start_time

        # All operations should complete quickly
        for op_name, op_time in operations.items():
            assert op_time < 5.0, f"{op_name} should complete within 5 seconds"

        # Store baseline for future comparison (in practice, would save to file)
        baseline = {
            "determinant": 0.1,  # Expected baseline times
            "eigenvalues": 0.1,
            "correlation_matrix": 0.2,
        }

        # Check against baseline (allow 2x slowdown)
        for op_name, op_time in operations.items():
            if op_name in baseline:
                assert (
                    op_time < baseline[op_name] * 2
                ), f"{op_name} performance regression detected"

    @pytest.mark.slow
    def test_memory_baseline(self):
        """Establish baseline memory usage"""
        initial_memory = memory_usage()

        # Standard operations
        n = 100
        A = np.random.randn(n, n)
        det_val = ff.dt_eigen(A)
        eigenvals = np.linalg.eigvals(A)

        peak_memory = memory_usage()
        memory_used = peak_memory - initial_memory

        # Clean up
        del A, det_val, eigenvals
        gc.collect()

        final_memory = memory_usage()
        memory_retained = final_memory - initial_memory

        # Memory usage should be reasonable
        assert (
            memory_used < 200
        ), "Peak memory usage should be reasonable"  # Less than 200 MB
        assert (
            memory_retained < 50
        ), "Memory retention should be minimal"  # Less than 50 MB


@pytest.mark.slow
class TestLongRunningPerformance:
    """Long-running performance tests (marked as slow)"""

    def test_extended_stress_test(self):
        """Extended stress test for long-term stability"""
        n_iterations = 1000
        n = 15

        start_memory = memory_usage()

        for i in range(n_iterations):
            A = np.random.randn(n, n)
            det_val = ff.dt(A)

            # Check every 100 iterations
            if i % 100 == 0:
                current_memory = memory_usage()
                memory_growth = current_memory - start_memory

                # Memory growth should be bounded
                assert memory_growth < 100, f"Memory growth too large at iteration {i}"

                # Result should be finite
                assert np.isfinite(det_val), f"Result should be finite at iteration {i}"

    def test_large_system_benchmark(self):
        """Benchmark with large systems"""
        sizes = [100, 200, 300, 400, 500]

        for n in sizes:
            try:
                A = np.random.randn(n, n)
                A = A + A.T

                start_time = time.time()
                eigenvals = np.linalg.eigvals(A)
                elapsed = time.time() - start_time

                # Should complete in reasonable time
                max_time = n**3 / 1000000  # Rough scaling estimate
                assert (
                    elapsed < max_time
                ), f"Size {n} should complete in reasonable time"

                # Clean up
                del A, eigenvals
                gc.collect()

            except MemoryError:
                # Acceptable if system runs out of memory
                break

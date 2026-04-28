// Website: https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-3-power-of-two-choices
// Track 14: Load Balancers
// Task 13: Implement Power-of-Two-Choices Load Balancing

// Website: https://builddistributedsystem.com/tracks/loadbalancers/tasks/task-20-3-3-power-of-two-choices
// Task: Implement Power-of-Two-Choices Load Balancing
// Java starter code
// Read from stdin, process data, write to stdout
// This is a general template - adapt it to your specific task

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

        try {
            String line;
            // Read input line by line
            while ((line = reader.readLine()) != null) {
                // TODO: Implement your task logic here
                // - Parse the input (might be JSON, plain text, etc.)
                // - Process according to the task requirements
                // - Output results to stdout

                // For debugging, use stderr:
                // System.err.println("Debug info: " + line);

                // Example: Echo input back (replace with your logic)
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading input: " + e.getMessage());
            System.exit(1);
        }
    }
}

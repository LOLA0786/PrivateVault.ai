package cmd

import (
        "fmt"
        "os"
        "os/exec"

        "github.com/spf13/cobra"
)

var replayCmd = &cobra.Command{
        Use:   "replay",
        Short: "Replay governance decisions",
        RunE: func(cmd *cobra.Command, args []string) error {

                py := exec.Command(
                        "python3",
                        "replay_engine.py",
                )

                // IMPORTANT:
                // Run from repo root so evidence.jsonl is found
                py.Dir = ".."

                py.Stdout = os.Stdout
                py.Stderr = os.Stderr

                err := py.Run()
                if err != nil {
                        return fmt.Errorf("replay failed: %w", err)
                }

                return nil
        },
}

func init() {
        rootCmd.AddCommand(replayCmd)
}

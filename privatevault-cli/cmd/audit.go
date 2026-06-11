package cmd

import (
        "fmt"
        "os"
        "os/exec"

        "github.com/spf13/cobra"
)

var auditCmd = &cobra.Command{
        Use:   "audit",
        Short: "Run PrivateVault governance audit",
        RunE: func(cmd *cobra.Command, args []string) error {

                py := exec.Command(
                        "python3",
                        "audit_summary.py",
                )

                py.Dir = ".."

                py.Stdout = os.Stdout
                py.Stderr = os.Stderr

                err := py.Run()
                if err != nil {
                        return fmt.Errorf("audit failed: %w", err)
                }

                return nil
        },
}

func init() {
        rootCmd.AddCommand(auditCmd)
}

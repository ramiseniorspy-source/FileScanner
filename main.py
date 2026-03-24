import argparse
from core.orchestrator import run_v5_scan

def main():
    parser = argparse.ArgumentParser(description="Scanner V5: AST-Aware Bug Bounty Engine")
    parser.add_argument("--repo", required=True, help="Path to the source code directory to analyze")
    parser.add_argument("--mode", choices=["recon", "bounty"], default="bounty", help="Analysis mode")
    
    args = parser.parse_args()

    try:
        run_v5_scan(args.repo, mode=args.mode)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Exiting...")

if __name__ == "__main__":
    main()

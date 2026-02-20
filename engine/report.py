def print_compliance_report(summary: dict):
    print(f"Applicable Controls: {summary['total_applicable']}")
    print(f"Compliant: {summary['total_compliant']}")
    print(f"Non-Compliant: {summary['total_non_compliant']}")
    print(f"Partial: {summary['total_partial']}")
    print(f"Not Tested: {summary['total_not_tested']}")
    print(f"Compliance Score: {summary['compliance_percent']:.1f}%\n")
    print("Domain breakdown:")
    for d, v in summary["domain_breakdown"].items():
        print(f"  {d}: {v['score_percent']:.1f}%")

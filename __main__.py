# rag_accuracy_evaluator/__main__.py
import argparse
from evaluator import RAGEvaluator

def main():
    parser = argparse.ArgumentParser(description="RAG Search Accuracy Evaluator")
    parser.add_argument('--config', type=str, required=True, help='Path to config file (YAML)')
    args = parser.parse_args()

    evaluator = RAGEvaluator(args.config)
    evaluator.run_all()
    evaluator.generate_html_report()

if __name__ == '__main__':
    main()

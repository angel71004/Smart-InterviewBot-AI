"""
Quick verification script to check if all dependencies are installed correctly
"""

import sys

def check_import(module_name, package_name=None):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {package_name or module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name} - FAILED: {e}")
        return False

def main():
    print("=" * 50)
    print("Verifying Dependencies")
    print("=" * 50)
    
    checks = [
        ("streamlit", "Streamlit"),
        ("PyPDF2", "PyPDF2"),
        ("docx", "python-docx"),
        ("spacy", "spaCy"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("sklearn", "scikit-learn"),
    ]
    
    results = []
    for module, name in checks:
        results.append(check_import(module, name))
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All dependencies are installed correctly!")
        print("=" * 50)
        
        # Check spaCy model
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model 'en_core_web_sm' is installed")
        except OSError:
            print("❌ spaCy model 'en_core_web_sm' is NOT installed")
            print("   Run: python -m spacy download en_core_web_sm")
        
        # Check CSV files
        import os
        csv_files = ["job_roles.csv", "interview_questions.csv"]
        print("\nChecking CSV files:")
        for csv_file in csv_files:
            if os.path.exists(csv_file):
                print(f"✅ {csv_file} - Found")
            else:
                print(f"❌ {csv_file} - Not found")
        
        print("\n" + "=" * 50)
        print("Setup verification complete!")
        print("You can now run: streamlit run app.py")
    else:
        print("❌ Some dependencies are missing!")
        print("Please run: pip install -r requirements.txt")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()


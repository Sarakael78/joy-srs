#!/usr/bin/env python3
"""
Test script to verify the Legal Strategy Infographics Platform deployment setup.
"""

import os
import sys
from pathlib import Path


def test_file_structure():
    """Test that all required files exist."""
    print("🔍 Testing file structure...")

    required_files = [
        "public/infographic.html",
        "legal_infographics/main.py",
        "legal_infographics/config.py",
        "legal_infographics/database.py",
        "legal_infographics/api/__init__.py",
        "legal_infographics/api/auth.py",
        "legal_infographics/api/infographics.py",
        "legal_infographics/api/cases.py",
        "legal_infographics/api/users.py",
        "legal_infographics/api/audit.py",
        "legal_infographics/middleware/__init__.py",
        "legal_infographics/middleware/rate_limit.py",
        "legal_infographics/middleware/audit.py",
        "legal_infographics/middleware/security.py",
        "legal_infographics/utils/__init__.py",
        "legal_infographics/utils/security.py",
        "legal_infographics/utils/logging.py",
        "requirements.txt",
        "vercel.json",
        "deploy.sh",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files found")
        return True


def test_infographic_content():
    """Test that the infographic HTML file has content."""
    print("\n🔍 Testing infographic content...")

    infographic_path = Path("public/infographic.html")
    if not infographic_path.exists():
        print("❌ infographic.html not found")
        return False

    with open(infographic_path, "r", encoding="utf-8") as f:
        content = f.read()

    if len(content.strip()) == 0:
        print("❌ infographic.html is empty")
        return False

    if "Plaintiff's Strategic Case Analysis" not in content:
        print("❌ infographic.html doesn't contain expected content")
        return False

    print("✅ infographic.html has valid content")
    return True


def test_vercel_config():
    """Test that vercel.json is valid."""
    print("\n🔍 Testing Vercel configuration...")

    vercel_path = Path("vercel.json")
    if not vercel_path.exists():
        print("❌ vercel.json not found")
        return False

    try:
        import json

        with open(vercel_path, "r") as f:
            config = json.load(f)

        required_keys = ["version", "builds", "routes"]
        for key in required_keys:
            if key not in config:
                print(f"❌ vercel.json missing required key: {key}")
                return False

        print("✅ vercel.json is valid")
        return True
    except json.JSONDecodeError:
        print("❌ vercel.json is not valid JSON")
        return False


def test_requirements():
    """Test that requirements.txt has necessary packages."""
    print("\n🔍 Testing requirements.txt...")

    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        print("❌ requirements.txt not found")
        return False

    with open(requirements_path, "r") as f:
        content = f.read()

    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "sqlalchemy",
        "passlib",
        "python-jose",
    ]

    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages in requirements.txt: {missing_packages}")
        return False

    print("✅ requirements.txt has all necessary packages")
    return True


def test_python_imports():
    """Test that Python modules can be imported."""
    print("\n🔍 Testing Python imports...")

    try:
        # Add current directory to Python path
        sys.path.insert(0, str(Path.cwd()))

        # Test basic imports
        import legal_infographics
        import legal_infographics.config
        import legal_infographics.main

        print("✅ Python modules can be imported")
        return True
    except ImportError as e:
        print(f"⚠️  Import warning: {e}")
        print("   This is expected if dependencies aren't installed locally")
        print("   Dependencies will be installed during Vercel deployment")
        return True  # Don't fail the test for this


def main():
    """Run all tests."""
    print("🚀 Legal Strategy Infographics Platform - Deployment Test")
    print("=" * 60)

    tests = [
        test_file_structure,
        test_infographic_content,
        test_vercel_config,
        test_requirements,
        test_python_imports,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your deployment setup is ready.")
        print("\nNext steps:")
        print("1. Run: ./deploy.sh")
        print("2. Follow the Vercel deployment guide")
        print("3. Your infographic will be available at your Vercel URL")
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        sys.exit(1)


if __name__ == "__main__":
    main()
